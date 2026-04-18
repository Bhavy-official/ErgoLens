import { useState } from "react"

const TABS = ["Summary", "Genre", "Sentiment", "Recommendation"]

export default function InsightPanel({ book }) {
  const [activeTab, setActiveTab] = useState("Summary")

  const content = {
    Summary: book.ai_summary || "No summary generated yet.",
    Genre: book.ai_genre || "Not classified yet.",
    Sentiment: book.ai_sentiment || "Not analyzed yet.",
    Recommendation: book.ai_recommendation_text || "No recommendation yet.",
  }

  return (
    <div className="bg-surface-container rounded-xl p-6">
      <h2
        className="text-lg font-semibold text-on-surface mb-5 flex items-center gap-2"
        style={{ fontFamily: "Manrope, sans-serif" }}
      >
        <span className="w-2 h-2 rounded-full bg-primary inline-block" />
        AI Insights
      </h2>
      <div className="flex gap-1 mb-5">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
              activeTab === tab
                ? "text-primary border-b-2 border-primary bg-primary/5"
                : "text-on-surface-variant hover:text-on-surface"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="insight-pulse">
        <p className="text-on-surface-variant leading-relaxed">{content[activeTab]}</p>
      </div>
    </div>
  )
}
