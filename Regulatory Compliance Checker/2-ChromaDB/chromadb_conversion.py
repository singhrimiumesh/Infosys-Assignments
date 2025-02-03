import pandas as pd
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
import os
import json

client = PersistentClient(path="./chroma")  

collection = client.get_or_create_collection("contracts")

model = SentenceTransformer("all-MiniLM-L6-v2")

df = pd.read_csv("./Dataset.csv")

output_dir = "./processed_data"
os.makedirs(output_dir, exist_ok=True)

embeddings_file = os.path.join(output_dir, "embeddings.json")

def process_and_upload_to_chromadb(df):
    all_data = []  
    for index, row in df.iterrows():

        d = {
            "category": row["Category"],
            "agreement_date": row["Agreement Date"] if "Agreement Date" in row else "",
            "contract_text": row["contract"],
            "exact_law": row["Exact Law"],
            "description": row["Description"]
        }

        metadata = {col: row[col] for col in df.columns if col not in d}

        embedding = model.encode(d["contract_text"]).tolist() 

        collection.add(
            ids=[f"contract_{index}"],
            metadatas=[metadata],
            embeddings=[embedding],
            documents=[d["contract_text"]]
        )

        formatted_data = {
            "id": f"contract_{index}",
            "formatted_text": (
                f"This is a contract of category {d['category']} with agreement date {d['agreement_date']}. "
                f"It follows laws {d['exact_law']}. Here is the contract text: {d['contract_text']}"
            ),
            "embedding": embedding,
            "metadata": metadata
        }
        all_data.append(formatted_data)

    with open(embeddings_file, "w") as f:
        json.dump(all_data, f, indent=4)
    print(f"Data saved to {embeddings_file}")

if __name__ == "__main__":
    process_and_upload_to_chromadb(df)
