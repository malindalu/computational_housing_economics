import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import TOWNS

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

def calculate_monthly_payments(df, down_payment_percent=0.5):
     # Process each town
     for town in TOWNS:
          if town not in df.columns:
               print(f"Column '{town}' not found in the data.")
               continue
          # Convert the town column to numeric
          zhvi_column = pd.to_numeric(df[town], errors='coerce')
          
          # Calculate the Conventional Loan (CL) monthly payment
          df[f'{town}_CL'] = zhvi_column * (df['mr30_1'] * ((1 + df['mr30_1']) ** 360)) / (((1 + df['mr30_1']) ** 360) - 1)
          
          mortgage_amount = zhvi_column * (1 - down_payment_percent)

          # Calculate the MRRP (Modified Reduced Rate Payment)
          df[f'{town}_MRRP'] = np.where(
               mortgage_amount < 550000,
               ((mortgage_amount) * (df['afr_month'] / 2)) + 
               ((mortgage_amount) * (df['mr30_1'] * ((1 + df['mr30_1']) ** 360)) / (((1 + df['mr30_1']) ** 360) - 1)),
               (550000 * (df['afr_month'] / 2)) + 
               ((zhvi_column - 550000) * (df['mr30_1'] * ((1 + df['mr30_1']) ** 360)) / (((1 + df['mr30_1']) ** 360) - 1))
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
     if f'{town}_MRRP' not in df.columns or  f'{town}_dif' not in df.columns:
          return None
     # create index to help lable x axis based on year and still plot by month
     all_months = pd.MultiIndex.from_product([range(2016, 2025), range(1, 13)], names=["year", "month"])
     df = df.set_index(["year", "month"]).reindex(all_months).reset_index()

     _, ax = plt.subplots(figsize=(10, 6))
     ax.bar(df.index, df[f'{town}_MRRP'], color='blue',label='w/ Program', alpha=0.5)
     ax.bar(df.index, df[f'{town}_dif'], bottom=df[f'{town}_MRRP'], color='orange', label='w/o program', alpha=0.5)

     # labeling
     ax.set_title(f'Comparison of Mortgage Payments for {town}')
     ax.set_xlabel('Month')
     ax.set_ylabel('Monthly Payment ($)')

     yearly_ticks = df[df['month'] == 1].index # start year label at january, can change
     ax.set_xticks(yearly_ticks)
     ax.set_xticklabels(df.loc[yearly_ticks, 'year'])

     # set y ticks
     ax.set_ylim(0, 14000)
     ax.set_yticks(np.arange(0, 14000, 4000))
     plt.legend(loc=1)
     plt.savefig('test')
     return plt
