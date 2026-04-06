import polars as pl
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import plotly.express as px
import plotly.io as pio


def discover_topics():
    #load data and take 5000 random samples
    path = r"data\dblp_parquet\dblp_data_2015_plus.parquet"
    df = pl.read_parquet(path).sample(5000, seed=42)
    
    # generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df["title"].to_list(), show_progress_bar=True)

    #clustering n=3 basaed on elblow method
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    df = df.with_columns(cluster_id = pl.Series(kmeans.fit_predict(embeddings)))

    #t-SNE 
    tsne = TSNE(n_components=2, perplexity=30, random_state=42, init='pca')
    coords = tsne.fit_transform(embeddings)
    df = df.with_columns(x = coords[:, 0], y = coords[:, 1])

    # chart
    fig = px.scatter(
        df.to_pandas(), x="x", y="y", color="cluster_id",
        hover_data=["title", "venue"], 
        title="Full t-SNE Topic Map (5000 papers)",
        template="plotly_white"
    )
    pio.write_json(fig, 'static_charts/topics_tsne_full.json')

    # df
    samples_df = (
        df.group_by("cluster_id")
        .head(10)
        .sort("cluster_id")
        .select(["cluster_id", "title", "year", "venue"])
    )
    
    samples_df.write_csv('static_charts/topic_samples.csv')

discover_topics()