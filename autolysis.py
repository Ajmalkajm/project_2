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

    # Add further analysis as needed
    return analysis_results

def visualize_data(data, folder_name):
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
    Create a README.md file with basic dataset analysis information and AI summary.
    """
    readme_content = f"# Dataset Analysis\n\n"
    readme_content += f"## Dataset Overview\n\n"
    readme_content += f"Columns: {', '.join(analysis_results['columns'])}\n\n"
    readme_content += f"## Dataset Information\n\n"
    readme_content += f"```\n{analysis_results['info']}\n```\n\n"
    readme_content += f"## Statistical Description\n\n"
    readme_content += f"```\n{analysis_results['description']}\n```\n\n"
    readme_content += f"## Correlation Matrix\n\nSee the `correlation_matrix.png` file for a visual representation of correlations between numeric columns.\n\n"

    # Add links to saved images (histograms for numeric columns)
    readme_content += f"## Histograms\n\n"
    numeric_columns = [column for column in analysis_results['description'].keys() if isinstance(analysis_results['description'].get(column, {}).get('mean'), (int, float))]
    for column in numeric_columns:
        readme_content += f"See the histogram for {column}: `{column}_histogram.png`\n"

    # Add AI Summary if provided
    if ai_summary:
        readme_content += f"\n## AI-Generated Summary\n\n{ai_summary}\n"

    # Save README.md in the folder
    readme_file = os.path.join(folder_name, "README.md")
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    print(f"Saved: {readme_file}")

def narrate_results(summary_text):
    """
    Generate a narrative from the summary of the analysis using OpenAI's GPT model through AI Proxy.
    """
    api_key = os.getenv("AIPROXY_TOKEN")
    if not api_key:
        print("Error: AIPROXY_TOKEN environment variable is not set.")
        return None

    # Using the AI Proxy endpoint
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "model": "gpt-4o-mini",  # Ensure you use the model supported by AI Proxy
        "messages": [{"role": "user", "content": f"Summarize this analysis: {summary_text}"}]
    }

    try:
        # Make the API call using requests.post
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        result = response.json()
        print("AI Response:", result)
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return None
    except KeyError:
        print("Unexpected response format from API:", response.text)
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

    # Create folder based on the dataset's name (without extension)
    folder_name = os.path.splitext(os.path.basename(args.dataset))[0]
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")
    
    # Visualize data and save the figures in the folder
    visualize_data(data, folder_name)

    # Create AI summary
    ai_summary = narrate_results(str(analysis_results['description']))

    # Create README.md and save it in the folder
    create_readme(analysis_results, folder_name, ai_summary)

if __name__ == "__main__":
    main()
