"""
Data Analysis Module

This module analyzes the scraped fanfiction data to find significant patterns
and insights.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List
import os


class FanfictionAnalyzer:
    """Analyzer for fanfiction data."""
    
    def __init__(self, data_path: str):
        """
        Initialize the analyzer with data.
        
        Args:
            data_path: Path to CSV file containing fanfiction data
        """
        self.df = pd.read_csv(data_path)
        self.output_dir = 'outputs'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set style for plots
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
    
    def basic_statistics(self) -> Dict:
        """
        Calculate basic statistics about the dataset.
        
        Returns:
            Dictionary containing basic statistics
        """
        stats = {
            'total_works': len(self.df),
            'unique_authors': self.df['author'].nunique(),
            'fandoms': self.df['fandom_searched'].value_counts().to_dict(),
            'avg_words': self.df['words'].mean(),
            'median_words': self.df['words'].median(),
            'avg_kudos': self.df['kudos'].mean(),
            'median_kudos': self.df['kudos'].median(),
            'avg_hits': self.df['hits'].mean(),
            'total_words': self.df['words'].sum()
        }
        
        return stats
    
    def print_summary(self):
        """Print a summary of the dataset."""
        stats = self.basic_statistics()
        
        print("=" * 60)
        print("FANFICTION DATASET SUMMARY")
        print("=" * 60)
        print(f"Total Works: {stats['total_works']}")
        print(f"Unique Authors: {stats['unique_authors']}")
        print(f"Total Words: {stats['total_words']:,.0f}")
        print(f"\nAverage Word Count: {stats['avg_words']:,.0f}")
        print(f"Median Word Count: {stats['median_words']:,.0f}")
        print(f"\nAverage Kudos: {stats['avg_kudos']:.1f}")
        print(f"Median Kudos: {stats['median_kudos']:.1f}")
        print(f"\nAverage Hits: {stats['avg_hits']:,.0f}")
        
        print(f"\nWorks by Fandom:")
        for fandom, count in stats['fandoms'].items():
            print(f"  {fandom}: {count}")
        
        print("=" * 60)
    
    def analyze_ratings(self):
        """Analyze rating distribution across fandoms."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Overall rating distribution
        rating_counts = self.df['rating'].value_counts()
        ax1.pie(rating_counts.values, labels=rating_counts.index, autopct='%1.1f%%')
        ax1.set_title('Overall Rating Distribution')
        
        # Rating by fandom
        rating_by_fandom = pd.crosstab(self.df['fandom_searched'], self.df['rating'])
        rating_by_fandom.plot(kind='bar', stacked=False, ax=ax2)
        ax2.set_title('Rating Distribution by Fandom')
        ax2.set_xlabel('Fandom')
        ax2.set_ylabel('Count')
        ax2.legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/rating_analysis.png', dpi=300, bbox_inches='tight')
        print(f"Saved rating analysis to {self.output_dir}/rating_analysis.png")
        plt.close()
    
    def analyze_word_counts(self):
        """Analyze word count distributions."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Overall word count distribution
        ax1 = axes[0, 0]
        self.df['words'].hist(bins=50, ax=ax1)
        ax1.set_title('Word Count Distribution (All Works)')
        ax1.set_xlabel('Word Count')
        ax1.set_ylabel('Frequency')
        
        # Word count by fandom (box plot)
        ax2 = axes[0, 1]
        self.df.boxplot(column='words', by='fandom_searched', ax=ax2)
        ax2.set_title('Word Count by Fandom')
        ax2.set_xlabel('Fandom')
        ax2.set_ylabel('Word Count')
        plt.sca(ax2)
        plt.xticks(rotation=45, ha='right')
        
        # Average word count by fandom (bar chart)
        ax3 = axes[1, 0]
        avg_words = self.df.groupby('fandom_searched')['words'].mean().sort_values(ascending=False)
        avg_words.plot(kind='bar', ax=ax3)
        ax3.set_title('Average Word Count by Fandom')
        ax3.set_xlabel('Fandom')
        ax3.set_ylabel('Average Words')
        ax3.tick_params(axis='x', rotation=45)
        
        # Word count vs kudos correlation
        ax4 = axes[1, 1]
        ax4.scatter(self.df['words'], self.df['kudos'], alpha=0.5)
        ax4.set_title('Word Count vs Kudos')
        ax4.set_xlabel('Word Count')
        ax4.set_ylabel('Kudos')
        
        # Calculate correlation
        correlation = self.df['words'].corr(self.df['kudos'])
        ax4.text(0.05, 0.95, f'Correlation: {correlation:.3f}',
                transform=ax4.transAxes, verticalalignment='top')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/word_count_analysis.png', dpi=300, bbox_inches='tight')
        print(f"Saved word count analysis to {self.output_dir}/word_count_analysis.png")
        plt.close()
    
    def analyze_engagement(self):
        """Analyze engagement metrics (kudos, bookmarks, hits)."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Average kudos by fandom
        ax1 = axes[0, 0]
        avg_kudos = self.df.groupby('fandom_searched')['kudos'].mean().sort_values(ascending=False)
        avg_kudos.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Average Kudos by Fandom')
        ax1.set_xlabel('Fandom')
        ax1.set_ylabel('Average Kudos')
        ax1.tick_params(axis='x', rotation=45)
        
        # Average hits by fandom
        ax2 = axes[0, 1]
        avg_hits = self.df.groupby('fandom_searched')['hits'].mean().sort_values(ascending=False)
        avg_hits.plot(kind='bar', ax=ax2, color='lightcoral')
        ax2.set_title('Average Hits by Fandom')
        ax2.set_xlabel('Fandom')
        ax2.set_ylabel('Average Hits')
        ax2.tick_params(axis='x', rotation=45)
        
        # Kudos to hits ratio
        ax3 = axes[1, 0]
        self.df['kudos_hit_ratio'] = self.df['kudos'] / (self.df['hits'] + 1)
        avg_ratio = self.df.groupby('fandom_searched')['kudos_hit_ratio'].mean().sort_values(ascending=False)
        avg_ratio.plot(kind='bar', ax=ax3, color='lightgreen')
        ax3.set_title('Average Kudos-to-Hits Ratio by Fandom')
        ax3.set_xlabel('Fandom')
        ax3.set_ylabel('Kudos/Hits Ratio')
        ax3.tick_params(axis='x', rotation=45)
        
        # Engagement comparison
        ax4 = axes[1, 1]
        engagement_data = self.df.groupby('fandom_searched')[['kudos', 'bookmarks', 'hits']].mean()
        engagement_data_normalized = engagement_data.div(engagement_data.max())
        engagement_data_normalized.plot(kind='bar', ax=ax4)
        ax4.set_title('Normalized Engagement Metrics by Fandom')
        ax4.set_xlabel('Fandom')
        ax4.set_ylabel('Normalized Value')
        ax4.legend(title='Metric')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/engagement_analysis.png', dpi=300, bbox_inches='tight')
        print(f"Saved engagement analysis to {self.output_dir}/engagement_analysis.png")
        plt.close()
    
    def analyze_categories(self):
        """Analyze category distribution."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Overall category distribution
        category_counts = self.df['category'].value_counts()
        ax1.barh(category_counts.index, category_counts.values)
        ax1.set_title('Overall Category Distribution')
        ax1.set_xlabel('Count')
        ax1.set_ylabel('Category')
        
        # Category by fandom
        category_by_fandom = pd.crosstab(self.df['fandom_searched'], self.df['category'])
        category_by_fandom.plot(kind='bar', stacked=True, ax=ax2)
        ax2.set_title('Category Distribution by Fandom')
        ax2.set_xlabel('Fandom')
        ax2.set_ylabel('Count')
        ax2.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/category_analysis.png', dpi=300, bbox_inches='tight')
        print(f"Saved category analysis to {self.output_dir}/category_analysis.png")
        plt.close()
    
    def find_top_works(self, n: int = 10):
        """
        Find top works by various metrics.
        
        Args:
            n: Number of top works to return
        """
        print("\n" + "=" * 60)
        print(f"TOP {n} WORKS")
        print("=" * 60)
        
        # Top by kudos
        print(f"\nTop {n} by Kudos:")
        top_kudos = self.df.nlargest(n, 'kudos')[['title', 'author', 'fandom_searched', 'kudos', 'words']]
        for idx, row in top_kudos.iterrows():
            print(f"  {row['kudos']:>6} kudos - {row['title'][:50]} by {row['author']}")
        
        # Top by hits
        print(f"\nTop {n} by Hits:")
        top_hits = self.df.nlargest(n, 'hits')[['title', 'author', 'fandom_searched', 'hits', 'words']]
        for idx, row in top_hits.iterrows():
            print(f"  {row['hits']:>7} hits - {row['title'][:50]} by {row['author']}")
        
        # Longest works
        print(f"\nTop {n} Longest Works:")
        longest = self.df.nlargest(n, 'words')[['title', 'author', 'fandom_searched', 'words', 'kudos']]
        for idx, row in longest.iterrows():
            print(f"  {row['words']:>8} words - {row['title'][:50]} by {row['author']}")
    
    def analyze_all(self):
        """Run all analyses."""
        print("\nRunning comprehensive analysis...\n")
        
        self.print_summary()
        self.analyze_ratings()
        self.analyze_word_counts()
        self.analyze_engagement()
        self.analyze_categories()
        self.find_top_works()
        
        print("\n" + "=" * 60)
        print("Analysis complete! Check the 'outputs' directory for visualizations.")
        print("=" * 60)


def main():
    """Main function to analyze fanfiction data."""
    
    data_file = 'data/ao3_fanfictions.csv'
    
    if not os.path.exists(data_file):
        print(f"Error: Data file '{data_file}' not found.")
        print("Please run the scraper first to collect data.")
        return
    
    analyzer = FanfictionAnalyzer(data_file)
    analyzer.analyze_all()


if __name__ == "__main__":
    main()
