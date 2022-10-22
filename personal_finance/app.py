from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
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


@st.experimental_memo
def get_transactions():
    with open("data/data.csv") as f:
        contents = f.readlines()
    header = contents.pop(0).split(",")
    df = pd.DataFrame(
        [
            {
                column: value
                for column, value in zip(header, row.split(",", maxsplit=len(header)))
            }
            for row in contents
        ]
    )
    return df


def parse_transactions(df: pd.DataFrame):
    new_rows = []
    for _, row in df.iterrows():
        new_rows.append(
            {
                "Date": pd.to_datetime(row["Date"], dayfirst=True),
                "Amount": float(row["Amount"]),
                "Memo": row["Memo\n"],
                "Category": categories.get(row["Memo\n"].split("\t")[0], "Other"),
            }
        )
    new_df = pd.DataFrame(new_rows).sort_values("Date", ascending=True)
    return new_df


transactions = get_transactions()
parsed = parse_transactions(transactions)

tabs = st.tabs(["Categorise transactions", "Track spending this month"])

with tabs[0]:
    uncategorised = parsed[parsed["Category"] == "Other"].sort_values("Date", ascending=False)
    st.write(uncategorised.astype(str))
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

with tabs[1]:
    with open("data/budget.json") as f:
        budget = json.load(f)
    if st.checkbox("Add a random grand per month to income"):
        budget["Income"] += 1000
    past_months = st.number_input("Choose month in the past", min_value=0, step=1)
    today = datetime.now() - relativedelta(months=past_months)
    st.header(f"This month: {today.strftime('%B')}")
    last_month = today - relativedelta(months=1)
    subscriptions_last_month = parsed[
        parsed["Date"].apply(
            lambda x: x.year == last_month.year and x.month == last_month.month
        )
        & (parsed["Category"] == "Subscriptions")
    ]
    st.subheader("Subscriptions last month")
    st.write(subscriptions_last_month.astype(str))
    transactions_this_month = parsed[
        parsed["Date"].apply(lambda x: x.year == today.year and x.month == today.month)
    ]
    excluded_transactions = (
        (transactions_this_month["Amount"] > 0)
        | (transactions_this_month["Category"] == "Rent")
        | (transactions_this_month["Category"] == "Subscriptions")
    )
    if st.checkbox("Remove (travel over £20, hotel) expenses"):
        excluded_transactions = (
            excluded_transactions
            | (
                (transactions_this_month["Category"] == "Travel")
                & (transactions_this_month["Amount"] < -20)
            )
            | (transactions_this_month["Category"] == "Hotel")
        )
    st.subheader("Excluded transactions this month")
    st.write(transactions_this_month[excluded_transactions].astype(str))
    st.subheader("Included transactions this month")
    included_transactions = transactions_this_month[~excluded_transactions]
    st.write(included_transactions.sort_values("Amount").astype(str))

    disposable_income = budget["Income"] - (
        budget["Rent (total)"] - budget["Rent subsidy"]
    )
    first_of_month = today - timedelta(days=today.day - 1)
    last_of_month = first_of_month + relativedelta(months=1) - timedelta(days=1)
    daily_allowance = disposable_income * 1 / (last_of_month - first_of_month).days

    st.subheader("Budget")
    st.caption(
        f"Disbosable income after rent: {disposable_income}. Daily allowance: £{daily_allowance:.0f}"
    )

    ratio_of_month_passed = included_transactions["Date"].apply(
        lambda day: (day - first_of_month).days / (last_of_month - first_of_month).days
    )
    expenses = np.cumsum(
        -included_transactions["Amount"]
    ) + ratio_of_month_passed * np.sum(-subscriptions_last_month["Amount"])
    pro_rated_income = disposable_income * ratio_of_month_passed

    fig, ax = plt.subplots()
    fig.autofmt_xdate(rotation=45)
    ax.plot(
        included_transactions["Date"],
        expenses,
        label="Expenses",
    )
    ax.plot(
        included_transactions["Date"],
        pro_rated_income,
        label="Budget",
    )
    ax.legend()
    st.write(fig)
    expenses_so_far = expenses.iloc[-1]
    income_so_far = pro_rated_income.iloc[-1]
    st.subheader(f"Net so far this month: {income_so_far - expenses_so_far:.0f} GBP")

    st.subheader("Breakdown of all expenses (excluding subscriptions and rent)")
    category_expenses = []
    for category, rows in included_transactions.groupby("Category"):
        category_expenses.append(
            {
                "Category": category,
                "Amount": -rows["Amount"].sum(),
            }
        )
    df = pd.DataFrame(category_expenses).set_index("Category")
    st.bar_chart(df)
