#!/usr/bin/env column
"""
================================================================================
PROJECT NAME: Customer Shopping Behavior Analysis
AUTHOR      : Data Analyst Portfolio Project
OBJECTIVE   : Conduct an end-to-end exploratory data analysis (EDA) to extract 
              actionable business insights, calculate critical financial KPIs, 
              and generate executive-ready visualizations.
LIBRARIES   : pandas, matplotlib.pyplot, os, time
================================================================================
README / INTERVIEW GUIDE:
- This script is designed as a modular, production-grade pipeline.
- It utilizes defensive programming (try-except blocks) to handle missing files 
  and runtime anomalies gracefully.
- Visualization styling leverages Matplotlib's 'ggplot' style for clean aesthetics,
  and exports at 300 DPI for presentation-ready quality.
================================================================================
"""

import os
import time
import pandas as pd
import matplotlib.pyplot as plt

# Global Configuration Constants
DATASET_PATH = "Dataset/shopping_trends_updated.csv"
OUTPUT_DIR = "Python/charts"
USD_TO_INR_RATE = 85.0

# Apply professional matplotlib style globally
plt.style.use("ggplot")


def load_data(file_path):
    """
    Loads the dataset safely from the given file path with explicit exception handling.
    
    Interview Note: Demonstrates industrial data-loading practices by handling 
    IO and formatting errors structurally.
    """
    print("\n" + "="*60)
    print(" 1. LOADING DATASET ".center(60, "="))
    print("="*60)
    
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file at '{file_path}' does not exist.")
        
        df = pd.read_csv(file_path)
        print(f"[SUCCESS] Dataset loaded successfully from: '{file_path}'")
        return df
    except FileNotFoundError as fnf_error:
        print(f"[ERROR] Critical Error: {fnf_error}")
        print("[ACTION] Please verify your folder structure and try again.")
        raise
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while loading data: {e}")
        raise


def show_dataset_information(df):
    """
    Displays comprehensive metadata regarding structural and data integrity metrics.
    
    Interview Note: Shows the interviewer that you prioritize understanding data 
    types, memory footprints, and data cleansing (nulls/duplicates) first.
    """
    print("\n" + "="*60)
    print(" 2. DATASET METADATA & INTEGRITY PROFILE ".center(60, "="))
    print("="*60)
    
    print(f"• Dataset Shape      : {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"• Duplicate Records  : {df.duplicated().sum()}")
    print(f"• Total Memory Usage : {df.memory_usage(deep=True).sum() / 1024:.2f} KB\n")
    
    print("-" * 60)
    print(f"{'Column Name':<25} | {'Data Type':<12} | {'Missing Values':<14} | {'Unique Values':<12}")
    print("-" * 60)
    for col in df.columns:
        print(f"{col:<25} | {str(df[col].dtype):<12} | {df[col].isnull().sum():<14} | {df[col].nunique():<12}")
    print("-" * 60)
    
    print("\n>>> FIRST 5 RECORDS PREVIEW:")
    print(df.head().to_string())
    print("="*60)


def calculate_kpis(df):
    """
    Calculates operational and financial high-level KPIs.
    
    Interview Note: Showcases cross-border financial handling capabilities 
    by calculating alternative currency valuations programmatically.
    """
    print("\n" + "="*60)
    print(" 3. EXECUTIVE KEY PERFORMANCE INDICATORS (KPIs) ".center(60, "="))
    print("="*60)
    
    try:
        # Check for mandatory columns to prevent calculation errors
        required_cols = ['Purchase Amount (USD)', 'Review Rating', 'Customer ID']
        for col in required_cols:
            if col not in df.columns:
                raise KeyError(f"Missing required metric column: '{col}'")
                
        total_sales_usd = df['Purchase Amount (USD)'].sum()
        total_sales_inr = total_sales_usd * USD_TO_INR_RATE
        avg_purchase = df['Purchase Amount (USD)'].mean()
        avg_rating = df['Review Rating'].mean()
        total_customers = df['Customer ID'].nunique()
        
        print(f"• Total Sales (USD)          : ${total_sales_usd:,.2f}")
        print(f"• Approximate Sales (INR)    : ₹{total_sales_inr:,.2f} (at 1 USD = {USD_TO_INR_RATE} INR)")
        print(f"• Average Purchase Value     : ${avg_purchase:,.2f}")
        print(f"• Average Review Rating      : {avg_rating:.2f} / 5.0")
        print(f"• Total Unique Customers     : {total_customers:,}")
        print("="*60)
        
        return {
            "total_sales_usd": total_sales_usd,
            "total_customers": total_customers
        }
    except Exception as e:
        print(f"[ERROR] Failed to calculate metrics: {e}")
        return None


def sales_by_category_chart(df, save_dir):
    """Generates and saves a Bar Chart for revenue generated by category."""
    try:
        data = df.groupby('Category')['Purchase Amount (USD)'].sum().sort_values(ascending=False)
        plt.figure(figsize=(8, 5))
        bars = plt.bar(data.index, data.values, color='royalblue', edgecolor='black')
        
        # Adding value labels on top of the bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + (max(data.values)*0.01), f"${yval:,.0f}", ha='center', va='bottom', fontsize=9)
            
        plt.title('Total Revenue Generation by Product Category', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Product Category', fontsize=10)
        plt.ylabel('Total Sales (USD)', fontsize=10)
        plt.tight_layout()
        
        path = os.path.join(save_dir, 'sales_by_category.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"[WARNING] Sales by Category chart failed: {e}")


def sales_by_gender_chart(df, save_dir):
    """Generates and saves a Pie Chart for revenue share split by gender."""
    try:
        data = df.groupby('Gender')['Purchase Amount (USD)'].sum()
        plt.figure(figsize=(6, 6))
        plt.pie(data.values, labels=data.index, autopct='%1.1f%%', startangle=90, 
                colors=['lightcoral', 'skyblue'], wedgeprops={'edgecolor': 'white', 'linewidth': 2})
        plt.title('Revenue Contribution Split by Gender', fontsize=12, fontweight='bold', pad=15)
        
        path = os.path.join(save_dir, 'sales_by_gender.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"[WARNING] Sales by Gender chart failed: {e}")


def sales_by_season_chart(df, save_dir):
    """Generates and saves a Line Chart showing seasonal trend analysis."""
    try:
        # Creating a custom order for chronological analysis flow
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        data = df.groupby('Season')['Purchase Amount (USD)'].sum().reindex(season_order)
        
        plt.figure(figsize=(8, 5))
        plt.plot(data.index, data.values, marker='o', color='darkorange', linewidth=2.5, markersize=8)
        
        for x, y in zip(data.index, data.values):
            plt.text(x, y + (max(data.values)*0.01), f"${y:,.0f}", ha='center', va='bottom', fontsize=9)
            
        plt.title('Seasonal Sales and Revenue Demand Trends', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Season', fontsize=10)
        plt.ylabel('Total Sales (USD)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        
        path = os.path.join(save_dir, 'sales_by_season.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"[WARNING] Sales by Season chart failed: {e}")


def payment_method_chart(df, save_dir):
    """Generates and saves a Horizontal Bar Chart for breakdown of payment modes."""
    try:
        data = df.groupby('Payment Method')['Purchase Amount (USD)'].sum().sort_values(ascending=True)
        plt.figure(figsize=(9, 5))
        bars = plt.barh(data.index, data.values, color='teal', edgecolor='black')
        
        for bar in bars:
            xval = bar.get_width()
            plt.text(xval + (max(data.values)*0.01), bar.get_y() + bar.get_height()/2, f"${xval:,.0f}", ha='left', va='center', fontsize=9)
            
        plt.title('Customer Revenue Breakdown by Payment Method', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Total Sales (USD)', fontsize=10)
        plt.ylabel('Payment Method', fontsize=10)
        plt.tight_layout()
        
        path = os.path.join(save_dir, 'payment_method_sales.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"[WARNING] Payment Method chart failed: {e}")


def top5_location_chart(df, save_dir):
    """Generates and saves a Horizontal Bar Chart containing Top 5 Revenue-generating locations."""
    try:
        data = df.groupby('Location')['Purchase Amount (USD)'].sum().sort_values(ascending=False).head(5)
        data = data.sort_values(ascending=True) # Sort ascending for better horizontal visual reading
        
        plt.figure(figsize=(9, 5))
        bars = plt.barh(data.index, data.values, color='purple', edgecolor='black')
        
        for bar in bars:
            xval = bar.get_width()
            plt.text(xval + (max(data.values)*0.01), bar.get_y() + bar.get_height()/2, f"${xval:,.0f}", ha='left', va='center', fontsize=9)
            
        plt.title('Top 5 Highest Revenue-Generating Locations', fontsize=12, fontweight='bold', pad=15)
        plt.xlabel('Total Sales (USD)', fontsize=10)
        plt.ylabel('Location (State)', fontsize=10)
        plt.tight_layout()
        
        path = os.path.join(save_dir, 'top5_locations.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"[WARNING] Top 5 Locations chart failed: {e}")


def generate_business_insights(df):
    """
    Extracts exactly 15 deep operational and corporate business insights from data metrics.
    
    Interview Note: Hard analytical evaluations here show an analytical candidate 
    who converts structural data arrays into actionable company strategies.
    """
    print("\n" + "="*60)
    print(" 4. CORE BUSINESS INSIGHTS (15 DEEP-DIVES) ".center(60, "="))
    print("="*60)
    
    try:
        # Calculations for building strict categorical insights
        cat_sales = df.groupby('Category')['Purchase Amount (USD)'].sum()
        loc_sales = df.groupby('Location')['Purchase Amount (USD)'].sum()
        item_counts = df['Item Purchased'].value_counts()
        avg_age = df['Age'].mean()
        pay_method = df['Payment Method'].value_counts()
        ship_type = df['Shipping Type'].value_counts()
        color_counts = df['Color'].value_counts()
        size_counts = df['Size'].value_counts()
        season_counts = df['Season'].value_counts()
        cat_rating = df.groupby('Category')['Review Rating'].mean()
        sub_pct = (df['Subscription Status'].value_counts(normalize=True).get('Yes', 0)) * 100
        avg_prev_purchases = df['Previous Purchases'].mean()
        gender_sales = df.groupby('Gender')['Purchase Amount (USD)'].sum()
        freq_purchases = df['Frequency of Purchases'].value_counts()
        
        # Display extracted insights programmatically
        print(f" 1. Highest Selling Category       : {cat_sales.idxmax()} (${cat_sales.max():,.2f})")
        print(f" 2. Highest Revenue State           : {loc_sales.idxmax()} (${loc_sales.max():,.2f})")
        print(f" 3. Most Purchased Item             : {item_counts.idxmax()} ({item_counts.max()} orders)")
        print(f" 4. Average Customer Age            : {avg_age:.1f} years old")
        print(f" 5. Most Preferred Payment Method   : {pay_method.idxmax()} ({pay_method.max()} transactions)")
        print(f" 6. Most Preferred Shipping Type     : {ship_type.idxmax()} ({ship_type.max()} selections)")
        print(f" 7. Most Purchased Color            : {color_counts.idxmax()} ({color_counts.max()} units)")
        print(f" 8. Most Preferred Size             : {size_counts.idxmax()} ({size_counts.max()} distributions)")
        print(f" 9. Most Common Season              : {season_counts.idxmax()} ({season_counts.max()} total activities)")
        print(f"10. Highest Rated Category          : {cat_rating.idxmax()} ({cat_rating.max():.2f}/5.0 stars)")
        print(f"11. Percentage of Subscribers       : {sub_pct:.1f}% of core customer database")
        print(f"12. Average Previous Purchases      : {avg_prev_purchases:.1f} orders per shopper")
        print(f"13. Male Revenue Contribution       : ${gender_sales.get('Male', 0):,.2f}")
        print(f"14. Female Revenue Contribution     : ${gender_sales.get('Female', 0):,.2f}")
        print(f"15. Most Frequent Purchase Pace    : {freq_purchases.idxmax()} ({freq_purchases.max()} responses)")
        
        print("="*60)
    except Exception as e:
        print(f"[ERROR] Failed extracting exact business insights configuration: {e}")


def project_summary(kpi_data, charts_count, saved_location):
    """Prints a formalized final execution closure report summarizing execution."""
    print("\n" + "="*60)
    print(" 5. PORTFOLIO PROJECT METRIC SUMMARY ".center(60, "="))
    print("="*60)
    
    total_cust = kpi_data["total_customers"] if kpi_data else "N/A"
    total_sls = f"${kpi_data['total_sales_usd']:,.2f}" if kpi_data else "N/A"
    
    print(f"• Number of Charts Generated : {charts_count}")
    print(f"• Charts Saved Location      : {saved_location}/")
    print(f"• Total Customers Highlighted: {total_cust}")
    print(f"• Total Revenue Summarized   : {total_sls}")
    print("• Project Status             : Analysis Completed Successfully")
    print("="*60)


def main():
    """Execution backbone orchestrating individual data processing modules."""
    start_time = time.time()
    
    print("="*60)
    print("     CUSTOMER SHOPPING BEHAVIOR ANALYSIS PIPELINE      ".center(60, "#"))
    print("="*60)
    
    # 1. Pipeline preparation - Auto-generate operational directories securely
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 2. Extract Stage
    df = load_data(DATASET_PATH)
    
    if df is not None:
        # 3. Profiling/Transform Stage
        show_dataset_information(df)
        kpi_metrics = calculate_kpis(df)
        
        # 4. Data Visualization Charting Pipeline
        print("\n>>> Generating high-fidelity chart components...")
        sales_by_category_chart(df, OUTPUT_DIR)
        sales_by_gender_chart(df, OUTPUT_DIR)
        sales_by_season_chart(df, OUTPUT_DIR)
        payment_method_chart(df, OUTPUT_DIR)
        top5_location_chart(df, OUTPUT_DIR)
        print(f"[SUCCESS] 5 Matplotlib visualization components saved inside: '{OUTPUT_DIR}'")
        
        # 5. Semantic Insights Engineering Stage
        generate_business_insights(df)
        
        # 6. Reporting Closures
        project_summary(kpi_metrics, charts_count=5, saved_location=OUTPUT_DIR)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print("\n" + "✓".center(60, "-"))
        print(" Execution Completed Successfully ".center(60, " "))
        print(f" Total Script Runtime: {execution_time:.4f} seconds ".center(60, " "))
        print("-"*60 + "\n")


if __name__ == "__main__":
    main()