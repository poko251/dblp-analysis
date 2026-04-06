# DBLP Dataset Analysis - Nokia Recruitment Task

## Online Version
* The dashboard is deployed  at: [https://dblp-analysis-5h6advevp2rwfctanljx53.streamlit.app/](https://dblp-analysis-5h6advevp2rwfctanljx53.streamlit.app/)

## Project Overview
This project was developed as a recruitment task for Nokia. It provides an exploratory analysis of the DBLP  dataset.

The analysis includes:
* **Exploratory Data Analysis:** General statistics on publication types, trends, and top research venues.
* **Co-authorship Network Analysis:** Analysis of collaboration patterns conducted using **Neo4j Aura**. 
* **Topic Clustering:** Titles were processed using **Sentence Transformers (SBERT)** to create embeddings, then grouped via K-Means and visualized with t-SNE.
* **Search:** Uses the Gemini API to convert English queries into Polars code for data filtering.

## Tech Stack
* **Data Processing:** Polars, Pandas
* **Graph Database:** Neo4j Aura 
* **AI/ML:** Sentence Transformers (`all-MiniLM-L6-v2`), Scikit-learn, Google GenAI
* **Visualization:** Plotly, t-SNE
* **Dashboard:** Streamlit

## How to Run Analysis
1. Clone the repository
2. pip install -r requirements.txt
3. streamlit run dashboard/main.py

## How to run search

1. Download DBLP and place it into source/ directory
2. Run
```text
python src/convert_to_parquet.py
```
3. Create a .env file in the root directory
4. Add your Google Gemini API key
```text
GEMINI_API_KEY=your_api_key_here
```
5. In search/ai_search.py type your query and run it.


## Project Structure
```text
dblp
 ┣ dashboard
 ┃ ┗ main.py                  # Main streamlit dashboard script
 ┣ data                       # Parquet files (Too large for GitHub)
 ┃ ┗ dblp_parquet 
 ┃ ┃ ┣ dblp_data.parquet
 ┃ ┃ ┗ dblp_data_2015_plus.parquet
 ┣ neo4j_data                 # Data exports from Neo4j Aura analysis
 ┃ ┣ co-authors_ammount.csv
 ┃ ┣ degree_distribution.csv
 ┃ ┣ edges_for_aura.csv
 ┃ ┣ graph-export.csv
 ┃ ┣ nodes_for_aura.csv
 ┃ ┗ top_duets.csv
 ┣ source                     # Original XML source files
 ┃ ┣ dblp.dtd
 ┃ ┗ dblp.xml.gz
 ┣ src 
 ┃ ┣ clustering               # Scripts for topic modeling and elbow method
 ┃ ┃ ┣ clustering.py
 ┃ ┃ ┗ elbow.py
 ┃ ┣ generate_charts          # Scripts used to generate JSON visualizations
 ┃ ┃ ┣ 2015_2025_charts.py
 ┃ ┃ ┣ graph.py
 ┃ ┃ ┗ neo4j_charts.py
 ┃ ┣ graph_edges_nodes 
 ┃ ┃ ┗ export_to_aura.py      # Script to prepare CSVs for Neo4j
 ┃ ┣ search
 ┃ ┃ ┗ ai_search.py           # Gemini AI search logic 
 ┃ ┣ analysis.ipynb           # Initial Jupyter notebook analysis
 ┃ ┗ convert_to_parquet.py    # XML to Parquet conversion 
 ┣ static_charts              # JSON charts for the dashboard
 ┣ .env                       # API Key
 ┣ .gitignore
 ┣ README.md
 ┗ requirements.txt
```