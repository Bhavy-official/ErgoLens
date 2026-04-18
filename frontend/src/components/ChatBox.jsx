import { useState } from "react"
import { queryRAG } from "../api/client"

export default function ChatBox({ sessionId, onNewMessage }) {
  const [question, setQuestion] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!question.trim() || loading) return

    setLoading(true)
    try {
      const res = await queryRAG(question, sessionId)
      onNewMessage({
        question,
        answer: res.data.answer,
        sources: res.data.sources,
      })
      setQuestion("")
    } catch (err) {
      console.error("RAG query failed:", err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about books..."
        className="flex-1 px-4 py-3 rounded-xl bg-surface-container-lowest text-on-surface placeholder:text-on-surface-variant/50 focus:outline-none focus:ring-2 focus:ring-primary"
        disabled={loading}
      />
      <button
        type="submit"
        disabled={loading}
        className="text-on-primary font-medium px-6 py-3 rounded-xl disabled:opacity-40 disabled:cursor-not-allowed transition-opacity"
        style={{
          background: "linear-gradient(135deg, #76d6d5 0%, #008080 100%)",
        }}
      >
        {loading ? (
          <span className="inline-flex items-center gap-2">
            <span className="inline-block w-4 h-4 border-2 border-on-primary border-t-transparent rounded-full animate-spin" />
            Asking...
          </span>
        ) : (
          "Ask"
        )}
      </button>
    </form>
  )
}
