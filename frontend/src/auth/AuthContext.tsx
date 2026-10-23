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

  const login = async (credentials: LoginInfo) => {
    setLoading(true)
    try {
      const res = await fetch(`${api}/auth/login`, {
        "method": "POST",
        body: new URLSearchParams({ username: credentials.email, password: credentials.password })
      })
      const data = await res.json();

      if (!res.ok) {
        console.log("Error")
        return;
      }

      if (!data?.access_token) {
        console.log("No access token returned from the servere")
        return;
      }
      console.log(data)
      localStorage.setItem("Access_token", data.access_token)
      setToken(data.access_token)
    } catch (error) {
      console.error("Error", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthContext.Provider value={{ user, login, loading }}>
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