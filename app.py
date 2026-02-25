"""
Streamlit Web Interface for Package Damage Risk Prediction
"""
import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Package Damage Risk Predictor",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .high-risk {
        background-color: #ffebee;
        border: 2px solid #f44336;
    }
    .medium-risk {
        background-color: #fff3e0;
        border: 2px solid #ff9800;
    }
    .low-risk {
        background-color: #e8f5e9;
        border: 2px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model_and_preprocessing():
    """Load the trained model and preprocessing artifacts."""
    try:
        models_dir = Path(__file__).parent / 'models'
        
        # Load model
        with open(models_dir / 'best_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Load preprocessing
        with open(models_dir / 'preprocessing.pkl', 'rb') as f:
            preprocessing = pickle.load(f)
        
        return model, preprocessing
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

@st.cache_data
def load_dataset():
    """Load the dataset for statistics."""
    try:
        data_path = Path(__file__).parent / 'data' / 'shipping_data.csv'
        return pd.read_csv(data_path)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

def preprocess_input(input_data, preprocessing):
    """Preprocess user input for prediction."""
    # Create DataFrame
    df = pd.DataFrame([input_data])
    
    # Encode categorical variables
    for col, encoder in preprocessing['encoders'].items():
        if col in df.columns:
            df[col] = encoder.transform(df[col])
    
    # Scale numerical features
    numerical_cols = ['package_weight', 'handling_quality', 'distance', 'num_transfers']
    df[numerical_cols] = preprocessing['scaler'].transform(df[numerical_cols])
    
    # Ensure correct column order
    df = df[preprocessing['feature_names']]
    
    return df

def predict_damage_risk(model, preprocessing, input_data):
    """Make prediction on user input."""
    # Preprocess input
    processed_data = preprocess_input(input_data, preprocessing)
    
    # Get prediction and probability
    prediction = model.predict(processed_data)[0]
    probability = model.predict_proba(processed_data)[0]
    
    return prediction, probability

def main():
    # Header
    st.title("📦 Package Damage Risk Predictor")
    st.markdown("### Predict the probability of package damage during shipping")
    
    # Load model and preprocessing
    model, preprocessing = load_model_and_preprocessing()
    
    if model is None or preprocessing is None:
        st.error("⚠️ Model not found. Please run the training pipeline first.")
        st.code("python src/train_model.py")
        return
    
    # Load dataset for statistics
    df = load_dataset()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 About")
        st.markdown("""
        This application predicts the risk of package damage based on:
        - Package characteristics
        - Handling conditions
        - Shipping route details
        - Weather conditions
        
        **Model Performance:**
        - Accuracy: ~77.5%
        - F1 Score: ~73-77%
        """)
        
        if df is not None:
            st.markdown("---")
            st.header("📈 Dataset Statistics")
            st.metric("Total Packages", f"{len(df):,}")
            st.metric("Damage Rate", f"{df['is_damaged'].mean():.1%}")
            st.metric("Avg Package Weight", f"{df['package_weight'].mean():.1f} kg")
    
    # Main content - Tabs
    tab1, tab2, tab3 = st.tabs(["🔮 Predict", "📊 Dashboard", "ℹ️ Info"])
    
    # Tab 1: Prediction Interface
    with tab1:
        st.header("Enter Package Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Package Information")
            
            package_weight = st.slider(
                "Package Weight (kg)",
                min_value=0.5,
                max_value=30.0,
                value=5.0,
                step=0.5,
                help="Weight of the package in kilograms"
            )
            
            packaging_type = st.selectbox(
                "Packaging Type",
                options=['cardboard', 'bubble_wrap', 'wooden_crate', 'plastic_container', 'fragile_box'],
                help="Type of packaging used"
            )
            
            handling_quality = st.slider(
                "Handling Quality (1-10)",
                min_value=1,
                max_value=10,
                value=5,
                help="Quality of handling (1=Poor, 10=Excellent)"
            )
        
        with col2:
            st.subheader("Shipping Details")
            
            distance = st.slider(
                "Shipping Distance (km)",
                min_value=10,
                max_value=5000,
                value=500,
                step=10,
                help="Total shipping distance in kilometers"
            )
            
            route_type = st.selectbox(
                "Route Type",
                options=['highway', 'urban', 'rural', 'mixed'],
                help="Type of route for shipping"
            )
            
            weather_condition = st.selectbox(
                "Weather Condition",
                options=['clear', 'rain', 'snow', 'storm'],
                help="Expected weather conditions during shipping"
            )
            
            num_transfers = st.slider(
                "Number of Transfers",
                min_value=0,
                max_value=10,
                value=2,
                help="Number of times the package will be transferred"
            )
        
        # Predict button
        st.markdown("---")
        if st.button("🔮 Predict Damage Risk", type="primary", use_container_width=True):
            # Prepare input data
            input_data = {
                'package_weight': package_weight,
                'packaging_type': packaging_type,
                'handling_quality': handling_quality,
                'distance': distance,
                'route_type': route_type,
                'weather_condition': weather_condition,
                'num_transfers': num_transfers
            }
            
            # Make prediction
            prediction, probability = predict_damage_risk(model, preprocessing, input_data)
            
            # Display results
            st.markdown("---")
            st.header("Prediction Results")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                damage_prob = probability[1] * 100
                
                # Determine risk level
                if damage_prob >= 70:
                    risk_level = "HIGH RISK"
                    risk_class = "high-risk"
                    risk_color = "#f44336"
                    emoji = "🔴"
                elif damage_prob >= 40:
                    risk_level = "MEDIUM RISK"
                    risk_class = "medium-risk"
                    risk_color = "#ff9800"
                    emoji = "🟡"
                else:
                    risk_level = "LOW RISK"
                    risk_class = "low-risk"
                    risk_color = "#4caf50"
                    emoji = "🟢"
                
                # Display prediction box
                st.markdown(f"""
                    <div class="prediction-box {risk_class}">
                        <h1>{emoji} {risk_level}</h1>
                        <h2>{damage_prob:.1f}% Damage Probability</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                # Gauge chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=damage_prob,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Damage Risk", 'font': {'size': 24}},
                    number={'suffix': "%", 'font': {'size': 40}},
                    gauge={
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': risk_color},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                            {'range': [0, 40], 'color': '#e8f5e9'},
                            {'range': [40, 70], 'color': '#fff3e0'},
                            {'range': [70, 100], 'color': '#ffebee'}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
                st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            st.markdown("---")
            st.header("💡 Recommendations")
            
            recommendations = []
            
            if damage_prob >= 70:
                st.error("⚠️ **HIGH RISK DETECTED** - Immediate action recommended!")
            elif damage_prob >= 40:
                st.warning("⚠️ **MEDIUM RISK** - Consider implementing some improvements")
            else:
                st.success("✅ **LOW RISK** - Package is well-protected")
            
            # Specific recommendations
            if packaging_type in ['cardboard', 'fragile_box']:
                recommendations.append("📦 Consider upgrading to wooden crate or plastic container for better protection")
            
            if handling_quality <= 5:
                recommendations.append("👷 Improve handling quality through better training and monitoring")
            
            if weather_condition in ['storm', 'snow']:
                recommendations.append("🌧️ Consider delaying shipment or using weather-protected routes")
            
            if num_transfers >= 3:
                recommendations.append("🔄 Minimize the number of transfers to reduce damage risk")
            
            if distance >= 2000:
                recommendations.append("🚚 For long distances, ensure extra packaging protection")
            
            if package_weight >= 15:
                recommendations.append("⚖️ Heavy package detected - use reinforced packaging and special handling")
            
            if recommendations:
                for rec in recommendations:
                    st.markdown(f"- {rec}")
            else:
                st.info("No specific recommendations - current setup looks good!")
    
    # Tab 2: Dashboard
    with tab2:
        st.header("📊 Analytics Dashboard")
        
        if df is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Packages", f"{len(df):,}")
            with col2:
                st.metric("Damaged", f"{df['is_damaged'].sum():,}")
            with col3:
                st.metric("Damage Rate", f"{df['is_damaged'].mean():.1%}")
            with col4:
                st.metric("Avg Weight", f"{df['package_weight'].mean():.1f} kg")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Damage rate by packaging type
                damage_by_pkg = df.groupby('packaging_type')['is_damaged'].mean().sort_values(ascending=False)
                fig = px.bar(
                    x=damage_by_pkg.values * 100,
                    y=damage_by_pkg.index,
                    orientation='h',
                    title="Damage Rate by Packaging Type",
                    labels={'x': 'Damage Rate (%)', 'y': 'Packaging Type'},
                    color=damage_by_pkg.values,
                    color_continuous_scale='Reds'
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Damage rate by weather
                damage_by_weather = df.groupby('weather_condition')['is_damaged'].mean().sort_values(ascending=False)
                fig = px.bar(
                    x=damage_by_weather.values * 100,
                    y=damage_by_weather.index,
                    orientation='h',
                    title="Damage Rate by Weather Condition",
                    labels={'x': 'Damage Rate (%)', 'y': 'Weather Condition'},
                    color=damage_by_weather.values,
                    color_continuous_scale='Blues'
                )
                fig.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Feature importance (if available)
            if hasattr(model, 'feature_importances_'):
                st.markdown("---")
                st.subheader("Feature Importance")
                
                importance_df = pd.DataFrame({
                    'Feature': preprocessing['feature_names'],
                    'Importance': model.feature_importances_
                }).sort_values('Importance', ascending=False)
                
                fig = px.bar(
                    importance_df,
                    x='Importance',
                    y='Feature',
                    orientation='h',
                    title="Feature Importance in Damage Prediction",
                    color='Importance',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Dataset not available for dashboard visualization.")
    
    # Tab 3: Information
    with tab3:
        st.header("ℹ️ About This Application")
        
        st.markdown("""
        ### Package Damage Risk Predictor
        
        This application uses machine learning to predict the probability of package damage during shipping operations.
        
        #### How It Works
        
        1. **Input Package Details**: Enter information about your package, shipping route, and conditions
        2. **AI Prediction**: Our trained model analyzes the data and calculates damage probability
        3. **Get Recommendations**: Receive actionable suggestions to minimize damage risk
        
        #### Model Information
        
        - **Algorithm**: Random Forest / Gradient Boosting Classifier
        - **Training Data**: 5,000 synthetic shipping records
        - **Accuracy**: ~77.5%
        - **Key Features**: Package weight, distance, handling quality, weather, packaging type
        
        #### Risk Levels
        
        - 🟢 **Low Risk (0-40%)**: Package is well-protected
        - 🟡 **Medium Risk (40-70%)**: Some improvements recommended
        - 🔴 **High Risk (70-100%)**: Immediate action needed
        
        #### Top Risk Factors
        
        1. **Package Weight** - Heavier packages are more prone to damage
        2. **Shipping Distance** - Longer distances increase risk
        3. **Handling Quality** - Poor handling significantly increases damage
        4. **Weather Conditions** - Adverse weather elevates risk
        5. **Number of Transfers** - More transfers = more risk
        
        #### Recommendations
        
        Based on your input, the system provides tailored recommendations such as:
        - Upgrading packaging materials
        - Improving handling procedures
        - Adjusting shipping routes
        - Weather-based scheduling
        - Minimizing transfer points
        
        ---
        
        **Note**: This application uses synthetic data for demonstration. For production use, 
        retrain the model with actual shipping and damage records.
        """)

if __name__ == "__main__":
    main()
