import { useState } from "react";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";

import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import Checkbox from "@mui/material/Checkbox";

import * as dayjs from "dayjs";

import axios from "axios";

import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

const OK_CODE = 200;

const BACKEND_URL = "http://127.0.0.1:8080";

function ResultsComponent({hours}) {
    let hour = 0;

  return (
    <>
    <h1>Available hours:</h1>
      <List
        dense
        sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}
      >
        {
          //Goes over the hours list and for each values creates a listitem with a checkbox based on the list items
          hours.map((value) => {
          hour++;
          const labelId = `checkbox-list-secondary-label-${hour}`;
          return (
            <ListItem
              key={hour}
              secondaryAction={
                <Checkbox disabled
                  edge="end"
                  checked={value === true}
                  inputProps={{ "aria-labelledby": labelId }}
                />
              }
              disablePadding
            >
              <ListItemButton>
                <ListItemText id={labelId} primary={`${hour-1}:00`} />
              </ListItemButton>
            </ListItem>
          );
          })}
      </List>
    </>
  );
}

function TimeComponent() {
  const [date, setDate] = useState(dayjs()); // initialize state with today's date

  const [hasChecked, setChecked] = useState(false);
  const [hours, setHours] = useState([]);


  /**
   * Click handler which performs the api request and updates the state of the hour list
   */
  const handleCheck = async () => {
    const response = await axios.get(BACKEND_URL + "/checkTakeoffTime", {
      params: { date: date.format("YYYY-MM-DD") },
    });
    const { status, data } = response;
    if (status === OK_CODE) {
        setChecked(true)
        setHours(data)
    }
  };

  return (
    <>
      <h1 className="upload-title">Weather checker for C130 (Shimshon)</h1>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DatePicker
          label="Choose date"
          value={date}
          onChange={(newValue) => {
            setDate(newValue);
          }}
          renderInput={(params) => <TextField {...params} />}
        />
      </LocalizationProvider>
      <Button
        sx={{ color: "rgb(19, 23, 32)", marginTop: "1.2rem" }}
        variant="outlined"
        onClick={handleCheck}
      >
        Check
      </Button>
      {hasChecked ? <ResultsComponent hours={hours}/>
      : null}
      
    </>
  );
}

export default TimeComponent;
