import Box from "@mui/material/Box"
import Card from "@mui/material/Card"
import CardActions from "@mui/material/CardActions"
import CardContent from "@mui/material/CardContent"
import Button from "@mui/material/Button"
import Typography from "@mui/material/Typography"
import type { Watchlist } from "../types/types"

type Props = {
  watchlist: Watchlist
}

export function WatchlistCards({ watchlist }: Props) {
  if (watchlist.length === 0) {
    return <Typography color="text.secondary">Your watchlist is empty.</Typography>
  }

  return (
    <Box sx={{ display: "flex", flexWrap: "wrap", gap: 2 }}>
      {watchlist.map((item) => (
        <Card key={item.id} variant="outlined" sx={{ minWidth: 275 }}>
          <CardContent>
            <Typography gutterBottom sx={{ color: "text.secondary", fontSize: 14 }}>
              Watchlist
            </Typography>
            <Typography variant="h5" component="div">
              {item.coin.name}
            </Typography>
          </CardContent>
          <CardActions>
            <Button size="small">View</Button>
          </CardActions>
        </Card>
      ))}
    </Box>
  )
}