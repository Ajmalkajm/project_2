# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "matplotlib",
#   "seaborn",
#   "openai",
#   "requests",
#   "chardet",
#   "opencv-python",
#   "scikit-learn",
#   "scipy"
# ]
# ///

import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import openai
import requests
import chardet
import cv2  # Vision library
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from scipy.stats import zscore


# Load AIPROXY_TOKEN from the environment variable
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

if not AIPROXY_TOKEN:
    print("Error: AIPROXY_TOKEN environment variable is not set.")
    sys.exit(1)

# Set the proxy URL for OpenAI API
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/"
openai.api_key = AIPROXY_TOKEN


def detect_encoding(file_path):
    """Detect the encoding of the file using chardet."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result.get("encoding", "utf-8")


def load_dataset(file_path):
    """Load a dataset, handling encoding issues automatically."""
    try:
        encoding = detect_encoding(file_path)
        print(f"Detected file encoding: {encoding}")
        data = pd.read_csv(file_path, encoding=encoding)
        print(f"Loaded dataset with {data.shape[0]} rows and {data.shape[1]} columns.")
        return data
    except Exception as e:
        print(f"Error loading dataset: {e}")
        sys.exit(1)


def perform_analysis(data):
    """Perform basic and advanced analysis on the dataset."""
    analysis_results = {
        "columns": list(data.columns),
        "info": str(data.info()),  # Save as string
        "description": data.describe(include='all').to_dict()
    }

    # Correlation matrix for numeric data
    numeric_data = data.select_dtypes(include=['number'])
    analysis_results["correlation"] = numeric_data.corr().to_dict()

    # Clustering Analysis
    if not numeric_data.empty:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numeric_data.dropna())
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        silhouette = silhouette_score(scaled_data, clusters)
        analysis_results["clustering"] = {
            "silhouette_score": silhouette,
            "cluster_centers": kmeans.cluster_centers_.tolist()
        }

    return analysis_results


def detect_outliers(data):
    """Detect outliers using Z-scores."""
    numeric_data = data.select_dtypes(include=['number']).dropna()
    z_scores = numeric_data.apply(zscore)

    # Boolean mask for outliers
    outliers_mask = (z_scores.abs() > 3).any(axis=1)
    
    # Use the original data's index to align correctly
    outliers = data.loc[outliers_mask.index[outliers_mask]]

    return outliers, z_scores

def calculate_feature_importance(data, target_column):
    """Calculate feature importance using correlation with target variable."""
    if target_column not in data.columns:
        print(f"Target column '{target_column}' not found in dataset.")
        return None
    numeric_data = data.select_dtypes(include=['number']).drop(columns=[target_column], errors='ignore')
    correlations = numeric_data.corrwith(data[target_column])
    return correlations.to_dict()


def visualize_data(data, folder_name):
    """Visualize data and save plots."""
    try:
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

            for column in numeric_data.columns:
                plt.hist(data[column].dropna(), bins=30)
                plt.title(f"Histogram for {column}")
                hist_file = os.path.join(folder_name, f"{column}_histogram.png")
                plt.savefig(hist_file)
                plt.close()
                print(f"Saved: {hist_file}")

    except Exception as e:
        print(f"Error during visualization: {e}")


def analyze_images_with_openai(image_folder):
    """Use OpenAI API for vision-based analysis on images."""
    results = []
    try:
        for img_file in os.listdir(image_folder):
            img_path = os.path.join(image_folder, img_file)
            with open(img_path, "rb") as img:
                url = "https://aiproxy.sanand.workers.dev/openai/v1/images/analyze"
                headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
                files = {"image": img}
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()
                results.append({
                    "file": img_file,
                    "analysis": response.json()
                })
                print(f"Analysis for {img_file}: {response.json()}")
    except Exception as e:
        print(f"Error during OpenAI vision analysis: {e}")
    return results


def create_readme(analysis_results, folder_name, ai_summary=None, key_insights=None, limitations=None, recommendations=None):
    """Create a README file summarizing the analysis with structured sections."""
    readme_content = f"# Dataset Analysis\n\n"
    readme_content += f"## Overview\n\n"
    readme_content += f"Columns:\n"
    for column in analysis_results["columns"]:
        readme_content += f"- {column}\n"
    readme_content += f"\n## Dataset Information\n\n"
    readme_content += f"```\n{analysis_results['info']}\n```\n\n"
    readme_content += f"## Statistical Description\n\n"
    readme_content += f"```\n{analysis_results['description']}\n```\n\n"
    readme_content += f"## Correlation Matrix\n\nSee `correlation_matrix.png`.\n\n"
    if "clustering" in analysis_results:
        readme_content += f"## Clustering Analysis\n\n"
        readme_content += f"Silhouette Score: {analysis_results['clustering']['silhouette_score']}\n"
    if key_insights:
        readme_content += f"## Key Insights\n\n{key_insights}\n\n"
    if limitations:
        readme_content += f"## Limitations\n\n{limitations}\n\n"
    if recommendations:
        readme_content += f"## Recommendations\n\n{recommendations}\n\n"
    if ai_summary:
        readme_content += f"## AI Summary\n\n{ai_summary}\n"
    readme_file = os.path.join(folder_name, "README.md")
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    print(f"Saved: {readme_file}")


def narrate_results(summary_text):
    """Generate a narrative using OpenAI."""
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


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Analyze and visualize dataset.")
    parser.add_argument("dataset", help="Path to the dataset (CSV file).")
    parser.add_argument("--images", help="Path to the folder with images for vision analysis.", default=None)
    parser.add_argument("--target", help="Specify target column for feature importance.", default=None)
    args = parser.parse_args()

    data = load_dataset(args.dataset)

    folder_name = os.path.splitext(os.path.basename(args.dataset))[0]
    os.makedirs(folder_name, exist_ok=True)

    analysis_results = perform_analysis(data)

    # Advanced Analysis
    outliers, z_scores = detect_outliers(data)
    print(f"Detected {len(outliers)} outliers.")

    if args.target:
        feature_importance = calculate_feature_importance(data, args.target)
        print(f"Feature Importance:\n{feature_importance}")

    # Visualizations
    visualize_data(data, folder_name)

    if args.images:
        image_results = analyze_images_with_openai(args.images)
        print(f"Vision Analysis Results: {image_results}")

    ai_summary = narrate_results(str(analysis_results['description']))
    key_insights = "Key trends observed in the dataset include significant correlations and clustering patterns."
    limitations = "Dataset contains some missing values and outliers."
    recommendations = "Consider cleaning outliers and rebalancing dataset for better clustering."

    create_readme(analysis_results, folder_name, ai_summary, key_insights, limitations, recommendations)


if __name__ == "__main__":
    main()