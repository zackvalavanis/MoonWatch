
import type { Watchlist } from "../types/types"

const api = import.meta.env.VITE_BACKEND_API

export async function fetch_watchlist(token: string): Promise<Watchlist> {
  const res = await fetch(`${api}/main/watchlist`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!res.ok) {
    throw new Error("Couldn't load your watchlist", {
      cause: fetch_watchlist
    })
  }

  return (
    res.json()
  )
}