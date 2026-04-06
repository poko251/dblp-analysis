import polars as pl
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


# creates charts based on 2015_plus dataset


def chart_publications_trend(df):
    # filtering
    data = df.filter((pl.col("year") >= 2015) & (pl.col("year") <= 2026))
    trend = data.group_by("year").len().sort("year").to_pandas()
    
    trend['year'] = trend['year'].astype(str)
    
    fig = px.bar(
        trend, 
        x='year', 
        y='len', 
        title="Annual Publication Trend (2015-2026)",
        labels={'year': 'Year', 'len': 'Count'},
        color='len', 
        color_continuous_scale='Viridis',
        orientation='v' 
    )
    
    fig.add_trace(go.Scatter(
        x=trend['year'], 
        y=trend['len'], 
        mode='lines+markers', 
        name='Trend',
        line=dict(color='red', width=2)
    ))
    
    pio.write_json(fig, 'static_charts/publications_trend.json')

def chart_type_comparison(df):
    data = df.filter(
        (pl.col("year") >= 2015) & (pl.col("year") <= 2026) & 
        (pl.col("type").is_in(['article', 'inproceedings']))
    )
    
    grouped = data.group_by(["year", "type"]).len().sort("year").to_pandas()
    
    grouped['year'] = grouped['year'].astype(str)
    
    fig = px.bar(
        grouped, 
        x='year', 
        y='len', 
        color='type',
        barmode='group', 
        title="Conferences vs Journals (2015-2026)",
        labels={'year': 'Year', 'len': 'Count', 'type': 'Type'},
        color_discrete_map={'article': '#2ecc71', 'inproceedings': '#3498db'},
        template="plotly_white",
        orientation='v'
    )
    
    pio.write_json(fig, 'static_charts/type_comparison_bar.json')

def chart_team_evolution(df):
    # calculate authors count and average per year
    evolution = (
        df.with_columns(auth_count = pl.col("authors").list.len())
        .group_by("year")
        .agg(pl.col("auth_count").mean().alias("avg_authors"))
        .sort("year")
    )
    
    fig = px.line(
        evolution.to_pandas(), x='year', y='avg_authors', markers=True,
        title="Average Team Size Evolution (2015-2026)",
        labels={'year': 'Year', 'avg_authors': 'Avg Authors Count'},
        template="plotly_white"
    )
    fig.update_traces(line=dict(color='firebrick', width=3))
    
    pio.write_json(fig, 'static_charts/team_evolution_trend.json')

def chart_type_pie_interactive(df):
    fig = go.Figure()
    years = sorted([y for y in df["year"].unique().to_list() if 2015 <= y <= 2026])
    
    # ddd pie chart for each year
    for year in years:
        year_df = df.filter(pl.col("year") == year)
        counts = year_df.group_by("type").len()
        
        fig.add_trace(go.Pie(
            labels=counts["type"].to_list(),
            values=counts["len"].to_list(),
            name=str(year),
            visible=(year == 2024) 
        ))

    # create buttons
    buttons = []
    for i, year in enumerate(years):
        visible = [False] * len(years)
        visible[i] = True
        buttons.append({
            "label": str(year),
            "method": "update",
            "args": [{"visible": visible}, {"title": f"Publication Types in {year}"}]
        })

    fig.update_layout(
        updatemenus=[{"buttons": buttons, "direction": "down", "x": 0, "y": 1.15}],
        title="Publication Type Distribution (Select Year)",
        template="plotly_white"
    )
    pio.write_json(fig, 'static_charts/type_pie_chart.json')

def chart_top_venues(df):
    top_10 = (
        df.group_by("venue").len()
        .rename({"len": "count"})
        .sort("count", descending=True).head(10)
    )
    
    fig = px.bar(
        top_10.to_pandas(), x='count', y='venue', orientation='h',
        title="Top 10 Most Popular Venues (2015-2026)",
        labels={'count': 'Publications', 'venue': 'Venue'},
        color='count', color_continuous_scale='Magma', text='count'
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, template="plotly_white")
    
    pio.write_json(fig, 'static_charts/top_venues.json')


df = pl.read_parquet('data\dblp_parquet\dblp_data_2015_plus.parquet')
    
chart_type_comparison(df)
chart_publications_trend(df)
chart_team_evolution(df)
chart_type_pie_interactive(df)
chart_top_venues(df)
    