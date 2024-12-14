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
    """Generate and save visualizations for numeric columns."""
    numeric_data = data.select_dtypes(include=['number'])

    if not numeric_data.empty:
        # Histogram for each numeric column
        for column in numeric_data.columns:
            plt.figure(figsize=(8, 6))
            sns.histplot(data[column].dropna(), kde=True, bins=30, color="blue", alpha=0.7)
            plt.title(f"Distribution of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            hist_file = os.path.join(folder_name, f"{column}_histogram.png")
            plt.savefig(hist_file)
            plt.close()
            print(f"Saved: {hist_file}")

        # Pairplot for relationships
        pairplot_file = os.path.join(folder_name, "pairplot.png")
        sns.pairplot(numeric_data)
        plt.savefig(pairplot_file)
        plt.close()
        print(f"Saved: {pairplot_file}")

        # Correlation heatmap
        correlation_matrix = numeric_data.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
        plt.title("Correlation Heatmap")
        corr_file = os.path.join(folder_name, "correlation_heatmap.png")
        plt.savefig(corr_file)
        plt.close()
        print(f"Saved: {corr_file}")
    else:
        print("No numeric data available for visualizations.")

def dynamic_prompt(data):
    """Generate a context-rich prompt for OpenAI summarization."""
    num_rows, num_columns = data.shape
    column_info = ", ".join(data.columns)

    return (
        "You are an expert data analyst. "
        "Analyze the dataset based on the following information: "
        f"The dataset contains {num_rows} rows and {num_columns} columns with fields: {column_info}. "
        "Your task is to summarize key insights including:\n"
        "- Patterns and trends in the data.\n"
        "- Relationships and correlations among variables.\n"
        "- Data quality issues such as missing values or outliers.\n"
        "- Recommendations for next steps and practical applications.\n\n"
        "Ensure the summary is concise, professional, and actionable for decision-making."
    )

def narrate_results(summary_text):
    """Generate a narrative using OpenAI via proxy."""
    try:
        url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": summary_text}]
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error during API call: {e}")
        return None

def create_readme(analysis_results, folder_name, ai_summary):
    """Generate a well-structured README file summarizing the analysis."""
    readme_content = (
        "# Dataset Analysis Report\n\n"
        "## Summary\n\n"
        f"{ai_summary}\n\n"
        "## Basic Statistics\n\n"
        "### Dataset Description\n"
        f"```\n{analysis_results['description']}\n```\n\n"
        "### Missing Values\n"
        f"```\n{analysis_results['missing_values']}\n```\n\n"
        "## Visualizations\n\n"
        "- **Histograms**: Distribution of numeric columns.\n"
        "- **Pairplot**: Relationships between variables.\n"
        "- **Correlation Heatmap**: Visualizes correlations among numeric columns.\n\n"
        "### PNG Files\n"
        "All visualizations are saved in the folder: `{folder_name}`.\n"
    )

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