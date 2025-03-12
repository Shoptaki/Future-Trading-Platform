import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import EditProfile from "./pages/EditProfile";
import BrokerageAccounts from "./pages/BrokerageAccounts";


function App() {
  return (
    <Router>
      <nav style={{ padding: "10px", display: "flex", gap: "15px" }}>
        <Link to="/">Home</Link>
        <Link to="/register">Register</Link>
        <Link to="/login">Login</Link>
      </nav>

      <Routes>
        <Route path="/" element={<h1>Welcome to the Trading Platform</h1>} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/edit-profile" element={<EditProfile />} />
        <Route path="/brokerage-accounts" element={<BrokerageAccounts />} />
      </Routes>
    </Router>
  );
}

export default App;
