from bs4 import BeautifulSoup
import pandas as pd
import requests
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows


# writer = pd.ExcelWriter("seasoninfo.xlsx")
wb = Workbook()
print("hello")

def get_table_data(soup, table_name):
    # finds the table on the webpage with the passed table_name id
    table_content = soup.find("table", {"id":table_name})

    # gets all links that are in the table given
    all_links = []
    for link in table_content.find_all('a', href=True):
        all_links.append(link["href"])

    # tr represents each table row
    headers = [tr for tr in table_content.findAll('tr')]
    # th is the content of each row
    headers = [th.getText() for th in headers[0].findAll('th')]
    # do not need to first column so set header to everything bu that first column
    headers = headers[1:]

    player_stats = [tr for tr in table_content.findAll('tr')]
    player_stats = player_stats[1:]
    player_stats = [[td.getText() for td in player_stats[i].findAll('td')]  for i in range(len(player_stats))]
    stats = pd.DataFrame(player_stats, columns = headers)
    stats = stats.dropna()

    # opens/makes seasoninfo.xlsx and saves the stats dataframe to that excel workbook
    # stats.to_excel(writer, index=False, sheet_name="{}".format(table_name))
    ws = wb.create_sheet(table_name)

    for r in dataframe_to_rows(stats, index=False, header=True):
        ws.append(r)
    wb.save(filename = "nba_stats.xlsx")

    return all_links


def get_player_data(player_links):
    # iterates through player_links
    for player in player_links:
        url = "https://www.basketball-reference.com{}".format(player)
        if "gamelog" in url:
            get_player_gamelog(url)
        else:
            print("-")


def get_player_gamelog(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    # gets the name of the player to name the new excel sheet
    name = soup.find("h1", {"itemprop":"name"}).getText()
    test = get_table_data(soup, "pgl_basic")





def main():
    player_links = get_table_data(soup, "per_game")
    get_player_data(player_links)
    # get_opp_team_data(opp_soup, opp_team)



team = input("Enter the team you would like to see stats for. (Use their 3 letter designation BOS, PHI, etc.)\n")
# opp_team = input("Who is this team playing that you would like to see matchup history for? (Same designation as before)\n")
# url = "https://www.basketball-reference.com/teams/BOS/2020.html"
url = "https://www.basketball-reference.com/teams/{}/2020.html".format(team)
# opp_url = "https://www.basketball-reference.com/teams/{}/2020/gamelog/".format(opp_team)
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
# r2 = requests.get(opp_url)
# opp_soup = BeautifulSoup(r2.content, "html.parser")
main()
