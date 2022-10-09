import json
import numpy as np
import streamlit as st
import pandas as pd

st.title("Personal finances")

category_path = "data/categories.json"

@st.experimental_singleton
def get_categories():
    with open(category_path) as f:
        return json.load(f)

categories = get_categories()
# st.write(categories)

def get_transactions():
    with open("data/data.csv") as f:
        contents = f.readlines()
    header = contents.pop(0).split(",")
    df = pd.DataFrame([
        {column: value for column, value in zip(header, row.split(",", maxsplit=len(header)))}
        for row in contents
    ])
    return df

def parse_transactions(df: pd.DataFrame):
    new_rows = []
    for _, row in df.iterrows():
        new_rows.append({
            "Date": pd.to_datetime(row["Date"], dayfirst=True),
            "Amount": float(row["Amount"]),
            "Memo": row["Memo\n"],
            "Category": categories.get(row["Memo\n"].split("\t")[0], "Other"),
        })
    new_df = pd.DataFrame(new_rows)
    return new_df


transactions = get_transactions()
parsed = parse_transactions(transactions)

st.write(parsed.astype(str))

def categorise(parsed):
    uncategorised = parsed[parsed["Category"] == "Other"]
    st.write(f"{len(uncategorised)} uncategorised transactions")
    options = set(categories.values())
    example_row = uncategorised.iloc[0]
    key = example_row["Memo"].split("\t")[0]
    st.write(key, example_row.astype(str))
    category = st.selectbox("Choose a category", {"Other"}.union(options))
    if category == "Other":
        category = st.text_input("Category")

    if st.button("Confirm"):
        categories[key] = category
        with open(category_path, "w") as f:
            json.dump(categories, f, sort_keys=True, indent=2)
        st.experimental_rerun()

if st.checkbox("Categorise transactions", value=False):
    categorise(parsed)
