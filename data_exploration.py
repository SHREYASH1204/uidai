"""
Aadhaar Data Analysis - DataThon Submission
Data Exploration and Structure Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AadhaarDataExplorer:
    def __init__(self):
        self.biometric_files = [
            'api_data_aadhar_biometric/api_data_aadhar_biometric_0_500000.csv',
            'api_data_aadhar_biometric/api_data_aadhar_biometric_500000_1000000.csv',
            'api_data_aadhar_biometric/api_data_aadhar_biometric_1000000_1500000.csv',
            'api_data_aadhar_biometric/api_data_aadhar_biometric_1500000_1861108.csv'
        ]
        
        self.demographic_files = [
            'api_data_aadhar_demographic/api_data_aadhar_demographic_0_500000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_500000_1000000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_1000000_1500000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_1500000_2000000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_2000000_2071700.csv'
        ]
        
        self.enrollment_files = [
            'api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv',
            'api_data_aadhar_enrolment/api_data_aadhar_enrolment_500000_1000000.csv',
            'api_data_aadhar_enrolment/api_data_aadhar_enrolment_1000000_1006029.csv'
        ]
        
    def load_data(self, file_list, sample_size=None):
        """Load and combine multiple CSV files"""
        dataframes = []
        for file in file_list:
            try:
                df = pd.read_csv(file)
                if sample_size:
                    df = df.sample(n=min(sample_size, len(df)), random_state=42)
                dataframes.append(df)
                print(f"Loaded {file}: {len(df)} records")
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            print(f"Total combined records: {len(combined_df)}")
            return combined_df
        return None
    
    def explore_dataset_structure(self):
        """Explore the structure of all three datasets"""
        print("="*60)
        print("AADHAAR DATASET STRUCTURE ANALYSIS")
        print("="*60)
        
        # Load sample data for structure analysis
        bio_sample = pd.read_csv(self.biometric_files[0], nrows=1000)
        demo_sample = pd.read_csv(self.demographic_files[0], nrows=1000)
        enroll_sample = pd.read_csv(self.enrollment_files[0], nrows=1000)
        
        datasets = {
            'Biometric': bio_sample,
            'Demographic': demo_sample,
            'Enrollment': enroll_sample
        }
        
        for name, df in datasets.items():
            print(f"\n{name.upper()} DATA STRUCTURE:")
            print("-" * 40)
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print(f"Data types:\n{df.dtypes}")
            print(f"Sample data:\n{df.head(3)}")
            print(f"Missing values:\n{df.isnull().sum()}")
            
        return datasets
    
    def analyze_data_quality(self, df, dataset_name):
        """Analyze data quality metrics"""
        print(f"\n{dataset_name.upper()} DATA QUALITY ANALYSIS:")
        print("-" * 50)
        
        # Basic statistics
        print("Basic Statistics:")
        print(df.describe())
        
        # Missing values
        missing_pct = (df.isnull().sum() / len(df)) * 100
        print(f"\nMissing Values Percentage:\n{missing_pct}")
        
        # Unique values
        print(f"\nUnique Values Count:")
        for col in df.columns:
            print(f"{col}: {df[col].nunique()}")
            
        # Date range
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            print(f"\nDate Range: {df['date'].min()} to {df['date'].max()}")
            
        return df

if __name__ == "__main__":
    explorer = AadhaarDataExplorer()
    
    # Explore dataset structures
    datasets = explorer.explore_dataset_structure()
    
    print("\n" + "="*60)
    print("LOADING FULL DATASETS FOR ANALYSIS...")
    print("="*60)
    
    # Load full datasets (with sampling for memory efficiency)
    bio_data = explorer.load_data(explorer.biometric_files, sample_size=50000)
    demo_data = explorer.load_data(explorer.demographic_files, sample_size=50000)
    enroll_data = explorer.load_data(explorer.enrollment_files, sample_size=50000)
    
    # Analyze data quality
    if bio_data is not None:
        bio_data = explorer.analyze_data_quality(bio_data, "Biometric")
    
    if demo_data is not None:
        demo_data = explorer.analyze_data_quality(demo_data, "Demographic")
        
    if enroll_data is not None:
        enroll_data = explorer.analyze_data_quality(enroll_data, "Enrollment")
    
    print("\nData exploration completed successfully!")