
export interface Coin {
  id: string
  cmc_id: number
  name: string
  symbol: string
  slug: string
  price_usd: string
  percent_change_24h: string
  market_cap: string
}


export interface User {
  id: string | null
  token: string | null
  first_name: string
  last_name: string
}

export interface LoginInfo {
  email: string
  password: string
}

export interface SignupInfo {
  first_name: string
  last_name: string
  email: string
  password: string
}


export interface AuthContextType {
  user: User | null
  loading: boolean
  login: (credentials: LoginInfo) => Promise<void>
  logout: () => void
  token: string | null
}

export interface WatchlistItem {
  id: string
  created_at: string
  coin: Coin
}

export type Watchlist = WatchlistItem[]