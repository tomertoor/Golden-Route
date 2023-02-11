import react, { useState } from 'react';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import * as dayjs from 'dayjs';

import axios from 'axios';

import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const BACKEND_URL = "http://127.0.0.1:8080"

function TimeComponent(props) {
    const [date, setDate] = useState(dayjs()); // initialize state with today's date

    const handleCheck = async () => {
        const response = await axios.get(BACKEND_URL + '/checkTakeoffTime', {params: {date: date.format('YYYY-MM-DD')}});
        const { status, data } = response;
        console.log(data, data.length);

    }

    return (
        <>
            <h1 className='upload-title'>Weather checker for C130 (Shimshon)</h1>
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
            <Button sx={{ color: 'rgb(19, 23, 32)', marginTop: '1.2rem' }} variant="outlined" onClick={handleCheck}>Check</Button>

        </>
    )
}

export default TimeComponent;