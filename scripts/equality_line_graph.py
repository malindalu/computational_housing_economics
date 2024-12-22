import matplotlib.pyplot as plt
import plotly.graph_objects as go


# Import Excel data

def filter_df(df):
     # Define date filter
     df = df[((df['year'] == 2016) & (df['month'] >= 2)) |
               ((df['year'] >= 2017) & (df['year'] <= 2023)) |
               ((df['year'] == 2024) & (df['month'] <= 4))]

     return df

# def plot_equality_graph(df, town):
#     _, ax = plt.subplots()
#     for year, color in zip(range(2016, 2025), ["green", "darkgreen", "forestgreen", "mediumseagreen", "mediumturquoise", 
#                                                "darkcyan", "steelblue", "dodgerblue", "blue"]):
#         yearly_data = df[df['year'] == year]
#         ax.scatter(yearly_data[f"{town}_MRRP"],yearly_data[f"{town}_CL"], color=color)

#     # Plot reference lines
#     # 45 degree line
#     ax.plot([0, 10000], [0, 10000], color="gray", linestyle="--")

#     ami_2016 = df[df['year'] == 2016]['AMI'].mean() / 36
#     ax.plot([0, ami_2016], [ami_2016, ami_2016],color="orange", linestyle="--", label="1/3 2016 Monthly AMI")
#     ax.plot([ami_2016, ami_2016],[0, ami_2016],color="orange", linestyle="--")
#     ami_2024  = df[df['year'] == 2024]['AMI'].mean() / 36
#     ax.plot([0, ami_2024], [ami_2024, ami_2024],color="red", linestyle="--", label="1/3 2024 Monthly AMI")
#     ax.plot([ami_2024, ami_2024],[0, ami_2024],color="red", linestyle="--")

#     # Labels, title, and legend
#     ax.set_xlabel(f"{town} with Program")
#     ax.set_ylabel(f"{town} without Program")
#     ax.set_title(f"Mortgage Payments for {town}")
#     ax.legend()
#     return plt
def plot_equality_graph(df, town):
    fig = go.Figure()

    # Add scatter points for each year with unique colors
    colors = ["green", "darkgreen", "forestgreen", "mediumseagreen", "mediumturquoise", 
              "darkcyan", "steelblue", "dodgerblue", "blue"]
    for year, color in zip(range(2016, 2025), colors):
        yearly_data = df[df['year'] == year]
        fig.add_trace(
            go.Scatter(
                x=yearly_data[f"{town}_MRRP"],
                y=yearly_data[f"{town}_CL"],
                mode='markers',
                marker=dict(color=color, size=8),
                name=f"{year}",
                showlegend=False, 
                hovertemplate=(
                    f"year: {year}<br>"
                    "w/ program: %{x:$,.2f}<br>"
                    "w/o program: %{y:$,.2f}<extra></extra>"
                )
                
            )
        )

    # Add 45-degree reference line
    fig.add_trace(
        go.Scatter(
            x=[0, 10000],
            y=[0, 10000],
            mode='lines',
            line=dict(color="gray", dash="dash"),
            name="45-degree line",
            hoverinfo="skip"
        )
    )

    # Add AMI lines for 2016
    ami_2016 = df[df['year'] == 2016]['AMI'].mean() / 36
    fig.add_trace(
        go.Scatter(
            x=[0, ami_2016],
            y=[ami_2016, ami_2016],
            mode='lines',
            line=dict(color="orange", dash="dash"),
            name="1/3 2016 Monthly AMI",
            hoverinfo="skip"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[ami_2016, ami_2016],
            y=[0, ami_2016],
            mode='lines',
            line=dict(color="orange", dash="dash"),
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Add AMI lines for 2024
    ami_2024 = df[df['year'] == 2024]['AMI'].mean() / 36
    fig.add_trace(
        go.Scatter(
            x=[0, ami_2024],
            y=[ami_2024, ami_2024],
            mode='lines',
            line=dict(color="red", dash="dash"),
            name="1/3 2024 Monthly AMI",
            hoverinfo="skip"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[ami_2024, ami_2024],
            y=[0, ami_2024],
            mode='lines',
            line=dict(color="red", dash="dash"),
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Mortgage Payments for {town}",
        xaxis=dict(title=f"{town} with Program"),
        yaxis=dict(title=f"{town} without Program"),
        legend=dict(bgcolor="rgba(255,255,255,0)"),
        template="plotly_white",
        hovermode="closest"
    )

    return fig