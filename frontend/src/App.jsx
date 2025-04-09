import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css"; // Updated styles
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import EditProfile from "./pages/EditProfile";
import BrokerageAccounts from "./pages/BrokerageAccounts";
import Trade from "./pages/Trade";

function App() {
  const isLoggedIn = !!localStorage.getItem("token"); // Check if user is logged in

  return (
    <Router>
      <div className="welcome-container">
        {!isLoggedIn && ( // Show navbar only if the user is not logged in
          <nav className="navbar">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/register" className="nav-link">Register</Link>
            <Link to="/login" className="nav-link">Login</Link>
          </nav>
        )}

        <Routes>
          <Route
            path="/"
            element={
              <div className="welcome-content">
                <h1 className="welcome-title">Welcome to the Trading Platform</h1>
                <p className="welcome-description">
                  Start your journey in AI-powered trading. Register or log in to access your dashboard.
                </p>
                <div className="welcome-buttons">
                  <Link to="/register" className="btn primary-btn">Get Started</Link>
                  <Link to="/login" className="btn secondary-btn">Login</Link>
                </div>
              </div>
            }
          />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/edit-profile" element={<EditProfile />} />
          <Route path="/brokerage-accounts" element={<BrokerageAccounts />} />
          <Route path="/trade" element={<Trade />} /> {/* Add Trade Route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
