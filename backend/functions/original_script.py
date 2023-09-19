from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import quote
from datetime import date
from datetime import datetime
from gspread_formatting import *
import gspread
import requests
import json
import os
from dotenv import load_dotenv

if "prod" not in os.environ:
    load_dotenv('./.env')

# this is the driver function for the scrapper.
# 1) Calls a GET request against the Airbnb link
# 2) Searches the returned data for the data-state/deferred-data-state object
# 3) Parses the results found
# 4) Creates a temporary Google sheet with the data
# Returns a tuple (True, google_sheet_link, array of data) or (False, string reason for failure)


def main(url):
    print('==== Airby Scraper called with url: ' + url)

    # use url parser to get the request queries
    url_breakdown = urlparse(url)
    queries = parse_qs(url_breakdown.query)

    # extract checkin and check out dates from the queries - if not specified, set to none
    checkin_date = None
    checkout_date = None
    if 'checkin' in queries and 'checkout' in queries:
        checkin_date = date_converter(queries['checkin'][0])
        checkout_date = date_converter(queries['checkout'][0])
        print('check in and check out dates are ' +
              queries['checkin'][0] + '-' + queries['checkout'][0])

    # extract the number of guests from the queries - if not specified default to 1
    adults = 1
    if 'adults' in queries:
        adults = int(queries['adults'][0])
        print('number of guests is: ' + str(adults))

    print('1) Calling API')
    # set up proxy
    apikey = os.environ.get('scrapingAnt_api_key')
    url_encoded = quote(url)
    proxy = f'https://api.scrapingant.com/v2/general?url={url_encoded}&x-api-key={apikey}&return_page_source=true&proxy_country=US'

    # call the request
    try:
        if "prod" not in os.environ:
            # set up the http request headers
            custom_headers = {'User-Agent': 'PostmanRuntime/7.28.4'}
            res = requests.get(url, headers=custom_headers, timeout=5)
        else:
            res = requests.get(proxy, timeout=10)
    except requests.exceptions.ConnectTimeout:
        return (False, 'Link timed out. Double check that it works and retry.')

    # print response code
    print(f'response code: {res.status_code}')
    if res.status_code == 200:

        # soup da results
        souped_request_data = BeautifulSoup(res.text, 'html.parser')
        print('2) Looking for search results')
        # try to find search results in data-state object, if its not in there, search the data-deferred-state object.
        ok, search_results = check_data_state(souped_request_data)
        if not ok:
            ok, search_results = check_deferred_state(souped_request_data)
            if not ok:
                print('No results - Exiting')
                return (False, 'No results found at that link.')

        # if we're here, we found results some

        # parse results if we found some
        print('3) Parsing results')
        result_list = parse_results(
            search_results, checkin_date, checkout_date, adults)

        # if there are no results, do not continue
        if len(result_list) <= 1:
            return (False, 'Results found at the link could not be parsed.')

        print('4) Creating Google sheet:')
        sheet_url = create_sheet(result_list)
        # if we cant login to our google service account, create_sheet will return False
        if sheet_url == False:
            return (False, 'Sorry! Internal service error.')
        print(sheet_url)
        return (True, sheet_url, result_list)
    else:
        print(res.reason)
        print(res.text)
        return (False, 'Invalid Link.')

# use gspread and gspread-formatting libraries to login to the google service account and produce a google sheet with the results


def create_sheet(result_list):
    if len(result_list) == 0:
        return
    # remove the duplicate link at the end of the row.
    result_list = [item[0:len(item)-1] if idx >
                   0 else item for idx, item in enumerate(result_list)]

    # google service account credentials from .env
    credentials = {
        "type": os.environ.get('type'),
        "project_id": os.environ.get('project_id'),
        "private_key_id": os.environ.get('private_key_id'),
        "private_key": os.environ.get('private_key'),
        "client_email": os.environ.get('client_email'),
        "client_id": os.environ.get('client_id'),
        "auth_uri": os.environ.get('auth_uri'),
        "token_uri": os.environ.get('token_uri'),
        "auth_provider_x509_cert_url": os.environ.get('auth_provider_x509_cert_url'),
        "client_x509_cert_url": os.environ.get('client_x509_cert_url')
    }

    # create a new spreadsheet
    try:
        servacc = gspread.service_account_from_dict(credentials)
    except Exception as e:
        print('Error: login to google service account failed: ')
        print(e)
        return False
    spreadsheet = servacc.create(f'New Spreadsheet {datetime.now()}')
    spreadsheet.share(email_address=None, perm_type='anyone', role='reader')

    worksheet = spreadsheet.get_worksheet(0)
    worksheet.update_title('Airbies')

    # formatting
    bold = CellFormat(
        textFormat=TextFormat(bold=True),
    )
    rightalign = CellFormat(
        horizontalAlignment='RIGHT'
    )

    centeralign = CellFormat(
        horizontalAlignment='CENTER'
    )
    dollars = CellFormat(
        numberFormat={'type': 'CURRENCY', 'pattern': '$#,###'}
    )

    with batch_updater(worksheet.spreadsheet) as batch:
        batch.format_cell_range(worksheet, '1', bold)
        batch.format_cell_range(worksheet, 'D', centeralign)
        batch.format_cell_range(worksheet, 'E2:E', dollars)
        batch.format_cell_range(worksheet, 'E', centeralign)
        batch.format_cell_range(worksheet, 'F', centeralign)
        batch.format_cell_range(worksheet, 'G', centeralign)
        batch.format_cell_range(worksheet, 'H', centeralign)
        batch.format_cell_range(worksheet, 'I', centeralign)
        batch.format_cell_range(worksheet, 'J', centeralign)
        batch.format_cell_range(worksheet, 'K', centeralign)
        batch.format_cell_range(worksheet, 'L', centeralign)
        batch.format_cell_range(worksheet, 'M', centeralign)
        batch.set_column_width(worksheet, 'A', 400)
        batch.set_column_width(worksheet, 'B', 180)
        batch.set_column_width(worksheet, 'C', 150)
        batch.set_column_width(worksheet, 'D', 50)
        batch.set_column_width(worksheet, 'E', 75)
        batch.set_column_width(worksheet, 'F', 100)
        batch.set_column_width(worksheet, 'G', 50)
        batch.set_column_width(worksheet, 'H', 75)
        batch.set_column_width(worksheet, 'I', 125)
        batch.set_column_width(worksheet, 'J', 75)
        batch.set_column_width(worksheet, 'K', 75)
        batch.set_column_width(worksheet, 'L', 75)
        batch.set_column_width(worksheet, 'M', 75)
        batch.set_column_width(worksheet, 'N', 75)

        batch.set_frozen(worksheet, rows=1)

    print('done formatting google sheet')
    # append the parsed data to the sheet
    worksheet.append_rows(result_list, value_input_option='USER_ENTERED')
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"


# helper method that checks long json paths - can handle object keys and array indexes
# *keys must be the chain of keys/array index IN THE ORDER that you suspect.
# example: to check this path myobj.keys[2].user.token[1] you would enter the parms like this:
# path_checker(myobj, 'keys', 2, 'user', 'token', 1)
# this will return a tuple with 3 items.
# if [0] is False, [1] will be None, and [2] will be the path keychain
# if [0] is True, the data will be in [1], and [2] will be the path keychain
def path_checker(element, *keys):
    inner_element = element
    keychain_string = 'Obj'

    # If we are passed a dict with keys or a list with some data, continue
    for key in keys:
        try:
            inner_element = inner_element[key]
            if isinstance(key, int):
                key = f'[{key}]'
            keychain_string += f' -> {key}'
        except:
            if isinstance(key, int):
                key = f'[{key}]'
            keychain_string += f' -X> {key}'
            return False, None, keychain_string

    return True, inner_element, keychain_string

# parse the results found in either the data-state or deferred-data-state script elements
# returns a list of innerlists where each innerlist follows this convention:
# ['Name', 'Type', 'City', 'Link', 'Total Price', 'Accurate Price', 'Beds', 'Bedrooms', 'Bathrooms', 'Reviews', 'Rating', 'Check In', 'Check Out']


def parse_results(results, checkin_date, checkout_date, adults):
    result_list = []
    result_list.append(['Name', 'Type', 'City', 'Link', 'Total Price', 'Accurate Price', 'Beds', 'Bedrooms',
                        'Bathrooms', 'Reviews', 'Rating', 'Check In', 'Check Out'])

    # results is a list of objects
    # for idx, result in enumerate(results):
    for idx, result in enumerate(results):
        print(f'Parsing result {idx}')

        result_obj = {}

        # find listing section and pricing section. if either of these are missing, forget this result
        ok, listing_section, listing_keychain = path_checker(result, 'listing')
        ok, pricing_section, pricing_keychain = path_checker(
            result, 'pricingQuote', 'structuredStayDisplayPrice')
        if listing_section == None or pricing_section == None:
            print(
                f'Error: Result #{idx} skipped. Reason: no {"listing section" if pricing_section else "pricing section"}')
            continue

        # if we get here, we should have a valid listing and pricing section. time to parse.

        ''' 
        ID 
        ex: 13769972
        integer
        '''
        ok, room_id, keychain = path_checker(listing_section, 'id')
        if ok:
            result_obj['id'] = room_id
        else:
            print(f'Error: Result #{idx} skipped. Reason: no id')
            continue
        print(f'================={idx}: {room_id}')

        ''' 
        BEDROOM INFO
        ex: ['1 beds', '2 bedrooms'] ["1 bed", "Studio"] ['1 bedroom']
        list of strings 

        - Some times there is only 1 item in the list, in this case set beds = 1 and bedrooms = 1
        - if there are two items in the list, parse # of beds and try to parse # of bedrooms
        - if you can't parse out a number, store the string into the result
        '''
        ok, bed_info, keychain = path_checker(
            listing_section, 'contextualPictures', 1, 'caption', 'messages')
        if ok:
            if len(bed_info) < 2:
                result_obj['beds'] = 1
                result_obj['bedrooms'] = 1
            else:
                bed_string = bed_info[0]
                bedroom_string = bed_info[1]

                # attempt to parse the number of beds
                try:
                    bed_final = int(bed_string.split(" ")[0])
                except:
                    bed_final = bed_string
                    # print('weird beds')
                    # print(bed_info)

                # attempt to parse number of bedrooms
                try:
                    bedroom_final = int(bedroom_string.split(" ")[0])
                except:
                    bedroom_final = bedroom_string
                    # print('weird bedrooms')
                    # print(bed_info)

                result_obj['beds'] = bed_final
                result_obj['bedrooms'] = bedroom_final
        else:
            print(
                f'Warning: Result #{idx} has weird bedroom info: {bed_info}. I cannot parse it.')
            result_obj['beds'] = None
            result_obj['bedrooms'] = None

        ''' 
        BATHROOM INFO
        ex: ['2 baths'], ["1 shared bath"] ["Shared half-bath"] ["1 private bath"] ["1.5 shared baths"]
        list of strings

        - Bathroom info is vastely general, just store the string.
        '''
        ok, bath_info, keychain = path_checker(
            listing_section, 'contextualPictures', 2, 'caption', 'messages')
        if ok:
            bathrooms_string = bath_info[0]
            result_obj['bathrooms'] = bathrooms_string

        else:
            print(
                f'Warning: Result #{idx} has no bathroom info')
            result_obj['bathrooms'] = None

        ''' 
        CITY 
        ex: 'South Lake Tahoe'
        string
        '''
        ok, city, keychain = path_checker(listing_section, 'city')
        if ok:
            # city = remove_utfs(city) # take this out if you don't want to remove weird utf characters
            result_obj['city'] = city
        else:
            print(
                f'Warning: Result #{idx} has no city')
            result_obj['city'] = None

        ''' 
        NAME 
        ex: 'Playpark Lodge Family Queen Fast WiFi, Dogs OK!'
        string
        '''
        ok, name, keychain = path_checker(listing_section, 'name')
        if ok:
            # name = remove_utfs(name) # take this out if you don't want to remove weird utf characters
            result_obj['name'] = name
        else:
            print(
                f'Warning: Result #{idx} has no name')
            result_obj['name'] = None

        ''' 
        PRODUCT 
        ex: 'Home in South Lake Tahoe' -> 'Home'
        string
        '''
        ok, title, keychain = path_checker(listing_section, 'title')
        if ok:
            # title = remove_utfs(title) # take this out if you don't want to remove weird utf characters
            product = title.split(" in ")
            result_obj['product'] = product

        else:
            print(
                f'Warning: Result #{idx} has no product')
            result_obj['product'] = None

        ''' 
        TYPE 
        ex: 'entire_home' 'private_room'
        string
        '''
        ok, room_type, keychain = path_checker(
            listing_section, 'roomTypeCategory')
        if ok:
            result_obj['type'] = room_type.replace('_', ' ')
        else:
            print(
                f'Warning: Result #{idx} has no room type')
            result_obj['type'] = None

        ''' 
        LATITUDE 
        ex: 38.90554
        float
        '''
        ok, latitude, keychain = path_checker(
            listing_section, 'coordinate', 'latitude')
        if ok:
            result_obj['latitude'] = latitude
        else:
            print(
                f'Warning: Result #{idx} has no latitude')
            result_obj['latitude'] = None

        ''' 
        LONGITUDE 
        ex: -120.00179
        float
        '''
        ok, longitude, keychain = path_checker(
            listing_section, 'coordinate', 'longitude')
        if ok:
            result_obj['longitude'] = longitude
        else:
            print(
                f'Warning: Result #{idx} has no longitude')
            result_obj['longitude'] = None

        ''' 
        RATINGS and REVIEWS 
        ex: '4.81 (43)'
        string
        '''
        ok, reviews_ratings, keychain = path_checker(
            listing_section, 'avgRatingLocalized')
        if ok and reviews_ratings != None:

            if reviews_ratings == "New":
                result_obj['rating'] = 0
                result_obj['reviews'] = 0
                # print('new listing 0 ratings 0 reviews')
                # print(reviews_ratings)
            else:
                print(reviews_ratings)
                rev_rate_list = reviews_ratings.split(' ')
                if len(rev_rate_list) == 1:
                    if '(' in rev_rate_list[0]:
                        reviews = rev_rate_list[0].replace('(', '')
                        reviews = int(reviews.replace(')', ''))
                        result_obj['rating'] = 0
                        result_obj['reviews'] = reviews
                    else:
                        rating = float(rev_rate_list[0])
                        result_obj['rating'] = rating
                        result_obj['reviews'] = 0
                else:
                    rating = float(rev_rate_list[0])
                    reviews = rev_rate_list[1].replace('(', '')
                    reviews = int(reviews.replace(')', ''))
                    result_obj['rating'] = rating
                    result_obj['reviews'] = reviews
        else:
            result_obj['rating'] = 0
            result_obj['reviews'] = 0
            print(
                f'Warning: Result #{idx} has no ratings or reviews info')
            # print(reviews_ratings)

        ''' 
        PRICE
        ex: '$887 total' '$887'
        string

        The price can be found in 3 locations: total price, discount price, and regular price. (price can be in discount and regular at the same time).
        The location that the price shows up depends on if the original query included checkin and checkout dates. 
        IF CHECKIN AND CHECKOUT DATES WERE SUPPLIED:
            total price will exist in:  pricing_section -> 'secondaryLine' -> 'price'. 
            This will be a total price for the whole stay, factors in service and cleaning fees, and is the most accurate
            In this case we pass down the checkin and checkout dates from the query strings. and calculate the number of nights
        ELSE:
            total price path will not exist.
            There will be a regular price in: pricing_section -> 'primaryLine' -> 'price'
            and MAYBE there will be a discount price in: pricing_section -> 'primaryLine' -> 'discountedPrice' if the host is currently providing a discount.
            this price will be a NIGHTLY price not a total price. 
            In this case, there will be checkin and checkout dates in each result (outside of both the listingsection and pricesection).
            We calculate the total price by multiplting the nights by the discount price or the regular price. 
            This total price is NOT accurate as it does not account for service and cleaning fee which cannot be seen unless you look into the actual listing.

        result_obj['accurate price'] will tell you whether it is the total price or a calculate price (no service/cleaning fee factored in)
        '''

        total_price_ok, total_price, total_price_keychain = path_checker(
            pricing_section, 'secondaryLine', 'price')

        discount_price_ok, discount_price, discount_price_keychain = path_checker(
            pricing_section, 'primaryLine', 'discountedPrice')

        regular_price_ok, regular_price, regular_price_keychain = path_checker(
            pricing_section, 'primaryLine', 'price')

        # if they specified a checkin and checkout price then get the checkin/checkout dates are gotten passed down from the query strings
        # also this means that every result object will have an explicit total price which factors service and cleaning. this price is accurate
        if total_price_ok:
            total_price_string = total_price.split(' ')[0]
            price = total_price_string.replace('$', '')
            price = int(price.replace(',', ''))
            # checkin and checkout dates are gotten and passed from the url query strings.
            date_delta = checkout_date - checkin_date
            nights = date_delta.days

            result_obj['price'] = price
            result_obj['nights'] = nights
            result_obj['accurate price'] = True

        # if they did not specify checkin and checkout dates, then the dates are gotten from the result object
        # if this is true, then the result object will not have an accurate explicit total price, only the night rate under "dicountedPrice" or "price"
        # this means we have to calculate the total price by mutliplying it by the number of nights. this results in a non-accurate price because it
        # does NOT factor in service or cleaning fee.
        elif discount_price_ok or regular_price_ok:
            if discount_price_ok:
                price_string = discount_price
            else:
                price_string = regular_price
            price = int(price_string[1:].replace(',', ''))

            # checkin and checkout dates are gotten from the result
            checkin_ok, checkin_string, keychain = path_checker(
                result, 'listingParamOverrides', 'checkin')
            checkout_ok, checkout_string, keychain = path_checker(
                result, 'listingParamOverrides', 'checkout')
            checkin_date = date_converter(checkin_string)
            checkout_date = date_converter(checkout_string)
            date_delta = checkout_date - checkin_date
            nights = date_delta.days

            result_obj['price'] = price * nights
            result_obj['nights'] = nights
            result_obj['accurate price'] = False

        else:
            print(
                f'Warning: Result #{idx} has no price info')
            result_obj['price'] = None
            result_obj['nights'] = None
            result_obj['accurate price'] = None

        ''' 
        CHECKIN and CHECKOUT
        
        parsed from the query strings of the input url or from the scraped results.
        stored as datetime objects
        '''
        if checkin_date != None and checkout_date != None:
            result_obj['checkin'] = checkin_date
            result_obj['checkout'] = checkout_date
        else:
            print(
                f'Warning: Result #{idx} has no check in or check out dates')
            result_obj['checkin'] = None
            result_obj['checkout'] = None

        ''' 
        URL 
        
        room_id must exist or we won't get here
        adults is parsed from the query string or 1.
        checkin and checkout can be None so we need to check if they exist before concatting them to the URL
        '''
        result_url = f'https://www.airbnb.com/rooms/{room_id}?adults={adults}'
        if checkin_date != None and checkout_date != None:
            result_url = result_url + \
                f'&check_in={checkin_date}&check_out={checkout_date}'
        result_obj['url'] = result_url

        ''' 
        PARSING COMPLETE
        '''
        # ['Name','Type','City','Total Price', 'Accurate Price', 'Beds','Bedrooms','Bathrooms','Reviews', 'Ratings', 'Checkin','Checkout','Longitude', 'Latitude', 'Link']
        result_arr = [
            result_obj['name'],
            f'{result_obj["product"][0]} - {result_obj["type"]}',
            result_obj['city'],
            f'=HYPERLINK("{result_obj["url"]}","link")',
            result_obj['price'],
            'Yes' if result_obj['accurate price'] else 'No',
            result_obj['beds'],
            result_obj['bedrooms'],
            result_obj['bathrooms'],
            result_obj['reviews'],
            result_obj['rating'],
            f'{result_obj["checkin"].month}-{result_obj["checkin"].day}',
            f'{result_obj["checkout"].month}-{result_obj["checkout"].day}',
            result_obj['url']

        ]

        result_list.append(result_arr)

    return result_list

# convert date strings from airbnb to a date object. 2023-08-18 => python date()


def date_converter(date_string):
    checkin_year = int(date_string[0:4])
    checkin_month = int(date_string[5:7])
    checkin_day = int(date_string[8:])

    return date(checkin_year, checkin_month, checkin_day)

# removing all emojis and random utf characters because git bash cant print it - although this wont be a problem after i remove all the prints
# So airbnb allows emojis and utf-8 symbols in their titles. Gitbash on windows can't handle them so this is


def remove_utfs(string):

    # create a character set of all keyboard letters/numbers/symbols. i use this to remove all weird symbols that cant be printed out.
    character_set = {
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '`', '~', '|', '\\', '/', '?', ',', '.', '<', '>', ';', ':',
        '"', '\'', '[', ']', '{', '}', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' '
    }

    for character in string:
        if character not in character_set:
            string = string.replace(character, '')
    return string


# the airbnb request returns with many script elements. one of which has the id='data-state'.
# inside the script element there is a large json object that has the search result we are looking for.
# this function checks if the results are in the data-state element - sometimes its in the data-deferred-state element instead
def check_data_state(souped_data):

    # try finding the data-state script element
    data_state_script_tag = souped_data.find("script", {"id": "data-state"})
    if data_state_script_tag == None:
        return False, "No <script id=data-state> script tag"

    # get only the text of the <script> tag
    data_state_json_text = data_state_script_tag.text

    # write out the data
    # with open("data_state_object.json", 'w', encoding='utf-8') as file:
    #     file.write(data_state_json_text)

    # stick the json object in the element into a python dict
    data_state_object = json.loads(data_state_json_text)

    # go to path of search result - list of object where each object is a search result
    ok, search_results, data_state_keychain = path_checker(data_state_object, 'niobeMinimalClientData', 1, 1,
                                                           'data', 'presentation', 'explore', 'sections', 'sectionIndependentData', 'staysSearch', 'searchResults')

    if ok:
        print(
            f'Nice! {len(search_results)} results found in the data-state object')
        # with open("data_state_object.json", 'w', encoding='utf-8') as file:
        #     file.write(json.dumps(search_results))
        return True, search_results
    else:
        # in this case data is the keychain
        print(
            f'results not found in the data-state object')
        return False, data_state_keychain

# the airbnb request returns with many script elements. one of which has the id='data-deferred-state'.
# inside the script element there is a large json object that has the search result we are looking for.
# this function checks if the results are in the data-deferred-state element - sometimes its in the data-state element instead


def check_deferred_state(souped_data):

    # try finding the data-deferred-state script element
    deferred_state_script_tag = souped_data.find(
        "script", {"id": "data-deferred-state"})
    if deferred_state_script_tag == None:
        return False, "No <script id=data-deferred-state> script tag"

    # get only the text of the <script> tag
    deferred_state_json_text = deferred_state_script_tag.text

    # write out the data
    # with open("deferred_state_object.json", 'w', encoding='utf-8') as file:
    #     file.write(deferred_state_json_text)

    # stick the json object in the element into a python dict
    deferred_state_object = json.loads(deferred_state_json_text)

    # go to path of search result - list of object where each object is a search result

    ok, search_results, deferred_state_keychain = path_checker(deferred_state_object, 'niobeMinimalClientData',
                                                               0, 1, 'data', 'presentation', 'explore', 'sections', 'sectionIndependentData', 'staysSearch', 'searchResults')

    if ok:
        print(
            f'Nice! {len(search_results)} results found in the deferred-state object')
        # with open("deferred_state_object.json", 'w', encoding='utf-8') as file:
        #     file.write(json.dumps(search_results))
        return True, search_results
    else:
        # in this case data is the keychain
        print(
            f'results not found in the deferred-state object')
        return False, deferred_state_keychain
