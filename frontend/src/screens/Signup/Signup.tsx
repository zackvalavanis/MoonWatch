import { useState } from "react"
import "./Signup.css"
import { useNavigate } from "react-router"
import type { SignupInfo } from "../../types/types"
import { useAuth } from "../../auth/useAuth"


export function Signup() {
  const [username, setUserName] = useState("")
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const api = import.meta.env.VITE_BACKEND_API
  const { login } = useAuth()

  const handleSignup = async (credentials: SignupInfo) => {
    try {
      const res = await fetch(`${api}/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          first_name: credentials.first_name,
          last_name: credentials.last_name,
          email: credentials.email,
          password: credentials.password,
        }),
      })
      if (!res.ok) {
        throw new Error("There was an error signing up.")
      }

      await login({ email: credentials.email, password: credentials.password })
      navigate("/")
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to signup")
    }
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)

    await handleSignup({
      first_name: firstName,
      last_name: lastName,
      email: username,
      password,
    })
  }

  return (
    <div className="signup-page">

      <div className="left-side-page">
        <div className="brand-logo"></div>
        <div className="branding-content">
          <h1>Data management, re-imagined from scratch.</h1>
          <p>Join over 40,000 developers building lightning-fast applications with our secure, global framework.</p>
        </div>
        <div className="brand-footer">© 2026 MoonWatch</div>


      </div>

      <div className="right-side-page">
        <form className='signup-form' onSubmit={handleSubmit}>
          <div className="form-header">
            <h2>Welcome</h2>
            <p>Enter your details to sign up</p>
          </div>

          <div className="input-group">
            <input
              id="first_name"
              name="first_name"
              type="text"
              placeholder="First Name"
              required
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
            />
          </div>

          <div className="input-group">
            <input
              id="last_name"
              name="last_name"
              type="text"
              placeholder="Last Name"
              required
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
            />
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
          <button type="submit" className="submit-btn">Sign up</button>
        </form>
        {error && <p>{error}</p>}
      </div>
    </div>
  )
}