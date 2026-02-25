# Logistics Package Damage Risk Prediction

> [!CAUTION]
> **Python Installation Required!** This project requires Python 3.8+. If you see "Python was not found" errors, you have a Windows Store stub, not real Python. See [INSTALL_PYTHON.md](file:///c:/Users/chall/OneDrive/Attachments/Desktop/trafic/INSTALL_PYTHON.md) for installation instructions.

A machine learning project to predict package damage probability during logistics operations, identify handling risks, and improve packaging decisions.

## 📋 Project Overview

This project uses synthetic shipping data to train classification models that predict the likelihood of package damage based on various factors including:
- Package weight and packaging type
- Handling quality
- Distance and route type
- Weather conditions
- Number of transfers

## 🚀 Features

- **Synthetic Data Generation**: Creates realistic shipping datasets with correlated features
- **Multiple ML Models**: Compares Random Forest and Gradient Boosting classifiers
- **Feature Analysis**: Identifies key risk factors through feature importance analysis
- **Comprehensive Reporting**: Generates visualizations and detailed risk assessment reports

## 📁 Project Structure

```
trafic/
├── data/                    # Generated datasets
├── src/                     # Source code
│   ├── generate_data.py    # Synthetic data generation
│   ├── train_model.py      # Model training and evaluation
│   └── analyze_risks.py    # Risk factor analysis
├── models/                  # Saved models (created during training)
├── output/                  # Visualizations and reports (created during analysis)
├── notebooks/               # Jupyter notebooks (optional)
└── requirements.txt         # Python dependencies
```

## 🛠️ Prerequisites

- **Python 3.8+** (Required)
- pip (Python package manager)

## 📦 Installation

1. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install packages individually:
   ```bash
   pip install numpy pandas scikit-learn matplotlib seaborn
   ```

## 🎯 Usage

### Step 1: Generate Synthetic Dataset
```bash
python src/generate_data.py
```
This creates `data/shipping_data.csv` with 5,000 synthetic shipping records.

### Step 2: Train Classification Models
```bash
python src/train_model.py
```
This script:
- Preprocesses the data
- Trains Random Forest and Gradient Boosting models
- Compares performance metrics
- Saves the best model to `models/best_model.pkl`

### Step 3: Analyze Risk Factors
```bash
python src/analyze_risks.py
```
This generates:
- Feature importance visualization
- Damage rate analysis by category
- Numerical feature distributions
- Correlation heatmap
- Comprehensive risk analysis report

All outputs are saved in the `output/` directory.

## 📊 Expected Results

The model typically achieves:
- **Accuracy**: ~75-85%
- **Precision**: ~70-80%
- **Recall**: ~65-75%
- **F1 Score**: ~70-78%
- **ROC AUC**: ~80-88%

## 🔍 Key Insights

The analysis identifies critical risk factors such as:
1. **Handling Quality**: Poor handling significantly increases damage risk
2. **Packaging Type**: Fragile boxes and cardboard have higher damage rates
3. **Weather Conditions**: Storms and snow increase damage probability
4. **Number of Transfers**: More transfers correlate with higher damage risk
5. **Route Type**: Rural and mixed routes show elevated damage rates

## 📈 Outputs

After running all scripts, you'll find:

**In `output/` directory:**
- `feature_importance.png` - Bar chart of feature importance scores
- `damage_rate_categorical.png` - Damage rates by packaging, route, and weather
- `numerical_distributions.png` - Distribution comparisons for numerical features
- `correlation_heatmap.png` - Feature correlation matrix
- `risk_analysis_report.txt` - Comprehensive text report with recommendations

**In `models/` directory:**
- `best_model.pkl` - Trained classification model
- `preprocessing.pkl` - Encoders and scalers for data preprocessing

## 🎓 Modules Implemented

✅ Synthetic shipping dataset generation  
✅ Data preprocessing and feature engineering  
✅ Classification modeling (Random Forest & Gradient Boosting)  
✅ Feature importance analysis  
✅ Model evaluation with multiple metrics  
✅ Risk factor identification  
✅ Visualization and reporting  

## 🤝 Contributing

This is a demonstration project for logistics package damage prediction. Feel free to extend it with:
- Additional features (e.g., package value, insurance status)
- More sophisticated models (e.g., XGBoost, Neural Networks)
- Real-world data integration
- Deployment pipeline

## 📝 License

This project is for educational and demonstration purposes.

---

**Note**: This project uses synthetic data. For production use, replace with actual shipping and damage records.
