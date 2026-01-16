"""
Simple validation script to test basic functionality.
This creates sample data and tests the analyzer without actually scraping AO3.
"""

import pandas as pd
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analyzer import FanfictionAnalyzer


def create_sample_data():
    """Create sample fanfiction data for testing."""
    
    sample_data = [
        {
            'title': 'Test Story 1',
            'author': 'TestAuthor1',
            'work_id': '12345',
            'rating': 'Teen And Up Audiences',
            'warnings': 'No Archive Warnings Apply',
            'category': 'M/M',
            'fandom_searched': 'Sherlock',
            'fandoms': 'Sherlock (TV)',
            'tags': 'Fluff, Angst',
            'relationships': 'Sherlock Holmes/John Watson',
            'characters': 'Sherlock Holmes, John Watson',
            'language': 'English',
            'words': 5000,
            'chapters': '1/1',
            'kudos': 150,
            'bookmarks': 20,
            'hits': 1000,
            'summary': 'A test story'
        },
        {
            'title': 'Test Story 2',
            'author': 'TestAuthor2',
            'work_id': '12346',
            'rating': 'General Audiences',
            'warnings': 'No Archive Warnings Apply',
            'category': 'Gen',
            'fandom_searched': 'Star Trek',
            'fandoms': 'Star Trek: The Original Series',
            'tags': 'Adventure, Friendship',
            'relationships': '',
            'characters': 'James T. Kirk, Spock',
            'language': 'English',
            'words': 8000,
            'chapters': '5/5',
            'kudos': 200,
            'bookmarks': 35,
            'hits': 1500,
            'summary': 'Another test story'
        },
        {
            'title': 'Test Story 3',
            'author': 'TestAuthor3',
            'work_id': '12347',
            'rating': 'Mature',
            'warnings': 'Graphic Depictions Of Violence',
            'category': 'F/M',
            'fandom_searched': 'My Chemical Romance',
            'fandoms': 'My Chemical Romance',
            'tags': 'Band Fic, AU',
            'relationships': '',
            'characters': 'Gerard Way, Frank Iero',
            'language': 'English',
            'words': 12000,
            'chapters': '10/10',
            'kudos': 300,
            'bookmarks': 50,
            'hits': 2500,
            'summary': 'Yet another test'
        },
        {
            'title': 'Test Story 4',
            'author': 'TestAuthor4',
            'work_id': '12348',
            'rating': 'Explicit',
            'warnings': 'No Archive Warnings Apply',
            'category': 'M/M',
            'fandom_searched': 'Fall Out Boy',
            'fandoms': 'Fall Out Boy',
            'tags': 'Romance, Hurt/Comfort',
            'relationships': '',
            'characters': 'Patrick Stump, Pete Wentz',
            'language': 'English',
            'words': 3000,
            'chapters': '1/1',
            'kudos': 100,
            'bookmarks': 15,
            'hits': 800,
            'summary': 'Test summary'
        }
    ]
    
    return sample_data


def main():
    """Run validation tests."""
    
    print("=" * 60)
    print("RUNNING VALIDATION TESTS")
    print("=" * 60)
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    # Create sample data
    print("\n1. Creating sample data...")
    sample_data = create_sample_data()
    df = pd.DataFrame(sample_data)
    
    # Save sample data
    test_file = 'data/test_fanfictions.csv'
    df.to_csv(test_file, index=False)
    print(f"   ✓ Created {test_file} with {len(sample_data)} sample works")
    
    # Test analyzer
    print("\n2. Testing analyzer...")
    try:
        analyzer = FanfictionAnalyzer(test_file)
        print("   ✓ Analyzer initialized successfully")
        
        # Test basic statistics
        stats = analyzer.basic_statistics()
        print(f"   ✓ Basic statistics calculated: {stats['total_works']} works")
        
        # Test summary
        print("\n3. Testing summary output...")
        analyzer.print_summary()
        print("   ✓ Summary printed successfully")
        
        # Test visualizations (but don't save them for the test)
        print("\n4. Testing visualization generation...")
        
        print("   - Testing rating analysis...")
        analyzer.analyze_ratings()
        print("   ✓ Rating analysis complete")
        
        print("   - Testing word count analysis...")
        analyzer.analyze_word_counts()
        print("   ✓ Word count analysis complete")
        
        print("   - Testing engagement analysis...")
        analyzer.analyze_engagement()
        print("   ✓ Engagement analysis complete")
        
        print("   - Testing category analysis...")
        analyzer.analyze_categories()
        print("   ✓ Category analysis complete")
        
        print("\n5. Testing top works finder...")
        analyzer.find_top_works(n=3)
        print("   ✓ Top works found successfully")
        
        print("\n" + "=" * 60)
        print("ALL VALIDATION TESTS PASSED! ✓")
        print("=" * 60)
        
        print("\nGenerated test outputs in 'outputs/' directory:")
        if os.path.exists('outputs') and os.listdir('outputs'):
            for file in os.listdir('outputs'):
                print(f"  - outputs/{file}")
        else:
            print("  (No output files generated)")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
