import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from utils import TOWNS, WELLESLEY_MAX_SECOND_LOAN, WELLESLEY_AFR_FRACTION

def filter_df(df):
     # Define date filter
     df = df[(df['year'] >= 2016) & (df['month'].between(2, 12)) |
          ((df['year'] >= 2017) & (df['month'].between(1, 12))) |
          ((df['year'] >= 2018) & (df['month'].between(1, 12))) |
          ((df['year'] >= 2019) & (df['month'].between(1, 12))) |
          ((df['year'] >= 2020) & (df['month'].between(1, 12))) |
          ((df['year'] >= 2021) & (df['month'].between(1, 12))) |
          ((df['year'] >= 2022) & (df['month'].between(1, 12))) |
          ((df['year'] >= 2023) & (df['month'].between(1, 12))) |
          ((df['year'] >= 2024) & (df['month'].between(2, 4)))]

     return df

def calculate_monthly_payments(df, max_second_loan = WELLESLEY_MAX_SECOND_LOAN, afr_fraction = WELLESLEY_AFR_FRACTION):
     # Process each town
     for town in TOWNS:
          if town not in df.columns:
               print(f"Column '{town}' not found in the data.")
               continue
          # Convert the town column to numeric
          zhvi_column = pd.to_numeric(df[town], errors='coerce')
          
          # Calculate the Conventional Loan (CL) monthly payment
          df[f'{town}_CL'] = zhvi_column * (df['mr30_1'] * ((1 + df['mr30_1']) ** 360)) / (((1 + df['mr30_1']) ** 360) - 1)
          
          mortgage_amount = zhvi_column / 2 # applicable amount

          # Calculate the MRRP (Modified Reduced Rate Payment)
          df[f'{town}_MRRP'] = np.where(
               mortgage_amount < max_second_loan,
               # if 50% of applicable amount is the lesser
               # 1/2 at half AFR rate and the other half at the original/given mortgage rate
               (mortgage_amount * (df['afr_month'] * afr_fraction)) + 
               ((mortgage_amount) * (df['mr30_1'] * ((1 + df['mr30_1']) ** 360)) / (((1 + df['mr30_1']) ** 360) - 1)),
               # else, 550000 max is the lesser
               (max_second_loan * (df['afr_month'] * afr_fraction)) + 
               ((zhvi_column - max_second_loan) * (df['mr30_1'] * ((1 + df['mr30_1']) ** 360)) / (((1 + df['mr30_1']) ** 360) - 1))
          )

          # # Calculate the MRRP (Modified Reduced Rate Payment)
          # df[f'{town}_MRRP'] = np.where(
          #      zhvi_column / 2 < 550000,
          #      ((zhvi_column / 2) * (df['afr_month'] / 2)) + 
          #      ((zhvi_column / 2) * (df['mr30_1'] * ((1 + df['mr30_1']) ** 360)) / (((1 + df['mr30_1']) ** 360) - 1)),
          #      (550000 * (df['afr_month'] / 2)) + 
          #      ((zhvi_column - 550000) * (df['mr30_1'] * ((1 + df['mr30_1']) ** 360)) / (((1 + df['mr30_1']) ** 360) - 1))
          # )
          
          # Calculate the difference (dif) between CL and MRRP
          df[f'{town}_dif'] = df[f'{town}_CL'] - df[f'{town}_MRRP']
     return df

def generate_plot(df, town):
     # if f'{town}_MRRP' not in df.columns or  f'{town}_dif' not in df.columns:
     #      return None
     # # create index to help lable x axis based on year and still plot by month
     # all_months = pd.MultiIndex.from_product([range(2016, 2025), range(1, 13)], names=["year", "month"])
     # df = df.set_index(["year", "month"]).reindex(all_months).reset_index()

     # _, ax = plt.subplots(figsize=(10, 6))
     # ax.bar(df.index, df[f'{town}_MRRP'], color='blue',label='w/ Program', alpha=0.5)
     # ax.bar(df.index, df[f'{town}_dif'], bottom=df[f'{town}_MRRP'], color='orange', label='w/o program', alpha=0.5)

     # # labeling
     # ax.set_title(f'Comparison of Mortgage Payments for {town}')
     # ax.set_xlabel('Month')
     # ax.set_ylabel('Monthly Payment ($)')

     # yearly_ticks = df[df['month'] == 1].index # start year label at january, can change
     # ax.set_xticks(yearly_ticks)
     # ax.set_xticklabels(df.loc[yearly_ticks, 'year'])

     # # set y ticks
     # ax.set_ylim(0, 14000)
     # ax.set_yticks(np.arange(0, 14000, 4000))
     # plt.legend(loc=1)
     # return plt

     if f'{town}_MRRP' not in df.columns or f'{town}_dif' not in df.columns:
        return None

     # Create index to help label x-axis based on year and still plot by month
     all_months = pd.MultiIndex.from_product([range(2016, 2025), range(1, 13)], names=["year", "month"])
     df = df.set_index(["year", "month"]).reindex(all_months).reset_index()

     df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
     df[f'{town}_without_program'] = df[f'{town}_MRRP'] + df[f'{town}_dif']


     # Create traces for the bar chart
     fig = go.Figure()
     
     # Bar for 'w/ Program'
     fig.add_trace(
          go.Bar(
               x=df.index, 
               y=df[f'{town}_MRRP'], 
               name='w/ Program', 
               marker_color='blue',
               opacity=0.7,
               hovertemplate=(
               'w/ program: %{y}<extra></extra><br>' 
               'difference: %{customdata:$,.2f}<br>'),
               customdata=df[f'{town}_dif'].values
          )
          
     )

     # Bar for 'w/o program'
     fig.add_trace(
          go.Bar(
               x=df.index, 
               y=df[f'{town}_dif'], 
               name='w/o Program', 
               marker_color='orange',
               opacity=0.7,
               hovertemplate='w/o program: %{customdata:$,.2f}<extra></extra>',
               customdata=(df[f'{town}_dif'] + df[f'{town}_MRRP']).values,
               base=df[f'{town}_MRRP']
          )
     )

     # Update layout for titles and labels
     fig.update_layout(
          title=f'Comparison of Mortgage Payments for {town}',
          xaxis=dict(
               title='Month',
               tickvals=df[df['month'] == 1].index,
               ticktext=df.loc[df['month'] == 1, 'year'],
          ),
          yaxis=dict(
               title='Monthly Payment ($)',
               range=[0, 14000],
               tickvals=list(range(0, 14000, 4000)),
          ),
          barmode='stack',
          legend=dict(x=1, y=1, bgcolor='rgba(255,255,255,0)'),
          hovermode='x unified',
          template='plotly_white'
     )
     
     return fig
