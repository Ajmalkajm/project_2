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
#   "scikit-learn",
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
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor

# Constants
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
OPENAI_MODEL = "gpt-4o-mini"
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

    if numeric_data.shape[1] >= 2:
        col1, col2 = numeric_data.columns[:2]
        
        # T-test
        t_stat, p_val = ttest_ind(data[col1].dropna(), data[col2].dropna())
        analysis_results["t_test"] = {"t_stat": t_stat, "p_value": p_val}

        # Linear regression
        slope, intercept, r_value, p_value, std_err = linregress(data[col1], data[col2])
        analysis_results["regression"] = {"slope": slope, "intercept": intercept, "r_value": r_value, "p_value": p_value, "std_err": std_err}

        # Pearson correlation
        corr, _ = pearsonr(data[col1].dropna(), data[col2].dropna())
        analysis_results["pearson_corr"] = {"correlation": corr}

        # Decision Tree Regression (Advanced)
        model = DecisionTreeRegressor()
        X = data[[col1]].dropna()
        y = data[col2].dropna()
        model.fit(X, y)
        y_pred = model.predict(X)
        mse = mean_squared_error(y, y_pred)
        analysis_results["decision_tree"] = {"mse": mse}
    
    return analysis_results

def outlier_detection(data):
    """Detect and analyze outliers in numeric columns."""
    numeric_data = data.select_dtypes(include=["number"])
    outliers_analysis = {}

    for column in numeric_data.columns:
        q1 = numeric_data[column].quantile(0.25)
        q3 = numeric_data[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = numeric_data[(numeric_data[column] < lower_bound) | (numeric_data[column] > upper_bound)][column]
        outlier_impact = (
            "potential errors, unusual cases, or influential factors in the dataset. "
            "These could significantly affect statistical analyses like mean or regression results."
            if len(outliers) > 0
            else "no significant impact on this column."
        )

        outliers_analysis[column] = {
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outliers": outliers.tolist(),
            "impact_analysis": outlier_impact,
        }

    return outliers_analysis

def pair_plots(data, folder_name):
    """Generate pair plots for numeric columns."""
    numeric_data = data.select_dtypes(include=['number'])
    pair_plot_file = os.path.join(folder_name, "pair_plots.png")
    sns.pairplot(numeric_data)
    plt.savefig(pair_plot_file)
    plt.close()
    return pair_plot_file

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
        sns.set_palette("coolwarm")

        # Histograms for numeric columns
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

        # Correlation matrix
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
    return f"Analyze a dataset with columns: {columns}. Provide insights and potential implications. No conclusion"

def request_summary_from_openai(prompt, is_conclusion=False):
    """Request analysis summary or conclusion from OpenAI."""
    try:
        url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
        
        # Adjust the prompt for conclusion
        if is_conclusion:
            prompt = f"Provide a detailed conclusion based on the following analysis:\n{prompt}"

        payload = {
            "model": OPENAI_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise ValueError(f"Error during API call: {e}")

def generate_conclusion_prompt(basic_analysis, advanced_analysis, outliers, visualization_summary):
    """Generate a detailed prompt to request a conclusion from OpenAI."""
    prompt = "Here is the dataset analysis:\n\n"
    
    # Add Basic Analysis
    prompt += "### Basic Analysis\n"
    prompt += f"Dataset Description:\n{basic_analysis['description'].to_string()}\n\n"
    prompt += f"Missing Values:\n{basic_analysis['missing_values'].to_string()}\n\n"
    
    # Add Advanced Analysis
    prompt += "### Advanced Statistical Findings\n"
    for key, value in advanced_analysis.items():
        prompt += f"- {key}: {value}\n"
    
    # Add Outliers Analysis
    prompt += "\n### Outliers Analysis\n"
    for column, data in outliers.items():
        prompt += (
            f"- {column}: {len(data['outliers'])} outliers detected "
            f"(lower bound: {data['lower_bound']}, upper bound: {data['upper_bound']}).\n"
        )
    
    # Add Visualizations
    prompt += "\n### Visualization Insights\n"
    for key, value in visualization_summary.items():
        prompt += f"- {key}: {value}\n"
    
    # Request a Conclusion
    prompt += (
        "\nBased on this analysis, provide a conclusion in one para.\n"
    )
    return prompt


def create_readme(basic_analysis, analysis_results, folder_name, ai_summary, visualization_summary, outliers, pair_plot_file, image_analysis=None,  conclusion=None):
    """Create README file with analysis summaries and results."""
    readme_content = "# Dataset Analysis Report\n\n"
   
    # Add Basic Statistics section as a Markdown table
    readme_content += "## Basic Statistics\n\n"
    description_df = basic_analysis["description"]
    description_markdown = description_df.to_markdown(index=True)  # Convert DataFrame to Markdown
    readme_content += description_markdown + "\n\n"
    
    # Add Missing Values section as a Markdown table
    readme_content += "## Missing Values\n\n"
    missing_values_df = basic_analysis["missing_values"]
    missing_values_markdown = missing_values_df.to_markdown()  # Convert missing values DataFrame to Markdown
    readme_content += missing_values_markdown + "\n\n"
    
    # Add Outliers section
    readme_content += "## Outliers Detection\n\n"
    for column, data in outliers.items():
        readme_content += f"### {column}\n"
        readme_content += (
                f"- **Bounds:** Lower Bound = {data['lower_bound']}, Upper Bound = {data['upper_bound']}\n"
                f"- **Number of Outliers:** {len(data['outliers'])}\n"
                f"- **Analysis:** Outliers in '{column}' could indicate {data['impact_analysis']}.\n\n"
            )
    
    # Add Pair Plot
    readme_content += "## Pair Plots\n\n"
    readme_content += f"![Pair Plots]({pair_plot_file})\n\n"
    
    # Add Significant Findings (only advanced analysis results)
    readme_content += "## Significant Findings\n\n"
    for analysis_type, result in analysis_results.items():
        readme_content += f"### {analysis_type}\n"
        readme_content += f"Result: {result}\n\n"
    
    # Add Visualizations section
    readme_content += "## Visualizations\n\n"
    for vis, desc in visualization_summary.items():
        readme_content += f"### {vis}\n{desc}\n\n"

    
    if image_analysis:
        readme_content += "## Image Analysis\n\n"
        for img_file, analysis in image_analysis:
            readme_content += f"### {img_file}\nAnalysis: {analysis}\n\n"
    
    readme_content += "## Summary\n\n"
    readme_content += ai_summary + "\n\n" if ai_summary else "AI summary could not be generated.\n\n"

        # Add Conclusion
    readme_content += "## Conclusion\n\n"
    readme_content += conclusion + "\n\n" if conclusion else "Conclusion could not be generated.\n\n"

    # Write to README.md file
    readme_path = os.path.join(folder_name, "README.md")
    with open(readme_path, "w") as readme_file:
        readme_file.write(readme_content)

def main():
    args = handle_arguments()
    dataset_filepath = args.dataset
    data = load_dataset(dataset_filepath)

    # Create output folder
    folder_name = os.path.splitext(os.path.basename(args.dataset))[0]
    os.makedirs(folder_name, exist_ok=True)

    # Perform analyses
    basic_analysis_results = perform_basic_analysis(data)
    advanced_analysis_results = perform_advanced_analysis(data)
    outliers = outlier_detection(data)
    visualization_summary = generate_visualizations(data, folder_name)
    pair_plot_file = pair_plots(data, folder_name)

    # Generate dynamic prompt and request AI summary
    dynamic_prompt_content = dynamic_prompt(data)
    ai_summary = request_summary_from_openai(dynamic_prompt_content)

    # Create a summary for the conclusion
    conclusion_prompt = generate_conclusion_prompt(
        basic_analysis_results, advanced_analysis_results, outliers, visualization_summary
    )
    
    # Request conclusion
    conclusion = request_summary_from_openai(conclusion_prompt, is_conclusion=True)

    # Analyze images if provided
    image_analysis = None
    if args.images:
        image_analysis = analyze_images(args.images)

    # Create README
    create_readme(
        basic_analysis_results,
        advanced_analysis_results,
        folder_name,
        ai_summary,
        visualization_summary,
        outliers,
        pair_plot_file,
        image_analysis=image_analysis,
        conclusion=conclusion,
    )

if __name__ == "__main__":
    main()