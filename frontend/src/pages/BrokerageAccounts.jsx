import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./styles.css";
import "./BrokerageAccounts.css";

export default function BrokerageAccounts() {
  const navigate = useNavigate();
  const [accounts, setAccounts] = useState([]);
  const [newAccount, setNewAccount] = useState("");
  const [loading, setLoading] = useState(true);  // 🔹 Add loading state
  const token = localStorage.getItem("token");

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }

    axios
      .get("http://127.0.0.1:8000/brokerage-accounts", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => {
        setAccounts(response.data);
      })
      .catch((error) => console.error("Error fetching accounts:", error))
      .finally(() => setLoading(false)); // 🔹 Set loading to false after API call
  }, [navigate, token]);

  const handleLinkAccount = () => {
    if (!newAccount) return;
    axios
      .post(
        "http://127.0.0.1:8000/brokerage-accounts",
        { account_name: newAccount },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then((response) => {
        setAccounts([...accounts, response.data]);
        setNewAccount("");
      })
      .catch((error) => console.error("Error linking account:", error));
  };

  const handleUnlinkAccount = (accountId) => {
    axios
      .delete(`http://127.0.0.1:8000/brokerage-accounts/${accountId}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(() => setAccounts(accounts.filter((acc) => acc.id !== accountId)))
      .catch((error) => console.error("Error unlinking account:", error));
  };

  return (
    <div className="brokerage-container">
      <h2 className="title">Manage Linked Brokerage Accounts</h2>

      {loading ? (
        <p>Loading accounts...</p>  // 🔹 Show loading message
      ) : accounts.length > 0 ? (
        <div className="account-list">
          {accounts.map((account) => (
            <div key={account.id} className="account-item">
              <span>{account.account_name}</span>
              <button className="unlink-button" onClick={() => handleUnlinkAccount(account.id)}>Unlink</button>
            </div>
          ))}
        </div>
      ) : null} {/* 🔹 If no accounts, don't display anything */}

      <div className="input-section">
        <input
          type="text"
          className="account-input"
          placeholder="Enter new brokerage account"
          value={newAccount}
          onChange={(e) => setNewAccount(e.target.value)}
        />
        <button className="link-button" onClick={handleLinkAccount}>Link Account</button>
      </div>

      <div className="button-container">
        <button className="back-button" onClick={() => navigate("/dashboard")}>Back to Dashboard</button>
      </div>
    </div>
  );
}
