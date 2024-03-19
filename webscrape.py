import requests
from bs4 import BeautifulSoup
import numpy as np


"First, you need to install the Selenium library using pip:

bash

pip install selenium

Next, you'll need to download a web driver for the browser you want to use. For example, if you want to use Chrome, download the ChromeDriver from the official website: https://sites.google.com/a/chromium.org/chromedriver/downloads

Place the downloaded executable file (e.g., chromedriver.exe) in the same directory as your Python script.

Now, you can modify your code to use Seleniu
"


def scrape_stats_from_page(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the stats table containing the player data
        stats_table = soup.find("table", class_="d3-o-table d3-o-table--detailed d3-o-player-stats--detailed d3-o-table--sortable")

        if stats_table:
            # Extract all rows from the table (excluding the header row)
            rows = stats_table.find_all("tr")[1:]

            # Define an empty list to store player stats collectively
            player_stats = []
        
            #Ordered array containing player names
            Players = []

            #Ordered array containing receptions
            Receptions = []
         
            #Ordered array containing yards
            Yards = []

            #Ordered array containing touchdowns
            Touchdowns = []

            #Ordered array containing number of 20+ catches
            yard_20_Catches = []

            #Ordered array containing number of 40+ catches
            yard_40_catches = []

            #Ordered array containing number of long gains
            Long_Gains = []

            # Extract numerical stats from each row and append to player_stats list
            for row in rows:
                # Get all data cells in the row
                data_cells = row.find_all("td")


                #Ordered array containing player names
                Players.append(data_cells[0].text.strip())

                #Ordered array containing receptions
                Receptions.append(data_cells[1].text.strip())

                #Ordered array containing yards
                Yards.append(data_cells[2].text.strip())

                #Ordered array containing touchdowns
                Touchdowns.append(data_cells[3].text.strip())

                #Ordered array containing number of 20+ catches
                yard_20_Catches.append(data_cells[4].text.strip())

                #Ordered array containing number of 40+ catches
                yard_40_catches.append(data_cells[5].text.strip())

                #Ordered array containing number of long gains
                Long_Gains.append(data_cells[6].text.strip())

             


                # Extract the numerical stats and store them in a dictionary
                stats = {
                    "Player": data_cells[0].text.strip(),
                    "Receptions": data_cells[1].text.strip(),
                    "Yards": data_cells[2].text.strip(),
                    "Touchdowns": data_cells[3].text.strip(),
                    "20+ Catches": data_cells[4].text.strip(), 
                    "40+ Catches": data_cells[5].text.strip(), 
                    "Long Gains": data_cells[6].text.strip()
                    # Add other stats here if needed
                }

                # Append the stats dictionary to the player_stats list
                player_stats.append(stats)

            # Print the player stats
            for stats in player_stats:
                print(stats)
        else:
            print("Stats table not found on the page.")
    else:
        print("Failed to retrieve data from the website.")

#nfl website i start the scraping from
base_url = "https://www.nfl.com/stats/player-stats/category/receiving/2022/reg/all/receivingreceptions/desc"
num_pages_to_scrape = 3

all_player_stats = []

for _ in range(num_pages_to_scrape):

    #add stats from current page to all stats
    stats_from_cur_pg = scrape_stats_from_page(base_url)

    if stats_from_cur_pg:
        #add stats from current page
        all_player_stats.extend(stats_from_cur_pg)

        #Extract the "aftercursor object from our current url)
        parsed_url = urlparse(base_url)
        print(parsed_url)
        query_params = parse_qs(parsed_url.query)
        print(query_params)
        aftercursor = query_params.get("aftercursor", [None])[0]
        print(aftercursor)
        if aftercursor: 
            #Update the base url for the next page 
            base_url = "{base_url}?aftercursor={aftercursor}"
        else:
            print("end of pages")
            break


    else:
        print("Failed to be a failure")
        break

for stats in all_player_stats:
    print(stats)
