import Box from "@mui/material/Box"
import Card from "@mui/material/Card"
import CardActions from "@mui/material/CardActions"
import CardContent from "@mui/material/CardContent"
import Button from "@mui/material/Button"
import Typography from "@mui/material/Typography"
import type { Watchlist } from "../types/types"
import { useState } from "react"
import { WatchListModal } from "./WatchListModal"

type WatchlistItem = Watchlist[number]

type Props = {
  watchlist: Watchlist
}

export function WatchlistCards({ watchlist }: Props) {
  const [selectedItem, setSelectedItem] = useState<WatchlistItem | null>(null)

  if (watchlist.length === 0) {
    return <Typography color="text.secondary">Your watchlist is empty.</Typography>
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", minHeight: "75vh" }}>
      <Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", flexWrap: "wrap", gap: 2 }}>
        {watchlist.map((item) => {
          const change = item.coin.percent_change_24h

          return (
            <Card
              key={item.id}
              variant="outlined"
              sx={{
                minWidth: 275,
                borderLeft: 4,
                borderLeftColor:
                  change == null ? "divider" : change < 0 ? "error.main" : "success.main",
              }}
            >
              <CardContent>
                <Typography gutterBottom sx={{ color: "text.secondary", fontSize: 14 }}>
                  {item.coin.symbol}
                </Typography>
                <Typography variant="h5" component="div">
                  {item.coin.name}
                </Typography>
                <Typography
                  sx={{
                    color: change == null ? "text.secondary" : change < 0 ? "error.main" : "success.main",
                  }}
                >
                  {change == null ? "—" : `${change > 0 ? "+" : ""}${change.toFixed(2)}%`}
                </Typography>
              </CardContent>
              <CardActions>
                <Button onClick={() => setSelectedItem(item)} size="small">
                  View
                </Button>
              </CardActions>
            </Card>
          )
        })}
      </Box>

      <WatchListModal item={selectedItem} onClose={() => setSelectedItem(null)} />
    </div>
  )
}