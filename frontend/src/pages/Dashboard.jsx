import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Dashboard.css"; // Ensure this file is correctly linked

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
    navigate("/");
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {user ? user.first_name : "User"}!</h1>
        <p>Your Trading Dashboard</p>
      </div>

      <div className="profile-section">
        {user ? (
          <>
            <p><strong>Name:</strong> {user.first_name} {user.last_name}</p>
            <p><strong>Email:</strong> {user.email}</p>
          </>
        ) : (
          <p>Loading profile...</p>
        )}
      </div>

      <div className="button-group">
        <button className="dashboard-button edit-profile" onClick={() => navigate("/edit-profile")}>
          Edit Profile
        </button>
        <button className="dashboard-button manage-accounts" onClick={() => navigate("/brokerage-accounts")}>
          Manage Brokerage Accounts
        </button>
        <button className="dashboard-button logout" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
}
