import os
import sys
import textwrap
from pathlib import Path
import pandas as pd
try:
    import matplotlib.pyplot as plt  # Used for creating charts and visualizations
except Exception:
    plt = None
from ai import get_ai_response  # Custom function to send a question to AI and get an answer
try:
    import seaborn as sns  # Library for more advanced and pretty charts
except Exception:
    sns = None

# Global dataset storage
DF = None        # Will hold the loaded dataset
DATA_NAME = None # Name of the loaded file

# Stores all actions and results during the session
SESSION_LOG = []

# Adjust Pandas display settings so data looks nicer in the terminal
pd.set_option("display.width", 120)
pd.set_option("display.max_rows", 30)
pd.set_option("display.max_columns", 20)
pd.set_option("display.precision", 4)

def pause():
    """Pause the program until the user presses Enter."""
    input("\nPress Enter to continue...")

def log_output(title, content, is_image=False):
    """Save a piece of output (text or image path) into the session log."""
    SESSION_LOG.append({
        "title": title,
        "content": content,
        "is_image": is_image
    })

def validate_dataset(df):
    """Check if dataset contains all required columns for the analysis."""
    required_columns = [
        "Age", "BMI", "BloodPressure", "Week",
        "Glucose", "ActivityLevel", "SleepHours", "RiskScore"
    ]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"⚠️ Warning: Missing required columns: {', '.join(missing)}")
        return False
    return True

def load_data():
    """Allow the user to choose between loading the default dataset or uploading their own CSV."""
    global DF, DATA_NAME
    print("== Load Data ==")
    print("1. Use the pre-loaded dataset.")
    print("2. Upload your own data.")

    choice = input("\nEnter your choice (1 or 2): ").strip()
    if choice == '1':
        DF = pd.read_csv('pregnancy_data.csv')  # Load default data
        DATA_NAME = "pregnancy_data.csv"
    elif choice == '2':
        src = input("Enter the path to your CSV file: ").strip()
        if not src:  # If empty input, use default
            DF = pd.read_csv('pregnancy_data.csv')
            DATA_NAME = "pregnancy_data.csv"
        else:
            p = Path(src)
            if p.exists() and p.suffix.lower() == ".csv":
                try:
                    DF = pd.read_csv(p)
                    DATA_NAME = str(p)
                except Exception as e:
                    print(f"Failed to read CSV: {e}. Using default dataset.")
                    DF = pd.read_csv('pregnancy_data.csv')
                    DATA_NAME = "pregnancy_data.csv"
            else:
                print("Invalid file. Using default dataset.")
                DF = pd.read_csv('pregnancy_data.csv')
                DATA_NAME = "pregnancy_data.csv"
    else:
        DF = pd.read_csv('pregnancy_data.csv')
        DATA_NAME = "pregnancy_data.csv"

    # Validate the dataset
    if not validate_dataset(DF):
        DF = None
        pause()
        return

    print(f"\nLoaded dataset: '{DATA_NAME}' with shape {DF.shape}.")
    pause()

def quick_profile(df):
    """Create a short text summary of the dataset (shape, dtypes, missing values, numeric stats)."""
    shape = df.shape
    dtypes = df.dtypes.astype(str)
    missing_pct = (df.isna().mean() * 100).round(2)
    num_desc = df.select_dtypes(include="number").describe().T

    profile_text = textwrap.dedent(f"""
    Source: {DATA_NAME}
    Shape: {shape[0]} rows × {shape[1]} columns

    Dtypes:
    {dtypes.to_string()}

    Missing (%):
    {missing_pct.to_string()}

    Numeric summary:
    {num_desc.to_string()}
    """).strip()
    return profile_text

def describe_data():
    """Print and log the dataset profile created by quick_profile()."""
    if DF is None:
        print("Load data first (option 1).")
        pause()
        return
    print("== Describe Data ==")
    profile = quick_profile(DF)
    print(profile)
    log_output("Describe Data", profile)
    pause()

def visualize_data():
    """Generate three visualizations: bar plot, pie chart, and correlation heatmap."""
    try:
        if DF is None:
            raise ValueError("No dataset loaded. Please load data first (option 1).")
        if sns is None or plt is None:
            raise ImportError("Seaborn/Matplotlib not available.")

        print("== Data Visualization ==")
        plots_info = []

        # Bar plot: Shows correlation of each numeric feature with RiskScore
        plt.figure(figsize=(8, 5))
        correlations = DF.corr(numeric_only=True)["RiskScore"].drop("RiskScore")
        corr_df = correlations.reset_index()
        corr_df.columns = ["Feature", "CorrelationWithRiskScore"]
        sns.barplot(data=corr_df, x="Feature", y="CorrelationWithRiskScore", palette="Blues_d")
        plt.title("Feature Correlation with RiskScore")
        plt.xticks(rotation=45)
        plt.tight_layout()
        img_path = "barplot.png"
        plt.savefig(img_path)
        plt.show()
        plots_info.append(img_path)

        # Pie chart: Categorizes RiskScore into Low, Medium, High
        plt.figure(figsize=(6, 6))
        risk_norm = (DF["RiskScore"] - DF["RiskScore"].min()) / (DF["RiskScore"].max() - DF["RiskScore"].min())
        bins = [0, 0.33, 0.66, 1]
        labels = ["Low Risk", "Medium Risk", "High Risk"]
        DF["RiskCategory"] = pd.cut(risk_norm, bins=bins, labels=labels, include_lowest=True)
        DF["RiskCategory"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90, colormap="coolwarm")
        plt.ylabel("")
        plt.title("Risk Score Category Distribution")
        plt.tight_layout()
        img_path = "piechart.png"
        plt.savefig(img_path)
        plt.show()
        plots_info.append(img_path)

        # Heatmap: Shows correlation between all numeric columns
        plt.figure(figsize=(8, 6))
        corr = DF.corr(numeric_only=True)
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        img_path = "heatmap.png"
        plt.savefig(img_path)
        plt.show()
        plots_info.append(img_path)

        # Save all plots in the session log
        for path in plots_info:
            log_output("Visualization", path, is_image=True)

    except Exception as e:
        print(f"{e}")
    pause()

def ask_ai():
    """Send a question about the dataset to the AI, including a profile and sample data."""
    if DF is None:
        print("No data exist. Load data first (option 1).")
        pause()
        return
    print("== Ask AI ==")
    question = input("Ask the AI about your data:\n> ").strip()
    if not question:
        print("No question provided.")
        pause()
        return
    base_context = quick_profile(DF)
    sample_data = DF.head(200).to_string()
    context = f"{base_context}\n\nSample Data (first 200 rows):\n{sample_data}"
    print("\nGetting AI response...")
    try:
        answer = get_ai_response(question, context=context)
    except Exception as e:
        answer = f"[AI error: {e}]"
    print("\nAI Answer:")
    print(answer)
    log_output("AI Question", f"Q: {question}\nA: {answer}")
    pause()

def save_session():
    """Save all session text and images to a folder for later review."""
    try:
        if not SESSION_LOG:
            print("No session data to save.")
            pause()
            return
        folder = input("Enter folder name to save (default: session_output): ").strip() or "session_output"
        os.makedirs(folder, exist_ok=True)

        # Save text log
        text_file = os.path.join(folder, "session_log.md")
        with open(text_file, "w", encoding="utf-8-sig") as f:
            for entry in SESSION_LOG:
                if not entry["is_image"]:
                    f.write(f"## {entry['title']}\n\n")
                    f.write("```\n")  # פתיחת block code
                    f.write(f"{entry['content']}\n")
                    f.write("```\n\n")  # סגירת block code
                    f.write("---\n\n")   # מפריד בין חלקים

        # Save images
        for entry in SESSION_LOG:
            if entry["is_image"]:
                img_name = os.path.basename(entry["content"])
                dest_path = os.path.join(folder, img_name)
                try:
                    os.replace(entry["content"], dest_path)
                except Exception:
                    pass
        print(f"Session saved to '{folder}'.")
    except Exception as e:
        print(f"Error saving session: {e}")
    pause()

def cleanup_temp_images():
    """Delete temporary image files created during the session."""
    try:
        for entry in SESSION_LOG:
            if entry["is_image"]:
                if os.path.exists(entry["content"]):
                    os.remove(entry["content"])
    except Exception as e:
        print(f"Error during cleanup: {e}")

def main():
    """Main menu loop for the Pregnancy Data Analyzer."""
    while True:
        print("Pregnancy Data Analyzer with AI")
        print("----------------------------")
        print("1) Load data")
        print("2) Describe data")
        print("3) Visualize data")
        print("4) Ask AI")
        print("5) Save session")
        print("6) Exit")
        choice = input("\nSelect: ").strip() 
        if choice == "1":
            load_data()
        elif choice == "2":
            describe_data()
        elif choice == "3":
            visualize_data()
        elif choice == "4":
            ask_ai()
        elif choice == "5":
            save_session()
        elif choice == "6":
            print("Thank you for using Pregnancy Data Analyzer. Mazal Tov!")
            cleanup_temp_images()
            sys.exit(0)
        else:
            print("Invalid choice.")
            pause()

if __name__ == "__main__":
    main()
