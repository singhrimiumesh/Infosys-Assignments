**Contract Law Extraction Script**

This Python script processes a dataset containing contract data and extracts the exact law and a brief description of each contract using the Groq API. The script follows these steps:

**Load the Dataset**: Reads the dataset.csv file into a Pandas DataFrame and ensures the necessary columns (Exact Law and Description) exist.

**API Integration**: Uses the Groq API to analyze each contract and determine the exact legal reference and a short description.

**Handling API Rate Limits**: Implements a retry mechanism to handle rate limit errors by waiting before retrying requests.

**Data Processing**: Iterates through each row in the dataset, sends contract text to the API, and updates the DataFrame with extracted legal details.

**Save Updated Data**: The processed dataset is saved as Dataset.csv, ensuring the extracted legal insights are stored for further analysis.
