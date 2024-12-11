import os
import numpy as np
import pandas as pd
from xgboost import XGBClassifier

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


x_train, y_train, x_test, y_test = get_data()


class Simple:
    def fit(self, x, y):
        avg_home = y[y == 0].count() / y.count()
        avg_draw = y[y == 1].count() / y.count()
        avg_away = y[y == 2].count() / y.count()
        assert avg_home + avg_draw + avg_away == 1
        self.probs = [avg_home, avg_draw, avg_away]

    def predict(self, x):
        return np.array([self.probs.index(max(self.probs))] * len(x))

    def predict_proba(self, x):
        return np.array([self.probs] * len(x))


class Bet365:
    def fit(self, x, y):
        pass

    def predict(self, x):
        odds = x[["B365H", "B365D", "B365A"]].values
        return odds.argmin(axis=1)

    def predict_proba(self, x):
        odds = x[["B365H", "B365D", "B365A"]].values
        return 1 / odds


class XGB:
    def __init__(self, **kwargs):
        self.model = XGBClassifier(**kwargs)
        self.x_columns = [
            "home_goals_last_5",
            "home_points_last_5",
            "away_goals_last_5",
            "away_points_last_5",
            "B365H",
            "B365D",
            "B365A",
        ]

    def fit(self, x, y):
        self.model.fit(x[self.x_columns], y)

    def predict(self, x):
        return self.model.predict(x[self.x_columns])

    def predict_proba(self, x):
        return self.model.predict_proba(x[self.x_columns])


models = {
    "XGBoost": XGB(enable_categorical=True, max_depth=3),
    "Baseline": Simple(),
    "Bet365": Bet365(),
}

for name, model in models.items():
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    accuracy = (predictions == y_test).sum() / len(y_test)
    print(f"{name} accuracy: {accuracy * 100:.2f}%")
    earnings = 0
    num_bets = 0
    probs = model.predict_proba(x_test)
    for i, (_, row) in enumerate(x_test.iterrows()):
        probs_this_game = probs[i]
        evs = []
        for outcome_to_bet_on in range(3):
            expected_value = (
                probs_this_game[outcome_to_bet_on]
                * row[f"B365{mapping[outcome_to_bet_on]}"]
                - (1 - probs_this_game[outcome_to_bet_on]) * 1
            )
            evs.append(expected_value)
        if any(ev > 0 for ev in evs):
            num_bets += 1
            outcome_to_bet_on = evs.index(max(ev for ev in evs))
            # print(
            #     f"{name} betting on {row['HomeTeam']} vs {row['AwayTeam']}. Predicted outcome: {mapping[predictions[i]]}. Betting on: {mapping[outcome_to_bet_on]}"
            # )
            if outcome_to_bet_on == y_test.iloc[i]:
                earnings += row[f"B365{mapping[outcome_to_bet_on]}"] - 1
            else:
                earnings -= 1
    print(f"{name} earnings after betting on {num_bets} games: {earnings}")
    print(f"{name} ROI: {earnings / num_bets * 100:.2f}%")
