import axios from "axios"

const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
})

export function getBooks(params = {}) {
  return api.get("/books/", { params })
}

export function getBook(id) {
  return api.get(`/books/${id}/`)
}

export function getRecommendations(id) {
  return api.get(`/books/${id}/recommendations/`)
}

export function triggerScrape(maxPages = 50) {
  return api.post("/scrape/", { max_pages: maxPages })
}

export function generateInsights(bookId) {
  return api.post("/insights/generate/", { book_id: bookId })
}

export function queryRAG(question, sessionId) {
  return api.post("/rag/query/", { question, session_id: sessionId })
}

export function getChatHistory(sessionId) {
  return api.get("/chat/history/", { params: { session_id: sessionId } })
}

export function clearChatHistory(sessionId) {
  return api.delete("/chat/history/clear/", { params: { session_id: sessionId } })
}

export default api
