import streamlit as st
import bar_graph as bar_graph
import equality_line_graph
import pandas as pd
from utils import TOWNS, DATA_FILE_PATH, process_file

st.set_page_config(layout="wide")


st.title('Wellesley Computational Housing Economics Lab')
st.subheader('Policy Oriented Mortgage Payment Simulator')

town1 = st.selectbox('What MA town are you interested in?', TOWNS)
town2 = st.selectbox(f'What MA town do you want to compare with {town1}?', TOWNS)

col1, col2 = st.columns(2)
df = process_file(DATA_FILE_PATH)
with col1:
     mortgage_rate = st.number_input("Enter your annual mortgage rate (e.g. 8.21 for 8.21%):", format="%.2f")/12/100
     if mortgage_rate:
          df['mr30_1'] = mortgage_rate
with col2:
     down_payment_percent = st.number_input("Enter your down payment as a percentage of total price (e.g. 50 for 50%):", value=50.00, format="%.2f")/100
df_bar = bar_graph.calculate_monthly_payments(bar_graph.filter_df(df),down_payment_percent)
# st.pyplot(bar_graph.generate_plot(df_bar, town))

df_equality_line = bar_graph.calculate_monthly_payments(equality_line_graph.filter_df(df), down_payment_percent)
# st.subheader('Equality Line Comparison For With and Without Program')
# st.pyplot(equality_line_graph.plot_equality_graph(df_equality_line, town))

with col1:
     st.header(town1)
     st.pyplot(bar_graph.generate_plot(df_bar, town1))
     st.pyplot(equality_line_graph.plot_equality_graph(df_equality_line, town1))


with col2:
     st.header(town2)
     st.pyplot(bar_graph.generate_plot(df_bar, town2))
     st.pyplot(equality_line_graph.plot_equality_graph(df_equality_line, town2))