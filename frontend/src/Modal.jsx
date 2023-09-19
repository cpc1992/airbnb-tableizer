import "./Modal.css";

export default function Modal({ setModal }) {
  return (
    <div
      className="Modal-overlay"
      onClick={() => {
        setModal((prev) => !prev);
      }}
    >
      <div
        className="Modal-main"
        onClick={(e) => {
          e.stopPropagation();
        }}
      >
        <div className="Modal-content">
          <h2 className="Modal-title">Welcome to the Airbnb Tableizer!</h2>
          <p>
            This is a tool that gathers Airbnb data into a Google Sheet. Prior
            to a trip, I would always do an Airbnb search and manually copy all
            of the data into a Google Sheet in order to compare rentals. That
            became too much work so I built this scraper tool to save some time.
          </p>
          <h3>How to use:</h3>
          <ul>
            <li>
              1) &ensp; Do a search on the Airbnb website (specifying
              checkin/checkout dates and number of guests helps, but is not
              necessary)
            </li>
            <li>
              2) &ensp; Copy that link into the Airbnb Tableizer and click
              Tableize!
            </li>
            <li>
              3) &ensp; The data will be previewed for you on the screen and a
              Google Sheet will be created for you.
            </li>
            <li>
              4) &ensp; Duplicate or save the contents of the Google Sheet for
              your own use.
            </li>
            <li>5) &ensp; Have a nice and relaxing vacation!</li>
          </ul>
          <h3>Usage notes:</h3>
          <p className="Modal-specs">
            * Some listings incorrectly list the bed & bedroom information in
            the bathrooms attribute.
            <br />* The Accurate column indicates if the price displayed is the
            price <i>after</i> service and cleaning fees.
          </p>
          <h3>Specs:</h3>
          <p className="Modal-specs">
            This app consists of a React frontend and a Flask backend. The
            webscraping is done with BeautifulSoup and the Google Sheet is
            generated using Gspread and Gspread-formatting.
          </p>
          <div className="Modal-footer">
            <div>CliffordPChan@gmail.com</div>
            <div className="Modal-links">
              <div className="Modal-icon" id="github">
                <a
                  href="https://github.com/cpc1992"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    className="Modal-svg"
                  >
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-4.466 19.59c-.405.078-.534-.171-.534-.384v-2.195c0-.747-.262-1.233-.55-1.481 1.782-.198 3.654-.875 3.654-3.947 0-.874-.312-1.588-.823-2.147.082-.202.356-1.016-.079-2.117 0 0-.671-.215-2.198.82-.64-.18-1.324-.267-2.004-.271-.68.003-1.364.091-2.003.269-1.528-1.035-2.2-.82-2.2-.82-.434 1.102-.16 1.915-.077 2.118-.512.56-.824 1.273-.824 2.147 0 3.064 1.867 3.751 3.645 3.954-.229.2-.436.552-.508 1.07-.457.204-1.614.557-2.328-.666 0 0-.423-.768-1.227-.825 0 0-.78-.01-.055.487 0 0 .525.246.889 1.17 0 0 .463 1.428 2.688.944v1.489c0 .211-.129.459-.528.385-3.18-1.057-5.472-4.056-5.472-7.59 0-4.419 3.582-8 8-8s8 3.581 8 8c0 3.533-2.289 6.531-5.466 7.59z" />
                  </svg>
                </a>
              </div>
              <div className="Modal-icon" id="linkedin">
                <a
                  href="https://www.linkedin.com/in/clifford-chan/"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    className="Modal-svg"
                  >
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
                  </svg>
                </a>
              </div>

              <div className="Modal-icon" id="website">
                <a
                  href="https://www.google.com"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <svg
                    version="1.1"
                    id="logo"
                    xmlns="http://www.w3.org/2000/svg"
                    x="0px"
                    y="0px"
                    viewBox="0 0 372 372"
                    className="Modal-svg"
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
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
