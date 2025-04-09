import { useState } from "react";
import BackButton from "../components/BackButton";
import "./Trade.css";

export default function Trade() {
  const [botStatus, setBotStatus] = useState("stopped");

  const handleStartBot = () => {
    setBotStatus("running");
    alert("Trade bot started!");
    // Add API call to start the bot if needed
  };

  const handleStopBot = () => {
    setBotStatus("stopped");
    alert("Trade bot stopped!");
    // Add API call to stop the bot if needed
  };

  return (
    <div className="trade-container trade-page">
      <h2>Trade Bot Control</h2>
      <p>Current Status: <strong>{botStatus === "running" ? "Running" : "Stopped"}</strong></p>
      <div className="button-group">
        <button className="start-button" onClick={handleStartBot}>
          Start Trade Bot
        </button>
        <button className="stop-button" onClick={handleStopBot}>
          Stop Trade Bot
        </button>
      </div>
      <div className="back-button-container">
        <BackButton />
      </div>
    </div>
  );
}