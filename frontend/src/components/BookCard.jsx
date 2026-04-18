import { Link } from "react-router-dom"
import RatingStars from "./RatingStars"

export default function BookCard({ book }) {
  return (
    <Link
      to={`/books/${book.id}`}
      className="block bg-surface-container rounded-xl overflow-hidden transition-colors hover:bg-surface-container-highest group"
      style={{ boxShadow: "0 20px 40px rgba(218, 226, 253, 0.06)" }}
    >
      <div
        className="aspect-[2/3] bg-surface-container-low overflow-hidden transition-transform duration-300 group-hover:-translate-y-1"
      >
        <img
          src={book.cover_image_url}
          alt={book.title}
          className="w-full h-full object-cover"
        />
      </div>
      <div className="p-4 space-y-2">
        <h3
          className="font-semibold text-on-surface text-sm line-clamp-2 leading-snug"
          style={{ fontFamily: "Manrope, sans-serif" }}
        >
          {book.title}
        </h3>
        <div className="flex items-center gap-2">
          <RatingStars rating={book.rating} />
          <span className="text-xs text-on-surface-variant">{book.rating}/5</span>
        </div>
        {book.genre && (
          <span
            className="inline-block text-xs text-primary px-2 py-0.5 rounded-full"
            style={{ background: "rgba(0, 128, 128, 0.15)" }}
          >
            {book.genre}
          </span>
        )}
        <p className="text-sm font-semibold text-secondary-container">{book.price}</p>
      </div>
    </Link>
  )
}

