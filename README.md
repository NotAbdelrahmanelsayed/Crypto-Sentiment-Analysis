# Crypto-Sentiment-Analysis

[Usage](#usage)
* [Scrapper](#scrapper)


### Scraper
The `scrapper.py` script is used to scrape data from specified subreddits. By default, it scrapes data for the `Bitcoin` subreddit from January 2021.

**Default usage**:
```bash
python scripts/scrapper.py
```
**arguments usage**:

*today=True: scrape data from 24 hours only*\
*subreddit="name of subreddit": default is Bitcoin*\
*path=The path to scrape the data default is data/raw/subreddit_submissions.csv*
```bash
python scripts/scrapper.py --today True --subreddit CryptoCurrency --path path/to/desired/dir
```
