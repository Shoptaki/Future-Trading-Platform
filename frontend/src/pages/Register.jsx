import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./styles.css"; // Import styles



export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
  
    const userData = {
      username,
      password,
      email,
      first_name: firstName,
      last_name: lastName,
    };
  
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/register",
        userData, // ✅ Send JSON instead of FormData
        { headers: { "Content-Type": "application/json" } } // ✅ Ensure JSON is sent
      );
  
      console.log("🔹 Response from Backend:", response.data);
  
      if (response.data.message === "User created") {
        navigate("/login");
      } else {
        setError("Error registering user");
      }
    } catch (error) {
      console.log("❌ Error:", error.response?.data);
      setError(error.response?.data?.detail || "Error registering user");
    }
  };
 
  
  return (
    <div className="container">
      <h1>Register</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button onClick={handleRegister}>Register</button>
      </form>
    </div>
    
  );
}