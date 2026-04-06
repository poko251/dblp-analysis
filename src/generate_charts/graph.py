import polars as pl
import networkx as nx
import plotly.graph_objects as go
import plotly.io as pio
#creates graph based on neo4j data

def generate_ego_network_graph():
    df = pl.read_csv("neo4j_data/graph-export.csv")
    
    # define center
    center = "Yu Qiao 0001"

    # filter relationships for the chosen author
    f = df.filter(
        (pl.col("~relationship_type") == "CO_AUTHORED_WITH") & 
        ((pl.col("~start_node_property_name") == center) | (pl.col("~end_node_property_name") == center))
    )

    # build graph
    G = nx.Graph()
    for r in f.iter_rows(named=True):
        G.add_edge(r["~start_node_property_name"], r["~end_node_property_name"], weight=float(r["~relationship_property_weight"]))

    # calculate layout
    pos = nx.spring_layout(G, k=1.0)

    #  edges
    edge_x, edge_y = [], []
    for u, v in G.edges():
        edge_x += [pos[u][0], pos[v][0], None]
        edge_y += [pos[u][1], pos[v][1], None]

    # nodes 
    nx_coords = [pos[n] for n in G.nodes()]
    node_styles = [("#e74c3c", 40) if n == center else ("#3498db", 15) for n in G.nodes()]
    colors, sizes = zip(*node_styles)

    # traces
    traces = [
        go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), mode='lines', hoverinfo='none'),
        go.Scatter(
            x=[c[0] for c in nx_coords], y=[c[1] for c in nx_coords], 
            text=list(G.nodes()), mode='markers+text', textposition="top center",
            marker=dict(color=colors, size=sizes, line_width=2, line_color='white')
        )
    ]

    # figure
    fig = go.Figure(data=traces, layout=go.Layout(
        title=f"Network: {center}", template="plotly_white", showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    ))

    pio.write_json(fig, 'static_charts/author_collaboration_graph.json')

generate_ego_network_graph()