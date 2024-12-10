# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "matplotlib",
#   "seaborn",
#   "openai",
#   "requests",
#   "chardet"
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai
import requests
import chardet  # Added for encoding detection

# Load AIPROXY_TOKEN from the environment variable
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

if not AIPROXY_TOKEN:
    print("Error: AIPROXY_TOKEN environment variable is not set.")
    sys.exit(1)

# Set the proxy URL for OpenAI API
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/"
openai.api_key = AIPROXY_TOKEN

def detect_encoding(file_path):
    """
    Detect the encoding of the file using chardet.
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result.get("encoding", "utf-8")

def load_dataset(file_path):
    """
    Load a dataset, handling encoding issues automatically.
    """
    try:
        # Detect encoding of the file
        encoding = detect_encoding(file_path)
        print(f"Detected file encoding: {encoding}")
        
        # Load the dataset using the detected encoding
        data = pd.read_csv(file_path, encoding=encoding)
        print(f"Loaded dataset with {data.shape[0]} rows and {data.shape[1]} columns.")
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        sys.exit(1)

# Other functions remain unchanged

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

    # Add further analysis as needed
    return analysis_results

def visualize_data(data, folder_name):
    """
    Visualize data and save plots.
    """
    try:
        # Correlation matrix heatmap (only for numeric data)
        numeric_data = data.select_dtypes(include=['number'])
        if not numeric_data.empty:
            correlation_matrix = numeric_data.corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
            plt.title("Correlation Matrix")
            correlation_file = os.path.join(folder_name, "correlation_matrix.png")
            plt.savefig(correlation_file)
            plt.close()
            print(f"Saved: {correlation_file}")
        
        # Visualize histograms for numeric columns
        numeric_columns = data.select_dtypes(include=['number']).columns
        for column in numeric_columns:
            plt.hist(data[column].dropna(), bins=30)
            plt.title(f"Histogram for {column}")
            hist_file = os.path.join(folder_name, f"{column}_histogram.png")
            plt.savefig(hist_file)
            plt.close()
            print(f"Saved: {hist_file}")
    except Exception as e:
        print(f"Error during visualization: {e}")

def create_readme(analysis_results, folder_name, ai_summary=None):
    """
    Create a polished README.md file with dataset details.
    """
    readme_content = f"# Dataset Analysis\n\n"
    readme_content += f"## Overview\n\n"
    readme_content += f"Columns:\n"
    for column in analysis_results["columns"]:
        readme_content += f"- {column}\n"
    readme_content += f"\n## Dataset Information\n\n"
    readme_content += f"```\n{analysis_results['info']}\n```\n\n"
    readme_content += f"## Statistical Description\n\n"
    readme_content += f"```\n{analysis_results['description']}\n```\n\n"
    readme_content += f"## Correlation Matrix\n\nSee the `correlation_matrix.png` file.\n\n"

    if ai_summary:
        readme_content += f"## AI Summary\n\n{ai_summary}\n"

    # Save README.md in the folder
    readme_file = os.path.join(folder_name, "README.md")
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    print(f"Saved: {readme_file}")

def narrate_results(summary_text):
    """
    Generate a narrative using OpenAI's GPT model via AI Proxy.
    """
    try:
        url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": f"Summarize this analysis: {summary_text}"}]
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error during API call: {e}")
        return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze and visualize dataset.")
    parser.add_argument("dataset", help="Path to the dataset (CSV file).")
    args = parser.parse_args()

    # Load dataset
    data = load_dataset(args.dataset)

    # Perform analysis
    analysis_results = perform_analysis(data)

    # Create folder for outputs
    folder_name = os.path.splitext(os.path.basename(args.dataset))[0]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # Visualize data
    visualize_data(data, folder_name)

    # AI-generated summary
    ai_summary = narrate_results(str(analysis_results['description']))

    # Create README.md
    create_readme(analysis_results, folder_name, ai_summary)

if __name__ == "__main__":
    main()