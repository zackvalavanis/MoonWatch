import { useEffect, useState } from "react";
import { useAuth } from "../../auth/useAuth";
import { fetch_watchlist } from "../../hooks/fetchwatchlist";
import type { Watchlist } from "../../types/types";
import { WatchlistCards } from "../../components/watchlist_cards"

export function ProfilePage() {
  const { user, token } = useAuth();
  const [watchlist, setWatchlist] = useState<Watchlist>([])

  console.log(watchlist)


  useEffect(() => {
    if (!token) return;
    fetch_watchlist(token)
      .then(setWatchlist)
      .catch((err) => console.log(err))
  }, [token])

  return (
    <div className="profile-page">
      <div className='watchlist-top-scrolling'>

      </div>
      <div className='name-top-left'>
        {user && <p>{user.first_name + " " + user.last_name}</p>}
      </div>

      <div className='middle-section'>
        <WatchlistCards watchlist={watchlist} />
      </div>
    </div>
  )
}