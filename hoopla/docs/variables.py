variables.py

#
##
### Segmentation of variables available for "Difference Makers"
##
#



# Variables of Interest

# What are the potential impacts on quarterly performance?

"""
* assists
* blocks
* offensive rebounds
* defensive rebounds
* 3 point shots
* Free throws
* Steals
* Turnovers
* Second chance points
* Points in the paint
"""


"""

IDENTIFIER  DateFrom,
IDENTIFIER  DateTo,
IDENTIFIER  OpponentTeamID,
IDENTIFIER  Period,
IDENTIFIER  TEAM_ID,
IDENTIFIER  TEAM_NAME,
IDENTIFIER  TeamID,


NOVALUE  CFID,
NOVALUE  CFPARAMS,
NOVALUE  GP,
NOVALUE  L,
NOVALUE  MeasureType,
NOVALUE  MIN,
NOVALUE  PACE,
NOVALUE  W,
NOVALUE  W_PCT

SCORING_RELATED  NET_RATING,
SCORING_RELATED  OPP_EFG_PCT,

TARGET_RELATED  PIE,
TARGET_RELATED  PLUS_MINUS,
TARGET_RELATED  PTS,

"""

#
## Exogenous variables
#

exo_variables = ["OFF_RATING",
"OPP_AST",
"OPP_BLK",
"OPP_BLKA",
"OPP_DREB",
"OPP_FG3_PCT",
"OPP_FG3A",
"OPP_FG3M",
"OPP_FG_PCT",
"OPP_FGA",
"OPP_FGM",
"OPP_FT_PCT",
"OPP_FTA",
"OPP_FTA_RATE",
"OPP_FTM",
"OPP_OREB",
"OPP_OREB_PCT",
"OPP_PF",
"OPP_PFD",
"OPP_PTS",
"OPP_PTS_2ND_CHANCE",
"OPP_PTS_FB",
"OPP_PTS_OFF_TOV",
"OPP_PTS_PAINT",
"OPP_REB",
"OPP_STL",
"OPP_TOV",
"OPP_TOV_PCT",
"OREB",
"OREB_PCT",
"PCT_AST_2PM",
"PCT_AST_3PM",
"PCT_AST_FGM",
"PCT_FGA_2PT",
"PCT_FGA_3PT",
"PCT_PTS_2PT",
"PCT_PTS_2PT_MR",
"PCT_PTS_3PT",
"PCT_PTS_FB",
"PCT_PTS_FT",
"PCT_PTS_OFF_TOV",
"PCT_PTS_PAINT",
"PCT_UAST_2PM",
"PCT_UAST_3PM",
"PCT_UAST_FGM",
"PF",
"PFD",
"PTS_2ND_CHANCE",
"PTS_FB",
"PTS_OFF_TOV",
"PTS_PAINT",
"REB",
"REB_PCT",
"STL",
"TM_TOV_PCT",
"TOV",
"TS_PCT",
"AST",
"AST_PCT",
"AST_RATIO",
"AST_TO",
"BLK",
"BLKA",
"DEF_RATING",
"DREB",
"DREB_PCT",
"EFG_PCT",
"FG3_PCT",
"FG3A",
"FG3M",
"FG_PCT",
"FGA",
"FGM",
"FT_PCT",
"FTA",
"FTA_RATE",
"FTM"]