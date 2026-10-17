import { BrowserRouter, Routes, Route } from "react-router";
import { Header } from "./screens/Header/Header";
import { Footer } from "./screens/Footer/Footer";
import { HomePage } from "./screens/HomePage/HomePage";
import { ProfilePage } from "./screens/Profile/ProfilePage";
import { AboutPage } from "./screens/About/AboutPage";


function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Header />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/About" element={<AboutPage />} />
            <Route path="/profile/:userId" element={<ProfilePage />} />
          </Routes>
        </main>
        <Footer />
      </div >
    </BrowserRouter >
  );
}

export default App;
