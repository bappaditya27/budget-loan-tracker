import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Finance Planner", layout="wide")

# Custom CSS to make it look cleaner
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏡 Smart Expenditure Planner")
st.write("Plan your journey from customer support to your dream village home.")

# --- SIDEBAR: INPUTS ---
st.sidebar.header("💳 Income & Fixed Costs")
salary = st.sidebar.number_input("In-hand Monthly Salary (₹)", value=20000, step=500)

st.sidebar.subheader("Fixed Monthly Needs")
rent = st.sidebar.slider("Rent & Utilities (₹)", 0, 10000, 5000)
food = st.sidebar.slider("Food & Groceries (₹)", 0, 8000, 4000)
others = st.sidebar.number_input("Others (₹)", value=1000)

# --- DEBT MANAGEMENT ---
st.header("📉 Debt & EMI Strategy")
col_loan, col_emi = st.columns(2)
with col_loan:
    loan_bal = st.number_input("Total Debt Remaining (₹)", value=50000)
with col_emi:
    emi = st.number_input("Monthly EMI (₹)", value=3000)

# --- CALCULATIONS ---
total_fixed = rent + food + others
total_outflow = total_fixed + emi
remaining_cash = salary - total_outflow
savings_percent = (remaining_cash / salary) * 100 if salary > 0 else 0

# --- DASHBOARD UI ---
st.divider()
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Outflow", f"₹{total_outflow}")
with c2:
    status = "Healthy" if remaining_cash > 2000 else "Tight"
    st.metric("Budget Status", status, delta=f"{round(savings_percent)}% Savings")
with c3:
    st.metric("Net Surplus", f"₹{remaining_cash}")
with c4:
    months_to_debt_free = round(loan_bal / emi) if emi > 0 else 0
    st.metric("Debt-Free In", f"{months_to_debt_free} Months")

# --- VISUAL PLANNING ---
st.subheader("📊 Your Expenditure Breakdown")
df_plot = pd.DataFrame({
    "Category": ["Rent/Utilities", "Food", "Others", "Debt (EMI)", "Potential Savings"],
    "Amount": [rent, food, others, emi, max(0, remaining_cash)]
})

fig = px.bar(df_plot, x="Category", y="Amount", color="Category", 
             text_auto='.2s', title="Monthly Cash Flow")
st.plotly_chart(fig, use_container_width=True)

# --- THE 'DREAM HOME' PLANNER ---
st.divider()
st.subheader("🏗️ Village Home Progress")
goal_amount = 500000 # Example: 5 Lakhs for construction
saved_so_far = st.number_input("Current Savings for Home (₹)", value=10000)

if remaining_cash > 0:
    months_to_goal = round((goal_amount - saved_so_far) / remaining_cash)
    st.write(f"💡 If you save your entire surplus of **₹{remaining_cash}**, you will reach your ₹5 Lakh goal in **{months_to_goal} months**.")
    st.progress(min(saved_so_far / goal_amount, 1.0))
else:
    st.warning("⚠️ You currently have no surplus to save for your home. Consider reducing expenses or increasing income.")
