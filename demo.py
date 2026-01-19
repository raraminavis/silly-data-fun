"""
Example Demo Script

This demonstrates how the fanfiction scraping and analysis project works
using sample data (to avoid actually scraping AO3 during development).

For real usage, run main.py instead.
"""

import pandas as pd
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analyzer import FanfictionAnalyzer


def create_demo_data():
    """Create realistic demo fanfiction data."""
    
    # This simulates what would be scraped from AO3
    demo_data = [
        # Sherlock fandom
        {'title': 'A Study in Pink Revisited', 'author': 'SherlockFan221', 'work_id': '100001', 
         'rating': 'Teen And Up Audiences', 'warnings': 'No Archive Warnings Apply', 
         'category': 'M/M', 'fandom_searched': 'Sherlock', 'fandoms': 'Sherlock (TV)',
         'tags': 'Fluff, Case Fic, First Kiss', 'relationships': 'Sherlock Holmes/John Watson',
         'characters': 'Sherlock Holmes, John Watson, Mrs Hudson', 'language': 'English',
         'words': 8500, 'chapters': '1/1', 'kudos': 342, 'bookmarks': 45, 'hits': 2891,
         'summary': 'An alternate take on how they met...'},
        
        {'title': 'The Consulting Detective and the Doctor', 'author': 'BBCFan', 'work_id': '100002',
         'rating': 'General Audiences', 'warnings': 'No Archive Warnings Apply',
         'category': 'Gen', 'fandom_searched': 'Sherlock', 'fandoms': 'Sherlock (TV)',
         'tags': 'Friendship, Baker Street, Humor', 'relationships': '',
         'characters': 'Sherlock Holmes, John Watson, Greg Lestrade', 'language': 'English',
         'words': 12000, 'chapters': '5/5', 'kudos': 521, 'bookmarks': 78, 'hits': 4523,
         'summary': 'Five times they solved a case together...'},
        
        # Star Trek fandom
        {'title': 'To Boldly Go', 'author': 'TrekkerForever', 'work_id': '100003',
         'rating': 'Teen And Up Audiences', 'warnings': 'No Archive Warnings Apply',
         'category': 'Gen', 'fandom_searched': 'Star Trek', 'fandoms': 'Star Trek: The Original Series',
         'tags': 'Space Exploration, Adventure, Team Bonding', 'relationships': '',
         'characters': 'James T. Kirk, Spock, Leonard McCoy', 'language': 'English',
         'words': 15000, 'chapters': '8/8', 'kudos': 678, 'bookmarks': 92, 'hits': 5234,
         'summary': 'A new mission on the edge of known space...'},
        
        {'title': 'Logical Conclusions', 'author': 'VulcanLogic', 'work_id': '100004',
         'rating': 'Mature', 'warnings': 'No Archive Warnings Apply',
         'category': 'M/M', 'fandom_searched': 'Star Trek', 'fandoms': 'Star Trek: The Original Series',
         'tags': 'Romance, Angst, Hurt/Comfort', 'relationships': 'James T. Kirk/Spock',
         'characters': 'James T. Kirk, Spock', 'language': 'English',
         'words': 25000, 'chapters': '12/12', 'kudos': 892, 'bookmarks': 156, 'hits': 8901,
         'summary': 'After a dangerous mission, Kirk and Spock must confront...'},
        
        # My Chemical Romance fandom
        {'title': 'Killjoys Never Die', 'author': 'DangerDaysForever', 'work_id': '100005',
         'rating': 'Mature', 'warnings': 'Graphic Depictions Of Violence',
         'category': 'M/M', 'fandom_searched': 'My Chemical Romance', 'fandoms': 'My Chemical Romance',
         'tags': 'Band Fic, Danger Days Era, Angst', 'relationships': 'Gerard Way/Frank Iero',
         'characters': 'Gerard Way, Frank Iero, Mikey Way, Ray Toro', 'language': 'English',
         'words': 18000, 'chapters': '10/10', 'kudos': 1245, 'bookmarks': 234, 'hits': 12456,
         'summary': 'In the zones, the killjoys fight for freedom...'},
        
        {'title': 'Black Parade Memories', 'author': 'MCRmy4ever', 'work_id': '100006',
         'rating': 'Teen And Up Audiences', 'warnings': 'No Archive Warnings Apply',
         'category': 'Gen', 'fandom_searched': 'My Chemical Romance', 'fandoms': 'My Chemical Romance',
         'tags': 'Tour Life, Friendship, Found Family', 'relationships': '',
         'characters': 'Gerard Way, Mikey Way, Frank Iero, Ray Toro', 'language': 'English',
         'words': 7500, 'chapters': '3/3', 'kudos': 567, 'bookmarks': 89, 'hits': 6789,
         'summary': 'Behind the scenes of the Black Parade tour...'},
        
        # Fall Out Boy fandom  
        {'title': 'Save Rock and Roll', 'author': 'FOBFanatic', 'work_id': '100007',
         'rating': 'Teen And Up Audiences', 'warnings': 'No Archive Warnings Apply',
         'category': 'M/M', 'fandom_searched': 'Fall Out Boy', 'fandoms': 'Fall Out Boy',
         'tags': 'Band Fic, Hiatus Era, Getting Back Together', 'relationships': 'Patrick Stump/Pete Wentz',
         'characters': 'Patrick Stump, Pete Wentz, Joe Trohman, Andy Hurley', 'language': 'English',
         'words': 22000, 'chapters': '15/15', 'kudos': 1089, 'bookmarks': 198, 'hits': 10234,
         'summary': 'During the hiatus, Patrick and Pete find their way back...'},
        
        {'title': 'Young Volcanoes', 'author': 'PeterickShipper', 'work_id': '100008',
         'rating': 'Explicit', 'warnings': 'No Archive Warnings Apply',
         'category': 'M/M', 'fandom_searched': 'Fall Out Boy', 'fandoms': 'Fall Out Boy',
         'tags': 'Romance, Smut, Band Dynamics', 'relationships': 'Patrick Stump/Pete Wentz',
         'characters': 'Patrick Stump, Pete Wentz', 'language': 'English',
         'words': 9500, 'chapters': '1/1', 'kudos': 678, 'bookmarks': 123, 'hits': 7891,
         'summary': 'A night after a show in Chicago...'},
    ]
    
    return demo_data


def main():
    """Run the demo."""
    
    print("=" * 70)
    print("FANFICTION DATA ANALYSIS - DEMO")
    print("=" * 70)
    print("\nThis demo shows what the project does using sample data.")
    print("To scrape real data from AO3, run: python main.py")
    print()
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    # Create and save demo data
    print("Creating demo dataset...")
    demo_data = create_demo_data()
    df = pd.DataFrame(demo_data)
    
    demo_file = 'data/demo_fanfictions.csv'
    df.to_csv(demo_file, index=False)
    print(f"✓ Created {len(demo_data)} demo works across 4 fandoms\n")
    
    # Analyze the data
    print("Running analysis...\n")
    analyzer = FanfictionAnalyzer(demo_file)
    analyzer.analyze_all()
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE!")
    print("=" * 70)
    print("\nCheck the 'outputs/' directory for visualizations:")
    print("  • rating_analysis.png - Rating distributions")
    print("  • word_count_analysis.png - Word count patterns")
    print("  • engagement_analysis.png - Kudos, hits, bookmarks")
    print("  • category_analysis.png - Relationship categories")
    print("\nTo use with real AO3 data:")
    print("  1. Run: python main.py")
    print("  2. Choose option 1 to scrape (or 3 to scrape and analyze)")
    print("  3. Wait for scraping to complete (respects 5-second rate limit)")
    print("  4. View results in outputs/")
    print()


if __name__ == "__main__":
    main()
