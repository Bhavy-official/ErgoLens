from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

from chat.models import ChatMessage
from .pipeline import RAGPipeline


@extend_schema(
    request=inline_serializer(
        name="RAGQueryRequest",
        fields={
            "question": serializers.CharField(),
            "session_id": serializers.CharField(),
        },
    ),
    responses={200: inline_serializer(
        name="RAGQueryResponse",
        fields={
            "answer": serializers.CharField(),
            "sources": serializers.ListField(child=serializers.DictField()),
        },
    )},
)
class RAGQueryView(APIView):
    def post(self, request):
        question = request.data.get("question", "").strip()
        session_id = request.data.get("session_id", "").strip()

        if not question:
            return Response(
                {"error": "question is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not session_id:
            return Response(
                {"error": "session_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pipeline = RAGPipeline()
        try:
            result = pipeline.query(question, session_id)
        except Exception as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        ChatMessage.objects.create(
            session_id=session_id,
            question=question,
            answer=result["answer"],
            sources=result["sources"],
        )

        return Response(result)
