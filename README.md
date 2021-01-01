# nba-stats-scrape

# Description 
Program that will scrape data from basketball-reference.com. The user will input a team name the program will then go to that teams page on basketball-reference.com and get every players average stats per game for the current season. The program will also get each player on the team's stats for each game they played in during the most recent season. This data is then written into an excel spread sheet and also an SQLite database.

# Why
I wrote this program because I wanted to brush up on my python skills and also wanted to create a database in which I could practice SQL queries and using a database. Program is not complete I will be taking a Machine Learning course Fall of 2021 and plan to use what I learn in that class to find different trends among the data.

# About
In this program I use BeautifulSoup4 for to get and parase through the html of a certain webpage. I used the requets library to connect to the webpage and use openpyxl to save data to an excel workbook. Finally I used pandas to convert the parsed html data retrevied form tables on the webpages into dataframes which were then converted to SQL and the added to a database of different tables using SQLite3.
