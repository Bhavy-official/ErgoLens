export default function RatingStars({ rating }) {
  const stars = []
  const fullStars = Math.floor(rating)
  const hasHalf = rating - fullStars >= 0.5

  for (let i = 0; i < 5; i++) {
    if (i < fullStars) {
      stars.push(
        <span key={i} className="text-secondary-container">★</span>
      )
    } else if (i === fullStars && hasHalf) {
      stars.push(
        <span key={i} style={{ position: "relative", display: "inline-block" }}>
          <span className="text-on-surface-variant/30">★</span>
          <span
            className="text-secondary-container overflow-hidden absolute inset-0"
            style={{ width: "50%" }}
          >★</span>
        </span>
      )
    } else {
      stars.push(
        <span key={i} className="text-on-surface-variant/30">★</span>
      )
    }
  }

  return <span className="inline-flex items-center gap-px">{stars}</span>
}
