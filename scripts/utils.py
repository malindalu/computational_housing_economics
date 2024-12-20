import pandas as pd

DATA_FILE_PATH = "data/MortgageRatesData.xlsx"

TOWNS = ["Acton", "Arlington", "Ashland", "Bedford", "Belmont", "Boston", "Brookline", "Cambridge", "Canton", "Concord",
         "Dedham", "Dover", "Framingham", "Franklin", "Holliston", "Hopkinton", "Hudson", "Lexington", "Lincoln", "Marlborough",
         "Maynard", "Medfield", "Medford", "Medway", "Millis", "Milton", "Natick", "Needham", "Newton", "Norfolk", "Norwood",
         "Sharon", "Sherborn", "Somerville", "Southborough", "Stow", "Sudbury", "Walpole", "Waltham", "Watertown", "Wayland",
         "Wellesley", "Weston", "Westwood", "Winchester"]

WELLESLEY_MAX_SECOND_LOAN = 550000
WELLESLEY_AFR_FRACTION = 1/2

def process_file(file_path):
     # Import Excel data
     df = pd.read_excel(file_path, sheet_name=0)

     # Calculate the monthly interest rate
     df['mr30_1'] = (pd.to_numeric(df['mr30yearfixed'], errors='coerce') / 12) / 100
     df['afr_month'] = pd.to_numeric(df['longtermafr'], errors='coerce') / 12

     # Change date to format and filter data by date
     df['date'] = pd.to_datetime(df['date'])
     df['year'] = df['date'].dt.year
     df['month'] = df['date'].dt.month
     return df