"""
Analyze feature importance and identify key risk factors for package damage.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pickle

def load_model_and_preprocessing():
    """
    Load the trained model and preprocessing artifacts.
    
    Returns:
    --------
    model : trained model
    preprocessing : dict
        Dictionary containing encoders, scaler, and feature names
    """
    models_dir = Path(__file__).parent.parent / 'models'
    
    # Load model
    model_path = models_dir / 'best_model.pkl'
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    # Load preprocessing artifacts
    preprocessing_path = models_dir / 'preprocessing.pkl'
    with open(preprocessing_path, 'rb') as f:
        preprocessing = pickle.load(f)
    
    return model, preprocessing

def analyze_feature_importance(model, feature_names):
    """
    Analyze and visualize feature importance.
    
    Parameters:
    -----------
    model : trained model
    feature_names : list
        List of feature names
    """
    # Get feature importance
    importance = model.feature_importances_
    
    # Create DataFrame for better visualization
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)
    
    print("="*60)
    print("Feature Importance Analysis")
    print("="*60)
    print(importance_df.to_string(index=False))
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    sns.barplot(data=importance_df, x='importance', y='feature', palette='viridis')
    plt.title('Feature Importance for Package Damage Prediction', fontsize=14, fontweight='bold')
    plt.xlabel('Importance Score', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.tight_layout()
    
    # Save plot
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    plot_path = output_dir / 'feature_importance.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"\nFeature importance plot saved to {plot_path}")
    plt.close()
    
    return importance_df

def analyze_risk_factors(data_path, preprocessing):
    """
    Analyze risk factors by examining the relationship between features and damage.
    
    Parameters:
    -----------
    data_path : Path
        Path to the dataset
    preprocessing : dict
        Preprocessing artifacts
    """
    # Load data
    df = pd.read_csv(data_path)
    
    print("\n" + "="*60)
    print("Risk Factor Analysis")
    print("="*60)
    
    # Analyze categorical features
    categorical_cols = ['packaging_type', 'route_type', 'weather_condition']
    
    for col in categorical_cols:
        damage_rate = df.groupby(col)['is_damaged'].agg(['mean', 'count'])
        damage_rate.columns = ['damage_rate', 'count']
        damage_rate = damage_rate.sort_values('damage_rate', ascending=False)
        
        print(f"\n{col.replace('_', ' ').title()} - Damage Rate:")
        print(damage_rate.to_string())
    
    # Analyze numerical features
    print("\n" + "="*60)
    print("Numerical Feature Statistics by Damage Status")
    print("="*60)
    
    numerical_cols = ['package_weight', 'handling_quality', 'distance', 'num_transfers']
    
    for col in numerical_cols:
        print(f"\n{col.replace('_', ' ').title()}:")
        stats = df.groupby('is_damaged')[col].describe()[['mean', 'std', '50%']]
        stats.index = ['Not Damaged', 'Damaged']
        print(stats.to_string())
    
    # Create visualizations
    create_risk_visualizations(df)

def create_risk_visualizations(df):
    """
    Create visualizations for risk analysis.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The shipping dataset
    """
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    
    # 1. Damage rate by categorical features
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    categorical_cols = ['packaging_type', 'route_type', 'weather_condition']
    
    for idx, col in enumerate(categorical_cols):
        damage_rate = df.groupby(col)['is_damaged'].mean().sort_values(ascending=False)
        sns.barplot(x=damage_rate.values, y=damage_rate.index, ax=axes[idx], palette='Reds_r')
        axes[idx].set_title(f'Damage Rate by {col.replace("_", " ").title()}', fontweight='bold')
        axes[idx].set_xlabel('Damage Rate')
        axes[idx].set_ylabel('')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'damage_rate_categorical.png', dpi=300, bbox_inches='tight')
    print(f"\nCategorical damage rate plot saved to {output_dir / 'damage_rate_categorical.png'}")
    plt.close()
    
    # 2. Distribution of numerical features by damage status
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    numerical_cols = ['package_weight', 'handling_quality', 'distance', 'num_transfers']
    
    for idx, col in enumerate(numerical_cols):
        for damage_status in [0, 1]:
            data = df[df['is_damaged'] == damage_status][col]
            label = 'Damaged' if damage_status == 1 else 'Not Damaged'
            axes[idx].hist(data, alpha=0.6, label=label, bins=30)
        
        axes[idx].set_title(f'{col.replace("_", " ").title()} Distribution', fontweight='bold')
        axes[idx].set_xlabel(col.replace('_', ' ').title())
        axes[idx].set_ylabel('Frequency')
        axes[idx].legend()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'numerical_distributions.png', dpi=300, bbox_inches='tight')
    print(f"Numerical distributions plot saved to {output_dir / 'numerical_distributions.png'}")
    plt.close()
    
    # 3. Correlation heatmap
    plt.figure(figsize=(10, 8))
    
    # Encode categorical variables for correlation
    df_encoded = df.copy()
    for col in categorical_cols:
        df_encoded[col] = pd.Categorical(df_encoded[col]).codes
    
    correlation = df_encoded.corr()
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Feature Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_dir / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print(f"Correlation heatmap saved to {output_dir / 'correlation_heatmap.png'}")
    plt.close()

def generate_risk_report(importance_df, data_path):
    """
    Generate a comprehensive risk analysis report.
    
    Parameters:
    -----------
    importance_df : pd.DataFrame
        Feature importance data
    data_path : Path
        Path to the dataset
    """
    df = pd.read_csv(data_path)
    
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    report_path = output_dir / 'risk_analysis_report.txt'
    
    with open(report_path, 'w') as f:
        f.write("="*70 + "\n")
        f.write("PACKAGE DAMAGE RISK ANALYSIS REPORT\n")
        f.write("="*70 + "\n\n")
        
        f.write("1. EXECUTIVE SUMMARY\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total packages analyzed: {len(df):,}\n")
        f.write(f"Overall damage rate: {df['is_damaged'].mean():.2%}\n")
        f.write(f"Total damaged packages: {df['is_damaged'].sum():,}\n\n")
        
        f.write("2. TOP RISK FACTORS (by importance)\n")
        f.write("-" * 70 + "\n")
        for idx, row in importance_df.head(5).iterrows():
            f.write(f"{idx+1}. {row['feature']}: {row['importance']:.4f}\n")
        f.write("\n")
        
        f.write("3. PACKAGING TYPE RISK ASSESSMENT\n")
        f.write("-" * 70 + "\n")
        pkg_risk = df.groupby('packaging_type')['is_damaged'].agg(['mean', 'count'])
        pkg_risk.columns = ['damage_rate', 'count']
        pkg_risk = pkg_risk.sort_values('damage_rate', ascending=False)
        for pkg_type, row in pkg_risk.iterrows():
            f.write(f"{pkg_type}: {row['damage_rate']:.2%} damage rate ({row['count']} packages)\n")
        f.write("\n")
        
        f.write("4. HANDLING QUALITY IMPACT\n")
        f.write("-" * 70 + "\n")
        handling_stats = df.groupby('is_damaged')['handling_quality'].describe()[['mean', '50%']]
        f.write(f"Average handling quality (not damaged): {handling_stats.loc[0, 'mean']:.2f}\n")
        f.write(f"Average handling quality (damaged): {handling_stats.loc[1, 'mean']:.2f}\n")
        f.write(f"Difference: {handling_stats.loc[0, 'mean'] - handling_stats.loc[1, 'mean']:.2f}\n\n")
        
        f.write("5. WEATHER CONDITION RISK\n")
        f.write("-" * 70 + "\n")
        weather_risk = df.groupby('weather_condition')['is_damaged'].mean().sort_values(ascending=False)
        for weather, rate in weather_risk.items():
            f.write(f"{weather}: {rate:.2%} damage rate\n")
        f.write("\n")
        
        f.write("6. KEY RECOMMENDATIONS\n")
        f.write("-" * 70 + "\n")
        f.write("- Improve handling quality training and monitoring\n")
        f.write("- Use stronger packaging for fragile items\n")
        f.write("- Minimize transfers when possible\n")
        f.write("- Implement weather-based routing and protection\n")
        f.write("- Focus on high-risk routes (rural, mixed terrain)\n")
        f.write("\n")
        
        f.write("="*70 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*70 + "\n")
    
    print(f"\nRisk analysis report saved to {report_path}")

if __name__ == '__main__':
    # Load model and preprocessing
    model, preprocessing = load_model_and_preprocessing()
    
    # Analyze feature importance
    importance_df = analyze_feature_importance(model, preprocessing['feature_names'])
    
    # Analyze risk factors
    data_path = Path(__file__).parent.parent / 'data' / 'shipping_data.csv'
    analyze_risk_factors(data_path, preprocessing)
    
    # Generate comprehensive report
    generate_risk_report(importance_df, data_path)
    
    print("\n" + "="*60)
    print("Analysis complete! Check the 'output' directory for visualizations and report.")
    print("="*60)
