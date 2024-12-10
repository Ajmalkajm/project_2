# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "matplotlib",
#   "seaborn",
#   "openai",
#   "requests", 
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai
import requests

# Load AIPROXY_TOKEN from the environment variable
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

if not AIPROXY_TOKEN:
    print("Error: AIPROXY_TOKEN environment variable is not set.")
    sys.exit(1)

# Set the proxy URL for OpenAI API
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/"
openai.api_key = AIPROXY_TOKEN

def load_dataset(file_path):
    try:
        data = pd.read_csv(file_path)
        print(f"Loaded dataset with {data.shape[0]} rows and {data.shape[1]} columns.")
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        sys.exit(1)

def perform_analysis(data):
    """
    Perform basic analysis on the dataset.
    """
    analysis_results = {    
        "columns": list(data.columns),
        "info": str(data.info()),  # Save as string because `data.info()` prints directly
        "description": data.describe(include='all').to_dict()
    }

    # Only include numeric columns for correlation
    numeric_data = data.select_dtypes(include=['number'])
    analysis_results["correlation"] = numeric_data.corr().to_dict()

    return analysis_results

def narrate_results(summary_text):
    """
    Generate a narrative from the summary of the analysis using OpenAI's GPT model through AI Proxy.
    """
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
    payload = {
        "model": "gpt-4o-mini",  # Ensure you use the model supported by AI Proxy
        "messages": [{"role": "user", "content": f"Summarize this analysis: {summary_text}"}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return None
    except KeyError:
        print("Unexpected response format from API:", response.text)
        return None

def create_polished_readme(analysis_results, folder_name, ai_summary=None):
    """
    Create a polished README.md file with professional formatting.
    """
    readme_content = (
        f"# Dataset Analysis\n\n"
        f"## Overview\n\n"
        f"This dataset contains information on various attributes, including:\n\n"
    )

    # Organize columns into categories (example categories, adjust based on actual columns)
    readme_content += "### Columns\n\n"
    readme_content += "1. **Identifiers**: Includes unique IDs and other metadata.\n"
    readme_content += "2. **Details**: Information about main attributes.\n"
    readme_content += "3. **Statistics**: Metrics like average ratings and counts.\n\n"

    readme_content += f"### Dataset Information\n\n"
    readme_content += f"```\n{analysis_results['info']}\n```\n\n"

    readme_content += f"### Statistical Description\n\n"
    readme_content += (
        f"Below is a statistical summary of the dataset's numeric columns:\n\n"
        f"```\n{analysis_results['description']}\n```\n\n"
    )

    readme_content += (
        f"### Correlation Matrix\n\n"
        f"Numeric columns were analyzed for correlation. "
        f"Refer to the `correlation_matrix.png` for the detailed heatmap.\n\n"
    )

    if ai_summary:
        readme_content += (
            f"### AI-Generated Summary\n\n"
            f"{ai_summary}\n\n"
        )

    # Save README.md in the folder
    readme_file = os.path.join(folder_name, "README.md")
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    print(f"Saved polished README: {readme_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze and visualize dataset.")
    parser.add_argument("dataset", help="Path to the dataset (CSV file).")
    args = parser.parse_args()

    # Load dataset
    data = load_dataset(args.dataset)

    # Perform analysis
    analysis_results = perform_analysis(data)

    # Create folder based on the dataset's name (without extension)
    folder_name = os.path.splitext(os.path.basename(args.dataset))[0]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")

    # Create AI summary
    ai_summary = narrate_results(str(analysis_results['description']))

    # Generate polished README and save it in the folder
    create_polished_readme(analysis_results, folder_name, ai_summary)

if __name__ == "__main__":
    main()