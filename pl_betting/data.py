

import pandas as pd


import os
mapping = ["H", "D", "A"]


def get_data():
    dfs = []
    for f in os.listdir("."):
        if f.endswith(".csv"):
            sub_df = pd.read_csv(f)
            sub_df["file"] = f
            dfs.append(sub_df)
    df = pd.concat(dfs).reset_index(drop=True)

    df["HomeTeam"] = df["HomeTeam"].astype("category")
    df["AwayTeam"] = df["AwayTeam"].astype("category")
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    df["days_since_first_game"] = (df["Date"] - df["Date"].min()).dt.days
    # Add four columns, two for the home and two for the away team. The columns will contain a) number of goals scored and b) points gained in the last 5 games
    df["home_goals_last_5"] = 0
    df["home_points_last_5"] = 0
    df["away_goals_last_5"] = 0
    df["away_points_last_5"] = 0

    for idx, row in df.iterrows():
        last_5_games_home_team = (
            df[
                (
                    (df["HomeTeam"] == row["HomeTeam"])
                    | (df["AwayTeam"] == row["HomeTeam"])
                )
                & (df["Date"] < row["Date"])
            ]
            .sort_values("Date")
            .tail(5)
        )
        for _, game in last_5_games_home_team.iterrows():
            if game["HomeTeam"] == row["HomeTeam"]:
                df.at[idx, "home_goals_last_5"] += game["FTHG"]
                df.at[idx, "home_points_last_5"] += (
                    3 if game["FTR"] == "H" else 1 if game["FTR"] == "D" else 0
                )
            else:
                df.at[idx, "home_goals_last_5"] += game["FTAG"]
                df.at[idx, "home_points_last_5"] += (
                    3 if game["FTR"] == "A" else 1 if game["FTR"] == "D" else 0
                )

        last_5_games_away_team = (
            df[
                (
                    (df["HomeTeam"] == row["AwayTeam"])
                    | (df["AwayTeam"] == row["AwayTeam"])
                )
                & (df["Date"] < row["Date"])
            ]
            .sort_values("Date")
            .tail(5)
        )
        for _, game in last_5_games_away_team.iterrows():
            if game["HomeTeam"] == row["AwayTeam"]:
                df.at[idx, "away_goals_last_5"] += game["FTHG"]
                df.at[idx, "away_points_last_5"] += (
                    3 if game["FTR"] == "H" else 1 if game["FTR"] == "D" else 0
                )
            else:
                df.at[idx, "away_goals_last_5"] += game["FTAG"]
                df.at[idx, "away_points_last_5"] += (
                    3 if game["FTR"] == "A" else 1 if game["FTR"] == "D" else 0
                )

    # Last 30 games
    test_indices = df.index.isin(df.sort_values("Date").tail(100).index)
    # test_indices = df["Date"] > pd.to_datetime("2024-11-22")
    print("Number of test games:", test_indices.sum())
    print("Number of training games:", (~test_indices).sum())
    x_columns = [
        "HomeTeam",
        "AwayTeam",
        "home_goals_last_5",
        "home_points_last_5",
        "away_goals_last_5",
        "away_points_last_5",
        "B365H",
        "B365D",
        "B365A",
    ]
    x = df[x_columns]
    y = df["FTR"].apply(lambda x: mapping.index(x))

    x_train = x[~test_indices]
    y_train = y[~test_indices]
    x_test = x[test_indices]
    y_test = y[test_indices]
    return x_train, y_train, x_test, y_test
