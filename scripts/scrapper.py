import argparse
import json
import csv
import time
import os

import requests


class Scrapper:
    SECS_IN_9_HOURS = 9 * 60 * 60
    FIELDS = [
    'ups', 'retrieved_on', 'selftext', 'media', 'link_flair_text', 'permalink', 'title',
    'secure_media_embed', 'downs', 'thumbnail', 'distinguished', 'domain', 'hide_score',
    'created_utc', 'author_flair_text', 'media_embed', 'subreddit', 'score', 'edited',
    'quarantine', 'stickied', 'secure_media', 'url', 'subreddit_id', 'from_kind', 'is_self',
    'from', 'author', 'name', 'link_flair_css_class', 'gilded', 'archived', 'id',
    'num_comments', 'author_flair_css_class', 'saved', 'over_18'
]
    START_EPOCH = 1609459200
    def __init__(self, subreddit, today, path):
        self.today = int(time.time()) - (24 * 60 * 60) # unix time at yesterday
        self.subreddit = subreddit
        self.start_epoch = self.START_EPOCH if not today else self.today
        self.output_file_path = path

        os.makedirs(os.path.dirname(self.output_file_path), exist_ok=True)
    def scrape(self):
        with open(self.output_file_path, "a", encoding='utf-8', newline="") as output_file:
            writer = writer = csv.writer(output_file, escapechar='\\', quoting=csv.QUOTE_ALL)
            file_exist = os.path.isfile(self.output_file_path) and os.path.getsize(self.output_file_path) > 0
            if not file_exist:
                writer.writerow(self.FIELDS)
            
            current_epoch = self.start_epoch
            file_lines = 0
            bad_lines = 0
            lines_added = 0

            while current_epoch <= self.today:
                try:
                    response = requests.get(f"https://api.pullpush.io/reddit/search/submission/?subreddit={self.subreddit}&after={current_epoch}&before={current_epoch + self.SECS_IN_9_HOURS}")
                    if response.status_code == 200:
                        data = response.json()['data']
                        for obj in data:
                            output_obj = []
                            for field in self.FIELDS:
                                output_obj.append(obj.get(field, None))
                            writer.writerow(output_obj)
                            file_lines += 1
                            lines_added += 1
                            if lines_added % 100 == 0:
                                print(f'progress: {lines_added} lines added....')
                    else:
                        print(f"Failed to fetch data for epoch {current_epoch}. Status code: {response.status_code}")
                except json.JSONDecodeError as e:
                    bad_lines += 1
                    print(f"JSONDecodeError for epoch {current_epoch}: {e}")
                except Exception as e:
                    print(f"Unexpected error for epoch {current_epoch}: {e}")
                finally:
                    current_epoch += self.SECS_IN_9_HOURS

            print(f"Completed. Total lines: {file_lines}, Bad lines: {bad_lines}")


if __name__ == '__main__':
    # Parse the arguments
    parser = argparse.ArgumentParser(description='Reddit scrapper')
    parser.add_argument('--subreddit', default='Bitcoin', help='Specify the subreddit name i.e(Bitcoin..)')
    parser.add_argument('--today', type=bool, default=False, help='Specify to start scrapping data from yesterday\'s date or from 2021')
    parser.add_argument('--path', help='path to save the scrapped the data. By default will be saved in data/raw folder')
    args = parser.parse_args()
    path = args.path or f"../data/raw/{args.subreddit}_submissions.csv" 
    
    scrapper = Scrapper(args.subreddit, args.today, path)
    scrapper.scrape()