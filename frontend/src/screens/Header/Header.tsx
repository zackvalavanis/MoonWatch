
import { useNavigate } from "react-router"
import "./Header.css"
import TemporaryDrawer from "../../components/MUDrawer"

export function Header() {
  const navigate = useNavigate();

  return (
    <div className='header'>

      <div className="left-side">

      </div>

      <div className="middle">
        <img onClick={() => navigate('/')} src="/moonIcon.svg" className="header-moon" alt="Moon Icon" />
      </div>

      <div className='right-side'>
        <TemporaryDrawer />
      </div>
    </div>
  )
}
