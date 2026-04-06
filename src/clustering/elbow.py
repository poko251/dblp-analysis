import polars as pl
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.io as pio

# using elbow methos  i want to check how may clusster do i need


def find_optimal_k():
    path = r"data\dblp_parquet\dblp_data_2015_plus.parquet"
    df = pl.read_parquet(path).sample(3000, seed=42) # smaller sample for speed
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df["title"].to_list(), show_progress_bar=True)

    # calculate for k from 1 to 10
    inertia_values = []
    k_range = range(1, 11)

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
        kmeans.fit(embeddings)
        inertia_values.append(kmeans.inertia_)

    # plot
    elbow_data = pl.DataFrame({
        "k": list(k_range),
        "inertia": inertia_values
    })

    fig = px.line(
        elbow_data.to_pandas(), x="k", y="inertia", 
        title="Elbow Method for Optimal K",
        markers=True,
        labels={"k": "Number of Clusters (k)", "inertia": "Inertia"},
        template="plotly_white"
    )

    pio.write_json(fig, 'static_charts/elbow_method.json')

find_optimal_k()