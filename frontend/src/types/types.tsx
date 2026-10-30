export interface Coin {
  id: string
  cmc_id: number
  name: string
  symbol: string
  slug: string | null
  price_usd: string | null
  market_cap: string | null
  percent_change_1h: number | null
  percent_change_24h: number | null
  percent_change_7d: number | null
  percent_change_30d: number | null
  percent_change_60d: number | null
  percent_change_90d: number | null
  volume: number | null
  volume_change_24h: number | null
  market_cap_dominance: number | null
  fully_diluted_market_cap: number | null
  last_updated: string | null
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

export interface WatchListModalProps {
  item: WatchlistItem | null
  onClose: () => void
}