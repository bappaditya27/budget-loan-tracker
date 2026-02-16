import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GramVikas Finance Tracker", layout="wide")
st.title("📊 Monthly Budget & Loan Visualization")

# Sidebar for Inputs
st.sidebar.header("💰 Monthly Income & Basics")
salary = st.sidebar.number_input("Monthly In-hand Salary (₹)", value=20000)
rent = st.sidebar.number_input("Rent & Utilities (₹)", value=5000)
food = st.sidebar.number_input("Food & Essentials (₹)", value=4000)
ngo = st.sidebar.number_input("NGO/Village Contribution (₹)", value=1000)

# Debt Section
st.header("📉 Debt & Loan Tracking")
with st.expander("Add Your Loans"):
    loan_name = st.text_input("Loan Name", "Personal Loan")
    principal = st.number_input("Remaining Principal (₹)", value=50000)
    emi = st.number_input("Monthly EMI (₹)", value=3000)

# Calculations
total_expenses = rent + food + ngo + emi
disposable_income = salary - total_expenses

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Expenses", f"₹{total_expenses}")
col2.metric("Monthly EMI", f"₹{emi}")
col3.metric("Left for Savings", f"₹{disposable_income}", delta_color="normal")

# Visualizations
st.subheader("Wallet Breakdown")
df_pie = pd.DataFrame({
    "Category": ["Rent", "Food", "NGO", "Debt (EMI)", "Savings"],
    "Amount": [rent, food, ngo, emi, max(0, disposable_income)]
})
fig = px.pie(df_pie, values='Amount', names='Category', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig)

st.success(f"At this rate, you will pay off '{loan_name}' in approximately {round(principal/emi)} months.")
