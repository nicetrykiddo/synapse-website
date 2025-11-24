import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class DatasetAnalyzer:
    def __init__(self, base_path="C:/xampp/htdocs/clg/project/data"):
        self.base_path = base_path
        self.datasets = {
            'field': {'raw': None, 'cleaned': None},
            'manufacturing': {'raw': None, 'cleaned': None},
            'sales': {'raw': None, 'cleaned': None},
            'testing': {'raw': None, 'cleaned': None}
        }
        self.analysis_results = {}

    def load_datasets(self):
        """Load all raw and cleaned datasets"""
        print("=" * 80)
        print("LOADING DATASETS")
        print("=" * 80)

        for dataset_name in self.datasets.keys():
            try:
                # Load raw data
                raw_path = f"{self.base_path}/raw/{dataset_name}.csv"
                self.datasets[dataset_name]['raw'] = pd.read_csv(raw_path)
                print(f"\n[OK] Loaded RAW {dataset_name}.csv: {self.datasets[dataset_name]['raw'].shape}")

                # Load cleaned data
                cleaned_path = f"{self.base_path}/cleaned/cleaned_{dataset_name}.csv"
                self.datasets[dataset_name]['cleaned'] = pd.read_csv(cleaned_path)
                print(f"[OK] Loaded CLEANED {dataset_name}.csv: {self.datasets[dataset_name]['cleaned'].shape}")

            except Exception as e:
                print(f"[ERROR] Error loading {dataset_name}: {str(e)}")

    def calculate_statistics(self, df):
        """Calculate comprehensive statistics for a dataframe"""
        stats_dict = {
            'shape': df.shape,
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB",
            'total_missing': int(df.isnull().sum().sum()),
            'missing_percentage': float(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100),
            'duplicate_rows': int(df.duplicated().sum()),
            'columns': list(df.columns),
            'dtypes': df.dtypes.astype(str).to_dict(),
        }

        # Per-column statistics
        stats_dict['column_stats'] = {}
        for col in df.columns:
            col_stats = {
                'missing_count': int(df[col].isnull().sum()),
                'missing_percentage': float(df[col].isnull().sum() / len(df) * 100),
                'completeness': float((len(df) - df[col].isnull().sum()) / len(df) * 100),
                'unique_values': int(df[col].nunique()),
                'dtype': str(df[col].dtype)
            }

            # Numerical statistics
            if pd.api.types.is_numeric_dtype(df[col]):
                col_stats.update({
                    'mean': float(df[col].mean()) if not df[col].isnull().all() else None,
                    'median': float(df[col].median()) if not df[col].isnull().all() else None,
                    'std': float(df[col].std()) if not df[col].isnull().all() else None,
                    'min': float(df[col].min()) if not df[col].isnull().all() else None,
                    'max': float(df[col].max()) if not df[col].isnull().all() else None,
                    'q25': float(df[col].quantile(0.25)) if not df[col].isnull().all() else None,
                    'q75': float(df[col].quantile(0.75)) if not df[col].isnull().all() else None,
                    'skewness': float(df[col].skew()) if not df[col].isnull().all() else None,
                    'kurtosis': float(df[col].kurtosis()) if not df[col].isnull().all() else None,
                })

                # Detect outliers using IQR method
                if not df[col].isnull().all():
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                    col_stats['outliers_count'] = int(outliers)
                    col_stats['outliers_percentage'] = float(outliers / len(df) * 100)

            # Categorical statistics
            else:
                col_stats['top_values'] = df[col].value_counts().head(5).to_dict()
                col_stats['most_frequent'] = str(df[col].mode()[0]) if len(df[col].mode()) > 0 else None
                col_stats['frequency_of_most_common'] = int(df[col].value_counts().iloc[0]) if len(df[col].value_counts()) > 0 else 0

            stats_dict['column_stats'][col] = col_stats

        # Data quality score
        completeness_score = (1 - stats_dict['missing_percentage'] / 100) * 100
        duplicate_score = (1 - stats_dict['duplicate_rows'] / df.shape[0]) * 100 if df.shape[0] > 0 else 100
        stats_dict['quality_score'] = float((completeness_score * 0.6 + duplicate_score * 0.4))

        return stats_dict

    def analyze_all_datasets(self):
        """Perform comprehensive analysis on all datasets"""
        print("\n" + "=" * 80)
        print("COMPREHENSIVE DATA ANALYSIS")
        print("=" * 80)

        for dataset_name, versions in self.datasets.items():
            print(f"\n{'='*80}")
            print(f"ANALYZING: {dataset_name.upper()}")
            print(f"{'='*80}")

            self.analysis_results[dataset_name] = {}

            for version in ['raw', 'cleaned']:
                df = versions[version]
                if df is not None:
                    print(f"\n--- {version.upper()} VERSION ---")
                    stats = self.calculate_statistics(df)
                    self.analysis_results[dataset_name][version] = stats

                    print(f"Shape: {stats['shape'][0]} rows × {stats['shape'][1]} columns")
                    print(f"Memory: {stats['memory_usage']}")
                    print(f"Missing Values: {stats['total_missing']} ({stats['missing_percentage']:.2f}%)")
                    print(f"Duplicates: {stats['duplicate_rows']}")
                    print(f"Quality Score: {stats['quality_score']:.2f}%")

                    # Print column statistics
                    print(f"\nColumn Statistics:")
                    for col, col_stats in stats['column_stats'].items():
                        print(f"  • {col}:")
                        print(f"    - Type: {col_stats['dtype']}")
                        print(f"    - Missing: {col_stats['missing_count']} ({col_stats['missing_percentage']:.2f}%)")
                        print(f"    - Completeness: {col_stats['completeness']:.2f}%")
                        print(f"    - Unique Values: {col_stats['unique_values']}")

                        if 'mean' in col_stats and col_stats['mean'] is not None:
                            print(f"    - Mean: {col_stats['mean']:.4f}")
                            print(f"    - Median: {col_stats['median']:.4f}")
                            print(f"    - Std Dev: {col_stats['std']:.4f}")
                            print(f"    - Range: [{col_stats['min']:.4f}, {col_stats['max']:.4f}]")
                            if 'outliers_count' in col_stats:
                                print(f"    - Outliers: {col_stats['outliers_count']} ({col_stats['outliers_percentage']:.2f}%)")

        # Save analysis results
        output_path = f"{self.base_path}/../analysis_results.json"
        with open(output_path, 'w') as f:
            json.dump(self.analysis_results, f, indent=2)
        print(f"\n[OK] Analysis results saved to: {output_path}")

    def create_visualizations(self):
        """Create comprehensive visualizations for all datasets"""
        print("\n" + "=" * 80)
        print("GENERATING VISUALIZATIONS")
        print("=" * 80)

        viz_path = f"{self.base_path}/../visualizations"
        os.makedirs(viz_path, exist_ok=True)

        for dataset_name, versions in self.datasets.items():
            print(f"\n--- Creating visualizations for {dataset_name.upper()} ---")

            raw_df = versions['raw']
            cleaned_df = versions['cleaned']

            if raw_df is None or cleaned_df is None:
                continue

            # 1. Data Quality Comparison
            self._create_quality_comparison(dataset_name, raw_df, cleaned_df, viz_path)

            # 2. Missing Values Heatmap
            self._create_missing_values_heatmap(dataset_name, raw_df, cleaned_df, viz_path)

            # 3. Numerical Distribution Plots
            self._create_distribution_plots(dataset_name, raw_df, cleaned_df, viz_path)

            # 4. Categorical Analysis
            self._create_categorical_plots(dataset_name, raw_df, cleaned_df, viz_path)

            # 5. Correlation Heatmap
            self._create_correlation_heatmap(dataset_name, raw_df, cleaned_df, viz_path)

            # 6. Outlier Detection
            self._create_outlier_plots(dataset_name, raw_df, cleaned_df, viz_path)

        print(f"\n[OK] All visualizations saved to: {viz_path}")

    def _create_quality_comparison(self, name, raw_df, cleaned_df, path):
        """Create data quality comparison chart"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(f'{name.upper()} - Data Quality Comparison', fontsize=16, fontweight='bold')

        # Missing values comparison
        raw_missing = (raw_df.isnull().sum().sum() / (raw_df.shape[0] * raw_df.shape[1])) * 100
        cleaned_missing = (cleaned_df.isnull().sum().sum() / (cleaned_df.shape[0] * cleaned_df.shape[1])) * 100

        axes[0].bar(['Raw', 'Cleaned'], [raw_missing, cleaned_missing], color=['#e74c3c', '#27ae60'])
        axes[0].set_ylabel('Missing Values (%)')
        axes[0].set_title('Missing Values Comparison')
        axes[0].set_ylim(0, max(raw_missing, cleaned_missing) * 1.2 if raw_missing > 0 else 10)

        # Duplicate comparison
        raw_dupes = (raw_df.duplicated().sum() / len(raw_df)) * 100
        cleaned_dupes = (cleaned_df.duplicated().sum() / len(cleaned_df)) * 100

        axes[1].bar(['Raw', 'Cleaned'], [raw_dupes, cleaned_dupes], color=['#e74c3c', '#27ae60'])
        axes[1].set_ylabel('Duplicate Rows (%)')
        axes[1].set_title('Duplicate Rows Comparison')
        axes[1].set_ylim(0, max(raw_dupes, cleaned_dupes) * 1.2 if raw_dupes > 0 else 10)

        # Record count comparison
        axes[2].bar(['Raw', 'Cleaned'], [len(raw_df), len(cleaned_df)], color=['#3498db', '#2ecc71'])
        axes[2].set_ylabel('Number of Records')
        axes[2].set_title('Record Count Comparison')

        plt.tight_layout()
        plt.savefig(f'{path}/{name}_quality_comparison.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Quality comparison chart saved")

    def _create_missing_values_heatmap(self, name, raw_df, cleaned_df, path):
        """Create missing values heatmap"""
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle(f'{name.upper()} - Missing Values Heatmap', fontsize=16, fontweight='bold')

        # Raw data heatmap
        if raw_df.isnull().sum().sum() > 0:
            sns.heatmap(raw_df.isnull(), cbar=True, yticklabels=False, cmap='YlOrRd', ax=axes[0])
            axes[0].set_title(f'Raw Data (Missing: {raw_df.isnull().sum().sum()})')
        else:
            axes[0].text(0.5, 0.5, 'No Missing Values', ha='center', va='center', fontsize=14)
            axes[0].set_title('Raw Data')

        # Cleaned data heatmap
        if cleaned_df.isnull().sum().sum() > 0:
            sns.heatmap(cleaned_df.isnull(), cbar=True, yticklabels=False, cmap='YlOrRd', ax=axes[1])
            axes[1].set_title(f'Cleaned Data (Missing: {cleaned_df.isnull().sum().sum()})')
        else:
            axes[1].text(0.5, 0.5, 'No Missing Values', ha='center', va='center', fontsize=14)
            axes[1].set_title('Cleaned Data')

        plt.tight_layout()
        plt.savefig(f'{path}/{name}_missing_values_heatmap.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Missing values heatmap saved")

    def _create_distribution_plots(self, name, raw_df, cleaned_df, path):
        """Create distribution plots for numerical columns"""
        numeric_cols = raw_df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) == 0:
            print(f"  [WARNING] No numerical columns found in {name}")
            return

        num_plots = min(len(numeric_cols), 6)  # Limit to 6 plots
        rows = (num_plots + 2) // 3

        fig, axes = plt.subplots(rows, 3, figsize=(18, rows * 5))
        fig.suptitle(f'{name.upper()} - Distribution Plots (Raw vs Cleaned)', fontsize=16, fontweight='bold')
        axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

        for idx, col in enumerate(numeric_cols[:num_plots]):
            ax = axes[idx]

            # Plot raw data
            raw_data = raw_df[col].dropna()
            if len(raw_data) > 0:
                ax.hist(raw_data, bins=30, alpha=0.5, label='Raw', color='red', edgecolor='black')

            # Plot cleaned data
            cleaned_data = cleaned_df[col].dropna()
            if len(cleaned_data) > 0:
                ax.hist(cleaned_data, bins=30, alpha=0.5, label='Cleaned', color='green', edgecolor='black')

            ax.set_xlabel(col)
            ax.set_ylabel('Frequency')
            ax.set_title(f'{col} Distribution')
            ax.legend()
            ax.grid(True, alpha=0.3)

        # Hide unused subplots
        for idx in range(num_plots, len(axes)):
            axes[idx].axis('off')

        plt.tight_layout()
        plt.savefig(f'{path}/{name}_distributions.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Distribution plots saved")

    def _create_categorical_plots(self, name, raw_df, cleaned_df, path):
        """Create plots for categorical columns"""
        categorical_cols = cleaned_df.select_dtypes(include=['object', 'category']).columns.tolist()

        if len(categorical_cols) == 0:
            print(f"  [WARNING] No categorical columns found in {name}")
            return

        num_plots = min(len(categorical_cols), 6)
        rows = (num_plots + 1) // 2

        fig, axes = plt.subplots(rows, 2, figsize=(16, rows * 5))
        fig.suptitle(f'{name.upper()} - Categorical Analysis', fontsize=16, fontweight='bold')
        axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

        for idx, col in enumerate(categorical_cols[:num_plots]):
            ax = axes[idx]

            # Get top categories
            cleaned_counts = cleaned_df[col].value_counts().head(10)

            ax.bar(range(len(cleaned_counts)), cleaned_counts.values, color='steelblue', edgecolor='black')
            ax.set_xticks(range(len(cleaned_counts)))
            ax.set_xticklabels(cleaned_counts.index, rotation=45, ha='right')
            ax.set_ylabel('Count')
            ax.set_title(f'{col} - Top Categories (Cleaned Data)')
            ax.grid(True, alpha=0.3, axis='y')

        # Hide unused subplots
        for idx in range(num_plots, len(axes)):
            axes[idx].axis('off')

        plt.tight_layout()
        plt.savefig(f'{path}/{name}_categorical.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Categorical analysis saved")

    def _create_correlation_heatmap(self, name, raw_df, cleaned_df, path):
        """Create correlation heatmap for numerical columns"""
        numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) < 2:
            print(f"  [WARNING] Not enough numerical columns for correlation in {name}")
            return

        fig, axes = plt.subplots(1, 2, figsize=(18, 7))
        fig.suptitle(f'{name.upper()} - Correlation Heatmap', fontsize=16, fontweight='bold')

        # Raw correlation
        raw_corr = raw_df[numeric_cols].corr()
        sns.heatmap(raw_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                    square=True, ax=axes[0], cbar_kws={'label': 'Correlation'})
        axes[0].set_title('Raw Data Correlation')

        # Cleaned correlation
        cleaned_corr = cleaned_df[numeric_cols].corr()
        sns.heatmap(cleaned_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                    square=True, ax=axes[1], cbar_kws={'label': 'Correlation'})
        axes[1].set_title('Cleaned Data Correlation')

        plt.tight_layout()
        plt.savefig(f'{path}/{name}_correlation.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Correlation heatmap saved")

    def _create_outlier_plots(self, name, raw_df, cleaned_df, path):
        """Create box plots to show outliers"""
        numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_cols) == 0:
            print(f"  [WARNING] No numerical columns for outlier detection in {name}")
            return

        num_plots = min(len(numeric_cols), 6)
        rows = (num_plots + 2) // 3

        fig, axes = plt.subplots(rows, 3, figsize=(18, rows * 5))
        fig.suptitle(f'{name.upper()} - Outlier Detection (Box Plots)', fontsize=16, fontweight='bold')
        axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]

        for idx, col in enumerate(numeric_cols[:num_plots]):
            ax = axes[idx]

            # Prepare data
            data_to_plot = [
                raw_df[col].dropna().values,
                cleaned_df[col].dropna().values
            ]

            bp = ax.boxplot(data_to_plot, labels=['Raw', 'Cleaned'], patch_artist=True)

            # Color boxes
            colors = ['lightcoral', 'lightgreen']
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)

            ax.set_ylabel(col)
            ax.set_title(f'{col} - Outlier Comparison')
            ax.grid(True, alpha=0.3, axis='y')

        # Hide unused subplots
        for idx in range(num_plots, len(axes)):
            axes[idx].axis('off')

        plt.tight_layout()
        plt.savefig(f'{path}/{name}_outliers.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Outlier detection plots saved")

    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print("\n" + "=" * 80)
        print("GENERATING SUMMARY REPORT")
        print("=" * 80)

        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("DATA ANALYSIS SUMMARY REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"\nGenerated on: {pd.Timestamp.now()}")
        report_lines.append(f"\nTotal Datasets Analyzed: {len(self.datasets)}")

        # Overall statistics
        total_raw_records = sum([len(v['raw']) for v in self.datasets.values() if v['raw'] is not None])
        total_cleaned_records = sum([len(v['cleaned']) for v in self.datasets.values() if v['cleaned'] is not None])

        report_lines.append(f"\n--- OVERALL STATISTICS ---")
        report_lines.append(f"Total Raw Records: {total_raw_records:,}")
        report_lines.append(f"Total Cleaned Records: {total_cleaned_records:,}")
        report_lines.append(f"Records Removed: {total_raw_records - total_cleaned_records:,}")
        report_lines.append(f"Data Retention Rate: {(total_cleaned_records / total_raw_records * 100):.2f}%")

        # Per-dataset summary
        for dataset_name, analysis in self.analysis_results.items():
            report_lines.append(f"\n{'='*80}")
            report_lines.append(f"DATASET: {dataset_name.upper()}")
            report_lines.append(f"{'='*80}")

            if 'raw' in analysis and 'cleaned' in analysis:
                raw_stats = analysis['raw']
                cleaned_stats = analysis['cleaned']

                report_lines.append(f"\n--- RAW DATA ---")
                report_lines.append(f"Records: {raw_stats['shape'][0]:,}")
                report_lines.append(f"Columns: {raw_stats['shape'][1]}")
                report_lines.append(f"Missing Values: {raw_stats['total_missing']:,} ({raw_stats['missing_percentage']:.2f}%)")
                report_lines.append(f"Duplicates: {raw_stats['duplicate_rows']:,}")
                report_lines.append(f"Quality Score: {raw_stats['quality_score']:.2f}%")

                report_lines.append(f"\n--- CLEANED DATA ---")
                report_lines.append(f"Records: {cleaned_stats['shape'][0]:,}")
                report_lines.append(f"Columns: {cleaned_stats['shape'][1]}")
                report_lines.append(f"Missing Values: {cleaned_stats['total_missing']:,} ({cleaned_stats['missing_percentage']:.2f}%)")
                report_lines.append(f"Duplicates: {cleaned_stats['duplicate_rows']:,}")
                report_lines.append(f"Quality Score: {cleaned_stats['quality_score']:.2f}%")

                report_lines.append(f"\n--- IMPROVEMENTS ---")
                missing_improvement = raw_stats['missing_percentage'] - cleaned_stats['missing_percentage']
                dupe_improvement = raw_stats['duplicate_rows'] - cleaned_stats['duplicate_rows']
                quality_improvement = cleaned_stats['quality_score'] - raw_stats['quality_score']

                report_lines.append(f"Missing Values Reduced: {missing_improvement:.2f}%")
                report_lines.append(f"Duplicates Removed: {dupe_improvement}")
                report_lines.append(f"Quality Score Improved: {quality_improvement:.2f}%")

        report_lines.append(f"\n{'='*80}")
        report_lines.append("END OF REPORT")
        report_lines.append(f"{'='*80}")

        # Save report
        report_path = f"{self.base_path}/../analysis_summary_report.txt"
        with open(report_path, 'w') as f:
            f.write('\n'.join(report_lines))

        # Print report
        print('\n'.join(report_lines))
        print(f"\n[OK] Summary report saved to: {report_path}")

def main():
    print("\n" + "=" * 80)
    print("COMPREHENSIVE DATA ANALYSIS & VISUALIZATION SYSTEM")
    print("=" * 80)
    print("Analyzing: field, manufacturing, sales, testing datasets")
    print("Versions: Raw and Cleaned")
    print("=" * 80)

    analyzer = DatasetAnalyzer()

    # Step 1: Load all datasets
    analyzer.load_datasets()

    # Step 2: Analyze all datasets
    analyzer.analyze_all_datasets()

    # Step 3: Create visualizations
    analyzer.create_visualizations()

    # Step 4: Generate summary report
    analyzer.generate_summary_report()

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nGenerated Files:")
    print("  1. analysis_results.json - Detailed statistical analysis")
    print("  2. analysis_summary_report.txt - Human-readable summary")
    print("  3. visualizations/ - All charts and graphs")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
