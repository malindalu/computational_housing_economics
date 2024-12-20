import streamlit as st
import bar_graph as bar_graph
import equality_line_graph
import pandas as pd
from utils import TOWNS, DATA_FILE_PATH, process_file, WELLESLEY_MAX_SECOND_LOAN, WELLESLEY_AFR_FRACTION

st.set_page_config(layout="wide")


st.subheader('Wellesley Computational Housing Economics Lab')
st.title('Policy Oriented Mortgage Payment Simulator')
st.subheader('Wellesley College Faculty Mortgage Program')

town1 = st.selectbox('What MA town are you interested in?', TOWNS)
town2 = st.selectbox(f'What MA town do you want to compare with {town1}?', TOWNS)

st.text("The simulator uses the College Program parameters as default. If you would like to adjust the parameters, feel free to enter them below:")

col1, col2 = st.columns(2)
df = process_file(DATA_FILE_PATH)
with col1:
     # mortgage_rate = st.number_input("Enter your annual mortgage rate (e.g. 8.21 for 8.21%):", format="%.2f")/12/100
     # if mortgage_rate:
     #      df['mr30_1'] = mortgage_rate
     max_second_loan = st.number_input(f"Enter the maximum second loan amount (Currently, the College provides ${WELLESLEY_MAX_SECOND_LOAN}):", value = WELLESLEY_MAX_SECOND_LOAN)
with col2:
     # down_payment_percent = st.number_input("Enter your down payment as a percentage of total price (e.g. 50 for 50%):", value=50.00, format="%.2f")/100
     afr_fraction = st.number_input("Enter the fraction of AFR used as the reduced interest rate (Currently, the College sets it at 1/2 AFR)", value = WELLESLEY_AFR_FRACTION)
df_bar = bar_graph.calculate_monthly_payments(bar_graph.filter_df(df), max_second_loan)

df_equality_line = bar_graph.calculate_monthly_payments(equality_line_graph.filter_df(df))

st.subheader("Below are the results:")

col1,col2 = st.columns(2)
with col1:
     st.header(town1)
     st.pyplot(bar_graph.generate_plot(df_bar, town1))

with col2:
     st.header(town2)
     st.pyplot(bar_graph.generate_plot(df_bar, town2))

st.text("Monthly mortgage payments with and without the program, from 2016 to 2024. We assume that home value = ZHVI (Zillow House Value Index), which measures the typical home value in the given town.")

col1,col2 = st.columns(2)
with col1:
     st.pyplot(equality_line_graph.plot_equality_graph(df_equality_line, town1))

with col2:
     st.pyplot(equality_line_graph.plot_equality_graph(df_equality_line, town2))

st.text("Monthly mortgage payment with and without the program, compared with 1/3 of monthly average median income (AMI) for 2016 and 2024.")
st.text("Note: each point represents the town in a specific year from 2016-2024. Greener points are closer to 2016 and bluer points are closer to 2024. ")
st.subheader("For interpretation of the graphs:")
st.text("- If a point is inside the AMI box, then the town can be considered affordable both with and without the program.")
st.text("- If a point is above the AMI box, then the town can be considered unafforidable without the program but affordable with the program.")
st.text("- If a point is outside the AMI box towards the top right, then the town can be considered unafforidable both with and without the program.")
