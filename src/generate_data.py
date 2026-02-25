"""
Generate synthetic shipping dataset for package damage prediction.
"""
import numpy as np
import pandas as pd
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

def generate_shipping_data(n_samples=5000):
    """
    Generate synthetic shipping data with realistic correlations.
    
    Parameters:
    -----------
    n_samples : int
        Number of samples to generate
        
    Returns:
    --------
    pd.DataFrame
        Synthetic shipping dataset
    """
    
    # Package weight (kg) - normally distributed
    package_weight = np.random.normal(loc=5.0, scale=3.0, size=n_samples)
    package_weight = np.clip(package_weight, 0.5, 30.0)  # Realistic bounds
    
    # Packaging type
    packaging_types = ['cardboard', 'bubble_wrap', 'wooden_crate', 'plastic_container', 'fragile_box']
    packaging_type = np.random.choice(packaging_types, size=n_samples, 
                                     p=[0.4, 0.25, 0.15, 0.15, 0.05])
    
    # Handling quality (1-10 scale, lower is worse)
    handling_quality = np.random.randint(1, 11, size=n_samples)
    
    # Distance (km)
    distance = np.random.exponential(scale=500, size=n_samples)
    distance = np.clip(distance, 10, 5000)
    
    # Route type
    route_types = ['highway', 'urban', 'rural', 'mixed']
    route_type = np.random.choice(route_types, size=n_samples,
                                  p=[0.3, 0.3, 0.2, 0.2])
    
    # Weather condition
    weather_conditions = ['clear', 'rain', 'snow', 'storm']
    weather_condition = np.random.choice(weather_conditions, size=n_samples,
                                        p=[0.5, 0.3, 0.1, 0.1])
    
    # Number of transfers
    num_transfers = np.random.poisson(lam=2, size=n_samples)
    num_transfers = np.clip(num_transfers, 0, 10)
    
    # Create damage probability based on features
    damage_prob = np.zeros(n_samples)
    
    # Base probability
    damage_prob += 0.05
    
    # Weight factor (heavier = more damage risk)
    damage_prob += (package_weight / 30.0) * 0.15
    
    # Packaging type factor
    packaging_risk = {
        'cardboard': 0.20,
        'bubble_wrap': 0.10,
        'wooden_crate': 0.05,
        'plastic_container': 0.08,
        'fragile_box': 0.30
    }
    for i, pkg in enumerate(packaging_type):
        damage_prob[i] += packaging_risk[pkg]
    
    # Handling quality (poor handling = more damage)
    damage_prob += (10 - handling_quality) / 10 * 0.25
    
    # Distance factor
    damage_prob += (distance / 5000) * 0.10
    
    # Route type factor
    route_risk = {
        'highway': 0.05,
        'urban': 0.10,
        'rural': 0.15,
        'mixed': 0.12
    }
    for i, route in enumerate(route_type):
        damage_prob[i] += route_risk[route]
    
    # Weather condition factor
    weather_risk = {
        'clear': 0.00,
        'rain': 0.08,
        'snow': 0.12,
        'storm': 0.20
    }
    for i, weather in enumerate(weather_condition):
        damage_prob[i] += weather_risk[weather]
    
    # Number of transfers (more transfers = more risk)
    damage_prob += (num_transfers / 10) * 0.15
    
    # Clip probability to [0, 1]
    damage_prob = np.clip(damage_prob, 0, 1)
    
    # Generate binary outcome
    is_damaged = (np.random.random(n_samples) < damage_prob).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'package_weight': package_weight,
        'packaging_type': packaging_type,
        'handling_quality': handling_quality,
        'distance': distance,
        'route_type': route_type,
        'weather_condition': weather_condition,
        'num_transfers': num_transfers,
        'is_damaged': is_damaged
    })
    
    return df

if __name__ == '__main__':
    # Generate dataset
    print("Generating synthetic shipping dataset...")
    df = generate_shipping_data(n_samples=5000)
    
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Save to CSV
    output_path = data_dir / 'shipping_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Dataset saved to {output_path}")
    print(f"\nDataset shape: {df.shape}")
    print(f"\nDamage rate: {df['is_damaged'].mean():.2%}")
    print(f"\nFirst few rows:")
    print(df.head())
    print(f"\nDataset info:")
    print(df.info())
