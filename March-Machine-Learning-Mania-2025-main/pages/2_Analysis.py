import streamlit as st
import sys
import os
import plotly.express as px
import pandas as pd

st.markdown("""
<style>

/* ===== MAIN APP BACKGROUND ===== */
.stApp {
    background-color: #0b0f1a;
}

/* ===== TEXT ===== */
html, body, [class*="css"] {
    color: #e6e6e6;
    font-family: 'Segoe UI', sans-serif;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: #e6e6e6;
}

/* ===== HEADERS ===== */
h1, h2, h3 {
    color: #ffffff;
    font-weight: 700;
}

/* ===== CARD STYLE ===== */
.card {
    background-color: #1c2433;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}

/* ===== ACCENT (ESPN RED) ===== */
.accent {
    color: #ff4b4b;
    font-weight: bold;
}

/* ===== BUTTONS ===== */
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 8px;
    border: none;
}

.stButton>button:hover {
    background-color: #e03a3a;
    color: white;
}

</style>
""", unsafe_allow_html=True)
#--------------------------------------------------------------------------------------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

#import scripts
from src import data_loader, processing

#TITLE
st.title("Tournament Game Insights")

#--------------------------------------LOAD DATA-----------------------
#MEN DATA
@st.cache_data
def get_data():
    return data_loader.load_men_data() 
    
men_df = get_data()


#WOMEN DATA
@st.cache_data
def get_data_f():
    return data_loader.load_women_data() 
    
women_df = get_data_f()

#---------------------------------SIDEBAR INFO------------------------------------------------
#Step 1: Select dataset first
league = st.sidebar.selectbox("League", ["Men", "Women"])

if league == "Men":
    df_source = men_df
else:
    df_source = women_df

#Step 2: Apply filters ONCE using the selected dataset
team = st.sidebar.multiselect("Team", df_source["LTeamName"].unique())
season = st.sidebar.multiselect("Season", df_source["Season"].unique())
round_options = ["All Rounds"] + list(df_source["Round"].dropna().unique())
round_ = st.sidebar.selectbox("Round", round_options)
outcome_options = ["All", "Win", "Loss"]
outcome = st.sidebar.selectbox("Outcome", outcome_options)


filtered_df = df_source.copy()

filtered_df = df_source.copy()

# Team filter (multiselect)
if team:
    filtered_df = filtered_df[
        (filtered_df["LTeamName"].isin(team)) |
        (filtered_df["WTeamName"].isin(team))
    ]

# Season filter (multiselect)
if season:
    filtered_df = filtered_df[filtered_df["Season"].isin(season)]

# Round filter
if round_ != "All Rounds":
    filtered_df = filtered_df[filtered_df["Round"] == round_]

#outcome filter
if team:  # only apply if user selected teams

    if outcome == "Win":
        filtered_df = filtered_df[filtered_df["WTeamName"].isin(team)]

    elif outcome == "Loss":
        filtered_df = filtered_df[filtered_df["LTeamName"].isin(team)]

    elif outcome == "All":
        filtered_df = filtered_df[
            (filtered_df["WTeamName"].isin(team)) |
            (filtered_df["LTeamName"].isin(team))
        ]

#-----------------------------------------------------------------------------------------------
# Total games
total_games = len(filtered_df)

# Wins
wins = len(filtered_df[filtered_df["WTeamName"].isin(team)])

# Losses
losses = len(filtered_df[filtered_df["LTeamName"].isin(team)])

#Win Percentage (Win Rate)
win_pct = wins / total_games if total_games > 0 else 0

# METRICS
st.subheader("📊 Overview")
st.info("Summary of selected filters")
col1, col2, col3, col4= st.columns(4)
col1.metric("Total Games", total_games)
col2.metric("Wins", wins)
col3.metric("Losses", losses)
col4.metric("Win %", f"{win_pct:.1%}")

st.markdown('----')

#choose df you want to show
st.subheader("📋 Game Data")
display_df = filtered_df.drop(['Date', 'Season','DayZero', 'DayNum', 'WTeamID', 'WLoc', 
                 'NumOT', 'Round'], axis = 1)
st.dataframe(display_df)

st.markdown('---')

#_--------------------------------------------------------------------------------------------------

st.subheader("📈 Trends")

tab1, tab2, tab3 = st.tabs([
    "Scores",
    "Assists",
    "Rebounds"
    ])

#--------------------------------------TRENDS-----------------------------------
@st.cache_data
def prepare_stat_trend(df, stat, team):
    """
    df: filtered dataframe
    stat: string e.g. 'Score', 'Ast', 'Reb'
    team: selected team (string or list)
    """

    win_col = f"W{stat}"
    loss_col = f"L{stat}"

    df = df.copy()

    df[f"Win{stat}"] = df[win_col].where(df["WTeamName"].isin(team))
    df[f"Loss{stat}"] = df[loss_col].where(df["LTeamName"].isin(team))

    grouped = df.groupby("Season")[[f"Win{stat}", f"Loss{stat}"]].mean().reset_index()

    melted = grouped.melt(
        id_vars="Season",
        value_vars=[f"Win{stat}", f"Loss{stat}"],
        var_name="Result",
        value_name=stat
    )
    melted["Result"] = melted["Result"].str.replace(f"{stat}", "")

    return melted

###SCORES
with tab1:
    st.info("Score trends over time")
    score_df = prepare_stat_trend(filtered_df, "Score", team)

    #FILTER
    if outcome == "Win":
        plot_df = score_df[score_df["Result"] == "Win"]

    elif outcome == "Loss":
        plot_df = score_df[score_df["Result"] == "Loss"]

    else:
        plot_df = score_df

    #PLOT
    fig = px.line(plot_df, x="Season", y="Score", color="Result")

    st.plotly_chart(fig)

#ASSISTS
with tab2:
    st.info("Assist trends over time")
    assist_df = prepare_stat_trend(filtered_df, "Ast", team)

    #FILTER
    if outcome == "Win":
        plot_df = assist_df[assist_df["Result"] == "Win"]

    elif outcome == "Loss":
        plot_df = assist_df[assist_df["Result"] == "Loss"]

    else:
        plot_df = assist_df

    #PLOT
    fig = px.line(plot_df, x="Season", y="Ast", color="Result")

    st.plotly_chart(fig)

#REBOUNDS
with tab3:
    st.info("Rebound trends over time")
    reb_df = prepare_stat_trend(filtered_df, "_rebounds", team)

    #FILTER
    if outcome == "Win":
        plot_df = reb_df[reb_df["Result"] == "Win"]

    elif outcome == "Loss":
        plot_df = reb_df[reb_df["Result"] == "Loss"]

    else:
        plot_df = reb_df

    #PLOT
    fig = px.line(plot_df, x="Season", y="_rebounds", color="Result")

    st.plotly_chart(fig)

st.write('---')
#--------------------------DISTRIBUTION-------------------------------
st.subheader("📊 Distribution")
tab1, tab2 = st.tabs([
    "Scores",
    "Score Breakdown"
    ])

with tab1:
    st.info("How are scores distributed? Are games usually close or high-scoring?")
    score_df = prepare_stat_trend(filtered_df, "Score", team)

    #FILTER
    if outcome == "Win":
        plot_df = score_df[score_df["Result"] == "Win"]

    elif outcome == "Loss":
        plot_df = score_df[score_df["Result"] == "Loss"]

    else:
        plot_df = score_df

    #PLOT
    fig = px.histogram(plot_df, x="Score", color="Result")

    st.plotly_chart(fig)
    

with tab2:
    st.info("""How does the team score its points? 
    Is it driven by 3-pointers, inside scoring, or free throws?""")


    #1. Create team-based stats (like you did for score)
    filtered_df["TeamFGM"] = filtered_df.apply(
    lambda row: row["WFGM"] if row["WTeamName"] == team else row["LFGM"],
    axis=1
    )

    filtered_df["TeamFGM3"] = filtered_df.apply(
    lambda row: row["WFGM3"] if row["WTeamName"] == team else row["LFGM3"],
    axis=1
    )

    filtered_df["TeamFTM"] = filtered_df.apply(
    lambda row: row["WFTM"] if row["WTeamName"] == team else row["LFTM"],
    axis=1
    )

    #compute totals
    total_3pt = (filtered_df["TeamFGM3"].sum()) * 3
    total_ft = filtered_df["TeamFTM"].sum()
    total_2pt = ((filtered_df["TeamFGM"] - filtered_df["TeamFGM3"]).sum()) * 2

    #create a dataframe
    score_breakdown = pd.DataFrame({
    "Type": ["2PT", "3PT", "FT"],
    "Points": [total_2pt, total_3pt, total_ft]
    })

    #plot
    fig = px.pie(
    score_breakdown,
    names="Type",
    values="Points",
    title="Scoring Breakdown"
    )

    st.plotly_chart(fig, use_container_width=True)