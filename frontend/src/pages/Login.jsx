import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./styles.css"; // Import styles
import { Link } from "react-router-dom";



export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
  
    try {
      const formData = new FormData();
      formData.append("username", username);
      formData.append("password", password);
  
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/login",
        formData,
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
      );
  
      console.log("🔹 Response from Backend:", response.data); // Debugging
  
      if (response.data.access_token && response.data.user_id) {
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("userId", response.data.user_id); // 🔹 Store userId
        navigate("/dashboard");
      } else {
        setError("Invalid login credentials");
      }
    } catch (error) {
      console.log("❌ Error:", error.response?.data);
      setError(error.response?.data?.detail || "Login failed");
    }
  };
  
  
  

  return (
    <div className="container">
      <h1>Login</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleLogin}>
        <input 
          type="text" 
          placeholder="Username" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
          required 
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          required 
        />
        <button type="submit">Login</button>
      </form>
      <p>
        Don't have an account? <Link to="/register">Register here</Link>
      </p>
    </div>
  );
}
