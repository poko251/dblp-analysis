import gzip
from lxml import etree
import pyarrow as pa
import pyarrow.parquet as pq

"""Based on DBLP guidelines, only a subset of paper types was included in this analysis. Citation data and external URLs were omitted as many are behind paywalls, making them inaccessible for scraping."""

# config
XML_FILE = 'source/dblp.xml.gz'
OUT_FILE = 'dblp_data_2015_plus.parquet'
LIMIT_YEAR = 2015

# schema
SCHEMA = pa.schema([
    ('key', pa.string()),
    ('type', pa.string()),
    ('title', pa.string()),
    ('year', pa.int32()),
    ('venue', pa.string()),
    ('authors', pa.list_(pa.string()))
])

def run():
    tags = {'article', 'inproceedings', 'proceedings', 'book', 'phdthesis', 'mastersthesis'}
    batch = []
    writer = pq.ParquetWriter(OUT_FILE, SCHEMA)

    # open and parse XML
    with gzip.open(XML_FILE, 'rb') as f:
        context = etree.iterparse(f, events=('end',), load_dtd=True)
        
        for _, elem in context:
            if elem.tag in tags:
                year = int(elem.findtext('year') or 0)
                
                if year >= LIMIT_YEAR:
                    # collect record
                    batch.append({
                        'key': elem.get('key'),
                        'type': elem.tag,
                        'title': elem.findtext('title'),
                        'year': year,
                        'venue': elem.findtext('journal') or elem.findtext('booktitle') or "",
                        'authors': [a.text for a in elem.findall('author') if a.text]
                    })

                # write batch to file
                if len(batch) >= 50000:
                    writer.write_table(pa.Table.from_pylist(batch, SCHEMA))
                    batch = []
                    print("saved 50k records")

            # memory cleanup
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        # save remaining records
        if batch:
            writer.write_table(pa.Table.from_pylist(batch, SCHEMA))
    
    writer.close()

if __name__ == "__main__":
    run()