import { useState, useEffect } from "react"
import { getChatHistory, clearChatHistory } from "../api/client"
import ChatBox from "../components/ChatBox"
import ChatHistory from "../components/ChatHistory"

function getSessionId() {
  let sessionId = localStorage.getItem("qa_session_id")
  if (!sessionId) {
    sessionId = crypto.randomUUID()
    localStorage.setItem("qa_session_id", sessionId)
  }
  return sessionId
}

export default function QAPage() {
  const [sessionId] = useState(getSessionId)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchHistory() {
      try {
        const res = await getChatHistory(sessionId)
        setMessages(res.data.results || res.data || [])
      } catch (err) {
        console.error("Failed to load chat history:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchHistory()
  }, [sessionId])

  const handleNewMessage = (msg) => {
    setMessages((prev) => [msg, ...prev])
  }

  const handleClearHistory = async () => {
    try {
      await clearChatHistory(sessionId)
      setMessages([])
    } catch (err) {
      console.error("Failed to clear chat history:", err)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <h1
        className="text-4xl font-bold text-on-surface mb-2"
        style={{ fontFamily: "Manrope, sans-serif" }}
      >
        Ask About Books
      </h1>
      <div className="flex items-center gap-3 mb-8">
        <p className="text-on-surface-variant">
          Ask questions about any book in our collection.
        </p>
        <span
          className="inline-block text-xs text-primary px-3 py-1 rounded-full whitespace-nowrap"
          style={{ background: "rgba(0, 128, 128, 0.15)" }}
        >
          Powered by RAG + Groq AI
        </span>
      </div>

      <div className="mb-8">
        <ChatBox sessionId={sessionId} onNewMessage={handleNewMessage} />
      </div>

      <div className="bg-surface-container rounded-xl p-6">
        <div className="flex items-center justify-between mb-5">
          <h2
            className="text-lg font-semibold text-on-surface"
            style={{ fontFamily: "Manrope, sans-serif" }}
          >
            Conversation History
          </h2>
          {messages.length > 0 && (
            <button
              onClick={handleClearHistory}
              className="text-xs text-on-surface-variant hover:text-red-400 transition-colors"
            >
              Clear History
            </button>
          )}
        </div>
        {loading ? (
          <div className="space-y-3">
            <div className="h-16 bg-surface-container-highest rounded-xl animate-pulse" />
            <div className="h-16 bg-surface-container-highest rounded-xl animate-pulse" />
          </div>
        ) : (
          <ChatHistory messages={messages} />
        )}
      </div>
    </div>
  )
}
