# QVL-Search: Gigabyte Server QVL Crawler

A Python web crawler designed to check Gigabyte's website for server QVL (Qualified Vendor List) compatibility with SSDs, specifically targeting **TRUSTA** and **T7P5** products.

## 🚀 Features

### Ver4 (Latest) - Smart URL Generation
- **🎯 Character-Based Categorization**: Efficiently determines server category from model's first character
- **🔄 Redirect Detection**: Automatically detects and logs final URLs after redirects
- **🔧 Version Suffix Fallback**: Tries `-rev-3x` and `-rev-1x` suffixes when base URL fails
- **⚡ Performance**: ~60-70% reduction in HTTP requests compared to brute-force approach

### Ver3 - Sequential Flow
- **🔄 Sequential Processing**: Detect server URL → If valid, crawl QVL → Move to next server
- **💾 Memory Efficient**: Processes servers individually instead of batch loading
- **🖥️ Cross-Platform**: Windows and Linux compatible Chrome driver configuration

## 📊 Crawler Flow


## 🛠️ Technical Stack

- **Python 3.9+** (tested)
- **Selenium WebDriver** - Browser automation
- **BeautifulSoup4** - HTML parsing
- **Pandas** - Data processing
- **Chrome/Chromium** - Headless browser

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/tiger423/QVL-search.git
cd QVL-search

# Install dependencies
pip install -r requirements.txt

# Run the crawler
python crawler-SSD.py
```

##To run the code under virtual enviroment 

##Windows:



git clone https://github.com/tiger423/QVL-search.git    # clone the codes

cd QVL-search                                           # get into the code folder

python -m venv my-venv    # create a virtual environment called my-venv (can be whatever name you like)

my-venv\scripts\activate  # activate crawler virtual environment

.still inside QVL-search folder
.since my-venv is activated, this pip is from my-venv\scripts\pip.exe. all packages will be installed 
.in QVL-search\my-venv\Lib\site-packages

pip install -r requirements.txt 

python crawler-SSD.py



## 🎯 Server Categorization (Ver4)

The crawler automatically categorizes servers based on their model's first character:

| First Character | Category | Example |
|----------------|----------|---------|
| **G** | GPU-Server | G293-S40-AAP1 |
| **R** | Rack-Server | R183-S95-AAD1 |
| **H** | High-Density-Server | H263-S66-AAW1 |
| **S** | Storage-Server | S123-TEST |
| **X** | Rack-Server | X456-TEST |
| **E** | Rack-Server | E789-TEST |
| **Other** | General-Purpose-Server | Z999-TEST |

## 📁 Output Files

The crawler generates several CSV files:

1. **`valid_servers_list_*.csv`** - List of servers with valid QVL pages
2. **`qvl_data_batch_*.csv`** - Raw QVL data extracted from tables
3. **`trusta_t7p5_matches_*.csv`** - Servers with TRUSTA/T7P5 compatibility
4. **`final_summary_statistics_*.csv`** - Summary statistics and counts

## 🔧 Configuration

Key parameters in `crawler-SSD.py`:

- **Base URLs**: Gigabyte Enterprise server pages
- **Server Models**: Comprehensive list of Gigabyte server models
- **Rate Limiting**: Random delays (2-4 seconds) between requests
- **Batch Size**: Configurable QVL data batch processing

## 📈 Performance Improvements

### Ver4 vs Ver3 Efficiency
- **Ver3**: Brute-force approach (10-14 HTTP requests per server)
- **Ver4**: Smart categorization (2-6 HTTP requests per server)
- **Improvement**: ~60-70% reduction in network requests

## 🐛 Troubleshooting

### Chrome Driver Issues
- Ensure Chrome/Chromium is installed
- Check Chrome driver compatibility with your Chrome version
- For Windows: Use the ver3+ branch for compatibility fixes

### Network Issues
- The crawler includes rate limiting to avoid being blocked
- Random delays between requests help prevent detection
- Retry logic handles temporary network failures

## 📝 Version History

- **Ver4**: Smart URL generation with character-based categorization
- **Ver3**: Sequential flow processing + Windows Chrome driver fix
- **Ver2**: Basic crawler with batch processing
- **Ver1**: Initial implementation

## 🤝 Contributing

This program is tested with Python 3.9. Feel free to submit issues or pull requests for improvements.
