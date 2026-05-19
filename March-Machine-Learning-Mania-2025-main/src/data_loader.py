import pandas as pd
from pathlib import Path

# Go up from src/ to project root
BASE_DIR = Path(__file__).resolve().parent.parent


def load_men_data():
    return pd.read_csv("https://raw.githubusercontent.com/ChisomNwankwo/ml-datasets/refs/heads/main/processed/mens_team.csv")



def load_women_data():
    return pd.read_csv("https://raw.githubusercontent.com/ChisomNwankwo/ml-datasets/refs/heads/main/processed/womens_team.csv")

