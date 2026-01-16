"""
AO3 Fanfiction Scraper

This module scrapes fanfiction metadata from Archive of Our Own (AO3).
It respects AO3's Terms of Service by implementing rate limiting and
only scraping publicly available metadata.
"""

import requests
from bs4 import BeautifulSoup
import time
import csv
import json
from typing import List, Dict
import re


class AO3Scraper:
    """Scraper for Archive of Our Own fanfiction metadata."""
    
    BASE_URL = "https://archiveofourown.org"
    SUMMARY_MAX_LENGTH = 200  # Maximum characters to keep from summary
    
    def __init__(self, rate_limit: float = 5.0):
        """
        Initialize the AO3 scraper.
        
        Args:
            rate_limit: Minimum seconds between requests (default 5 seconds)
        """
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; FandomResearchBot/1.0; Educational Research Project)'
        })
        
    def search_fandom(self, fandom_name: str, max_pages: int = 5) -> List[Dict]:
        """
        Search for fanfictions in a specific fandom.
        
        Args:
            fandom_name: Name of the fandom to search
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of dictionaries containing fanfiction metadata
        """
        works = []
        
        for page in range(1, max_pages + 1):
            print(f"Scraping {fandom_name} - Page {page}/{max_pages}")
            
            # Construct search URL
            search_url = f"{self.BASE_URL}/works/search"
            params = {
                'work_search[query]': fandom_name,
                'work_search[sort_column]': 'kudos_count',
                'page': page
            }
            
            try:
                response = self.session.get(search_url, params=params)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                work_items = soup.find_all('li', class_='work blurb group')
                
                for work in work_items:
                    work_data = self._parse_work_blurb(work, fandom_name)
                    if work_data:
                        works.append(work_data)
                
                # Rate limiting
                time.sleep(self.rate_limit)
                
            except requests.RequestException as e:
                print(f"Error scraping page {page}: {e}")
                break
                
        return works
    
    def _parse_work_blurb(self, work_element, fandom: str) -> Dict:
        """
        Parse a work blurb element to extract metadata.
        
        Args:
            work_element: BeautifulSoup element containing work info
            fandom: Fandom name being scraped
            
        Returns:
            Dictionary with work metadata
        """
        try:
            data = {'fandom_searched': fandom}
            
            # Title
            title_elem = work_element.find('h4', class_='heading')
            if title_elem and title_elem.find('a'):
                data['title'] = title_elem.find('a').get_text(strip=True)
                data['work_id'] = title_elem.find('a')['href'].split('/')[-1]
            else:
                return None
            
            # Author
            author_elem = work_element.find('a', rel='author')
            data['author'] = author_elem.get_text(strip=True) if author_elem else 'Anonymous'
            
            # Rating
            rating_elem = work_element.find('span', class_='rating')
            data['rating'] = rating_elem.get_text(strip=True) if rating_elem else 'Not Rated'
            
            # Warnings
            warnings_elem = work_element.find('span', class_='warnings')
            data['warnings'] = warnings_elem.get_text(strip=True) if warnings_elem else 'No Archive Warnings Apply'
            
            # Category
            category_elem = work_element.find('span', class_='category')
            data['category'] = category_elem.get_text(strip=True) if category_elem else 'N/A'
            
            # Fandoms
            fandoms_elem = work_element.find('h5', class_='fandoms')
            if fandoms_elem:
                data['fandoms'] = fandoms_elem.get_text(strip=True)
            else:
                data['fandoms'] = fandom
            
            # Tags
            tags = work_element.find_all('li', class_='freeforms')
            data['tags'] = ', '.join([tag.get_text(strip=True) for tag in tags[:10]])
            
            # Relationships
            relationships = work_element.find_all('li', class_='relationships')
            data['relationships'] = ', '.join([rel.get_text(strip=True) for rel in relationships[:5]])
            
            # Characters
            characters = work_element.find_all('li', class_='characters')
            data['characters'] = ', '.join([char.get_text(strip=True) for char in characters[:10]])
            
            # Stats
            stats = work_element.find('dl', class_='stats')
            if stats:
                # Language
                lang_elem = stats.find('dd', class_='language')
                data['language'] = lang_elem.get_text(strip=True) if lang_elem else 'English'
                
                # Words
                words_elem = stats.find('dd', class_='words')
                if words_elem:
                    words_text = words_elem.get_text(strip=True).replace(',', '')
                    data['words'] = int(words_text) if words_text.isdigit() else 0
                else:
                    data['words'] = 0
                
                # Chapters
                chapters_elem = stats.find('dd', class_='chapters')
                data['chapters'] = chapters_elem.get_text(strip=True) if chapters_elem else '1/1'
                
                # Kudos
                kudos_elem = stats.find('dd', class_='kudos')
                if kudos_elem:
                    kudos_text = kudos_elem.get_text(strip=True).replace(',', '')
                    data['kudos'] = int(kudos_text) if kudos_text.isdigit() else 0
                else:
                    data['kudos'] = 0
                
                # Bookmarks
                bookmarks_elem = stats.find('dd', class_='bookmarks')
                if bookmarks_elem:
                    bookmarks_text = bookmarks_elem.get_text(strip=True).replace(',', '')
                    data['bookmarks'] = int(bookmarks_text) if bookmarks_text.isdigit() else 0
                else:
                    data['bookmarks'] = 0
                
                # Hits
                hits_elem = stats.find('dd', class_='hits')
                if hits_elem:
                    hits_text = hits_elem.get_text(strip=True).replace(',', '')
                    data['hits'] = int(hits_text) if hits_text.isdigit() else 0
                else:
                    data['hits'] = 0
            
            # Summary
            summary_elem = work_element.find('blockquote', class_='summary')
            if summary_elem:
                data['summary'] = summary_elem.get_text(strip=True)[:self.SUMMARY_MAX_LENGTH]
            else:
                data['summary'] = ''
            
            return data
            
        except Exception as e:
            print(f"Error parsing work: {e}")
            return None
    
    def save_to_csv(self, data: List[Dict], filename: str):
        """
        Save scraped data to CSV file.
        
        Args:
            data: List of work dictionaries
            filename: Output CSV filename
        """
        if not data:
            print("No data to save")
            return
        
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Saved {len(data)} works to {filename}")
    
    def save_to_json(self, data: List[Dict], filename: str):
        """
        Save scraped data to JSON file.
        
        Args:
            data: List of work dictionaries
            filename: Output JSON filename
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(data)} works to {filename}")


def main():
    """Main function to scrape fanfiction data."""
    
    # Define fandoms to scrape
    fandoms = [
        "My Chemical Romance",
        "Fall Out Boy",
        "Sherlock",
        "Star Trek"
    ]
    
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


if __name__ == "__main__":
    main()
