# import requests
# import json
# import csv
# from datetime import datetime
# import time
# import os

# today = int(time.time()) # unix time
# # Constants
# start_epoch = 1609459200
# secs_in_9_hours = 9 * 60 * 60
# subreddits = ['Bitcoin', 'CryptoCurrency']
# fields = ['ups', 'retrieved_on', 'selftext', 'media', 'link_flair_text', 'permalink', 'title', 'secure_media_embed', 'downs', 'thumbnail', 'distinguished', 'domain', 'hide_score', 'created_utc', 'author_flair_text', 'media_embed', 'subreddit', 'score', 'edited', 'quarantine', 'stickied', 'secure_media', 'url', 'subreddit_id', 'from_kind', 'is_self', 'from', 'author', 'name', 'link_flair_css_class', 'gilded', 'archived', 'id', 'num_comments', 'author_flair_css_class', 'saved', 'over_18']

# for subreddit in subreddits:
#     # File setup
#     output_file_path = f"../data/raw/{subreddit}_submissions.csv"

#     # Check if file exists and its size to determine if header needs to be written
#     file_exists = os.path.isfile(output_file_path) and os.path.getsize(output_file_path) > 0

#     with open(output_file_path, "a", encoding='utf-8', newline="") as output_file:
#         writer = csv.writer(output_file, escapechar='\\', quoting=csv.QUOTE_ALL)
#         if not file_exists:
#             writer.writerow(fields)

#         current_epoch = start_epoch
#         file_lines = 0
#         bad_lines = 0
#         lines_added = 0

#         while current_epoch <= today:
#             try:
#                 response = requests.get(f"https://api.pullpush.io/reddit/search/submission/?subreddit={subreddit}&after={current_epoch}&before={current_epoch + secs_in_9_hours}")
#                 if response.status_code == 200:
#                     data = response.json()['data']
#                     for obj in data:
#                         output_obj = []
#                         for field in fields:
#                             output_obj.append(obj.get(field, None))
#                         writer.writerow(output_obj)
#                         file_lines += 1
#                         lines_added += 1
#                         if lines_added % 100 == 0:
#                             print(f'progress: {lines_added} lines added....')
#                 else:
#                     print(f"Failed to fetch data for epoch {current_epoch}. Status code: {response.status_code}")
#             except json.JSONDecodeError as e:
#                 bad_lines += 1
#                 print(f"JSONDecodeError for epoch {current_epoch}: {e}")
#             except Exception as e:
#                 print(f"Unexpected error for epoch {current_epoch}: {e}")
#             finally:
#                 current_epoch += secs_in_9_hours

#         print(f"Completed. Total lines: {file_lines}, Bad lines: {bad_lines}")




import requests
import json
import csv
from datetime import datetime
import time
import os

today = int(time.time())  # unix time
# Constants
start_epoch = 1609459200
secs_in_9_hours = 9 * 60 * 60
subreddits = ['Bitcoin', 'CryptoCurrency']
fields = ['ups', 'retrieved_on', 'selftext', 'media', 'link_flair_text', 'permalink', 'title', 'secure_media_embed', 'downs', 'thumbnail', 'distinguished', 'domain', 'hide_score', 'created_utc', 'author_flair_text', 'media_embed', 'subreddit', 'score', 'edited', 'quarantine', 'stickied', 'secure_media', 'url', 'subreddit_id', 'from_kind', 'is_self', 'from', 'author', 'name', 'link_flair_css_class', 'gilded', 'archived', 'id', 'num_comments', 'author_flair_css_class', 'saved', 'over_18']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for subreddit in subreddits:
    # File setup
    output_file_path = f"../data/raw/{subreddit}_submissions.csv"

    # Check if file exists and its size to determine if header needs to be written
    file_exists = os.path.isfile(output_file_path) and os.path.getsize(output_file_path) > 0

    with open(output_file_path, "a", encoding='utf-8', newline="") as output_file:
        writer = csv.writer(output_file, escapechar='\\', quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writerow(fields)

        current_epoch = start_epoch
        file_lines = 0
        bad_lines = 0
        lines_added = 0

        while current_epoch <= today:
            try:
                response = requests.get(f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&after={current_epoch}&before={current_epoch + secs_in_9_hours}", headers=headers)
                if response.status_code == 200:
                    data = response.json()['data']
                    for obj in data:
                        output_obj = []
                        for field in fields:
                            output_obj.append(obj.get(field, None))
                        writer.writerow(output_obj)
                        file_lines += 1
                        lines_added += 1
                        if lines_added % 100 == 0:
                            print(f'progress: {lines_added} lines added....')
                else:
                    print(f"Failed to fetch data for epoch {current_epoch}. Status code: {response.status_code}")
                    if response.status_code == 403:
                        print("Access forbidden. Check if you need to provide API key or credentials.")
                    if response.status_code == 502:
                        time.sleep(5)  # Wait for 5 seconds before retrying
            except json.JSONDecodeError as e:
                bad_lines += 1
                print(f"JSONDecodeError for epoch {current_epoch}: {e}")
            except requests.RequestException as e:
                print(f"RequestException for epoch {current_epoch}: {e}")
                time.sleep(5)  # Wait for 5 seconds before retrying
            except Exception as e:
                print(f"Unexpected error for epoch {current_epoch}: {e}")
            finally:
                current_epoch += secs_in_9_hours

        print(f"Completed. Total lines: {file_lines}, Bad lines: {bad_lines}")