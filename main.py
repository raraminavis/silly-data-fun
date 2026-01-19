"""
Main script to run the fanfiction data scraping and analysis pipeline.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ao3_scraper import AO3Scraper
from analyzer import FanfictionAnalyzer


def main():
    """Main pipeline to scrape and analyze fanfiction data."""
    
    print("=" * 60)
    print("FANFICTION DATA SCRAPING AND ANALYSIS PROJECT")
    print("=" * 60)
    print("\nThis project scrapes fanfiction data from Archive of Our Own")
    print("and performs comprehensive analysis to find significant patterns.")
    print()
    
    # Ask user what to do
    print("Options:")
    print("1. Scrape data from AO3")
    print("2. Analyze existing data")
    print("3. Both (scrape then analyze)")
    print()
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        print("\n" + "=" * 60)
        print("STARTING DATA SCRAPING")
        print("=" * 60)
        
        # Define fandoms to scrape
        fandoms = [
            "My Chemical Romance",
            "Fall Out Boy", 
            "Sherlock",
            "Star Trek"
        ]
        
        # Create directories
        os.makedirs('data', exist_ok=True)
        
        scraper = AO3Scraper(rate_limit=5.0)
        all_works = []
        
        for fandom in fandoms:
            print(f"\n{'='*60}")
            print(f"Scraping fandom: {fandom}")
            print(f"{'='*60}")
            
            works = scraper.search_fandom(fandom, max_pages=3)
            all_works.extend(works)
            
            print(f"Collected {len(works)} works from {fandom}")
        
        # Save data
        print(f"\n{'='*60}")
        print(f"Total works collected: {len(all_works)}")
        print(f"{'='*60}")
        
        scraper.save_to_csv(all_works, 'data/ao3_fanfictions.csv')
        scraper.save_to_json(all_works, 'data/ao3_fanfictions.json')
        
        print("\nScraping complete!")
    
    if choice in ['2', '3']:
        print("\n" + "=" * 60)
        print("STARTING DATA ANALYSIS")
        print("=" * 60)
        
        data_file = 'data/ao3_fanfictions.csv'
        
        if not os.path.exists(data_file):
            print(f"Error: Data file '{data_file}' not found.")
            print("Please run the scraper first to collect data.")
            return
        
        analyzer = FanfictionAnalyzer(data_file)
        analyzer.analyze_all()
    
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
