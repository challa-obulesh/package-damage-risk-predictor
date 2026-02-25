"""
Train classification model for package damage prediction.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix, classification_report
)
import pickle

def load_and_preprocess_data(data_path):
    """
    Load and preprocess the shipping data.
    
    Parameters:
    -----------
    data_path : str or Path
        Path to the CSV file
        
    Returns:
    --------
    X_train, X_test, y_train, y_test : arrays
        Split and preprocessed data
    encoders : dict
        Dictionary of label encoders for categorical features
    scaler : StandardScaler
        Fitted scaler for numerical features
    feature_names : list
        List of feature names after encoding
    """
    # Load data
    df = pd.read_csv(data_path)
    
    print(f"Loaded dataset with {len(df)} samples")
    print(f"Damage rate: {df['is_damaged'].mean():.2%}")
    
    # Separate features and target
    X = df.drop('is_damaged', axis=1)
    y = df['is_damaged']
    
    # Identify categorical and numerical columns
    categorical_cols = ['packaging_type', 'route_type', 'weather_condition']
    numerical_cols = ['package_weight', 'handling_quality', 'distance', 'num_transfers']
    
    # Encode categorical variables
    encoders = {}
    X_encoded = X.copy()
    
    for col in categorical_cols:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X[col])
        encoders[col] = le
    
    # Scale numerical features
    scaler = StandardScaler()
    X_encoded[numerical_cols] = scaler.fit_transform(X[numerical_cols])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    return X_train, X_test, y_train, y_test, encoders, scaler, X_encoded.columns.tolist()

def train_and_evaluate_model(X_train, X_test, y_train, y_test, model_type='random_forest'):
    """
    Train and evaluate a classification model.
    
    Parameters:
    -----------
    X_train, X_test, y_train, y_test : arrays
        Training and test data
    model_type : str
        Type of model to train ('random_forest' or 'gradient_boosting')
        
    Returns:
    --------
    model : trained model
    metrics : dict
        Dictionary of evaluation metrics
    """
    print(f"\n{'='*60}")
    print(f"Training {model_type.replace('_', ' ').title()} model...")
    print(f"{'='*60}")
    
    # Initialize model
    if model_type == 'random_forest':
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )
    elif model_type == 'gradient_boosting':
        model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Train model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }
    
    # Print results
    print(f"\nModel Performance:")
    print(f"  Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1 Score:  {metrics['f1_score']:.4f}")
    print(f"  ROC AUC:   {metrics['roc_auc']:.4f}")
    
    print(f"\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Not Damaged', 'Damaged']))
    
    return model, metrics

def save_model_artifacts(model, encoders, scaler, feature_names, model_name='model'):
    """
    Save model and preprocessing artifacts.
    
    Parameters:
    -----------
    model : trained model
    encoders : dict
        Label encoders
    scaler : StandardScaler
        Fitted scaler
    feature_names : list
        Feature names
    model_name : str
        Name for the saved model
    """
    # Create models directory
    models_dir = Path(__file__).parent.parent / 'models'
    models_dir.mkdir(exist_ok=True)
    
    # Save model
    model_path = models_dir / f'{model_name}.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved to {model_path}")
    
    # Save preprocessing artifacts
    preprocessing = {
        'encoders': encoders,
        'scaler': scaler,
        'feature_names': feature_names
    }
    preprocessing_path = models_dir / 'preprocessing.pkl'
    with open(preprocessing_path, 'wb') as f:
        pickle.dump(preprocessing, f)
    print(f"Preprocessing artifacts saved to {preprocessing_path}")

if __name__ == '__main__':
    # Load and preprocess data
    data_path = Path(__file__).parent.parent / 'data' / 'shipping_data.csv'
    X_train, X_test, y_train, y_test, encoders, scaler, feature_names = load_and_preprocess_data(data_path)
    
    # Train Random Forest model
    rf_model, rf_metrics = train_and_evaluate_model(
        X_train, X_test, y_train, y_test, 
        model_type='random_forest'
    )
    
    # Train Gradient Boosting model
    gb_model, gb_metrics = train_and_evaluate_model(
        X_train, X_test, y_train, y_test,
        model_type='gradient_boosting'
    )
    
    # Compare models and save the best one
    print(f"\n{'='*60}")
    print("Model Comparison:")
    print(f"{'='*60}")
    print(f"Random Forest F1 Score: {rf_metrics['f1_score']:.4f}")
    print(f"Gradient Boosting F1 Score: {gb_metrics['f1_score']:.4f}")
    
    if rf_metrics['f1_score'] >= gb_metrics['f1_score']:
        print("\nRandom Forest selected as the best model.")
        save_model_artifacts(rf_model, encoders, scaler, feature_names, 'best_model')
        best_model = rf_model
    else:
        print("\nGradient Boosting selected as the best model.")
        save_model_artifacts(gb_model, encoders, scaler, feature_names, 'best_model')
        best_model = gb_model
