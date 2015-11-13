"""hoopla - nba stats 



"""
# Libraries
import pandas as pd
import cPickle as pickle
import datetime
import os
import requests
import statsmodels.formula.api as smf
from sklearn import preprocessing




#
##
### Constants
##
#

Periods = ["1","2","3","4"]
MeasureTypes = ["Base","Advanced","Misc","Four Factors","Scoring","Opponent"] # "Usage" doesn't apply as these are team stats
Seasons = ["2013-14","2014-15","2015-16"]

init_args = {
    'DateFrom':"1-1-1900",
    'DateTo':"1-1-1900",
    'MeasureType':'Base',
    'Period':'1',
    'TeamID':'1610612746',
    'OpponentTeamID':'1610612744'
    
}

_today_ = pd.Timestamp(datetime.date.today())


# API Call List
apivariables = ["DateFrom","DateTo","Division","GameScope","GameSegment","LastNGames","LeagueID","Location","MeasureType","Month","OpponentTeamID","Outcome","PORound","PaceAdjust","PerMode","Period","PlayerExperience","PlayerPosition","PlusMinus","Rank","Season","SeasonSegment","SeasonType","ShotClockRange","StarterBench","TeamID","VsConference","VsDivision"]
# API Initialize List
dictinit={"LastNGames":"0","LeagueID":"00","MeasureType":"Base","Month":"0","TeamID":"0","OpponentTeamID":"0","PaceAdjust":"N","PaceAdjust":"N","Period":"0","PerMode":"Totals","PlusMinus":"N","PORound":"0","Rank":"N","Season":"2014-15","SeasonType":"Regular Season"}


PtMeasureTypes = ["SpeedDistance",
"CatchShoot",
"Defense",
"Drives",
"Passing",
"Possessions",
"PullUpShot",
"Rebounding",
"Efficiency",
"ElbowTouch",
"PostTouch",
"PaintTouch"
]



#
##
### Data Acquisition Functions
##
#


#
## Team Stats Iteration Script(s)
#

def grab_quarter_stats(base_payload,base_args,gamedates):
	"""Make dataframe with stats per quarter
	"""
	newargs = base_args
	payload = base_payload

	# Initialize list
	quarters_list = []

	for D in gamedates:
	        newargs.update({'DateFrom':D,'DateTo':D})
	        for P in Periods:
	            newargs.update({"Period":P})
	            # initialize a periodframe
	            periodframe = pd.DataFrame()
	            for m in MeasureTypes:
	                print m

	                newargs.update({"MeasureType":m}) # Set MeasureType
	                newline = grabdataline(payload,newargs)
	                # Check for new arguments
	                old_cols = periodframe.columns.tolist()
	                print old_cols
	                all_new_cols = newline.columns.tolist()
	                newcols = list(set(all_new_cols)-set(old_cols))     
	                print newcols
	                if old_cols == []: # If first measure type, initialize
	                    print "initializing periodframe"
	                    periodframe = newline
	                else:

	                    # Add columns to frame
	                    periodframe = periodframe.join(newline[newcols])
	            
	            quarters_list.append(periodframe)
	            
	full_frame = pd.concat(quarters_list)
	return(full_frame)





def init_payload():
    """Initialize payload
    
    >>> payload = init_payload()
    """
    # Initialize payload
    _payload = {}

    # Load blank payload
    _payload = _payload.fromkeys(apivariables,"")

    # Load initialized values from payloadinit
    for k,v in dictinit.iteritems():
        _payload[k] = v
    return(_payload)

def get_reg_season_gamedates_2013_2014_2015(teamname,opponentname,beforedate=_today_):
    """Get gamedates before today (or given date) 2013-2016 in a list for two teams
    
    >>> gdates = get_reg_season_gamedates_2013_2014_2015(teamname,opponentname)
    
    """
    # Load df
    df = pd.read_pickle("data/schedule/reg_season_schedule_2013_2014_2015.p")


    # Get all relevant teamname homegames
    df = df[df['Visitor'].str.contains(teamname) | df['Home'].str.contains(teamname)]
    
    
    # Get all relevant opponentname homegames
    df = df[df['Visitor'].str.contains(opponentname) | df['Home'].str.contains(opponentname)]
    
 
    # Output List as Strings
    gamedates = df.index.tolist()
    
    # Only keep dates before today

    keepdates = []
    for d in gamedates:
        if d < beforedate:
            keepdates.append(d)
    print "Past games to analyze: %s" % len(keepdates)
    print "Future games this season: %s" % str(len(gamedates) - len(keepdates))
    
    gamedates = keepdates    


    # Convert to API String format
    new_gamedates = []
    for d in gamedates:
       new_date = str(d.month) + "-" + str(d.day) + "-" + str(d.year)
       new_gamedates.append(new_date)

    gamedates = new_gamedates
    
    return(new_gamedates)


def get2014gamedates(team1,team2):
    """Get gamedates in a list for two teams
    """
    print "#"
    print "##"
    print "###get2014gamedates is deprecated.  Please use get_reg_season_gamedates_2013_2014_2015"
    print "##"
    print "#"


    # Load df
    df = pd.read_csv("data/schedule_20142015_regularseason.csv")

    # Set Date
    df['Date'] = pd.DatetimeIndex(df['Date'])

    # Get all clippers games
    df = df[df['Visitor/Neutral'].str.contains(team1) | df['Home/Neutral'].str.contains(team1)]

    # Get all warriors games
    df = df[df['Visitor/Neutral'].str.contains(team2) | df['Home/Neutral'].str.contains(team2)]
    
    # Convert to string
    
    
    # Output List
    gamedates = df['Date'].tolist()
    
    
    # Convert to string
    new_gamedates = []
    for d in gamedates:
        new_date = str(d.month) + "-" + str(d.day) + "-" + str(d.year)
        new_gamedates.append(new_date)

    gamedates = new_gamedates
    
    return(gamedates)


# Grab data
def grabdataline(payload,newargs):
    """
    Grab one line of stats for a quarter
    """
    payload.update(newargs)
    #temp
    print payload
    baseurl = "http://stats.nba.com/stats/leaguedashteamstats"
    response=requests.get(baseurl,params=payload)
    print response.url
    print response
    # Grab headers
    headers = response.json()['resultSets'][0]['headers']

    # Grab stats

    stats = response.json()['resultSets'][0]['rowSet']

    periodframe = pd.DataFrame(stats,columns = headers )
    # Add arguments to data line
    for k,v in newargs.iteritems():
        periodframe[k] = v
    return(periodframe)

def response_to_frame(url):
    """Take a request response and convert to dataframe
    Only if headers and stats conform to sample nba protocol
    
    >>> df = response_to_frame(url)
    
    """
    # Get response
    response=requests.get(url)
    # Grab column heads
    headers = response.json()['resultSets'][0]['headers']

    # Grab rows
    stats = response.json()['resultSets'][0]['rowSet']
    
    # Form frame
    df = pd.DataFrame(stats,columns = headers )
    
    # Return frame
    return(df)



def separate_dates(__gdates):
    """
    Take in date list, return list of date lists per season
    
    >>> date_list = separate_dates(gdates)
    
    """

    _gdates = __gdates

    # HACK DATE ACQUISITION BY SEASON
    dates2013 = []
    for q in _gdates:
        if pd.to_datetime(q) < pd.to_datetime('5-1-2014'):
            dates2013.append(q)
    for d in dates2013:
        if d in _gdates:
            _gdates.remove(d)


    # HACK DATE ACQUISITION BY SEASON
    dates2014 = []
    for q in _gdates:
        if pd.to_datetime(q) < pd.to_datetime('5-1-2015'):
            dates2014.append(q)
    for d in dates2014:
        if d in _gdates:
            _gdates.remove(d)


    # HACK DATE ACQUISITION BY SEASON
    dates2015 = []
    for q in _gdates:
        if pd.to_datetime(q) < pd.to_datetime('5-1-2016'):
            dates2015.append(q)
    for d in dates2015:
        if d in _gdates:
            _gdates.remove(d)
    
    date_dict = {}
    date_dict['2013-14'] = dates2013
    date_dict['2014-15'] = dates2014
    date_dict['2015-16'] = dates2015

    return(date_dict)




def get_model_var(_vars_of_interest,_target,_df,result):
    """Run linear model on targets, get back frame of results
    
    >>> pvals = get_model_var(vars_of_interest,target,df,"pvalue")
    """
    output = []
    for v in _vars_of_interest:
        formstring = _target + " ~ " + v
        #print formstring
        try:
            lm = smf.ols(formula=formstring,data=_df).fit()
            if result == "pvalue":
                output.append((v,lm.pvalues[1]))
            if result == "rsquared":
                output.append((v,lm.rsquared))
            if result == "coef":
                output.append((v,lm.params[1]))
        except:
            output.append((v,9999))
    output = pd.DataFrame(output,columns=['variable',result])
    output.set_index('variable',inplace=True)
    return(output)
        
    
def make_model_frame(_df,_vars_of_interest,_target):
    """Take dataframe, vars and target and return table of pvalue, rsqared and coefs
    """
    # Make model frame
    pvals = get_model_var(_vars_of_interest,_target,_df,"pvalue")
    rsqrs = get_model_var(_vars_of_interest,_target,_df,"rsquared")
    coefs = get_model_var(_vars_of_interest,_target,_df,"coef")

    outputs = pvals.join(rsqrs)
    outputs = outputs.join(coefs)

    # limit to significant
    topouts = outputs[outputs.pvalue < .05].sort("rsquared").tail(30)

    # ignore significance
    # topouts = outputs.sort("rsquared").tail(20)



    topouts.rsquared.plot(kind='barh',title='Top Significant Effects')
    
    return(outputs)



def make_formstring(key_vars,target):
    """Make formstring for statmodels
    
    >>> formstring = make_formstring(key_vars,target)
    """
    # Create formula 
    ind_vars = ""
    for v in key_vars:
        ind_vars = ind_vars + v + " + "
    ind_vars = ind_vars[:-3]
    formstring = target + " ~ " + ind_vars
    print formstring
    return(formstring)



#
##
### General Functions
##
#

def make_zscore_frame(_df):
    """Make zscore frame from dataframe
    Currently will return errors if columns aren't scalable.
    
    >>> df_std = make_zscore_frame(df)
    
    Requires:
    
        sklearn.preprocessing
    """    
    std_scale = preprocessing.StandardScaler().fit(_df)
    _df_std = std_scale.transform(_df)
    _df_std = pd.DataFrame(_df_std,columns = _df.columns,index=_df.index)
    return(_df_std)


def timestamp():
    return(datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))


def get_team_id(team):
	"""Enter a capitalized team name or city.  Spits out TeamID
	"""
	tf = pd.read_csv("data/team_ids.csv",index_col=2)
	tf=tf['TEAM_ID']
	teamid = tf[tf.index.str.contains(team)][0]
	return(teamid)



def main():
      return()

if __name__ == '__main__':
    main()