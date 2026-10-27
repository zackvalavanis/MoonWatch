import { useState } from "react"
import { useAuth } from "../../auth/useAuth"
import type { FormEvent } from "react"
import './Login.css'
import { useNavigate } from "react-router"


export function Login() {
  const { login, user } = useAuth()
  const [username, setUserName] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)

    try {
      await login({ email: username, password })
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message)
      } else {
        setError("Something went wrong")
      }
    }
    if (user) {
      navigate('/')
    }
  }

  return (
    <div className="login-page">

      <div className="left-side-page">
        <div className="brand-logo"></div>
        <div className="branding-content">
          <h1>Data management, re-imagined from scratch.</h1>
          <p>Join over 40,000 developers building lightning-fast applications with our secure, global framework.</p>
        </div>
        <div className="brand-footer">© 2026 MoonWatch</div>


      </div>

      <div className="right-side-page">
        <form className='login-form' onSubmit={handleSubmit}>
          <div className="form-header">
            <h2>Welcome back</h2>
            <p>Enter your details to sign in to your workspace</p>
          </div>

          <div className="input-group">
            <input
              id="username"
              name="username"
              type="email"
              placeholder="you@example.com"
              required
              value={username}
              onChange={(e) => setUserName(e.target.value)}
            />
          </div>

          <div className="input-group">
            <input
              id="password"
              name="password"
              type="password"
              placeholder="••••••••"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" className="submit-btn">Sign in to Account</button>
        </form>
        {error && <p>{error}</p>}
      </div>
    </div>
  )
}