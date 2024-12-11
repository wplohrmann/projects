import os
import pandas as pd
from xgboost import XGBClassifier

dfs = []
for f in os.listdir("."):
    if f.endswith(".csv"):
        sub_df = pd.read_csv(f)
        sub_df["file"] = f
        dfs.append(sub_df)
df = pd.concat(dfs)


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
            ((df["HomeTeam"] == row["HomeTeam"]) | (df["AwayTeam"] == row["HomeTeam"]))
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
            ((df["HomeTeam"] == row["AwayTeam"]) | (df["AwayTeam"] == row["AwayTeam"]))
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


all_except_last_game = df[df["Date"] < df.groupby("HomeTeam")["Date"].transform("max")]
test_indices = df["Date"] > pd.to_datetime("2024-11-22")
print("Number of test games:", test_indices.sum())
print("Number of training games:", (~test_indices).sum())
x_columns = [
    # "HomeTeam",
    # "AwayTeam",
    "home_goals_last_5",
    "home_points_last_5",
    "away_goals_last_5",
    "away_points_last_5",
    "B365H",
    "B365D",
    "B365A",
]
x = df[x_columns]
home_games_count = df["HomeTeam"].value_counts()
away_games_count = df["AwayTeam"].value_counts()

x_train = df[~test_indices][x_columns]
mapping = ["H", "D", "A"]
y_train = df[~test_indices]["FTR"].apply(lambda x: mapping.index(x))
x_test = df[test_indices][x_columns]
y_test = df[test_indices]["FTR"].apply(lambda x: ["H", "D", "A"].index(x))

model = XGBClassifier(enable_categorical=True, max_depth=3)
model.fit(x_train, y_train)
# predictions = model.predict(x_test)
# for i, (_, row) in enumerate(x_test.iterrows()):
#     print(row["HomeTeam"], row["AwayTeam"], "Prediction:", mapping[predictions[i]], "Actual:", mapping[y_test.iloc[i]])
# model.predict_proba(x_test)

print("XGBoost score:", model.score(x_test, y_test))

# Calculate the baseline probabilities
total_games = len(df)
home_wins = len(df[df["FTR"] == "H"])
draws = len(df[df["FTR"] == "D"])
away_wins = len(df[df["FTR"] == "A"])

home_prob = home_wins / total_games
draw_prob = draws / total_games
away_prob = away_wins / total_games

# Predict using the baseline model
baseline_predictions = [home_prob, draw_prob, away_prob]

# Calculate the accuracy of the baseline model
baseline_correct_predictions = 0
for actual in y_test:
    if actual == baseline_predictions.index(max(baseline_predictions)):
        baseline_correct_predictions += 1

baseline_accuracy = baseline_correct_predictions / len(y_test)
print("Baseline accuracy:", baseline_accuracy)
