"""
Advanced Analytics and Predictive Insights for Aadhaar Data
DataThon Submission - Advanced Analysis Module
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class AdvancedAadhaarAnalytics:
    def __init__(self):
        self.bio_data = None
        self.demo_data = None
        self.enroll_data = None
        self.combined_data = None
        
    def load_and_prepare_data(self):
        """Load and prepare data for advanced analytics"""
        print("Loading data for advanced analytics...")
        
        # Load sample data for analysis
        try:
            self.bio_data = pd.read_csv('api_data_aadhar_biometric/api_data_aadhar_biometric_0_500000.csv').sample(n=10000, random_state=42)
            self.demo_data = pd.read_csv('api_data_aadhar_demographic/api_data_aadhar_demographic_0_500000.csv').sample(n=10000, random_state=42)
            self.enroll_data = pd.read_csv('api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv').sample(n=10000, random_state=42)
            
            # Preprocess dates
            for df in [self.bio_data, self.demo_data, self.enroll_data]:
                df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
                df['month'] = df['date'].dt.month
                df['day'] = df['date'].dt.day
                df['weekday'] = df['date'].dt.dayofweek
            
            # Add calculated columns
            self.bio_data['total_bio'] = self.bio_data['bio_age_5_17'] + self.bio_data['bio_age_17_']
            self.demo_data['total_demo'] = self.demo_data['demo_age_5_17'] + self.demo_data['demo_age_17_']
            self.enroll_data['total_enroll'] = self.enroll_data['age_0_5'] + self.enroll_data['age_5_17'] + self.enroll_data['age_18_greater']
            
            print("Data loaded and preprocessed successfully!")
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def perform_clustering_analysis(self):
        """Perform clustering analysis to identify patterns"""
        print("\n" + "="*60)
        print("CLUSTERING ANALYSIS - IDENTIFYING DISTRICT PATTERNS")
        print("="*60)
        
        if self.enroll_data is None:
            return
        
        # Aggregate data by district for clustering
        district_features = self.enroll_data.groupby(['state', 'district']).agg({
            'age_0_5': 'mean',
            'age_5_17': 'mean', 
            'age_18_greater': 'mean',
            'total_enroll': ['mean', 'std', 'sum'],
            'month': 'nunique',
            'pincode': 'nunique'
        }).reset_index()
        
        # Flatten column names
        district_features.columns = ['state', 'district', 'avg_age_0_5', 'avg_age_5_17', 'avg_age_18_greater', 
                                   'avg_total', 'std_total', 'sum_total', 'months_active', 'pincode_count']
        
        # Prepare features for clustering
        feature_cols = ['avg_age_0_5', 'avg_age_5_17', 'avg_age_18_greater', 'avg_total', 'std_total', 'pincode_count']
        X = district_features[feature_cols].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        district_features['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Visualize clusters
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('District Clustering Analysis', fontsize=16, fontweight='bold')
        
        # Cluster distribution
        cluster_counts = district_features['cluster'].value_counts().sort_index()
        axes[0,0].bar(cluster_counts.index, cluster_counts.values, color=['red', 'blue', 'green', 'orange'])
        axes[0,0].set_title('Districts per Cluster')
        axes[0,0].set_xlabel('Cluster')
        axes[0,0].set_ylabel('Number of Districts')
        
        # Average enrollment by cluster
        cluster_avg = district_features.groupby('cluster')['avg_total'].mean()
        axes[0,1].bar(cluster_avg.index, cluster_avg.values, color=['red', 'blue', 'green', 'orange'])
        axes[0,1].set_title('Average Enrollment by Cluster')
        axes[0,1].set_xlabel('Cluster')
        axes[0,1].set_ylabel('Average Enrollment')
        
        # Age distribution by cluster
        age_cols = ['avg_age_0_5', 'avg_age_5_17', 'avg_age_18_greater']
        cluster_age = district_features.groupby('cluster')[age_cols].mean()
        
        x = np.arange(len(cluster_age.index))
        width = 0.25
        
        for i, col in enumerate(age_cols):
            axes[1,0].bar(x + i*width, cluster_age[col], width, label=col.replace('avg_age_', '').replace('_', '-') + ' years')
        
        axes[1,0].set_title('Age Group Distribution by Cluster')
        axes[1,0].set_xlabel('Cluster')
        axes[1,0].set_ylabel('Average Count')
        axes[1,0].set_xticks(x + width)
        axes[1,0].set_xticklabels(cluster_age.index)
        axes[1,0].legend()
        
        # Scatter plot of key features
        scatter = axes[1,1].scatter(district_features['avg_total'], district_features['std_total'], 
                                  c=district_features['cluster'], cmap='viridis', alpha=0.6)
        axes[1,1].set_title('Districts by Average vs Standard Deviation')
        axes[1,1].set_xlabel('Average Total Enrollment')
        axes[1,1].set_ylabel('Standard Deviation')
        plt.colorbar(scatter, ax=axes[1,1])
        
        plt.tight_layout()
        plt.savefig('clustering_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Print cluster characteristics
        print("\nCLUSTER CHARACTERISTICS:")
        for cluster in sorted(district_features['cluster'].unique()):
            cluster_data = district_features[district_features['cluster'] == cluster]
            print(f"\nCluster {cluster} ({len(cluster_data)} districts):")
            print(f"  Average enrollment: {cluster_data['avg_total'].mean():.1f}")
            print(f"  Average std deviation: {cluster_data['std_total'].mean():.1f}")
            print(f"  Top states: {cluster_data['state'].value_counts().head(3).to_dict()}")
        
        return district_features
    
    def detect_anomalies(self):
        """Detect anomalies in the data using statistical methods"""
        print("\n" + "="*60)
        print("ANOMALY DETECTION ANALYSIS")
        print("="*60)
        
        anomalies_found = {}
        
        # Analyze enrollment data for anomalies
        if self.enroll_data is not None:
            # Statistical outliers using IQR method
            Q1 = self.enroll_data['total_enroll'].quantile(0.25)
            Q3 = self.enroll_data['total_enroll'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = self.enroll_data[(self.enroll_data['total_enroll'] < lower_bound) | 
                                      (self.enroll_data['total_enroll'] > upper_bound)]
            
            anomalies_found['enrollment_outliers'] = len(outliers)
            
            # Isolation Forest for multivariate anomalies
            features = ['age_0_5', 'age_5_17', 'age_18_greater', 'month', 'day']
            X = self.enroll_data[features].fillna(0)
            
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomaly_labels = iso_forest.fit_predict(X)
            
            anomalies_found['multivariate_anomalies'] = sum(anomaly_labels == -1)
            
            # Visualize anomalies
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('Anomaly Detection Results', fontsize=16, fontweight='bold')
            
            # Box plot for outliers
            axes[0,0].boxplot(self.enroll_data['total_enroll'])
            axes[0,0].set_title('Enrollment Distribution (Box Plot)')
            axes[0,0].set_ylabel('Total Enrollment')
            
            # Histogram with outliers marked
            axes[0,1].hist(self.enroll_data['total_enroll'], bins=50, alpha=0.7, color='skyblue')
            axes[0,1].axvline(lower_bound, color='red', linestyle='--', label='Lower Bound')
            axes[0,1].axvline(upper_bound, color='red', linestyle='--', label='Upper Bound')
            axes[0,1].set_title('Enrollment Distribution with Outlier Bounds')
            axes[0,1].set_xlabel('Total Enrollment')
            axes[0,1].set_ylabel('Frequency')
            axes[0,1].legend()
            
            # Anomaly scores
            anomaly_scores = iso_forest.decision_function(X)
            axes[1,0].hist(anomaly_scores, bins=50, alpha=0.7, color='orange')
            axes[1,0].set_title('Isolation Forest Anomaly Scores')
            axes[1,0].set_xlabel('Anomaly Score')
            axes[1,0].set_ylabel('Frequency')
            
            # Time series of anomalies
            daily_anomalies = self.enroll_data[anomaly_labels == -1].groupby('date').size()
            if len(daily_anomalies) > 0:
                axes[1,1].plot(daily_anomalies.index, daily_anomalies.values, marker='o', color='red')
                axes[1,1].set_title('Daily Anomaly Count')
                axes[1,1].set_xlabel('Date')
                axes[1,1].set_ylabel('Number of Anomalies')
                axes[1,1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('anomaly_detection.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        print("\nANOMALY DETECTION RESULTS:")
        for anomaly_type, count in anomalies_found.items():
            print(f"  {anomaly_type.replace('_', ' ').title()}: {count}")
        
        return anomalies_found
    
    def correlation_analysis(self):
        """Perform correlation analysis across different data types"""
        print("\n" + "="*60)
        print("CORRELATION ANALYSIS")
        print("="*60)
        
        # Create combined dataset for correlation analysis
        if all([self.bio_data is not None, self.demo_data is not None, self.enroll_data is not None]):
            
            # Aggregate by state and date for correlation
            bio_agg = self.bio_data.groupby(['state', 'date']).agg({
                'bio_age_5_17': 'sum',
                'bio_age_17_': 'sum',
                'total_bio': 'sum'
            }).reset_index()
            
            demo_agg = self.demo_data.groupby(['state', 'date']).agg({
                'demo_age_5_17': 'sum',
                'demo_age_17_': 'sum',
                'total_demo': 'sum'
            }).reset_index()
            
            enroll_agg = self.enroll_data.groupby(['state', 'date']).agg({
                'age_0_5': 'sum',
                'age_5_17': 'sum',
                'age_18_greater': 'sum',
                'total_enroll': 'sum'
            }).reset_index()
            
            # Merge datasets
            combined = enroll_agg.merge(bio_agg, on=['state', 'date'], how='outer')
            combined = combined.merge(demo_agg, on=['state', 'date'], how='outer')
            combined = combined.fillna(0)
            
            # Calculate correlation matrix
            numeric_cols = combined.select_dtypes(include=[np.number]).columns
            correlation_matrix = combined[numeric_cols].corr()
            
            # Visualize correlation matrix
            plt.figure(figsize=(14, 10))
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
            sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=0.5, cbar_kws={"shrink": .8})
            plt.title('Correlation Matrix - Aadhaar Services', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            # Print strong correlations
            print("\nSTRONG CORRELATIONS (|r| > 0.7):")
            strong_corr = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_val = correlation_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        strong_corr.append((correlation_matrix.columns[i], correlation_matrix.columns[j], corr_val))
            
            for var1, var2, corr in sorted(strong_corr, key=lambda x: abs(x[2]), reverse=True):
                print(f"  {var1} <-> {var2}: {corr:.3f}")
            
            return correlation_matrix
    
    def predictive_insights(self):
        """Generate predictive insights and trends"""
        print("\n" + "="*60)
        print("PREDICTIVE INSIGHTS AND TRENDS")
        print("="*60)
        
        insights = []
        
        if self.enroll_data is not None:
            # Trend analysis
            daily_trends = self.enroll_data.groupby('date')['total_enroll'].sum().sort_index()
            
            if len(daily_trends) > 1:
                # Calculate growth rate
                growth_rates = daily_trends.pct_change().dropna()
                avg_growth = growth_rates.mean()
                
                insights.append(f"Average daily growth rate: {avg_growth:.2%}")
                
                # Predict next period
                last_value = daily_trends.iloc[-1]
                predicted_next = last_value * (1 + avg_growth)
                insights.append(f"Predicted next day enrollment: {predicted_next:.0f}")
                
                # Seasonal patterns
                monthly_avg = self.enroll_data.groupby('month')['total_enroll'].mean()
                peak_month = monthly_avg.idxmax()
                low_month = monthly_avg.idxmin()
                
                insights.append(f"Peak enrollment month: {peak_month}")
                insights.append(f"Lowest enrollment month: {low_month}")
                
                # Weekly patterns
                weekly_avg = self.enroll_data.groupby('weekday')['total_enroll'].mean()
                peak_day = weekly_avg.idxmax()
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                
                insights.append(f"Peak enrollment day: {days[peak_day]}")
        
        # Service utilization predictions
        if all([self.bio_data is not None, self.demo_data is not None, self.enroll_data is not None]):
            total_enroll = self.enroll_data['total_enroll'].sum()
            total_bio = self.bio_data['total_bio'].sum()
            total_demo = self.demo_data['total_demo'].sum()
            
            # Calculate service ratios
            bio_ratio = total_bio / total_enroll if total_enroll > 0 else 0
            demo_ratio = total_demo / total_enroll if total_enroll > 0 else 0
            
            insights.append(f"Biometric update rate: {bio_ratio:.2f} per enrollment")
            insights.append(f"Demographic update rate: {demo_ratio:.2f} per enrollment")
            
            # Predict future service demand
            if total_enroll > 0:
                predicted_bio_demand = total_enroll * bio_ratio * 1.1  # 10% growth assumption
                predicted_demo_demand = total_enroll * demo_ratio * 1.1
                
                insights.append(f"Predicted biometric demand (10% growth): {predicted_bio_demand:.0f}")
                insights.append(f"Predicted demographic demand (10% growth): {predicted_demo_demand:.0f}")
        
        print("\nPREDICTIVE INSIGHTS:")
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
        
        return insights
    
    def generate_advanced_recommendations(self):
        """Generate advanced recommendations based on analytics"""
        print("\n" + "="*60)
        print("ADVANCED RECOMMENDATIONS")
        print("="*60)
        
        recommendations = [
            "PREDICTIVE RESOURCE ALLOCATION:",
            "• Use clustering analysis to categorize districts and allocate resources accordingly",
            "• Deploy predictive models to forecast peak demand periods",
            "• Implement dynamic staffing based on temporal patterns",
            "",
            "ANOMALY MONITORING SYSTEM:",
            "• Set up automated anomaly detection for real-time monitoring",
            "• Create alerts for unusual enrollment patterns that may indicate issues",
            "• Implement quality checks for data points flagged as anomalies",
            "",
            "SERVICE OPTIMIZATION:",
            "• Leverage correlation insights to optimize service delivery",
            "• Cross-promote services based on usage patterns",
            "• Implement targeted campaigns for underutilized services",
            "",
            "CAPACITY PLANNING:",
            "• Use growth rate predictions for infrastructure planning",
            "• Plan maintenance during predicted low-activity periods",
            "• Scale resources based on seasonal and weekly patterns",
            "",
            "DATA-DRIVEN POLICY MAKING:",
            "• Use district clustering to create targeted policies",
            "• Implement differentiated service strategies based on regional patterns",
            "• Monitor policy impact using established baseline metrics"
        ]
        
        for rec in recommendations:
            print(rec)
        
        return recommendations

def main():
    """Execute advanced analytics"""
    print("ADVANCED AADHAAR DATA ANALYTICS")
    print("="*60)
    
    # Initialize advanced analyzer
    analyzer = AdvancedAadhaarAnalytics()
    
    # Load and prepare data
    analyzer.load_and_prepare_data()
    
    # Perform advanced analyses
    district_clusters = analyzer.perform_clustering_analysis()
    anomalies = analyzer.detect_anomalies()
    correlations = analyzer.correlation_analysis()
    predictions = analyzer.predictive_insights()
    
    # Generate recommendations
    recommendations = analyzer.generate_advanced_recommendations()
    
    print("\n" + "="*60)
    print("ADVANCED ANALYSIS COMPLETED!")
    print("Generated: clustering_analysis.png, anomaly_detection.png, correlation_analysis.png")
    print("="*60)

if __name__ == "__main__":
    main()