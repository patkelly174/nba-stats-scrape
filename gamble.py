from bs4 import BeautifulSoup
import pandas as pd
import requests
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import sqlite3
from sqlite3 import Error


wb = Workbook()


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
    # no headers need to be changed if its the overal season stats per player
    if "per_game" != table_name:
        headers[4] = "H/A"
        headers[6] = "DROP2"

    player_stats = [tr for tr in table_content.findAll('tr')]
    player_stats = player_stats[1:]
    player_stats = [[td.getText() for td in player_stats[i].findAll('td')]  for i in range(len(player_stats))]
    # gets the title of the webpage to be used to name database tables and excel sheets
    name = soup.find("h1", {"itemprop":"name"}).getText()
    name = name.split()

    if "Boston" in name:
        web_title  = '_'.join(name[1:3])
    else:
        web_title  = '_'.join(name[:2])

    # i will get the player name in order to set the index to the palyer name for better identification
    i = [web_title for i in range(len(player_stats))]

    stats = pd.DataFrame(player_stats, index = i, columns = headers)
    stats = stats.dropna()
    # drops some useless columns from dataframe
    if "per_game" != table_name:
        stats = stats.drop(["Age", "GS", "DROP2"], axis=1)

    # creates a new sheet to add dataframe too string is the title of the webpage
    ws = wb.create_sheet(web_title)

    # adds the created dataframe into a database
    df_to_db(web_title, stats)

    # writes dataframe to the previously created excel workbook
    for r in dataframe_to_rows(stats, index=True, header=True):
        ws.append(r)
    wb.save(filename = "nba_stats.xlsx")

    # all_links is all the links found in the tables that were webscraped **varibale not currently used**
    return all_links


def df_to_db (web_title, stats):
    conn = sqlite3.connect("pythonsqlite.db")
    # creates a new table in previously made database name of the database is web_title
    try:
        stats.to_sql(web_title, con = conn, if_exists='replace')
    except Error as e:
        print(e)


def get_player_data(player_links):
    # iterates through player_links
    for player in player_links:
        url = "https://www.basketball-reference.com{}".format(player)
        if "gamelog" in url:
            # passes the url of the gamelog for a given player
            get_player_gamelog(url)
        else:
            print("-")
            # placeholder


def get_player_gamelog(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    # gets the name of the player to name the new excel sheet **not currently used**
    name = soup.find("h1", {"itemprop":"name"}).getText()
    # pgl_basic is the table id for the stats "soup" is the html content for the url it is passed
    player_links = get_table_data(soup, "pgl_basic")
    # **player_links variable not currently used**


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
