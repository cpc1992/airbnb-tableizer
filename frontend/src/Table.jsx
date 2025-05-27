import "./Table.css";

function Table({ results }) {
  return (
    <div className="Table-shadow">
      <table className="Table-main">
        <thead>
          <tr>
            <th className="Table-left">Name</th>
            <th className="Table-left">Type</th>
            <th className="Table-left">City</th>
            <th>Total Price</th>
            <th>Price / Night</th>
            <th>Ratings</th>
            <th>Reviews</th>
            <th>Checkin</th>
            <th>Checkout</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result, idx) => {
            return (
              <tr className="Table-row" key={result[0]}>
                <td className="Table-Name">{result[0]}</td>
                <td className="Table-Type">{result[1]}</td>
                <td className="Table-City">{result[2]}</td>
                <td className="Table-Price Table-centered">{result[4]}</td>
                <td className="Table-Price-Per-Night Table-centered">
                  {result[5]}
                </td>
                <td className="Table-Ratings Table-centered">
                  {result[6].toFixed(2)}
                </td>
                <td className="Table-Reviews Table-centered">{result[7]}</td>
                <td className="Table-Checkin Table-centered">{result[8]}</td>
                <td className="Table-Checkout Table-centered">{result[9]}</td>
                <td className="Table-Link Table-centered">
                  <a target="_blank" rel="noopener noreferrer" href={result[3]}>
                    Link
                  </a>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default Table;
