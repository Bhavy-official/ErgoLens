import { useState, useEffect, useCallback } from "react"
import { getBooks, triggerScrape } from "../api/client"
import BookCard from "../components/BookCard"

export default function BookList() {
  const [books, setBooks] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState("")
  const [genre, setGenre] = useState("")
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [scraping, setScraping] = useState(false)

  const genres = [
    "", "Fiction", "Mystery", "Romance", "Science Fiction", "Fantasy",
    "Thriller", "Historical Fiction", "Non-Fiction", "Biography",
    "Self-Help", "Philosophy", "Poetry", "Horror", "Adventure",
    "Young Adult", "Children", "Humor", "Travel", "Music", "Art", "Default",
  ]

  const fetchBooks = useCallback(async () => {
    setLoading(true)
    try {
      const params = { page }
      if (search) params.search = search
      if (genre) params.genre = genre
      const res = await getBooks(params)
      setBooks(res.data.results)
      setTotalPages(Math.ceil(res.data.count / 20))
    } catch (err) {
      console.error("Failed to fetch books:", err)
    } finally {
      setLoading(false)
    }
  }, [page, search, genre])

  useEffect(() => {
    fetchBooks()
  }, [fetchBooks])

  useEffect(() => {
    const timer = setTimeout(() => {
      setPage(1)
      fetchBooks()
    }, 300)
    return () => clearTimeout(timer)
  }, [search, genre])

  const handleScrape = async () => {
    setScraping(true)
    try {
      await triggerScrape(5)
      alert("Scraping started in background! Refresh in a few minutes.")
    } catch (err) {
      console.error("Scrape failed:", err)
    } finally {
      setScraping(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      <div className="flex items-center justify-between mb-8">
        <h1
          className="text-4xl font-bold text-on-surface"
          style={{ fontFamily: "Manrope, sans-serif" }}
        >
          Book Insights
        </h1>
        <button
          onClick={handleScrape}
          disabled={scraping}
          className="text-on-surface-variant hover:text-primary text-sm px-5 py-2 rounded-xl bg-surface-container-highest disabled:opacity-40 transition-colors"
          style={{ border: "1px solid rgba(62,73,73,0.4)" }}
        >
          {scraping ? "Scraping..." : "Scrape Books"}
        </button>
      </div>

      <div className="flex gap-4 mb-8">
        <input
          type="text"
          placeholder="Search by title..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 px-4 py-3 rounded-xl bg-surface-container-lowest text-on-surface placeholder:text-on-surface-variant/50 focus:outline-none focus:ring-2 focus:ring-primary"
        />
        <select
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
          className="px-4 py-3 rounded-xl bg-surface-container-lowest text-on-surface focus:outline-none focus:ring-2 focus:ring-primary"
        >
          {genres.map((g) => (
            <option key={g} value={g}>
              {g || "All Genres"}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {Array.from({ length: 20 }).map((_, i) => (
            <div key={i} className="bg-surface-container h-64 rounded-xl animate-pulse" />
          ))}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-8">
            {books.map((book) => (
              <BookCard key={book.id} book={book} />
            ))}
          </div>
          {books.length === 0 && (
            <p className="text-center text-on-surface-variant py-8">No books found.</p>
          )}
        </>
      )}

      {totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-10 flex-wrap">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="px-4 py-2 rounded-xl bg-surface-container text-on-surface-variant hover:bg-surface-container-high disabled:opacity-30 transition-colors"
          >
            Previous
          </button>
          {Array.from({ length: totalPages }).map((_, i) => (
            <button
              key={i + 1}
              onClick={() => setPage(i + 1)}
              className={`px-4 py-2 rounded-xl transition-colors ${
                page === i + 1
                  ? "bg-primary text-on-primary font-semibold"
                  : "bg-surface-container text-on-surface-variant hover:bg-surface-container-high"
              }`}
            >
              {i + 1}
            </button>
          ))}
          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="px-4 py-2 rounded-xl bg-surface-container text-on-surface-variant hover:bg-surface-container-high disabled:opacity-30 transition-colors"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}
