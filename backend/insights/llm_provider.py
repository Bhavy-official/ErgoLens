import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def _try_openai(messages, max_tokens=1024):
    """Attempt completion via OpenAI."""
    api_key = getattr(settings, "OPENAI_API_KEY", None)
    if not api_key:
        raise ValueError("OpenAI API key is missing.")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        model = getattr(settings, "OPENAI_FALLBACK_MODEL", "gpt-4o-mini")
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
        )
        logger.info("Used OpenAI model: %s", model)
        return response.choices[0].message.content.strip()
    except Exception as exc:
        logger.warning("OpenAI request failed: %s", exc)
        raise

def _try_groq(messages, max_tokens=1024):
    """Attempt completion via Groq, falling back to OpenAI if it fails."""
    api_key = getattr(settings, "GROQ_API_KEY", None)
    if not api_key:
        raise ValueError("Groq API key is missing.")
        
    try:
        from groq import Groq, RateLimitError
        client = Groq(api_key=api_key)
        
        primary = settings.GROQ_PRIMARY_MODEL
        fallbacks = [m.strip() for m in settings.GROQ_FALLBACK_MODELS.split(",") if m.strip()]
        
        seen = set()
        chain = []
        for m in [primary] + fallbacks:
            if m not in seen:
                seen.add(m)
                chain.append(m)

        last_exc = None
        for model in chain:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.7,
                )
                if model != primary:
                    logger.info("Used Groq fallback model: %s", model)
                else:
                    logger.info("Used Groq primary model: %s", model)
                return response.choices[0].message.content.strip()
            except RateLimitError as exc:
                logger.warning("Rate limit on Groq/%s, trying next. %s", model, exc)
                last_exc = exc
            except Exception as exc:
                logger.warning("Groq request failed on model %s: %s", model, exc)
                last_exc = exc
        
        raise last_exc
        
    except Exception as groq_exc:
        logger.warning("Groq pipeline entirely failed: %s. Falling back to OpenAI if configured.", groq_exc)
        
        # Fallback to OpenAI
        if getattr(settings, "OPENAI_API_KEY", None):
            return _try_openai(messages, max_tokens)
            
        raise Exception(f"All Groq models failed, and no OpenAI API key configured. Original error: {groq_exc}")

def chat(messages, max_tokens=1024):
    """
    Route requests to the correct provider: 'openai' or 'groq'.
    messages: List of dicts in OpenAI format, e.g., [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    """
    provider = getattr(settings, "DEFAULT_PROVIDER", "openai").lower()
    
    if provider == "openai":
        return _try_openai(messages, max_tokens)
    elif provider == "groq":
        return _try_groq(messages, max_tokens)
    else:
        raise ValueError(f"Unknown DEFAULT_PROVIDER: {provider}. Options are 'openai' or 'groq'.")
