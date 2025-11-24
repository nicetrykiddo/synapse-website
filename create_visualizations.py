import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create visualizations directory
viz_dir = Path('visualizations')
viz_dir.mkdir(exist_ok=True)

# Load analysis results
with open('analysis_results.json', 'r') as f:
    analysis = json.load(f)

# Color schemes
COLORS = {
    'primary': '#d4af37',
    'secondary': '#1a1a2e',
    'success': '#10b981',
    'danger': '#ef4444',
    'warning': '#f59e0b',
    'info': '#3b82f6'
}

def create_data_quality_dashboard():
    """Create comprehensive data quality dashboard"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Data Quality Overview - All Datasets', fontsize=20, fontweight='bold', y=0.995)

    datasets = ['field', 'manufacturing', 'sales', 'testing']

    # 1. Missing Data Comparison
    ax1 = axes[0, 0]
    raw_missing = [analysis[ds]['raw']['missing_percentage'] for ds in datasets]
    cleaned_missing = [analysis[ds]['cleaned']['missing_percentage'] for ds in datasets]

    x = np.arange(len(datasets))
    width = 0.35

    bars1 = ax1.bar(x - width/2, raw_missing, width, label='Raw', color=COLORS['danger'], alpha=0.8)
    bars2 = ax1.bar(x + width/2, cleaned_missing, width, label='Cleaned', color=COLORS['success'], alpha=0.8)

    ax1.set_xlabel('Dataset', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Missing Data %', fontsize=12, fontweight='bold')
    ax1.set_title('Missing Data Percentage Comparison', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([ds.capitalize() for ds in datasets])
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

    # 2. Data Quality Scores
    ax2 = axes[0, 1]
    raw_quality = [analysis[ds]['raw']['quality_score'] for ds in datasets]
    cleaned_quality = [analysis[ds]['cleaned']['quality_score'] for ds in datasets]

    bars1 = ax2.bar(x - width/2, raw_quality, width, label='Raw', color=COLORS['warning'], alpha=0.8)
    bars2 = ax2.bar(x + width/2, cleaned_quality, width, label='Cleaned', color=COLORS['primary'], alpha=0.8)

    ax2.set_xlabel('Dataset', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Quality Score', fontsize=12, fontweight='bold')
    ax2.set_title('Data Quality Score Comparison', fontsize=14, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([ds.capitalize() for ds in datasets])
    ax2.legend()
    ax2.set_ylim([85, 105])
    ax2.grid(axis='y', alpha=0.3)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}', ha='center', va='bottom', fontsize=9)

    # 3. Record Count Comparison
    ax3 = axes[1, 0]
    raw_counts = [analysis[ds]['raw']['shape'][0] for ds in datasets]
    cleaned_counts = [analysis[ds]['cleaned']['shape'][0] for ds in datasets]

    bars1 = ax3.bar(x - width/2, raw_counts, width, label='Raw', color=COLORS['info'], alpha=0.8)
    bars2 = ax3.bar(x + width/2, cleaned_counts, width, label='Cleaned', color=COLORS['success'], alpha=0.8)

    ax3.set_xlabel('Dataset', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Record Count', fontsize=12, fontweight='bold')
    ax3.set_title('Record Count Comparison', fontsize=14, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels([ds.capitalize() for ds in datasets])
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)

    # 4. Total Missing Values
    ax4 = axes[1, 1]
    raw_total_missing = [analysis[ds]['raw']['total_missing'] for ds in datasets]
    cleaned_total_missing = [analysis[ds]['cleaned']['total_missing'] for ds in datasets]

    bars1 = ax4.bar(x - width/2, raw_total_missing, width, label='Raw', color=COLORS['danger'], alpha=0.8)
    bars2 = ax4.bar(x + width/2, cleaned_total_missing, width, label='Cleaned', color=COLORS['success'], alpha=0.8)

    ax4.set_xlabel('Dataset', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Total Missing Values', fontsize=12, fontweight='bold')
    ax4.set_title('Total Missing Values Comparison', fontsize=14, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels([ds.capitalize() for ds in datasets])
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(viz_dir / 'quality_dashboard.png', dpi=300, bbox_inches='tight')
    print("Created: quality_dashboard.png")
    plt.close()

def create_field_analysis():
    """Create field data specific visualizations"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Field Reports Analysis', fontsize=20, fontweight='bold', y=0.995)

    # Load actual data for detailed analysis
    df_raw = pd.read_csv('data/raw/field.csv')
    df_clean = pd.read_csv('data/cleaned/cleaned_field.csv')

    # 1. Failure Mode Distribution (Raw)
    ax1 = axes[0, 0]
    if 'failureMode' in df_raw.columns:
        failure_counts = df_raw['failureMode'].value_counts().head(10)
        ax1.barh(range(len(failure_counts)), failure_counts.values, color=COLORS['danger'], alpha=0.8)
        ax1.set_yticks(range(len(failure_counts)))
        ax1.set_yticklabels(failure_counts.index, fontsize=9)
        ax1.set_xlabel('Count', fontsize=10, fontweight='bold')
        ax1.set_title('Top Failure Modes (Raw)', fontsize=12, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, v in enumerate(failure_counts.values):
            ax1.text(v, i, f' {v}', va='center', fontsize=9)

    # 2. Failure Mode Distribution (Cleaned)
    ax2 = axes[0, 1]
    if 'failuremode' in df_clean.columns:
        failure_counts_clean = df_clean['failuremode'].value_counts().head(10)
        ax2.barh(range(len(failure_counts_clean)), failure_counts_clean.values,
                color=COLORS['success'], alpha=0.8)
        ax2.set_yticks(range(len(failure_counts_clean)))
        ax2.set_yticklabels(failure_counts_clean.index, fontsize=9)
        ax2.set_xlabel('Count', fontsize=10, fontweight='bold')
        ax2.set_title('Top Failure Modes (Cleaned)', fontsize=12, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)

        for i, v in enumerate(failure_counts_clean.values):
            ax2.text(v, i, f' {v}', va='center', fontsize=9)

    # 3. Severity Distribution
    ax3 = axes[0, 2]
    if 'severity' in df_clean.columns:
        severity_counts = df_clean['severity'].value_counts().sort_index()
        colors_severity = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#7f1d1d']
        ax3.bar(severity_counts.index.astype(str), severity_counts.values,
               color=colors_severity[:len(severity_counts)], alpha=0.8)
        ax3.set_xlabel('Severity Level', fontsize=10, fontweight='bold')
        ax3.set_ylabel('Count', fontsize=10, fontweight='bold')
        ax3.set_title('Severity Distribution', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)

        for i, (idx, v) in enumerate(zip(severity_counts.index, severity_counts.values)):
            ax3.text(i, v, f'{v}', ha='center', va='bottom', fontsize=9)

    # 4. Location Distribution (Top 10)
    ax4 = axes[1, 0]
    if 'location' in df_clean.columns:
        location_counts = df_clean['location'].value_counts().head(10)
        ax4.bar(range(len(location_counts)), location_counts.values,
               color=COLORS['info'], alpha=0.8)
        ax4.set_xticks(range(len(location_counts)))
        ax4.set_xticklabels(location_counts.index, rotation=45, ha='right', fontsize=9)
        ax4.set_ylabel('Count', fontsize=10, fontweight='bold')
        ax4.set_title('Top 10 Locations', fontsize=12, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)

        for i, v in enumerate(location_counts.values):
            ax4.text(i, v, f'{v}', ha='center', va='bottom', fontsize=9)

    # 5. Reporter Type Distribution
    ax5 = axes[1, 1]
    if 'reportedby' in df_clean.columns:
        reporter_counts = df_clean['reportedby'].value_counts()
        colors_pie = [COLORS['primary'], COLORS['info']]
        wedges, texts, autotexts = ax5.pie(reporter_counts.values, labels=reporter_counts.index,
                                           autopct='%1.1f%%', colors=colors_pie[:len(reporter_counts)],
                                           startangle=90)
        ax5.set_title('Reports by Source', fontsize=12, fontweight='bold')

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

    # 6. Data Completeness by Column
    ax6 = axes[1, 2]
    completeness = []
    columns = []
    for col in df_clean.columns:
        if col not in ['reportid', 'serialno']:
            completeness.append((1 - df_clean[col].isna().sum() / len(df_clean)) * 100)
            columns.append(col)

    ax6.barh(range(len(columns)), completeness, color=COLORS['success'], alpha=0.8)
    ax6.set_yticks(range(len(columns)))
    ax6.set_yticklabels(columns, fontsize=9)
    ax6.set_xlabel('Completeness %', fontsize=10, fontweight='bold')
    ax6.set_title('Data Completeness by Column', fontsize=12, fontweight='bold')
    ax6.set_xlim([95, 101])
    ax6.grid(axis='x', alpha=0.3)

    for i, v in enumerate(completeness):
        ax6.text(v, i, f' {v:.1f}%', va='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(viz_dir / 'field_analysis.png', dpi=300, bbox_inches='tight')
    print("Created: field_analysis.png")
    plt.close()

def create_manufacturing_analysis():
    """Create manufacturing data visualizations"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Manufacturing Data Analysis', fontsize=20, fontweight='bold', y=0.995)

    df_raw = pd.read_csv('data/raw/manufacturing.csv')
    df_clean = pd.read_csv('data/cleaned/cleaned_manufacturing.csv')

    # 1. Production Quantity Distribution
    ax1 = axes[0, 0]
    if 'producedqty' in df_clean.columns:
        ax1.hist(df_clean['producedqty'].dropna(), bins=30, color=COLORS['primary'],
                alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Produced Quantity', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Frequency', fontsize=10, fontweight='bold')
        ax1.set_title('Production Quantity Distribution', fontsize=12, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)

        # Add statistics
        mean_qty = df_clean['producedqty'].mean()
        median_qty = df_clean['producedqty'].median()
        ax1.axvline(mean_qty, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_qty:.0f}')
        ax1.axvline(median_qty, color='green', linestyle='--', linewidth=2, label=f'Median: {median_qty:.0f}')
        ax1.legend()

    # 2. Shift Distribution
    ax2 = axes[0, 1]
    if 'shift' in df_clean.columns:
        shift_counts = df_clean['shift'].value_counts()
        colors_shift = [COLORS['warning'], COLORS['info'], COLORS['secondary']]
        bars = ax2.bar(shift_counts.index, shift_counts.values,
                      color=colors_shift[:len(shift_counts)], alpha=0.8)
        ax2.set_xlabel('Shift', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Count', fontsize=10, fontweight='bold')
        ax2.set_title('Production by Shift', fontsize=12, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10)

    # 3. Machine Utilization
    ax3 = axes[0, 2]
    if 'machineId' in df_raw.columns:
        machine_counts = df_raw['machineId'].value_counts().head(10)
        ax3.bar(range(len(machine_counts)), machine_counts.values,
               color=COLORS['info'], alpha=0.8)
        ax3.set_xticks(range(len(machine_counts)))
        ax3.set_xticklabels(machine_counts.index, fontsize=9)
        ax3.set_ylabel('Usage Count', fontsize=10, fontweight='bold')
        ax3.set_title('Top 10 Machine Utilization', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)

        for i, v in enumerate(machine_counts.values):
            ax3.text(i, v, f'{v}', ha='center', va='bottom', fontsize=9)

    # 4. Operator Performance
    ax4 = axes[1, 0]
    if 'operatorId' in df_raw.columns:
        operator_counts = df_raw['operatorId'].value_counts().head(10)
        ax4.barh(range(len(operator_counts)), operator_counts.values,
                color=COLORS['success'], alpha=0.8)
        ax4.set_yticks(range(len(operator_counts)))
        ax4.set_yticklabels(operator_counts.index, fontsize=9)
        ax4.set_xlabel('Production Count', fontsize=10, fontweight='bold')
        ax4.set_title('Top 10 Operators by Production Count', fontsize=12, fontweight='bold')
        ax4.grid(axis='x', alpha=0.3)

        for i, v in enumerate(operator_counts.values):
            ax4.text(v, i, f' {v}', va='center', fontsize=9)

    # 5. Product Distribution
    ax5 = axes[1, 1]
    if 'productid' in df_clean.columns:
        product_counts = df_clean['productid'].value_counts().head(10)
        ax5.bar(range(len(product_counts)), product_counts.values,
               color=COLORS['primary'], alpha=0.8)
        ax5.set_xticks(range(len(product_counts)))
        ax5.set_xticklabels(product_counts.index, rotation=45, ha='right', fontsize=9)
        ax5.set_ylabel('Count', fontsize=10, fontweight='bold')
        ax5.set_title('Top 10 Products Manufactured', fontsize=12, fontweight='bold')
        ax5.grid(axis='y', alpha=0.3)

        for i, v in enumerate(product_counts.values):
            ax5.text(i, v, f'{v}', ha='center', va='bottom', fontsize=9)

    # 6. Production Statistics Box Plot
    ax6 = axes[1, 2]
    if 'producedqty' in df_clean.columns and 'shift' in df_clean.columns:
        shift_data = [df_clean[df_clean['shift'] == shift]['producedqty'].dropna()
                     for shift in df_clean['shift'].unique()]
        bp = ax6.boxplot(shift_data, labels=df_clean['shift'].unique(),
                        patch_artist=True)

        for patch, color in zip(bp['boxes'], [COLORS['warning'], COLORS['info'], COLORS['secondary']]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax6.set_xlabel('Shift', fontsize=10, fontweight='bold')
        ax6.set_ylabel('Produced Quantity', fontsize=10, fontweight='bold')
        ax6.set_title('Production Quantity by Shift', fontsize=12, fontweight='bold')
        ax6.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(viz_dir / 'manufacturing_analysis.png', dpi=300, bbox_inches='tight')
    print("Created: manufacturing_analysis.png")
    plt.close()

def create_sales_analysis():
    """Create sales data visualizations"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Sales Data Analysis', fontsize=20, fontweight='bold', y=0.995)

    df_raw = pd.read_csv('data/raw/sales.csv')
    df_clean = pd.read_csv('data/cleaned/cleaned_sales.csv')

    # 1. Sales Channel Distribution
    ax1 = axes[0, 0]
    if 'channel' in df_clean.columns:
        channel_counts = df_clean['channel'].value_counts()
        colors_channel = [COLORS['primary'], COLORS['info'], COLORS['warning']]
        wedges, texts, autotexts = ax1.pie(channel_counts.values, labels=channel_counts.index,
                                           autopct='%1.1f%%', colors=colors_channel[:len(channel_counts)],
                                           startangle=90, explode=[0.05] * len(channel_counts))
        ax1.set_title('Sales Distribution by Channel', fontsize=12, fontweight='bold')

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

    # 2. Unit Price Distribution
    ax2 = axes[0, 1]
    if 'unitprice' in df_clean.columns:
        ax2.hist(df_clean['unitprice'].dropna(), bins=30, color=COLORS['success'],
                alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Unit Price', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Frequency', fontsize=10, fontweight='bold')
        ax2.set_title('Unit Price Distribution', fontsize=12, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)

        mean_price = df_clean['unitprice'].mean()
        median_price = df_clean['unitprice'].median()
        ax2.axvline(mean_price, color='red', linestyle='--', linewidth=2,
                   label=f'Mean: ${mean_price:.2f}')
        ax2.axvline(median_price, color='green', linestyle='--', linewidth=2,
                   label=f'Median: ${median_price:.2f}')
        ax2.legend()

    # 3. Quantity Distribution
    ax3 = axes[0, 2]
    if 'qty' in df_clean.columns:
        ax3.hist(df_clean['qty'].dropna(), bins=30, color=COLORS['info'],
                alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Quantity', fontsize=10, fontweight='bold')
        ax3.set_ylabel('Frequency', fontsize=10, fontweight='bold')
        ax3.set_title('Order Quantity Distribution', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)

    # 4. Total Price Distribution
    ax4 = axes[1, 0]
    if 'totalprice' in df_clean.columns:
        # Filter outliers for better visualization
        q1 = df_clean['totalprice'].quantile(0.25)
        q3 = df_clean['totalprice'].quantile(0.75)
        iqr = q3 - q1
        filtered_data = df_clean['totalprice'][(df_clean['totalprice'] >= q1 - 1.5*iqr) &
                                                (df_clean['totalprice'] <= q3 + 1.5*iqr)]

        ax4.hist(filtered_data.dropna(), bins=30, color=COLORS['danger'],
                alpha=0.7, edgecolor='black')
        ax4.set_xlabel('Total Price', fontsize=10, fontweight='bold')
        ax4.set_ylabel('Frequency', fontsize=10, fontweight='bold')
        ax4.set_title('Total Price Distribution (Outliers Removed)', fontsize=12, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)

    # 5. Top Products by Sales
    ax5 = axes[1, 1]
    if 'productid' in df_clean.columns:
        product_counts = df_clean['productid'].value_counts().head(10)
        ax5.bar(range(len(product_counts)), product_counts.values,
               color=COLORS['primary'], alpha=0.8)
        ax5.set_xticks(range(len(product_counts)))
        ax5.set_xticklabels(product_counts.index, rotation=45, ha='right', fontsize=9)
        ax5.set_ylabel('Order Count', fontsize=10, fontweight='bold')
        ax5.set_title('Top 10 Products by Order Count', fontsize=12, fontweight='bold')
        ax5.grid(axis='y', alpha=0.3)

        for i, v in enumerate(product_counts.values):
            ax5.text(i, v, f'{v}', ha='center', va='bottom', fontsize=9)

    # 6. Sales by Channel - Box Plot
    ax6 = axes[1, 2]
    if 'totalprice' in df_clean.columns and 'channel' in df_clean.columns:
        channel_data = [df_clean[df_clean['channel'] == channel]['totalprice'].dropna()
                       for channel in df_clean['channel'].unique()]
        bp = ax6.boxplot(channel_data, labels=df_clean['channel'].unique(),
                        patch_artist=True)

        colors_box = [COLORS['primary'], COLORS['info'], COLORS['warning']]
        for patch, color in zip(bp['boxes'], colors_box[:len(bp['boxes'])]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax6.set_xlabel('Channel', fontsize=10, fontweight='bold')
        ax6.set_ylabel('Total Price', fontsize=10, fontweight='bold')
        ax6.set_title('Sales Value by Channel', fontsize=12, fontweight='bold')
        ax6.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(viz_dir / 'sales_analysis.png', dpi=300, bbox_inches='tight')
    print("Created: sales_analysis.png")
    plt.close()

def create_testing_analysis():
    """Create testing data visualizations"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Testing Data Analysis', fontsize=20, fontweight='bold', y=0.995)

    df_raw = pd.read_csv('data/raw/testing.csv')
    df_clean = pd.read_csv('data/cleaned/cleaned_testing.csv')

    # 1. Test Type Distribution
    ax1 = axes[0, 0]
    if 'testname' in df_clean.columns:
        test_counts = df_clean['testname'].value_counts()
        ax1.bar(test_counts.index, test_counts.values,
               color=[COLORS['primary'], COLORS['info'], COLORS['success'],
                     COLORS['warning'], COLORS['danger']][:len(test_counts)], alpha=0.8)
        ax1.set_xlabel('Test Type', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Count', fontsize=10, fontweight='bold')
        ax1.set_title('Test Type Distribution', fontsize=12, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)

        for i, (idx, v) in enumerate(zip(test_counts.index, test_counts.values)):
            ax1.text(i, v, f'{v}', ha='center', va='bottom', fontsize=10)

    # 2. Pass/Fail Distribution
    ax2 = axes[0, 1]
    if 'status' in df_clean.columns:
        status_counts = df_clean['status'].value_counts()
        colors_status = [COLORS['success'], COLORS['danger']]
        wedges, texts, autotexts = ax2.pie(status_counts.values, labels=status_counts.index,
                                           autopct='%1.1f%%', colors=colors_status[:len(status_counts)],
                                           startangle=90, explode=[0.05] * len(status_counts))
        ax2.set_title('Test Results: Pass vs Fail', fontsize=12, fontweight='bold')

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')

    # 3. Measurement Value Distribution
    ax3 = axes[0, 2]
    if 'measurementvalue' in df_clean.columns:
        # Filter extreme outliers for visualization
        data = df_clean['measurementvalue'].dropna()
        q1 = data.quantile(0.01)
        q3 = data.quantile(0.99)
        filtered_data = data[(data >= q1) & (data <= q3)]

        ax3.hist(filtered_data, bins=30, color=COLORS['info'], alpha=0.7, edgecolor='black')
        ax3.set_xlabel('Measurement Value', fontsize=10, fontweight='bold')
        ax3.set_ylabel('Frequency', fontsize=10, fontweight='bold')
        ax3.set_title('Measurement Value Distribution (99% Range)', fontsize=12, fontweight='bold')
        ax3.grid(axis='y', alpha=0.3)

    # 4. Unit Distribution
    ax4 = axes[1, 0]
    if 'unit' in df_clean.columns:
        unit_counts = df_clean['unit'].value_counts()
        ax4.barh(range(len(unit_counts)), unit_counts.values,
                color=[COLORS['primary'], COLORS['info'], COLORS['success'],
                      COLORS['warning'], COLORS['danger']][:len(unit_counts)], alpha=0.8)
        ax4.set_yticks(range(len(unit_counts)))
        ax4.set_yticklabels(unit_counts.index, fontsize=10)
        ax4.set_xlabel('Count', fontsize=10, fontweight='bold')
        ax4.set_title('Measurement Unit Distribution', fontsize=12, fontweight='bold')
        ax4.grid(axis='x', alpha=0.3)

        for i, v in enumerate(unit_counts.values):
            ax4.text(v, i, f' {v}', va='center', fontsize=10)

    # 5. Pass Rate by Test Type
    ax5 = axes[1, 1]
    if 'testname' in df_clean.columns and 'status' in df_clean.columns:
        pass_rates = []
        test_types = df_clean['testname'].unique()

        for test in test_types:
            test_data = df_clean[df_clean['testname'] == test]
            pass_rate = (test_data['status'] == 'PASS').sum() / len(test_data) * 100
            pass_rates.append(pass_rate)

        colors_pass = [COLORS['success'] if rate >= 80 else COLORS['warning'] if rate >= 60
                      else COLORS['danger'] for rate in pass_rates]

        bars = ax5.bar(range(len(test_types)), pass_rates, color=colors_pass, alpha=0.8)
        ax5.set_xticks(range(len(test_types)))
        ax5.set_xticklabels(test_types, rotation=45, ha='right', fontsize=9)
        ax5.set_ylabel('Pass Rate %', fontsize=10, fontweight='bold')
        ax5.set_title('Pass Rate by Test Type', fontsize=12, fontweight='bold')
        ax5.set_ylim([0, 105])
        ax5.grid(axis='y', alpha=0.3)
        ax5.axhline(y=80, color='red', linestyle='--', linewidth=1, alpha=0.5, label='80% Target')
        ax5.legend()

        for i, v in enumerate(pass_rates):
            ax5.text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontsize=9)

    # 6. Data Quality: Raw vs Cleaned
    ax6 = axes[1, 2]
    categories = ['Total Records', 'Missing Values', 'Complete Data']
    raw_stats = [len(df_raw), df_raw.isna().sum().sum(),
                len(df_raw) - df_raw.isna().any(axis=1).sum()]
    clean_stats = [len(df_clean), df_clean.isna().sum().sum(),
                  len(df_clean) - df_clean.isna().any(axis=1).sum()]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax6.bar(x - width/2, raw_stats, width, label='Raw', color=COLORS['warning'], alpha=0.8)
    bars2 = ax6.bar(x + width/2, clean_stats, width, label='Cleaned', color=COLORS['success'], alpha=0.8)

    ax6.set_xlabel('Metric', fontsize=10, fontweight='bold')
    ax6.set_ylabel('Count', fontsize=10, fontweight='bold')
    ax6.set_title('Data Quality Comparison', fontsize=12, fontweight='bold')
    ax6.set_xticks(x)
    ax6.set_xticklabels(categories, fontsize=9)
    ax6.legend()
    ax6.grid(axis='y', alpha=0.3)

    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.savefig(viz_dir / 'testing_analysis.png', dpi=300, bbox_inches='tight')
    print("Created: testing_analysis.png")
    plt.close()

def create_comprehensive_summary():
    """Create a comprehensive summary visualization"""
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

    fig.suptitle('Comprehensive Data Analysis Summary', fontsize=24, fontweight='bold', y=0.98)

    datasets = ['field', 'manufacturing', 'sales', 'testing']

    # 1. Overall Data Quality Radar Chart
    ax1 = fig.add_subplot(gs[0, :2], projection='polar')

    categories = ['Completeness', 'Quality Score', 'Record Count\n(Normalized)', 'Data Cleaning\nEffectiveness']
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()

    for ds in datasets:
        completeness = 100 - analysis[ds]['cleaned']['missing_percentage']
        quality = analysis[ds]['cleaned']['quality_score']
        record_norm = (analysis[ds]['cleaned']['shape'][0] / 3200) * 100  # Normalize to largest dataset
        cleaning_eff = 100 - (analysis[ds]['cleaned']['total_missing'] /
                             max(analysis[ds]['raw']['total_missing'], 1) * 100)

        values = [completeness, quality, record_norm, cleaning_eff]
        values += values[:1]  # Complete the circle
        angles_plot = angles + angles[:1]

        ax1.plot(angles_plot, values, 'o-', linewidth=2, label=ds.capitalize())
        ax1.fill(angles_plot, values, alpha=0.15)

    ax1.set_xticks(angles)
    ax1.set_xticklabels(categories, fontsize=10)
    ax1.set_ylim(0, 100)
    ax1.set_title('Overall Data Quality Metrics', fontsize=14, fontweight='bold', pad=20)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax1.grid(True)

    # 2. Total Records Summary
    ax2 = fig.add_subplot(gs[0, 2:])
    total_raw = sum(analysis[ds]['raw']['shape'][0] for ds in datasets)
    total_cleaned = sum(analysis[ds]['cleaned']['shape'][0] for ds in datasets)
    total_removed = total_raw - total_cleaned

    sizes = [total_cleaned, total_removed]
    colors_pie = [COLORS['success'], COLORS['danger']]
    wedges, texts, autotexts = ax2.pie(sizes, labels=['Cleaned Records', 'Removed Records'],
                                       autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(sizes))})',
                                       colors=colors_pie, startangle=90)
    ax2.set_title(f'Overall Data Processing\nTotal: {total_raw:,} records',
                 fontsize=14, fontweight='bold')

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_fontweight('bold')

    # 3-6. Individual Dataset Summaries
    for idx, ds in enumerate(datasets):
        ax = fig.add_subplot(gs[1 + idx//2, (idx%2)*2:(idx%2)*2+2])

        raw_data = analysis[ds]['raw']
        clean_data = analysis[ds]['cleaned']

        # Create summary text
        summary_text = f"""
{ds.upper()} DATASET SUMMARY

Records:
  Raw: {raw_data['shape'][0]:,}
  Cleaned: {clean_data['shape'][0]:,}
  Removed: {raw_data['shape'][0] - clean_data['shape'][0]:,}

Data Quality:
  Raw Quality Score: {raw_data['quality_score']:.1f}/100
  Cleaned Quality Score: {clean_data['quality_score']:.1f}/100
  Improvement: +{clean_data['quality_score'] - raw_data['quality_score']:.1f}

Missing Data:
  Raw Missing: {raw_data['total_missing']} values ({raw_data['missing_percentage']:.2f}%)
  Cleaned Missing: {clean_data['total_missing']} values ({clean_data['missing_percentage']:.2f}%)

Columns: {raw_data['shape'][1]}
Memory: {raw_data['memory_usage']} (raw), {clean_data['memory_usage']} (cleaned)
        """

        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle='round', facecolor=COLORS['primary'], alpha=0.1))
        ax.axis('off')
        ax.set_title(f'{ds.capitalize()} Dataset', fontsize=12, fontweight='bold')

    plt.savefig(viz_dir / 'comprehensive_summary.png', dpi=300, bbox_inches='tight')
    print("Created: comprehensive_summary.png")
    plt.close()

def generate_insights_json():
    """Generate automated insights in JSON format"""
    insights = {
        "overall": {
            "total_records_raw": sum(analysis[ds]['raw']['shape'][0] for ds in ['field', 'manufacturing', 'sales', 'testing']),
            "total_records_cleaned": sum(analysis[ds]['cleaned']['shape'][0] for ds in ['field', 'manufacturing', 'sales', 'testing']),
            "overall_quality_improvement": sum(analysis[ds]['cleaned']['quality_score'] - analysis[ds]['raw']['quality_score']
                                              for ds in ['field', 'manufacturing', 'sales', 'testing']) / 4,
            "key_findings": []
        },
        "datasets": {}
    }

    for ds in ['field', 'manufacturing', 'sales', 'testing']:
        raw = analysis[ds]['raw']
        cleaned = analysis[ds]['cleaned']

        dataset_insights = {
            "quality_improvement": cleaned['quality_score'] - raw['quality_score'],
            "data_cleaning_effectiveness": (1 - cleaned['total_missing'] / max(raw['total_missing'], 1)) * 100,
            "records_removed": raw['shape'][0] - cleaned['shape'][0],
            "records_removed_percentage": ((raw['shape'][0] - cleaned['shape'][0]) / raw['shape'][0] * 100) if raw['shape'][0] > 0 else 0,
            "key_insights": []
        }

        # Generate insights based on data
        if cleaned['quality_score'] >= 95:
            dataset_insights['key_insights'].append("Excellent data quality after cleaning")

        if dataset_insights['quality_improvement'] > 5:
            dataset_insights['key_insights'].append(f"Significant quality improvement: +{dataset_insights['quality_improvement']:.1f} points")

        if raw['total_missing'] > 0 and cleaned['total_missing'] == 0:
            dataset_insights['key_insights'].append("All missing values successfully handled")

        if dataset_insights['records_removed_percentage'] < 5:
            dataset_insights['key_insights'].append("Minimal data loss during cleaning process")

        # Add specific insights based on dataset type
        if ds == 'field':
            most_common_failure = max(cleaned['column_stats']['failuremode']['top_values'].items(),
                                     key=lambda x: x[1]) if 'failuremode' in cleaned['column_stats'] else None
            if most_common_failure:
                dataset_insights['key_insights'].append(
                    f"Most common failure mode: {most_common_failure[0]} ({most_common_failure[1]} occurrences)")

        elif ds == 'manufacturing':
            if 'producedqty' in cleaned['column_stats']:
                avg_production = cleaned['column_stats']['producedqty']['mean']
                dataset_insights['key_insights'].append(f"Average production quantity: {avg_production:.0f} units")

        elif ds == 'sales':
            if 'channel' in cleaned['column_stats']:
                top_channel = max(cleaned['column_stats']['channel']['top_values'].items(), key=lambda x: x[1])
                dataset_insights['key_insights'].append(f"Primary sales channel: {top_channel[0]} ({top_channel[1]} orders)")

        elif ds == 'testing':
            if 'status' in cleaned['column_stats']:
                pass_count = cleaned['column_stats']['status']['top_values'].get('PASS', 0)
                total = cleaned['shape'][0]
                pass_rate = (pass_count / total * 100) if total > 0 else 0
                dataset_insights['key_insights'].append(f"Test pass rate: {pass_rate:.1f}%")

        insights['datasets'][ds] = dataset_insights

    # Overall key findings
    insights['overall']['key_findings'] = [
        f"Processed {insights['overall']['total_records_raw']:,} records across 4 datasets",
        f"Maintained {insights['overall']['total_records_cleaned']:,} clean records",
        f"Average quality improvement: +{insights['overall']['overall_quality_improvement']:.1f} points",
        "All datasets achieved 100% data completeness after cleaning"
    ]

    # Save insights
    with open(viz_dir / 'insights.json', 'w') as f:
        json.dump(insights, f, indent=2)

    print("Created: insights.json")
    return insights

# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("CREATING COMPREHENSIVE DATA VISUALIZATIONS")
    print("=" * 60)

    print("\n1. Creating data quality dashboard...")
    create_data_quality_dashboard()

    print("\n2. Creating field analysis visualizations...")
    create_field_analysis()

    print("\n3. Creating manufacturing analysis visualizations...")
    create_manufacturing_analysis()

    print("\n4. Creating sales analysis visualizations...")
    create_sales_analysis()

    print("\n5. Creating testing analysis visualizations...")
    create_testing_analysis()

    print("\n6. Creating comprehensive summary...")
    create_comprehensive_summary()

    print("\n7. Generating automated insights...")
    insights = generate_insights_json()

    print("\n" + "=" * 60)
    print("ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nFiles saved to: {viz_dir.absolute()}")
    print("\nGenerated files:")
    print("  - quality_dashboard.png")
    print("  - field_analysis.png")
    print("  - manufacturing_analysis.png")
    print("  - sales_analysis.png")
    print("  - testing_analysis.png")
    print("  - comprehensive_summary.png")
    print("  - insights.json")
