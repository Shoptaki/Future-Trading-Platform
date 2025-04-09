import { useNavigate } from "react-router-dom";
import "./BackButton.css";

export default function BackButton() {
  const navigate = useNavigate();

  return (
    <button className="back-button" onClick={() => navigate("/dashboard")}>
      Back to Dashboard
    </button>
  );
}