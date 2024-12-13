import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot(player_name, data):
    # data preparation
    matches = {
        "Solo": data["solo_mathes"] + data["solo-fpp_mathes"],
        "Duo": data["duo_mathes"] + data["duo-fpp_mathes"],
        "Squad": data["squad_mathes"] + data["squad-fpp_mathes"],
    }

    movement_types = ["Walk", "Swim", "Ride"]
    movement_distances = [data["total_walk"], data["total_swim"], data["total_ride"]]

    kills_data = {
        "Category": ["Kills", "Assists", "Headshots"],
        "Values": [data["total_kills"], data["total_assists"], data["total_headshots"]],
    }

    match_stats = {
        "Category": ["Top 10", "Wins", "Other Matches"],
        "Values": [
            data["total_top10"],
            data["total_wins"],
            data["total_matches"] - data["total_top10"] - data["total_wins"],
        ],
    }

    # Prepare table data
    total_data = [
        data["total_kills"],
        data["total_assists"],
        data["total_wins"],
        data["total_heals"],
        data["total_boosts"],
        data["total_damage"],
        data["total_walk"] + data["total_swim"] + data["total_ride"],
    ]
    average_data = [
        round(data["total_kills"] / data["total_matches"], 2),
        round(data["total_assists"] / data["total_matches"], 2),
        round(data["total_wins"] / data["total_matches"], 2),
        round(data["total_heals"] / data["total_matches"], 2),
        round(data["total_boosts"] / data["total_matches"], 2),
        round(data['total_damage'] / data["total_matches"], 2),
        round((data["total_walk"] + data["total_swim"] + data["total_ride"]) / data["total_matches"], 2)
    ]

    # Create subplots
    fig = make_subplots(
        rows=3,
        cols=2,
        specs=[
            [{"type": "bar"}, {"type": "pie"}],
            [{"type": "bar"}, {"type": "pie"}],
            [{"type": "table", "colspan": 1}, {"type": "indicator"}],
        ],
        subplot_titles=(
            "Matches Played by Mode",
            "Distance Covered by Movement Type",
            "Kills, Assists, and Headshots Distribution",
            "Match Results (Top 10, Wins, Other)",
            "Total and Average Stats",
            "Longest Kill"
        ),
    )

    # Add bar plot for matches distribution
    fig.add_trace(
        go.Bar(
            x=list(matches.keys()),
            y=list(matches.values()),
            name="Matches Played",
            marker_color="#3d3d3d",  # Google blue
        ),
        row=1,
        col=1,
    )

    # Add pie chart for movement distances
    fig.add_trace(
        go.Pie(
            labels=movement_types,
            values=movement_distances,
            name="Movement Distances",
            marker=dict(colors=["#12752b", "#374b82", "#4f5054"]),
            hole=0.5  # Google colors
        ),
        row=1,
        col=2,
    )

    # Add bar plot for kills, assists, and headshots distribution
    fig.add_trace(
        go.Bar(
            x=kills_data["Category"],
            y=kills_data["Values"],
            name="Kills, Assists, Headshots",
            marker_color="#3d3d3d",  # Google green
        ),
        row=2,
        col=1,
    )

    # Add pie chart for match results (Top 10, Wins, Other)
    fig.add_trace(
        go.Pie(
            labels=match_stats["Category"],
            values=match_stats["Values"],
            name="Match Results",
            marker=dict(colors=["#9e9e9d", "#ffbf00", "#1f1f1f"]),  # Google colors
        ),
        row=2,
        col=2,
    )

    # Add table for Total and Average Stats
    fig.add_trace(
        go.Table(
            header=dict(
                values=["Stats", "Total", "Average"],
                fill_color="#E8EAED",  # Google gray
                align="center",
            ),
            cells=dict(
                values=[
                    ["Kills", "Assists", "Wins", "Heals", "Boosts", "Damage", "Distance"],
                    total_data,
                    average_data,
                ],
                fill_color="#F1F3F4",  # Google lighter gray
                align="center",
            ),
        ),
        row=3,
        col=1,
    )

    # Add indicator for Longest Kill
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=data["longest_kill"],
            title={"text": "Longest Kill (m)"},
            number={"font": {"size": 36, "color": "black"}},
            domain={"x": [0.5, 1], "y": [0, 0.5]},
        ),
        row=3,
        col=2,
    )

    # Update layout
    fig.update_layout(
        height=1000,
        width=1000,
        title_text=f"PUBG Player Dashboard - {player_name}",
        title_font_size=20,
        title_x=0.5,
        showlegend=False,
        font=dict(size=12),
    )

    name = "tmp"
    fig.write_html(name + ".html")
    fig.write_image(name + ".png")
    return name + ".html", name + ".png"

# if __name__ == "__main__":
#     plot(data=DATA)
