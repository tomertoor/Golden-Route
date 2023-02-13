import "./App.css";

import { useEffect } from "react";

import TakeoffComponent from "./TakeoffComponent";
import TimeComponent from "./CheckTime";



function App() {
  //Sets the title
  useEffect(() => 
  {
    document.title = "Golden route submission"
  }, []);


  return (
    <>
      <div className="outer-div">
        <TakeoffComponent></TakeoffComponent>
      </div>

      <div className="outer-div">
        <TimeComponent></TimeComponent>
      </div>
    </>
  );
}

export default App;
