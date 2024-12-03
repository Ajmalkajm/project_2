# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "matplotlib",
#     "seaborn",
#     "httpx",
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import httpx

# Ensure AIPROXY_TOKEN is set
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
if not AIPROXY_TOKEN:
    raise EnvironmentError("AIPROXY_TOKEN environment variable is not set.")

# Define LLM interaction function
def ask_llm(prompt):
    """Send a prompt to the LLM via AI Proxy and return its response."""
    url = "https://api.aiproxy.example.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}", "Content-Type": "application/json"}
    payload = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}
    response = httpx.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def analyze_dataset(filename):
    """Analyze the dataset and generate insights."""
    # Load the dataset
    try:
        data = pd.read_csv(filename)
    except Exception as e:
        raise ValueError(f"Error reading file {filename}: {e}")
    
    # Summarize the dataset
    summary = {
        "shape": data.shape,
        "columns": data.dtypes.to_dict(),
        "missing_values": data.isnull().sum().to_dict(),
        "sample_rows": data.head(5).to_dict(orient="records"),
    }

    # Generate a correlation matrix if applicable
    numeric_data = data.select_dtypes(include=["number"])
    if not numeric_data.empty:
        correlation_matrix = numeric_data.corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.savefig("correlation_matrix.png")
        plt.close()

    # Send summary to LLM for insights
    prompt = (
        "Here is the summary of a dataset:\n"
        f"Shape: {summary['shape']}\n"
        f"Columns and types: {summary['columns']}\n"
        f"Missing values: {summary['missing_values']}\n"
        f"Sample rows: {summary['sample_rows']}\n"
        "What insights can you derive from this data?"
    )
    insights = ask_llm(prompt)

    # Create README.md
    with open("README.md", "w") as f:
        f.write("# Automated Dataset Analysis\n")
        f.write("## Dataset Summary\n")
        f.write(f"Shape: {summary['shape']}\n\n")
        f.write(f"### Column Information\n{summary['columns']}\n\n")
        f.write(f"### Missing Values\n{summary['missing_values']}\n\n")
        f.write(f"### Sample Data\n{pd.DataFrame(summary['sample_rows']).to_markdown(index=False)}\n\n")
        f.write("## Insights\n")
        f.write(insights + "\n\n")
        f.write("## Visualizations\n")
        f.write("![Correlation Matrix](correlation_matrix.png)\n")

# Main script
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run autolysis.py <dataset.csv>")
        sys.exit(1)

    dataset_file = sys.argv[1]
    analyze_dataset(dataset_file)
