import pandas as pd
from sportsreference.nba.roster import Player
from sportsreference.nba.roster import Roster
from sportsreference.nba.teams import Teams
from sportsreference.nba.schedule import Schedule


from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows





boston_schedule = Schedule('BOS')
for game in boston_schedule:
    print(game.date)  # Prints the date the game was played
    print(game.result)  # Prints whether the team won or lost
    # Creates an instance of the Boxscore class for the game.
    boxscore = game.boxscore

# boston = Roster('BOS')
# # gets all stats season by season for all current players on the BOS CELTICS
# # and writes it to an excel sheet
# for player in boston.players:
#         df = player.dataframe
#         df.to_excel(writer, index = False, sheet_name="{}".format(player.name))



writer.save()
