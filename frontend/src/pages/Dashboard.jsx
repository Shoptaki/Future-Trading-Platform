import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Dashboard.css";

export default function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }

    axios
      .get("http://127.0.0.1:8000/profile", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => {
        setUser(response.data);
      })
      .catch((error) => {
        console.error("Error fetching profile:", error);
        navigate("/login");
      });
  }, [navigate, token]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="dashboard-layout">
      <nav className="tab-menu">
        <button onClick={() => navigate("/dashboard")}>Dashboard</button>
        <button onClick={() => navigate("/edit-profile")}>Edit Profile</button>
        <button onClick={() => navigate("/brokerage-accounts")}>
          Manage Accounts
        </button>
        <button onClick={() => navigate("/backtest")}>Backtest</button>
        <button onClick={() => navigate("/trade")}>Trade</button>
        <button onClick={handleLogout}>Logout</button>
      </nav>
      <main className="dashboard-content">
        <header>
          <h1>Welcome, {user ? user.first_name : "User"}!</h1>
          <p>Your Trading Dashboard</p>
        </header>
        <section className="dashboard-details">
          <p>Here you can manage your trading activities, backtest strategies, and more.</p>
        </section>
      </main>
    </div>
  );
}
