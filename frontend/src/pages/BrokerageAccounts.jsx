import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./styles.css";
import "./BrokerageAccounts.css";

export default function BrokerageAccounts() {
  const navigate = useNavigate();
  const [accounts, setAccounts] = useState([]);
  const [broker, setBroker] = useState("");  // 🔹 Changed from newAccount to broker
  const [accountNumber, setAccountNumber] = useState("");
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token");
  const userId = localStorage.getItem("userId"); 

  
  useEffect(() => {
    if (!token || !userId) {
      navigate("/login");
      return;
    }
  
    axios
      .get(`http://127.0.0.1:8000/brokerage-accounts/${userId}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => setAccounts(response.data))
      .catch((error) => {
        console.error("Error fetching accounts:", error);
        if (error.response && error.response.status === 401) {
          localStorage.removeItem("token");
          navigate("/login");
        }
      })
      .finally(() => setLoading(false));
  }, [navigate, token, userId]);
  

  const handleLinkAccount = () => {
    if (!broker || !accountNumber) return;
  
    axios
      .post(
        "http://127.0.0.1:8000/brokerage-accounts",
        { user_id: parseInt(userId), broker, account_number: accountNumber },  // 🔹 Added user_id
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then((response) => {
        setAccounts([...accounts, response.data.account]);
        setBroker("");
        setAccountNumber("");
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
        <p>Loading accounts...</p>
      ) : accounts.length > 0 ? (
        <div className="account-list">
          {accounts.map((account) => (
            <div key={account.id} className="account-item">
              <span>{account.broker} - {account.account_number}</span>  {/* 🔹 Display both fields */}
              <button className="unlink-button" onClick={() => handleUnlinkAccount(account.id)}>Unlink</button>
            </div>
          ))}
        </div>
      ) : (
        <p>No linked accounts yet.</p>  // 🔹 Show a message instead of empty space
      )}

      <div className="input-section">
        <input
          type="text"
          className="account-input"
          placeholder="Broker Name (e.g., IBKR, Tradeovate)"
          value={broker}
          onChange={(e) => setBroker(e.target.value)}
        />
        <input
          type="text"
          className="account-input"
          placeholder="Account Number"
          value={accountNumber}
          onChange={(e) => setAccountNumber(e.target.value)}
        />
        <button className="link-button" onClick={handleLinkAccount}>Link Account</button>
      </div>

      <div className="button-container">
        <button className="back-button" onClick={() => navigate("/dashboard")}>Back to Dashboard</button>
      </div>
    </div>
  );
}
