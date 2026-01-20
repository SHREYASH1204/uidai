"""
Aadhaar Data Analysis - Comprehensive Analysis and Insights
DataThon Submission - Main Analysis Script
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class AadhaarAnalyzer:
    def __init__(self):
        self.bio_data = None
        self.demo_data = None
        self.enroll_data = None
        
    def load_all_data(self):
        """Load all datasets efficiently"""
        print("Loading Aadhaar datasets...")
        
        # Biometric data
        bio_files = [
            'api_data_aadhar_biometric/api_data_aadhar_biometric_0_500000.csv',
            'api_data_aadhar_biometric/api_data_aadhar_biometric_500000_1000000.csv',
            'api_data_aadhar_biometric/api_data_aadhar_biometric_1000000_1500000.csv',
            'api_data_aadhar_biometric/api_data_aadhar_biometric_1500000_1861108.csv'
        ]
        
        # Demographic data
        demo_files = [
            'api_data_aadhar_demographic/api_data_aadhar_demographic_0_500000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_500000_1000000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_1000000_1500000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_1500000_2000000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_2000000_2071700.csv'
        ]
        
        # Enrollment data
        enroll_files = [
            'api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv',
            'api_data_aadhar_enrolment/api_data_aadhar_enrolment_500000_1000000.csv',
            'api_data_aadhar_enrolment/api_data_aadhar_enrolment_1000000_1006029.csv'
        ]
        
        # Load with sampling for memory efficiency
        self.bio_data = self._load_files(bio_files, "Biometric")
        self.demo_data = self._load_files(demo_files, "Demographic") 
        self.enroll_data = self._load_files(enroll_files, "Enrollment")
        
        # Data preprocessing
        self._preprocess_data()
        
    def _load_files(self, file_list, data_type, sample_frac=0.1):
        """Load and combine files with sampling"""
        dfs = []
        for file in file_list:
            try:
                df = pd.read_csv(file)
                # Sample for memory efficiency
                if len(df) > 10000:
                    df = df.sample(frac=sample_frac, random_state=42)
                dfs.append(df)
            except Exception as e:
                print(f"Error loading {file}: {e}")
        
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            print(f"{data_type} data loaded: {len(combined)} records")
            return combined
        return None
    
    def _preprocess_data(self):
        """Preprocess all datasets"""
        datasets = [
            (self.bio_data, "Biometric"),
            (self.demo_data, "Demographic"), 
            (self.enroll_data, "Enrollment")
        ]
        
        for data, name in datasets:
            if data is not None:
                # Convert date column
                data['date'] = pd.to_datetime(data['date'], format='%d-%m-%Y')
                data['month'] = data['date'].dt.month
                data['day'] = data['date'].dt.day
                
                # Add total columns for analysis
                if name == "Biometric":
                    data['total_bio'] = data['bio_age_5_17'] + data['bio_age_17_']
                elif name == "Demographic":
                    data['total_demo'] = data['demo_age_5_17'] + data['demo_age_17_']
                elif name == "Enrollment":
                    data['total_enroll'] = data['age_0_5'] + data['age_5_17'] + data['age_18_greater']
    
    def analyze_geographic_patterns(self):
        """Analyze geographic distribution patterns"""
        print("\n" + "="*60)
        print("GEOGRAPHIC PATTERN ANALYSIS")
        print("="*60)
        
        fig, axes = plt.subplots(2, 2, figsize=(20, 15))
        fig.suptitle('Geographic Distribution Analysis', fontsize=16, fontweight='bold')
        
        # State-wise enrollment analysis
        if self.enroll_data is not None:
            state_enroll = self.enroll_data.groupby('state')['total_enroll'].sum().sort_values(ascending=False).head(15)
            axes[0,0].bar(range(len(state_enroll)), state_enroll.values)
            axes[0,0].set_title('Top 15 States by Enrollment Volume')
            axes[0,0].set_xticks(range(len(state_enroll)))
            axes[0,0].set_xticklabels(state_enroll.index, rotation=45, ha='right')
            axes[0,0].set_ylabel('Total Enrollments')
        
        # State-wise biometric analysis
        if self.bio_data is not None:
            state_bio = self.bio_data.groupby('state')['total_bio'].sum().sort_values(ascending=False).head(15)
            axes[0,1].bar(range(len(state_bio)), state_bio.values, color='orange')
            axes[0,1].set_title('Top 15 States by Biometric Updates')
            axes[0,1].set_xticks(range(len(state_bio)))
            axes[0,1].set_xticklabels(state_bio.index, rotation=45, ha='right')
            axes[0,1].set_ylabel('Total Biometric Updates')
        
        # State-wise demographic analysis
        if self.demo_data is not None:
            state_demo = self.demo_data.groupby('state')['total_demo'].sum().sort_values(ascending=False).head(15)
            axes[1,0].bar(range(len(state_demo)), state_demo.values, color='green')
            axes[1,0].set_title('Top 15 States by Demographic Updates')
            axes[1,0].set_xticks(range(len(state_demo)))
            axes[1,0].set_xticklabels(state_demo.index, rotation=45, ha='right')
            axes[1,0].set_ylabel('Total Demographic Updates')
        
        # District-level analysis (top performing districts)
        if self.enroll_data is not None:
            district_enroll = self.enroll_data.groupby(['state', 'district'])['total_enroll'].sum().sort_values(ascending=False).head(10)
            district_labels = [f"{idx[1]}, {idx[0]}" for idx in district_enroll.index]
            axes[1,1].barh(range(len(district_enroll)), district_enroll.values, color='red')
            axes[1,1].set_title('Top 10 Districts by Enrollment')
            axes[1,1].set_yticks(range(len(district_enroll)))
            axes[1,1].set_yticklabels(district_labels)
            axes[1,1].set_xlabel('Total Enrollments')
        
        plt.tight_layout()
        plt.savefig('geographic_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return state_enroll if self.enroll_data is not None else None
    
    def analyze_age_demographics(self):
        """Analyze age group patterns"""
        print("\n" + "="*60)
        print("AGE DEMOGRAPHIC ANALYSIS")
        print("="*60)
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Age Group Analysis Across Services', fontsize=16, fontweight='bold')
        
        # Enrollment age distribution
        if self.enroll_data is not None:
            age_cols = ['age_0_5', 'age_5_17', 'age_18_greater']
            age_totals = [self.enroll_data[col].sum() for col in age_cols]
            age_labels = ['0-5 years', '5-17 years', '18+ years']
            
            axes[0,0].pie(age_totals, labels=age_labels, autopct='%1.1f%%', startangle=90)
            axes[0,0].set_title('Enrollment Distribution by Age Groups')
        
        # Biometric age distribution
        if self.bio_data is not None:
            bio_age_totals = [self.bio_data['bio_age_5_17'].sum(), self.bio_data['bio_age_17_'].sum()]
            bio_labels = ['5-17 years', '17+ years']
            
            axes[0,1].pie(bio_age_totals, labels=bio_labels, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral'])
            axes[0,1].set_title('Biometric Updates by Age Groups')
        
        # Demographic age distribution
        if self.demo_data is not None:
            demo_age_totals = [self.demo_data['demo_age_5_17'].sum(), self.demo_data['demo_age_17_'].sum()]
            demo_labels = ['5-17 years', '17+ years']
            
            axes[1,0].pie(demo_age_totals, labels=demo_labels, autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightyellow'])
            axes[1,0].set_title('Demographic Updates by Age Groups')
        
        # Comparative analysis
        if all([self.enroll_data is not None, self.bio_data is not None, self.demo_data is not None]):
            services = ['Enrollment\n(5-17)', 'Enrollment\n(18+)', 'Biometric\n(5-17)', 'Biometric\n(17+)', 'Demographic\n(5-17)', 'Demographic\n(17+)']
            values = [
                self.enroll_data['age_5_17'].sum(),
                self.enroll_data['age_18_greater'].sum(),
                self.bio_data['bio_age_5_17'].sum(),
                self.bio_data['bio_age_17_'].sum(),
                self.demo_data['demo_age_5_17'].sum(),
                self.demo_data['demo_age_17_'].sum()
            ]
            
            axes[1,1].bar(services, values, color=['skyblue', 'navy', 'orange', 'darkorange', 'lightgreen', 'darkgreen'])
            axes[1,1].set_title('Service Usage Comparison by Age Groups')
            axes[1,1].set_ylabel('Total Transactions')
            axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('age_demographics_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def analyze_temporal_patterns(self):
        """Analyze temporal trends and patterns"""
        print("\n" + "="*60)
        print("TEMPORAL PATTERN ANALYSIS")
        print("="*60)
        
        fig, axes = plt.subplots(2, 2, figsize=(18, 12))
        fig.suptitle('Temporal Trends Analysis', fontsize=16, fontweight='bold')
        
        # Daily trends for enrollment
        if self.enroll_data is not None:
            daily_enroll = self.enroll_data.groupby('date')['total_enroll'].sum().sort_index()
            axes[0,0].plot(daily_enroll.index, daily_enroll.values, marker='o', linewidth=2)
            axes[0,0].set_title('Daily Enrollment Trends')
            axes[0,0].set_xlabel('Date')
            axes[0,0].set_ylabel('Total Enrollments')
            axes[0,0].tick_params(axis='x', rotation=45)
        
        # Daily trends for biometric
        if self.bio_data is not None:
            daily_bio = self.bio_data.groupby('date')['total_bio'].sum().sort_index()
            axes[0,1].plot(daily_bio.index, daily_bio.values, marker='s', color='orange', linewidth=2)
            axes[0,1].set_title('Daily Biometric Update Trends')
            axes[0,1].set_xlabel('Date')
            axes[0,1].set_ylabel('Total Biometric Updates')
            axes[0,1].tick_params(axis='x', rotation=45)
        
        # Monthly comparison
        datasets = []
        labels = []
        if self.enroll_data is not None:
            monthly_enroll = self.enroll_data.groupby('month')['total_enroll'].sum()
            datasets.append(monthly_enroll)
            labels.append('Enrollment')
        
        if self.bio_data is not None:
            monthly_bio = self.bio_data.groupby('month')['total_bio'].sum()
            datasets.append(monthly_bio)
            labels.append('Biometric')
        
        if self.demo_data is not None:
            monthly_demo = self.demo_data.groupby('month')['total_demo'].sum()
            datasets.append(monthly_demo)
            labels.append('Demographic')
        
        if datasets:
            months = range(1, 13)
            for i, (data, label) in enumerate(zip(datasets, labels)):
                axes[1,0].plot(months, [data.get(m, 0) for m in months], marker='o', label=label, linewidth=2)
            axes[1,0].set_title('Monthly Service Usage Comparison')
            axes[1,0].set_xlabel('Month')
            axes[1,0].set_ylabel('Total Transactions')
            axes[1,0].legend()
            axes[1,0].set_xticks(months)
        
        # Day of month analysis
        if self.enroll_data is not None:
            day_enroll = self.enroll_data.groupby('day')['total_enroll'].sum()
            axes[1,1].bar(day_enroll.index, day_enroll.values, alpha=0.7)
            axes[1,1].set_title('Enrollment by Day of Month')
            axes[1,1].set_xlabel('Day of Month')
            axes[1,1].set_ylabel('Total Enrollments')
        
        plt.tight_layout()
        plt.savefig('temporal_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def identify_anomalies_and_insights(self):
        """Identify anomalies and generate insights"""
        print("\n" + "="*60)
        print("ANOMALY DETECTION AND KEY INSIGHTS")
        print("="*60)
        
        insights = []
        
        # Geographic anomalies
        if self.enroll_data is not None:
            state_stats = self.enroll_data.groupby('state')['total_enroll'].agg(['mean', 'std', 'sum'])
            high_variance_states = state_stats[state_stats['std'] > state_stats['std'].quantile(0.9)]
            insights.append(f"High variance enrollment states: {list(high_variance_states.index)}")
        
        # Age group insights
        if all([self.enroll_data is not None, self.bio_data is not None]):
            enroll_adult_ratio = self.enroll_data['age_18_greater'].sum() / self.enroll_data['total_enroll'].sum()
            bio_adult_ratio = self.bio_data['bio_age_17_'].sum() / self.bio_data['total_bio'].sum()
            insights.append(f"Adult enrollment ratio: {enroll_adult_ratio:.2%}")
            insights.append(f"Adult biometric ratio: {bio_adult_ratio:.2%}")
        
        # Service utilization patterns
        if all([self.enroll_data is not None, self.bio_data is not None, self.demo_data is not None]):
            total_enroll = self.enroll_data['total_enroll'].sum()
            total_bio = self.bio_data['total_bio'].sum()
            total_demo = self.demo_data['total_demo'].sum()
            
            insights.append(f"Service usage - Enrollment: {total_enroll:,}, Biometric: {total_bio:,}, Demographic: {total_demo:,}")
            
            # Calculate ratios
            bio_to_enroll = total_bio / total_enroll if total_enroll > 0 else 0
            demo_to_enroll = total_demo / total_enroll if total_enroll > 0 else 0
            
            insights.append(f"Biometric to Enrollment ratio: {bio_to_enroll:.2f}")
            insights.append(f"Demographic to Enrollment ratio: {demo_to_enroll:.2f}")
        
        # Print insights
        print("\nKEY INSIGHTS:")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
        
        return insights
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        print("\n" + "="*60)
        print("RECOMMENDATIONS FOR SYSTEM IMPROVEMENT")
        print("="*60)
        
        recommendations = [
            "1. RESOURCE ALLOCATION: Focus additional enrollment centers in high-demand states identified in geographic analysis",
            "2. AGE-SPECIFIC CAMPAIGNS: Develop targeted outreach for underrepresented age groups",
            "3. TEMPORAL OPTIMIZATION: Schedule maintenance and updates during low-activity periods identified in temporal analysis",
            "4. QUALITY ASSURANCE: Implement additional verification for districts showing unusual patterns",
            "5. CAPACITY PLANNING: Use identified trends to predict future resource requirements",
            "6. DIGITAL LITERACY: Enhance support in regions with lower biometric/demographic update ratios",
            "7. MOBILE SERVICES: Deploy mobile enrollment units in districts with geographic access challenges"
        ]
        
        for rec in recommendations:
            print(rec)
        
        return recommendations

def main():
    """Main analysis execution"""
    print("AADHAAR DATA ANALYSIS - DATATHON SUBMISSION")
    print("="*60)
    
    # Initialize analyzer
    analyzer = AadhaarAnalyzer()
    
    # Load data
    analyzer.load_all_data()
    
    # Perform comprehensive analysis
    analyzer.analyze_geographic_patterns()
    analyzer.analyze_age_demographics()
    analyzer.analyze_temporal_patterns()
    
    # Generate insights and recommendations
    insights = analyzer.identify_anomalies_and_insights()
    recommendations = analyzer.generate_recommendations()
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETED SUCCESSFULLY!")
    print("Generated visualizations: geographic_analysis.png, age_demographics_analysis.png, temporal_analysis.png")
    print("="*60)

if __name__ == "__main__":
    main()