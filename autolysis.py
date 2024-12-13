# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "matplotlib",
#   "seaborn",
#   "requests",
#   "chardet",
#   "opencv-python",
#   "scikit-learn",
#   "scipy"
# ]
# ///

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, linregress
import requests
import chardet

# Load AIPROXY_TOKEN from the environment variable
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

if not AIPROXY_TOKEN:
    print("Error: AIPROXY_TOKEN environment variable is not set.")
    exit(1)

def handle_arguments():
    """Handle command-line arguments."""
    import argparse
    parser = argparse.ArgumentParser(description="Analyze and visualize dataset.")
    parser.add_argument("dataset", help="Path to the dataset (CSV file).")
    parser.add_argument("--images", help="Path to the folder with images for vision analysis.", default=None)
    return parser.parse_args()

def load_dataset(filepath):
    """Load a dataset from the specified filepath with encoding detection."""
    try:
        with open(filepath, 'rb') as file:
            raw_data = file.read()
            detected_encoding = chardet.detect(raw_data)['encoding']

        data = pd.read_csv(filepath, encoding=detected_encoding)
        print(f"Dataset loaded with shape: {data.shape} and encoding: {detected_encoding}")
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        exit(1)

def perform_basic_analysis(data):
    """Perform basic analysis of the dataset."""
    description = data.describe(include='all')
    missing_values = data.isnull().sum()
    print("Basic Analysis Completed")
    return {"description": description, "missing_values": missing_values}

def perform_advanced_analysis(data):
    """Perform advanced statistical analysis."""
    numeric_data = data.select_dtypes(include=['number'])
    analysis_results = {}

    if numeric_data.shape[1] >= 2:
        col1, col2 = numeric_data.columns[:2]
        t_stat, p_val = ttest_ind(data[col1].dropna(), data[col2].dropna())
        analysis_results["t_test"] = {"t_stat": t_stat, "p_value": p_val}

        slope, intercept, r_value, p_value, std_err = linregress(data[col1], data[col2])
        analysis_results["regression"] = {
            "slope": slope, "intercept": intercept, "r_value": r_value,
            "p_value": p_value, "std_err": std_err
        }
    return analysis_results

def generate_visualizations(data, folder_name):
    """Generate visualizations for numeric columns and save them."""
    numeric_data = data.select_dtypes(include=['number'])

    if not numeric_data.empty:
        for column in numeric_data.columns:
            plt.hist(data[column].dropna(), bins=30, alpha=0.7, label=column)
            plt.title(f"Histogram for {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.legend()
            hist_file = os.path.join(folder_name, f"{column}_histogram.png")
            plt.savefig(hist_file)
            plt.close()
            print(f"Saved: {hist_file}")

        correlation_matrix = numeric_data.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Matrix")
        corr_file = os.path.join(folder_name, "correlation_matrix.png")
        plt.savefig(corr_file)
        plt.close()
        print(f"Saved: {corr_file}")
    else:
        print("No numeric data available for visualizations.")

def dynamic_prompt(data):
    """Generate a dynamic prompt for OpenAI summarization."""
    column_info = ", ".join(data.columns)
    return f"Analyze a dataset with columns: {column_info}. Provide insights, limitations, and recommendations."

def narrate_results(summary_text):
    """Generate a narrative using OpenAI via proxy."""
    try:
        url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": f"Summarize: {summary_text}"}]
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error during API call: {e}")
        return None

def create_readme(analysis_results, folder_name, ai_summary):
    """Generate a README file summarizing the analysis."""
    readme_content = "# Dataset Analysis Report\n\n"
    readme_content += "## Summary\n\n"
    readme_content += ai_summary + "\n\n"
    readme_content += "## Basic Statistics\n\n"
    readme_content += str(analysis_results["description"]) + "\n\n"
    readme_content += "## Missing Values\n\n"
    readme_content += str(analysis_results["missing_values"]) + "\n\n"
    readme_path = os.path.join(folder_name, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write(readme_content)
    print(f"README generated at: {readme_path}")

def main():
    args = handle_arguments()

    data = load_dataset(args.dataset)

    folder_name = os.path.splitext(os.path.basename(args.dataset))[0]
    os.makedirs(folder_name, exist_ok=True)

    basic_results = perform_basic_analysis(data)
    advanced_results = perform_advanced_analysis(data)
    print("Advanced Analysis:", advanced_results)

    generate_visualizations(data, folder_name)

    prompt_text = dynamic_prompt(data)
    ai_summary = narrate_results(prompt_text)

    create_readme(basic_results, folder_name, ai_summary)

if __name__ == "__main__":
    main()
