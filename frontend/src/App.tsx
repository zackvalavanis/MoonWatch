import { BrowserRouter, Routes, Route } from "react-router";
import { Header } from "./screens/Header/Header";
import { Footer } from "./screens/Footer/Footer";
import { HomePage } from "./screens/HomePage/HomePage";
import { ProfilePage } from "./screens/Profile/ProfilePage";
import { AboutPage } from "./screens/About/AboutPage";
import { Login } from "./screens/Login/Login";
import { Signup } from "./screens/Signup/Signup";


function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Header />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/About" element={<AboutPage />} />
            <Route path="/profile/:userId" element={<ProfilePage />} />
            <Route path="/signup" element={<Signup />} />
          </Routes>
        </main>
        <Footer />
      </div >
    </BrowserRouter >
  );
}

export default App;
