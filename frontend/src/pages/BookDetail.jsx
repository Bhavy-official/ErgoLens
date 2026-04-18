import { useState, useEffect } from "react"
import { useParams, Link } from "react-router-dom"
import { getBook, getRecommendations, generateInsights } from "../api/client"
import RatingStars from "../components/RatingStars"
import InsightPanel from "../components/InsightPanel"
import BookCard from "../components/BookCard"

export default function BookDetail() {
  const { id } = useParams()
  const [book, setBook] = useState(null)
  const [similarBooks, setSimilarBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [generateError, setGenerateError] = useState(null)

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      try {
        const [bookRes, recsRes] = await Promise.all([
          getBook(id),
          getRecommendations(id),
        ])
        setBook(bookRes.data)
        setSimilarBooks(recsRes.data || [])
      } catch (err) {
        console.error("Failed to fetch book:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [id])

  const handleGenerate = async () => {
    setGenerating(true)
    setGenerateError(null)
    try {
      await generateInsights(book.id)
      const res = await getBook(id)
      setBook(res.data)
    } catch (err) {
      const msg =
        err?.response?.data?.error ||
        err?.message ||
        "Insight generation failed. Please try again."
      setGenerateError(msg)
    } finally {
      setGenerating(false)
    }
  }

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-6 py-12">
        <div className="animate-pulse space-y-6">
          <div className="h-6 bg-surface-container rounded w-1/3" />
          <div className="h-72 bg-surface-container rounded-2xl" />
        </div>
      </div>
    )
  }

  if (!book) {
    return (
      <div className="max-w-5xl mx-auto px-6 py-12">
        <p className="text-on-surface-variant">Book not found.</p>
        <Link to="/" className="text-primary hover:underline mt-2 inline-block">
          ← Back to all books
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-12">
      
      {/* Back Link */}
      <Link
        to="/"
        className="text-sm text-primary hover:underline mb-8 inline-block"
      >
        ← Back to all books
      </Link>

      {/* Main Layout */}
      <div className="grid md:grid-cols-3 gap-10">
        
        {/* LEFT - Cover */}
        <div>
          <div className="rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition duration-300">
            <img
              src={book.cover_image_url}
              alt={book.title}
              className="w-full object-cover"
            />
          </div>

          <button
            onClick={handleGenerate}
            disabled={generating || book.insights_generated}
            className="mt-5 w-full py-3 rounded-xl font-medium text-white transition-all duration-300
              bg-gradient-to-r from-teal-400 to-teal-700
              hover:scale-[1.02] hover:shadow-lg
              disabled:opacity-40 disabled:hover:scale-100"
          >
            {generating
              ? "Generating..."
              : book.insights_generated
              ? "Insights Generated"
              : "Generate AI Insights"}
          </button>

          {generateError && (
            <p className="mt-2 text-xs text-red-500">{generateError}</p>
          )}
        </div>

        {/* RIGHT - Details */}
        <div className="md:col-span-2 space-y-6">

          {/* Title */}
          <h1 className="text-4xl md:text-5xl font-bold leading-tight">
            {book.title}
          </h1>

          {/* Rating */}
          <div className="flex items-center gap-3">
            <RatingStars rating={book.rating} />
            <span className="font-semibold text-lg">{book.rating}/5</span>
            <span className="text-sm text-on-surface-variant">
              ({book.num_reviews} reviews)
            </span>
          </div>

          {/* Info Grid */}
          <div className="grid grid-cols-2 gap-4 bg-surface-container/60 backdrop-blur-md border border-white/5 rounded-2xl p-6 shadow-inner">
            {[
              ["Genre", book.genre || "Unknown"],
              ["Price", book.price || "N/A"],
              ["Availability", book.availability || "N/A"],
              ["Author", book.author],
            ].map(([label, value]) => (
              <div key={label}>
                <p className="text-xs uppercase text-on-surface-variant mb-1 tracking-wide">
                  {label}
                </p>
                <p className="font-semibold text-lg">{value}</p>
              </div>
            ))}
          </div>

          {/* Description */}
          <div className="bg-surface-container/70 backdrop-blur-md border border-white/5 rounded-2xl p-6 leading-relaxed shadow-sm">
            <p className="text-xs uppercase text-on-surface-variant mb-2 tracking-wide">
              Description
            </p>
            <p className="text-on-surface-variant">
              {book.description}
            </p>
          </div>
        </div>
      </div>

      {/* Insights */}
      {book.insights_generated && (
        <div className="mt-12">
          <InsightPanel book={book} />
        </div>
      )}

      {/* Similar Books */}
      {similarBooks.length > 0 && (
        <div className="mt-14">
          <h2 className="text-2xl font-bold mb-6">Similar Books</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {similarBooks.map((b) => (
              <div className="hover:scale-105 transition duration-300" key={b.id}>
                <BookCard book={b} />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}