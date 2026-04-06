import polars as pl
import plotly.express as px
import plotly.io as pio


# creates charts based on neo4j_data exported from neo4j aura


def chart_coauthors_ranking():
    # load data
    df = pl.read_csv('neo4j_data/co-authors_ammount.csv')
    top_10 = df.head(10).to_pandas()
    
    fig = px.bar(
        top_10, x='degree', y='author', orientation='h',
        title="Top 10 Authors by Co-author Count",
        labels={'degree': 'Co-authors Count', 'author': 'Author'},
        color='degree', color_continuous_scale='Blues', template="plotly_white"
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    
    pio.write_json(fig, 'static_charts/top_coauthors_ranking.json')

def chart_degree_distribution():
    df = pl.read_csv('neo4j_data/degree_distribution.csv').to_pandas()
    
    fig = px.bar(
        df, x='degree', y='count_of_authors',
        title="Node Degree Distribution",
        labels={'degree': 'Degree', 'count_of_authors': 'Authors Count'},
        template="plotly_white", log_y=True
    )
    
    pio.write_json(fig, 'static_charts/degree_distribution.json')

def chart_top_duets():
    df = pl.read_csv('neo4j_data/top_duets.csv')
    top_10_pairs = df.head(10).to_pandas()
    
    fig = px.bar(
        top_10_pairs, x='common_papers', y='pair', orientation='h',
        title="Top 10 Strongest Collaborations (Duets)",
        labels={'common_papers': 'Common Papers', 'pair': 'Author Pair'},
        color='common_papers', color_continuous_scale='Reds', template="plotly_white"
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    
    pio.write_json(fig, 'static_charts/top_duets_ranking.json')



def chart_degree_distribution_loglog():
    df = pl.read_csv('neo4j_data/degree_distribution.csv').to_pandas()
    

    fig = px.scatter(
        df, 
        x='degree', 
        y='count_of_authors',
        title="Degree Distribution (Log-Log Scale)",
        labels={'degree': 'Degree (log scale)', 'count_of_authors': 'Authors Count (log scale)'},
        template="plotly_white",
        log_x=True,
        log_y=True  
    )
    
    fig.update_traces(marker=dict(size=8, color='royalblue', opacity=0.6))

    pio.write_json(fig, 'static_charts/degree_distribution_loglog.json')

chart_coauthors_ranking()
chart_degree_distribution()
chart_top_duets()
chart_degree_distribution_loglog()