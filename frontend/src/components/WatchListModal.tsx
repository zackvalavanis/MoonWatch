import Box from "@mui/material/Box"
import Modal from "@mui/material/Modal"
import Typography from "@mui/material/Typography"
import type { WatchlistItem } from "../types/types"

type Props = {
  item: WatchlistItem | null
  onClose: () => void
}

export function WatchListModal({ item, onClose }: Props) {
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
            <Typography>24h: {item.coin.percent_change_24h?.toFixed(2)}%</Typography>
          </>
        )}
      </Box>
    </Modal>
  )
}