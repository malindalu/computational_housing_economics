import matplotlib.pyplot as plt

# Import Excel data

def filter_df(df):
     # Define date filter
     df = df[((df['year'] == 2016) & (df['month'] >= 2)) |
               ((df['year'] >= 2017) & (df['year'] <= 2023)) |
               ((df['year'] == 2024) & (df['month'] <= 4))]

     return df

def plot_equality_graph(df, town):
    _, ax = plt.subplots()
    for year, color in zip(range(2016, 2025), ["green", "darkgreen", "forestgreen", "mediumseagreen", "mediumturquoise", 
                                               "darkcyan", "steelblue", "dodgerblue", "blue"]):
        yearly_data = df[df['year'] == year]
        ax.scatter(yearly_data[f"{town}_CL"], yearly_data[f"{town}_MRRP"], color=color, label=str(year))

    # Plot reference lines
    ax.plot([0, 10000], [0, 10000], color="gray", linestyle="--", label="y = x line")
    ax.axhline(y=df[df['year'] == 2024]['AMI'].mean() / 36, color="red", linestyle="--", label="1/3 2024 Monthly AMI")
    ax.axhline(y=df[df['year'] == 2016]['AMI'].mean() / 36, color="orange", linestyle="--", label="1/3 2016 Monthly AMI")
    
    # Labels, title, and legend
    ax.set_xlabel(f"{town} with Program")
    ax.set_ylabel(f"{town} without Program")
    ax.set_title(f"Mortgage Payments for {town}")
    ax.legend()
    return plt
