import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GramVikas Finance Tracker", layout="wide")
st.title("📊 Monthly Budget & Loan Amortization")

# Sidebar for Inputs
st.sidebar.header("💰 Monthly Income & Basics")
salary = st.sidebar.number_input("Monthly In-hand Salary (₹)", value=20000)
rent = st.sidebar.number_input("Rent & Utilities (₹)", value=5000)
food = st.sidebar.number_input("Food & Essentials (₹)", value=4000)
ngo = st.sidebar.number_input("NGO Contribution (₹)", value=1000)

# Debt Section
st.header("📉 Debt Details")
col_a, col_b, col_c = st.columns(3)
with col_a:
    loan_name = st.text_input("Loan Name", "Personal Loan")
with col_b:
    balance = st.number_input("Remaining Principal (₹)", value=50000)
with col_c:
    annual_interest = st.number_input("Annual Interest Rate (%)", value=12.0)

emi = st.number_input("Monthly EMI (₹)", value=3000)

# Amortization Logic
st.subheader("🗓️ Loan Amortization Table")
schedule = []
current_balance = balance
monthly_rate = annual_interest / (12 * 100)

month = 1
while current_balance > 0 and month <= 60: # Limit to 5 years for safety
    interest_payment = current_balance * monthly_rate
    principal_payment = min(emi - interest_payment, current_balance)
    current_balance -= principal_payment
    
    schedule.append({
        "Month": month,
        "Interest Paid (₹)": round(interest_payment, 2),
        "Principal Paid (₹)": round(principal_payment, 2),
        "Remaining Balance (₹)": round(max(0, current_balance), 2)
    })
    month += 1
    if emi <= interest_payment:
        st.error("Error: Your EMI is too low to cover the interest. The debt will never be paid off!")
        break

df_schedule = pd.DataFrame(schedule)

# Display Table & Metrics
st.dataframe(df_schedule, use_container_width=True)

# Visualizing Interest vs Principal over time
st.subheader("Interest vs. Principal Trend")
fig_trend = px.area(df_schedule, x="Month", y=["Interest Paid (₹)", "Principal Paid (₹)"],
                   title="How your payments change over time",
                   color_discrete_sequence=['#EF553B', '#00CC96'])
st.plotly_chart(fig_trend, use_container_width=True)

# Final Summary
total_interest = df_schedule["Interest Paid (₹)"].sum()
st.info(f"Summary: You will pay a total of **₹{total_interest:,.2f}** in interest over **{len(schedule)} months**.")
