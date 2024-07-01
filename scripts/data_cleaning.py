import re 
import os
import string

import pandas as pd
import numpy as np

class CleanData:
    def __init__(self, data_path, output_path):
        self.data_path = data_path
        self.output_path = output_path
    
    def read_data(self):
        return pd.read_csv(self.data_path)
    
    def clean_data(self):
        df = self.read_data()
        df['cleaned_text'] = df['selftext'].apply(lambda x: self.clean_text(x))
        df['title'] = df['title'].apply(self.clean_text)
        df['date'] = pd.to_datetime(df.created_utc, unit='s').dt.date
        
        # Keep the neccessary features for sentiment analysis
        df = df[['cleaned_text', 'title', 'date']]
        
        # Save the cleaned dataframe
        df.to_csv(self.output_path, index=False)
        return df

    def clean_text(self, text):
        ## AI generate for (re).
        if isinstance(text, str):  # check if text is a string
            text = text.lower()  # convert text to lower case
            text = re.sub(r'\[.*?\]', '', text)  # remove text in square brackets
            text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)  # remove punctuation
            text = re.sub(r'\w*\d\w*', '', text)  # remove words containing numbers
            return text
        else:
            return ""

if __name__ == '__main__':
    data_path = '../data/raw/Bitcoin_submissions.csv'
    output_path = '../data/processed/Bitcoin_cleaned.csv'
    data_cleaner = CleanData(data_path, output_path)
    data_cleaner.clean_data()