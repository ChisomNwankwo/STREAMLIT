import pandas as pd

### MEN
def top_5_points(df):
    winners = df[['WTeamName', 'WScore']].rename(columns = {'WTeamName': 'Team', 'WScore':'points'})
    losers = df[['LTeamName', 'LScore']].rename(columns = {'LTeamName': 'Team', 'LScore':'points'})

    team = pd.concat([winners, losers])
    top_5_df = team.groupby('Team')['points'].mean().reset_index().sort_values(
        by = 'points', ascending = False).head(5)
    top_5_df['points'] = top_5_df['points'].round(0).astype(int)

    return top_5_df
    
def top_5_rebounds(df):
    df['W_rebounds'] = df['WOR'] + df['WDR']
    df['L_rebounds'] = df['LOR'] + df['LDR']

    winners = df[['WTeamName', 'W_rebounds']].rename(columns = {'WTeamName': 'Team', 'W_rebounds':'rebounds'})
    losers = df[['LTeamName', 'L_rebounds']].rename(columns = {'LTeamName': 'Team', 'L_rebounds':'rebounds'})

    team = pd.concat([winners, losers])
    top_5_df = team.groupby('Team')['rebounds'].mean().reset_index().sort_values(
        by = 'rebounds', ascending = False).head(5)
    top_5_df['rebounds'] = top_5_df['rebounds'].round(0).astype(int)
    
    return top_5_df


def top_5_assists(df):

    winners = df[['WTeamName', 'WAst']].rename(columns = {'WTeamName': 'Team', 'WAst':'assists'})
    losers = df[['LTeamName', 'LAst']].rename(columns = {'LTeamName': 'Team', 'LAst':'assists'})

    team = pd.concat([winners, losers])
    top_5_df = team.groupby('Team')['assists'].mean().reset_index().sort_values(
        by = 'assists', ascending = False).head(5)
    top_5_df['assists'] = top_5_df['assists'].round(0).astype(int)
    
    return top_5_df


#--------------------------------------WOMEN--------------------------------

def top_W_points(df):
    winners = df[['WTeamName', 'WScore']].rename(columns = {'WTeamName': 'Team', 'WScore':'points'})
    losers = df[['LTeamName', 'LScore']].rename(columns = {'LTeamName': 'Team', 'LScore':'points'})

    team = pd.concat([winners, losers])
    top_5_df = team.groupby('Team')['points'].mean().reset_index().sort_values(
        by = 'points', ascending = False).head(5)
    top_5_df['points'] = top_5_df['points'].round(0).astype(int)
    top_5_df['points'] = top_5_df['points'].round(0).astype(int)
    
    return top_5_df
    
def top_W_rebounds(df):

    winners = df[['WTeamName', 'W_rebounds']].rename(columns = {'WTeamName': 'Team', 'W_rebounds':'rebounds'})
    losers = df[['LTeamName', 'L_rebounds']].rename(columns = {'LTeamName': 'Team', 'L_rebounds':'rebounds'})

    team = pd.concat([winners, losers])
    top_5_df = team.groupby('Team')['rebounds'].mean().reset_index().sort_values(
        by = 'rebounds', ascending = False).head(5)
    top_5_df['rebounds'] = top_5_df['rebounds'].round(0).astype(int)
    
    return top_5_df


def top_W_assists(df):

    winners = df[['WTeamName', 'WAst']].rename(columns = {'WTeamName': 'Team', 'WAst':'assists'})
    losers = df[['LTeamName', 'LAst']].rename(columns = {'LTeamName': 'Team', 'LAst':'assists'})

    team = pd.concat([winners, losers])
    top_5_df = team.groupby('Team')['assists'].mean().reset_index().sort_values(
        by = 'assists', ascending = False).head(5)
    top_5_df['assists'] = top_5_df['assists'].round(0).astype(int)
    
    return top_5_df


#------------------------GET NAMES------------------------

def names_list_M(df):
    winners = df[['WTeamName', 'WScore']].rename(columns = {'WTeamName': 'team', 'WScore':'points'})
    losers = df[['LTeamName', 'LScore']].rename(columns = {'LTeamName': 'team', 'LScore':'points'})

    team = pd.concat([winners, losers])
    names = sorted(team['team'].unique())

    return names
    

def names_list_F(df):
    winners = df[['WTeamName', 'WScore']].rename(columns = {'WTeamName': 'team', 'WScore':'points'})
    losers = df[['LTeamName', 'LScore']].rename(columns = {'LTeamName': 'team', 'LScore':'points'})

    team = pd.concat([winners, losers])
    names = sorted(team['team'].unique())

    return names
    