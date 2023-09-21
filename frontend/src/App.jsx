import { useState, useEffect } from "react";
import "./App.css";
import Table from "./Table.jsx";
import axios from "axios";
import Modal from "./Modal.jsx";
import Loader from "./Loader.jsx";

function App() {
  const [airData, setAirData] = useState([]);
  const [sheetLink, setSheetLink] = useState("");
  const [link, setLink] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [modal, setModal] = useState(false);

  const callScrape = async () => {
    let inputLink = link;
    if (link == "") {
      setLink("https://www.airbnb.com/s/California--United-States/homes");
      inputLink = "https://www.airbnb.com/s/California--United-States/homes";
    }

    // let backendAPI = "http://localhost:5000/apiv1";
    let backendAPI = import.meta.env.VITE_BACKEND;
    let res;

    try {
      res = await axios.post(backendAPI, { url: inputLink });
    } catch (e) {
      setError("Whoops! Error in our backend. Please try again later.");
      setLoading(false);
      return;
    }
    // if we are here then we got something back from our api

    if (res.data.ok) {
      // build table and set sheetlink
      setSheetLink(res.data.link);
      setAirData(res.data.data);
    } else {
      setError(res.data.error);
    }
    setLoading(false);
  };

  useEffect(async () => {
    let backendAPI = import.meta.env.VITE_BACKEND;
    try {
      res = await axios.get(backendAPI);
      console.log('backend connected')
    } catch (e) {
      console.log('backend error')
      console.log(e)
    }

  },[])

  return (
    <>
      <nav className="App-nav">
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://clifford-chan.vercel.app/"
        >
          <svg
            version="1.1"
            id="logo"
            xmlns="http://www.w3.org/2000/svg"
            x="0px"
            y="0px"
            viewBox="0 0 372 372"
            className="App-nav-logo"
          >
            <g>
              <path
                d="M186,0C83.439,0,0,83.439,0,186s83.439,186,186,186s186-83.439,186-186S288.561,0,186,0z M350.163,210.679h-85.292
              C270.751,201.699,280.85,196,292.1,196h59.59C351.394,200.953,350.886,205.85,350.163,210.679z M186,20
              c88.174,0,160.501,69.106,165.69,156H292.1c-24.333,0-45.337,16.514-51.079,40.16l-17.96,73.964l-37.159-153.032
              c-6.827-28.117-31.803-47.754-60.737-47.754H51.127C81.283,47.381,130.502,20,186,20z M38.797,109.338h86.368
              c17.638,0,33.106,10.736,39.466,26.733H27.677C30.613,126.782,34.349,117.846,38.797,109.338z M21.837,210.685
              c-0.723-4.83-1.231-9.729-1.527-14.685h63.068c11.249,0,21.348,5.699,27.228,14.679H21.952
              C21.913,210.679,21.876,210.684,21.837,210.685z M26.114,230.679H117.4l28.252,116.353
              C87.928,332.563,42.095,287.794,26.114,230.679z M167.149,350.923c-0.035-0.19-0.062-0.38-0.108-0.57L134.456,216.16
              C128.714,192.514,107.71,176,83.377,176H20.31c0.404-6.758,1.207-13.41,2.399-19.929h147.22l42.841,176.434l-4.334,17.848
              c-0.01,0.043-0.015,0.086-0.024,0.128C201.08,351.476,193.601,352,186,352C179.626,352,173.338,351.626,167.149,350.923z
              M230.062,346.053l28.015-115.374h87.809C330.249,286.563,286.033,330.626,230.062,346.053z"
              />
            </g>
          </svg>
        </a>
        <h1 className="App-nav-title">Airbnb Tableizer</h1>
        <p
          className="App-nav-info "
          onClick={() => {
            setModal((prev) => !prev);
          }}
        >
          Info
        </p>
      </nav>

      <div className="App-helloTraveler">
        <div className="App-bigtext">Hello Traveler,</div>
        <div className="App-smalltext">
          Enter an Airbnb link below and I will tableize it for you:
        </div>
        {/* <div className="App-smalltext">
          &emsp; &emsp; Enter an airbnb link below:
        </div> */}
      </div>
      <div className="App-form">
        <input
          className="App-input"
          placeholder="https://www.airbnb.com/s/California--United-States/homes"
          type="text"
          value={link}
          onChange={(e) => {
            setLink(e.target.value);
          }}
        />
        <button
          className="App-button"
          onClick={() => {
            if (!loading) {
              setError("");
              setSheetLink("");
              setAirData([]);
              setLoading(true);
              callScrape();
            }
          }}
        >
          Tableize!
        </button>
      </div>
      {modal && <Modal setModal={setModal} />}
      {loading == true ? (
        <Loader />
      ) : error != "" ? (
        <div className="App-errormsg">Error: {error}</div>
      ) : airData.length > 0 ? (
        <>
          <div className="App-googleSheet">
            Google Sheet for your convenience: &ensp;
            <a target="_blank" rel="noopener noreferrer" href={sheetLink}>
              {sheetLink}
            </a>
          </div>
          <Table results={airData} />
        </>
      ) : (
        ""
      )}
    </>
  );
}

export default App;
