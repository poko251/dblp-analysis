import streamlit as st
import plotly.io as pio
import pandas as pd

st.set_page_config(page_title="DBLP Fast Dashboard", layout="wide")

st.title("DBLP Dashboard")

tab1, tab2, tab3 = st.tabs(["2015-2026 analisys", "Co-authorship Network Analysis", "Title analysis"])

#charts
chart_path = r'static_charts/publications_trend.json'
chart_path2 = r'static_charts/type_pie_chart.json'
chart_path3 = r'static_charts/type_comparison_bar.json'
chart_path4 = r'static_charts/team_evolution_trend.json'
chart_path5 = r'static_charts/top_venues.json'


#graph charts
chart_path6 = r'static_charts/degree_distribution.json'
chart_path7 = r'static_charts/top_coauthors_ranking.json'
chart_path8 = r'static_charts/top_duets_ranking.json'
chart_path9 = r'static_charts/degree_distribution_loglog.json'
chart_path10 = r'static_charts/author_collaboration_graph.json'


#nlp charts
chart_path11 = r'static_charts/topics_tsne_full.json'
chart_path12 = r'static_charts/elbow_method.json'

with tab1:

    st.header("2015-2026 Analysis")
    st.write("Data processed and converted to Parquet (convert_to_parquet.py) for optimized performance. To manage the dataset's size effectively, this study focuses on the last 10 years of global research output. Charts were generated (generate_charts/2015_2025_charts.py) and saved to .json")
    st.write("Based on DBLP guidelines, only a subset of paper types was included in this analysis. Citation data and external URLs were omitted as many are behind paywalls, making them inaccessible for scraping.")

    fig = pio.read_json(chart_path)
    st.plotly_chart(fig, use_container_width=True)
    st.info('This chart illustrates a consistent upward trend in scientific output')

    fig2 = pio.read_json(chart_path2)
    st.plotly_chart(fig2, use_container_width=True)
    st.info('This visualization tracks the ratio between types of publications. While the split between articles and inproceedings was initially even, Articles have become the dominant publication format in the DBLP database.')        

    fig3 = pio.read_json(chart_path3)
    st.plotly_chart(fig3, use_container_width=True)
    st.info('To further investigate the trends seen in the previous chart, I created this comparison, it highlights exactly how and when Articles surpassed Inproceedings in total publication volume.')

    fig4 = pio.read_json(chart_path4)
    st.plotly_chart(fig4, use_container_width=True)
    st.info('The data shows that the average author count per paper has climbed from 3.5 to 4.5')
        
    fig5 = pio.read_json(chart_path5)
    st.plotly_chart(fig5, use_container_width=True)
    st.info('The data shows that CoRR (Computing Research Repository) is the most frequent publication venue.')

with tab2:

    st.header("Co-authorship Network Analysis")
    st.write("This section presents a graph-based analysis using Neo4j Aura. To comply with the free-tier limitations (max. 200,000 nodes and 400,000 relationships), the dataset was specifically filtered to include publications from 2024 onwards across several high-impact venues.")
    st.write("Graph Overview: Nodes (Authors): ~70,000, Relationships: ~370,000. The data transformation and export process were handled by graph_edges_nodes/export_to_aura.py. Following initial processing in Neo4j, the results were exported as CSV files. Final visualizations and network metrics were generated using the generate_charts/neo4j_charts.py and generate_charts/neo4j_graph.py modules.")


    fig6 = pio.read_json(chart_path6)
    st.plotly_chart(fig6, use_container_width=True)
    st.info("The first step in the analysis was examining the degree distribution. The results reveal a clear Power-Law distribution, which is a defining characteristic of scale-free networks.")

    fig9 = pio.read_json(chart_path9)
    st.plotly_chart(fig9, use_container_width=True)
    st.info("By transforming the data to a log-log scale, we can clearly see the points aligning in a straight line. This confirms that our graph follows a Power Law.")

    fig8 = pio.read_json(chart_path8)
    st.plotly_chart(fig8, use_container_width=True)
    st.info("A ranking of the most frequent author pairings in the dataset. This chart highlights the highest edge weights in our graph, revealing which researchers have the most significant collaborative impact together")

    fig7 = pio.read_json(chart_path7)
    st.plotly_chart(fig7, use_container_width=True)
    st.info("This chart displays the researchers with the highest Degree Centrality in the dataset. Yu Qiao 0001 dominates the ranking as the most highly connected node.")
    

    fig10 = pio.read_json(chart_path10)
    st.plotly_chart(fig10, use_container_width=True)
    st.info("Based on the previous chart, I crated a graph. There's Yu Qiao 0001 and his co-authors. (It's better to zoom-in).")

with tab3:
    
    st.header("Title Analysis: Semantic Topic Discovery")
    st.write("The process began with the Elbow Method to determine the optimal number of clusters (k=3). I then used Sentence-Transformers (SBERT) to convert titles into vectors, which were grouped using K-Means. Finally, the t-SNE algorithm was applied to project these relationships into a 2D plot. Representative samples from each group are provided below the visualization. Files are in (clustering/clustering.py) and (clustering/elbow.py)")

    
    fig12 = pio.read_json(chart_path12)
    st.plotly_chart(fig12, use_container_width=True)
    st.info("Elbow method to detemine number of clusters.")

    fig11 = pio.read_json(chart_path11)
    st.plotly_chart(fig11, use_container_width=True)
    st.info("Chart shows 3 clusters of topics.")

    df = pd.read_csv(r'static_charts/topic_samples.csv')
    st.dataframe(df)

