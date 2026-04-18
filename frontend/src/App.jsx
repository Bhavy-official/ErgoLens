import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom"
import BookList from "./pages/BookList"
import BookDetail from "./pages/BookDetail"
import QAPage from "./pages/QAPage"

function Nav() {
  const linkClass = ({ isActive }) =>
    `relative px-3 py-2 text-sm font-medium transition-all duration-200 ${
      isActive
        ? "text-primary"
        : "text-on-surface-variant hover:text-on-surface"
    }`

  return (
    <nav className="sticky top-0 z-50 bg-surface/80 backdrop-blur-xl border-b border-outline-variant">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        
        {/* Logo */}
        <div className="flex items-center gap-8">
          <span
            className="text-xl font-bold text-primary tracking-tight"
            style={{ fontFamily: "Manrope, sans-serif" }}
          >
            ErgoLens
          </span>

          {/* Links */}
          <div className="flex items-center gap-4">
            <NavLink to="/" className={linkClass}>
              {({ isActive }) => (
                <span className="relative">
                  Dashboard
                  {isActive && (
                    <span className="absolute left-0 -bottom-1 w-full h-[2px] bg-primary rounded-full" />
                  )}
                </span>
              )}
            </NavLink>

            <NavLink to="/qa" className={linkClass}>
              {({ isActive }) => (
                <span className="relative">
                  Q&amp;A
                  {isActive && (
                    <span className="absolute left-0 -bottom-1 w-full h-[2px] bg-primary rounded-full" />
                  )}
                </span>
              )}
            </NavLink>
          </div>
        </div>

        {/* Right side (future ready) */}
        <div className="flex items-center gap-3">
          <div className="hidden md:flex items-center bg-surface-container border border-outline-variant rounded-lg px-3 py-1.5">
            <input
              placeholder="Search..."
              className="bg-transparent outline-none text-sm text-on-surface placeholder:text-on-surface-variant w-36"
            />
          </div>
        </div>

      </div>
    </nav>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-surface">
        <Nav />
        <Routes>
          <Route path="/" element={<BookList />} />
          <Route path="/books/:id" element={<BookDetail />} />
          <Route path="/qa" element={<QAPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}