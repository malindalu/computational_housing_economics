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
        ax.scatter(yearly_data[f"{town}_MRRP"],yearly_data[f"{town}_CL"], color=color)

    # Plot reference lines
    # 45 degree line
    ax.plot([0, 10000], [0, 10000], color="gray", linestyle="--")

    ami_2016 = df[df['year'] == 2016]['AMI'].mean() / 36
    ax.plot([0, ami_2016], [ami_2016, ami_2016],color="orange", linestyle="--", label="1/3 2016 Monthly AMI")
    ax.plot([ami_2016, ami_2016],[0, ami_2016],color="orange", linestyle="--")
    ami_2024  = df[df['year'] == 2024]['AMI'].mean() / 36
    ax.plot([0, ami_2024], [ami_2024, ami_2024],color="red", linestyle="--", label="1/3 2024 Monthly AMI")
    ax.plot([ami_2024, ami_2024],[0, ami_2024],color="red", linestyle="--")

    # Labels, title, and legend
    ax.set_xlabel(f"{town} with Program")
    ax.set_ylabel(f"{town} without Program")
    ax.set_title(f"Mortgage Payments for {town}")
    ax.legend()
    return plt
