import Box from "@mui/material/Box"
import Modal from "@mui/material/Modal"
import Typography from "@mui/material/Typography"
import type { WatchlistItem } from "../types/types"

type Props = {
  item: WatchlistItem | null
  onClose: () => void
}

export function WatchListModal({ item, onClose }: Props) {
  const changeColor = (value: number | null) =>
    value == null ? "text.secondary" : value < 0 ? "error.main" : "success.main"

  return (
    <Modal open={item !== null} onClose={onClose}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: 400,
          bgcolor: "background.paper",
          borderRadius: 2,
          boxShadow: 24,
          p: 4,
        }}
      >
        {item && (
          <>
            <Typography variant="h5">
              {item.coin.name} ({item.coin.symbol})
            </Typography>
            <Typography>Price: ${Number(item.coin.price_usd).toLocaleString()}</Typography>

            <Typography sx={{ color: changeColor(item.coin.percent_change_1h) }}>
              1h: {item.coin.percent_change_1h?.toFixed(2)}%
            </Typography>

            <Typography sx={{ color: changeColor(item.coin.percent_change_24h) }}>
              24h: {item.coin.percent_change_24h?.toFixed(2)}%
            </Typography>

            <Typography sx={{ color: changeColor(item.coin.percent_change_30d) }}>
              30d: {item.coin.percent_change_30d?.toFixed(2)}%
            </Typography>

            <Typography sx={{ color: changeColor(item.coin.percent_change_60d) }}>
              60d: {item.coin.percent_change_60d?.toFixed(2) ?? "—"}%
            </Typography>
            <Typography>Market cap: ${Number(item.coin.market_cap).toLocaleString(undefined, { maximumFractionDigits: 0 })}</Typography>
            <div>
              <h1>GRAPH HERE</h1>
            </div>

          </>
        )}
      </Box>
    </Modal>
  )
}