export default function ChatHistory({ messages }) {
  if (!messages.length) {
    return (
      <p className="text-on-surface-variant text-sm italic">
        No conversation yet. Ask a question to get started!
      </p>
    )
  }

  return (
    <div className="space-y-4">
      {messages.map((msg, idx) => (
        <div key={idx} className="bg-surface-container rounded-xl p-4 space-y-3">
          <div>
            <p className="text-primary text-xs font-semibold uppercase tracking-wide mb-1">
              Your Question
            </p>
            <p className="text-on-surface font-medium">{msg.question}</p>
          </div>
          <div>
            <p className="text-secondary-container text-xs font-semibold uppercase tracking-wide mb-1">
              Answer
            </p>
            <div className="insight-pulse">
              <p className="text-on-surface-variant leading-relaxed">{msg.answer}</p>
            </div>
          </div>
          {msg.sources && msg.sources.length > 0 && (
            <div className="bg-surface-container-lowest rounded-lg px-3 py-2 space-y-1">
              <p className="text-on-surface-variant/70 text-xs font-semibold">Sources</p>
              {msg.sources.map((source, i) => (
                <p key={i} className="text-on-surface-variant/70 text-xs">
                  · {source.book_title}
                </p>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
