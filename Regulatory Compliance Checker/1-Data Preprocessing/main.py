import pandas as pd
import requests
import json
import time

# Load the dataset
file_path = '/content/dataset.csv'
data = pd.read_csv(file_path)

data['Exact Law'] = data['Exact Law'].astype('object') if 'Exact Law' in data else ''
data['Description'] = data['Description'].astype('object') if 'Description' in data else ''

GROQ_API_KEY = "gsk_nTHIjW2I5ozEvA0kKl7oWGdyb3FY5Fe8RIXPCd9ep3idnKUMraiSmoir"

def get_exact_law_and_description(contract_text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a contract analyser, given a contract data you have to find out the Exact law of the contract "
                    "it belongs to and short description of the same. Output format: \nExact Law: ... \nDescription: ..."
                )
            },
            {"role": "user", "content": contract_text}
        ],
        "model": "llama3-8b-8192",
        "temperature": 1,
        "max_completion_tokens": 4000,
        "top_p": 1,
        "stream": False,
        "stop": None
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))  
        print(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)
        return get_exact_law_and_description(contract_text)  
    if response.status_code == 200:
        content = response.json()
        message = content.get("choices", [{}])[0].get("message", {}).get("content", "")
        exact_law = ""
        description = ""
        if "Exact Law:" in message and "Description:" in message:
            exact_law = message.split("Exact Law:")[1].split("Description:")[0].strip()
            description = message.split("Description:")[1].strip()
        return exact_law, description
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None

# Process each row in the dataset
for index, row in data.iterrows():
    contract_text = row['contract']
    if pd.notnull(contract_text):
        print(f"Processing row {index + 1}...")
        exact_law, description = get_exact_law_and_description(contract_text)

        data.at[index, 'Exact Law'] = exact_law
        data.at[index, 'Description'] = description
        time.sleep(1)  

output_file = 'Dataset.csv'
data.to_csv(output_file, index=False)
print(f"Updated dataset saved to {output_file}")
