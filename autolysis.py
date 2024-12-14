# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
#   "matplotlib",
#   "seaborn",
#   "requests",
#   "chardet",
#   "opencv-python",
#   "openai",
#   "tabulate",
#   "scipy"
# ]
# ///

import os
import pandas as pd
import openai
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, linregress, pearsonr
import cv2
import chardet
import requests
import base64
import argparse
import tabulate

# Constants
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
OPENAI_MODEL = "gpt-4o-mini"  # This can be made dynamic as needed
IMAGE_SIZE = (512, 512)

# Ensure API key is set
if not AIPROXY_TOKEN:
    raise EnvironmentError("AIPROXY_TOKEN environment variable is not set.")

openai.api_key = AIPROXY_TOKEN

def handle_arguments():
    """Handles command-line arguments."""
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
        return data
    except Exception as e:
        raise ValueError(f"Error loading dataset: {e}")

def perform_basic_analysis(data):
    """Perform basic analysis of the dataset."""
    description = data.describe(include='all')
    missing_values = data.isnull().sum()
    return {"description": description, "missing_values": missing_values}

def perform_advanced_analysis(data):
    """Perform advanced statistical analysis."""
    numeric_data = data.select_dtypes(include=['number'])
    analysis_results = {}

    # T-test between the first two numeric columns
    if numeric_data.shape[1] >= 2:
        col1, col2 = numeric_data.columns[:2]
        t_stat, p_val = ttest_ind(data[col1].dropna(), data[col2].dropna())
        analysis_results["t_test"] = {"t_stat": t_stat, "p_value": p_val}

        # Linear regression between the first two numeric columns
        slope, intercept, r_value, p_value, std_err = linregress(data[col1], data[col2])
        analysis_results["regression"] = {
            "slope": slope, "intercept": intercept, "r_value": r_value,
            "p_value": p_value, "std_err": std_err
        }

        # Pearson Correlation for the first two numeric columns
        corr, _ = pearsonr(data[col1].dropna(), data[col2].dropna())
        analysis_results["pearson_corr"] = {"correlation": corr}
    
    return analysis_results

def resize_image(img_path, size=IMAGE_SIZE):
    """Resize image to specific size."""
    try:
        img = cv2.imread(img_path)
        img_resized = cv2.resize(img, size)
        return img_resized
    except Exception as e:
        raise ValueError(f"Error resizing image {img_path}: {e}")

def generate_visualizations(data, folder_name):
    """Generate visualizations and save them with detailed explanations."""
    numeric_data = data.select_dtypes(include=['number'])
    visualization_summary = {}

    if not numeric_data.empty:
        # Color palette for consistency
        sns.set_palette("coolwarm")

        # Generate histograms for numeric columns
        for column in numeric_data.columns:
            plt.hist(data[column].dropna(), bins=30, alpha=0.7, label=column)
            plt.title(f"Histogram of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.legend()

            hist_file = os.path.join(folder_name, f"{column}_histogram.png")
            plt.savefig(hist_file)
            plt.close()

            img_resized = resize_image(hist_file)
            if img_resized is not None:
                cv2.imwrite(hist_file, img_resized)

            visualization_summary[column] = f"Histogram of {column} showing frequency distribution."

        # Generate a correlation matrix
        correlation_matrix = numeric_data.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Matrix")
        corr_file = os.path.join(folder_name, "correlation_matrix.png")
        plt.savefig(corr_file)
        plt.close()

        img_resized = resize_image(corr_file)
        if img_resized is not None:
            cv2.imwrite(corr_file, img_resized)

        visualization_summary["correlation_matrix"] = "Correlation matrix showing relationships between numeric features."
    
    return visualization_summary

def encode_image_to_base64(img_path):
    """Encode an image to base64."""
    try:
        with open(img_path, "rb") as img_file:
            img_data = img_file.read()
            return base64.b64encode(img_data).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Error encoding image {img_path}: {e}")

def request_image_analysis_from_openai(img_base64):
    """Send image base64 to OpenAI for analysis."""
    prompt = f"Analyze the following image and provide a short summary of key insights and trends: {img_base64}"
    try:
        response = openai.Completion.create(
            model=OPENAI_MODEL,
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise ValueError(f"Error with OpenAI image analysis: {e}")

def analyze_images(image_folder):
    """Analyze images and summarize results."""
    image_analysis = []
    for img_name in os.listdir(image_folder):
        img_path = os.path.join(image_folder, img_name)
        if img_name.endswith(('.png', '.jpg', '.jpeg')):
            img_base64 = encode_image_to_base64(img_path)
            analysis = request_image_analysis_from_openai(img_base64)
            image_analysis.append((img_name, analysis))
    return image_analysis

def dynamic_prompt(data):
    """Generate dynamic prompt based on dataset structure."""
    columns = ", ".join(data.columns)
    return f"Analyze a dataset with columns: {columns}. Provide insights and potential implications."

def request_summary_from_openai(prompt):
    """Request analysis summary from OpenAI."""
    try:
        url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
        payload = {
            "model": OPENAI_MODEL,
            "messages": [{"role": "user", "content": f"Summarize: {prompt}"}]
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise ValueError(f"Error during API call: {e}")

def create_readme(analysis_results, folder_name, ai_summary, visualization_summary, image_analysis=None):
    """Create README file with analysis summaries and results."""
    readme_content = "# Dataset Analysis Report\n\n"
    readme_content += "## Summary\n\n"
    
    readme_content += ai_summary if ai_summary else "AI summary could not be generated.\n\n"
    
    # Add Basic Statistics section as a Markdown table
    readme_content += "## Basic Statistics\n\n"
    description_df = analysis_results["description"]
    description_markdown = description_df.to_markdown(index=True)  # Convert DataFrame to Markdown
    readme_content += description_markdown + "\n\n"
    
    # Add Missing Values section as a Markdown table
    readme_content += "## Missing Values\n\n"
    missing_values_df = analysis_results["missing_values"]
    missing_values_markdown = missing_values_df.to_markdown()  # Convert missing values DataFrame to Markdown
    readme_content += missing_values_markdown + "\n\n"

    # Add Visualizations section
    readme_content += "## Visualizations\n\n"
    for vis, desc in visualization_summary.items():
        readme_content += f"### {vis}\n{desc}\n\n"

    if image_analysis:
        readme_content += "## Image Analysis\n\n"
        for img_file, analysis in image_analysis:
            readme_content += f"### {img_file}\nAnalysis: {analysis}\n\n"

    # Write to README.md file
    readme_path = os.path.join(folder_name, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write(readme_content)
    
    print(f"README generated at: {readme_path}")

def main():
    args = handle_arguments()

    # Load dataset
    data = load_dataset(args.dataset)

    # Create output folder
    folder_name = os.path.splitext(os.path.basename(args.dataset))[0]
    os.makedirs(folder_name, exist_ok=True)

    # Perform basic and advanced analysis
    basic_results = perform_basic_analysis(data)
    advanced_results = perform_advanced_analysis(data)

    # Generate visualizations
    visualization_summary = generate_visualizations(data, folder_name)

    # Request AI summary
    prompt_text = dynamic_prompt(data)
    ai_summary = request_summary_from_openai(prompt_text)

    # Create README file
    create_readme(basic_results, folder_name, ai_summary, visualization_summary)

    # Analyze images if provided
    if args.images:
        image_analysis = analyze_images(args.images)
        print("Image Analysis Results:", image_analysis)

if __name__ == "__main__":
    main()