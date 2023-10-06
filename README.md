# Airbnb Tableizer

A simple tool that can scrape the listings from an Airbnb search link and generate a Google Sheet with the results. 

Live Site: https://airbnb-tableizer.vercel.app/

## How to use

1. Perform a search on the Airbnb website. Specify location, check in & check out dates, and number of guests for better results.
2. Copy that link into the Airbnb Tableizer and click Tableize!
3. Your results will be previewed on the screen and a Google Sheet will be generated for you.
4. Duplicate or copy the Google sheet data to keep for your plans.
5. Have a wonderful trip or vacation!

## Usage notes

* Some listings incorrectly write their bed & bedroom data into the bathroom attribute.
* If you get a server error, try again later or try with a different link. This happens occasionally when the destination is somewhere outside of the US. Or if this is the first request of the day and server has to cold start.
* the "Accurate" column indicates whether the price is the true price after all the service/cleaning fees or not.

## Technologies used

The front-end is written using React.   
The back-end is handled by a Flask server.  
The scraping is done with BeautifulSoup.  
The Google Sheet is generated using Gspread and Gspread-formatting.  

## Authors

Clifford Chan (cpc1992)
