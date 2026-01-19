# silly-data-fun

Peering into silly data to gain insights on silly stuffs! 🎭📊

## Project Overview

This project scrapes fanfiction data from **Archive of Our Own (AO3)** for various fandoms and performs comprehensive data analysis to uncover interesting patterns and insights. The project focuses on fanfictions from:

- **My Chemical Romance** 🎸
- **Fall Out Boy** 🎤
- **Sherlock** 🔍
- **Star Trek** 🚀

## Features

### Data Scraping (`src/ao3_scraper.py`)
- Respectful web scraping with built-in rate limiting (5 seconds between requests)
- Extracts metadata including:
  - Title, Author, Rating, Category
  - Word count, Chapter count
  - Engagement metrics (Kudos, Bookmarks, Hits)
  - Tags, Characters, Relationships
  - Summaries
- Saves data in both CSV and JSON formats
- Implements proper User-Agent headers

### Data Analysis (`src/analyzer.py`)
- **Basic Statistics**: Total works, unique authors, average metrics
- **Rating Analysis**: Distribution across fandoms
- **Word Count Analysis**: 
  - Distribution patterns
  - Correlation with engagement
  - Comparison across fandoms
- **Engagement Metrics**:
  - Kudos, Bookmarks, and Hits analysis
  - Kudos-to-Hits ratio (engagement quality)
  - Normalized comparisons
- **Category Distribution**: Relationship types across fandoms
- **Top Works**: By kudos, hits, and word count
- **Visualizations**: All analyses include beautiful matplotlib/seaborn charts

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/raraminavis/silly-data-fun.git
cd silly-data-fun
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start: Run the Demo

Try the demo with sample data to see what the project does:

```bash
python demo.py
```

This will:
- Generate sample fanfiction data
- Run all analyses
- Create visualizations in the `outputs/` directory
- Show you what to expect from real data

### Option 1: Interactive Mode (Recommended)

Run the main script and choose what to do:

```bash
python main.py
```

You'll be prompted to:
1. Scrape data from AO3
2. Analyze existing data
3. Both (scrape then analyze)

### Option 2: Run Modules Individually

**Scrape data only**:
```bash
python src/ao3_scraper.py
```

**Analyze data only** (requires existing `data/ao3_fanfictions.csv`):
```bash
python src/analyzer.py
```

## Project Structure

```
silly-data-fun/
├── README.md
├── requirements.txt
├── .gitignore
├── main.py                    # Main pipeline script
├── demo.py                    # Demo with sample data
├── test_validation.py         # Validation tests
├── src/
│   ├── __init__.py
│   ├── ao3_scraper.py        # AO3 web scraper
│   └── analyzer.py           # Data analysis module
├── data/                      # Scraped data (gitignored)
│   ├── ao3_fanfictions.csv
│   └── ao3_fanfictions.json
└── outputs/                   # Analysis outputs (gitignored)
    ├── rating_analysis.png
    ├── word_count_analysis.png
    ├── engagement_analysis.png
    └── category_analysis.png
```

## Output Examples

After running the analysis, you'll get:

1. **Console Output**:
   - Summary statistics
   - Top works by various metrics
   - Key insights

2. **Visualizations** (saved to `outputs/` directory):
   - Rating distribution charts
   - Word count analysis plots
   - Engagement metrics comparisons
   - Category breakdowns

## Data Fields

Each scraped work includes:

| Field | Description |
|-------|-------------|
| `title` | Work title |
| `author` | Author username |
| `work_id` | Unique AO3 work ID |
| `rating` | Content rating (G, T, M, E, etc.) |
| `category` | Relationship category (M/M, F/F, Gen, etc.) |
| `warnings` | Archive warnings |
| `fandoms` | Associated fandoms |
| `tags` | Freeform tags |
| `relationships` | Character relationships |
| `characters` | Featured characters |
| `words` | Word count |
| `chapters` | Chapter info (e.g., "5/10") |
| `kudos` | Number of kudos |
| `bookmarks` | Number of bookmarks |
| `hits` | Number of hits |
| `language` | Work language |
| `summary` | Brief summary |

## Ethical Considerations

This project respects AO3's Terms of Service:
- ✅ Only scrapes publicly available metadata
- ✅ Implements rate limiting (5 second delay between requests)
- ✅ Uses appropriate User-Agent headers
- ✅ Does not scrape the actual fanfiction content
- ✅ Does not overload AO3 servers

## Future Enhancements

Potential additions mentioned in the project vision:
- 🧠 Neural network analysis (sentiment analysis, topic modeling)
- 📈 Time-series analysis of fandom trends
- 🔗 Network analysis of character relationships
- 🎨 More advanced visualizations
- 📊 Comparative analysis across more fandoms

## Dependencies

- `requests` - HTTP library for web scraping
- `beautifulsoup4` - HTML parsing
- `pandas` - Data manipulation and analysis
- `matplotlib` - Data visualization
- `seaborn` - Statistical visualizations
- `numpy` - Numerical computing

## License

This is a personal data analysis project for educational purposes.

## Contributing

Feel free to fork, experiment, and submit pull requests!

## Author

Created as part of exploring silly data to gain insights on silly stuffs! 🎉
