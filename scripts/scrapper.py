import requests
import json
import csv
from datetime import datetime
import time
import os


class Scrapper:
    secs_in_9_hours = 9 * 60 * 60
    fields = [
    'ups', 'retrieved_on', 'selftext', 'media', 'link_flair_text', 'permalink', 'title',
    'secure_media_embed', 'downs', 'thumbnail', 'distinguished', 'domain', 'hide_score',
    'created_utc', 'author_flair_text', 'media_embed', 'subreddit', 'score', 'edited',
    'quarantine', 'stickied', 'secure_media', 'url', 'subreddit_id', 'from_kind', 'is_self',
    'from', 'author', 'name', 'link_flair_css_class', 'gilded', 'archived', 'id',
    'num_comments', 'author_flair_css_class', 'saved', 'over_18'
]
    
    def __init__(self, subreddit='Bitcoin', start_epoch=1609459200, today=False, repo=True):
        self.today = int(time.time()) # Today's unix time
        self.subreddit = subreddit
        self.start_epoch = start_epoch if not today else self.today
        self.repo = repo

    def file_setup(self):
        if self.repo:
            self.output_file_path = f"../data/raw/{self.subreddit}_submissions.csv"
        else:
            self.output_file_path = f'{self.subreddit}_submissions.csv'
    
    def scrape(self):
        self.file_setup()
        with open(self.output_file_path, "a", encoding='utf-8', newline="") as output_file:
            writer = writer = csv.writer(output_file, escapechar='\\', quoting=csv.QUOTE_ALL)
            file_exist = os.path.isfile(self.output_file_path) and os.path.getsize(self.output_file_path) > 0
            if not file_exist:
                writer.writerow(self.fields)
            
            current_epoch = self.start_epoch
            file_lines = 0
            bad_lines = 0
            lines_added = 0

            while current_epoch <= self.today:
                try:
                    response = requests.get(f"https://api.pullpush.io/reddit/search/submission/?subreddit={self.subreddit}&after={current_epoch}&before={current_epoch + self.secs_in_9_hours}")
                    if response.status_code == 200:
                        data = response.json()['data']
                        for obj in data:
                            output_obj = []
                            for field in self.fields:
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
                    current_epoch += self.secs_in_9_hours

            print(f"Completed. Total lines: {file_lines}, Bad lines: {bad_lines}")


scrapper = Scrapper()
scrapper.scrape()
