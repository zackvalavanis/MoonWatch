


export interface User {
  token: string | null
  first_name: string
  last_name: string
}

export interface LoginInfo {
  email: string
  password: string
}

export interface AuthContextType {
  user: User | null
  loading: boolean
  login: (credentials: LoginInfo) => Promise<void>
  logout: () => void
}