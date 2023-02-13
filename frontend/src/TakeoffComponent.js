import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import { useState } from "react";
import axios from 'axios'
import "./App.css";

const BACKEND_URL = "http://127.0.0.1:8080";

const OK_CODE = 200;

function TakeoffComponent() {
  const [takeoffTime, setTakeoffTime] = useState("");
  const [takeoffDistance, setTakeoffDistance] = useState("");
  const [takeoffOverweightMass, setTakeoffOverweightMass] = useState("");
  const [aircraftMass, setAircraftMass] = useState("");


  /**
   * Handles the click generate, will handle query and result output
   * @param {*} event 
   */
  const handleGenerate = async (event) => {
    const response = await axios.get(
      BACKEND_URL + "/getTakeoffStats?mass=" + aircraftMass
    );
    const { status, data } = response;
    if (status === OK_CODE) {
      setTakeoffDistance(data["takeoff_distance"]);
      setTakeoffTime(data["takeoff_time"]);
      if (data["overweight_mass"] != null) {
        setTakeoffOverweightMass(data["overweight_mass"]);
      } else {
        setTakeoffOverweightMass("Not required");
      }
    } else {
      setTakeoffDistance(data);
      setTakeoffOverweightMass(data);
      setTakeoffTime(data);
    }
  };


  /**
   * Handles the validity check of the mass input
   * @param {Event} event the event of the string input   
   */
  const handleInput = (event) => {
    const value = event.target.value;
    if (!/^\d+$/.test(value)) {
      return;
    }
    setAircraftMass(value);
  };
  return (
    <>
      <h1 className="upload-title">Takeoff stats for C130 (Shimshon)</h1>

      <TextField
        label="Aircraft Mass"
        value={aircraftMass}
        onInput={handleInput}
        error={false}
        variant="outlined"
      />

      <Button
        sx={{ color: "rgb(19, 23, 32)", marginTop: "1.2rem" }}
        variant="outlined"
        onClick={handleGenerate}
      >
        Generate
      </Button>

      <div className="results">
        <TextField
          className="upload-"
          disabled={true}
          label="Takeoff distance"
          value={takeoffDistance}
          error={false}
          variant="outlined"
        />
        <TextField
          className="upload-"
          disabled={true}
          label="Takeoff Time"
          value={takeoffTime}
          variant="outlined"
        />
        <TextField
          className="upload-"
          disabled={true}
          label="Overweight mass"
          value={takeoffOverweightMass}
          variant="outlined"
        />
      </div>
    </>
  );
}

export default TakeoffComponent;