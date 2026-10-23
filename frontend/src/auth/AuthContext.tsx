import React, { useContext, useState } from "react"
import type { LoginInfo, User } from "../types/types"
import type { AuthContextType } from "../types/types"
import { createContext } from "react"
import type { ReactNode } from "react"

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const api = import.meta.env.VITE_BACKEND_API
  console.log(api)


  const logout = () => {
    setToken(null)
    localStorage.removeItem("Access_token")
    setUser(null)
  }

  const login = async (credentials: LoginInfo) => {
    setLoading(true)
    try {
      const res = await fetch(`${api}/auth/login`, {
        "method": "POST",
        body: new URLSearchParams({ username: credentials.email, password: credentials.password })
      })
      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Login Failed")
      }

      if (!data?.access_token) {
        throw new Error('Something went wrong')
      }

      const accessToken = data.access_token
      console.log(data)
      localStorage.setItem("Access_token", accessToken)
      setToken(accessToken)

      try {
        const get_current_user = await fetch(`${api}/auth/me`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        })

        if (!get_current_user.ok) {
          logout()
          throw new Error("Couldn't load your account. Please try again.")
        }

        const currentUser = await get_current_user.json()
        setUser(currentUser)
      } catch (error) {
        logout()
        throw new Error("Couldn't load your account. Please try again.")
      }
    } catch (error) {
      console.error("Login error", error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthContext.Provider value={{ user, login, loading, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)

  if (context == null) {
    throw new Error("useAuth must be inside AuthProvider")
  }

  return context;
}