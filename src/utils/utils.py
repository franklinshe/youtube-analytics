import pandas as pd
import json
import requests

from isodate import parse_duration
from django.conf import settings

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def reformat_history(history):
    """Reformat uploaded JSON history into pandas dataframe 
    and use Youtube Data API to add category and duration column."""
    history_df = pd.DataFrame(history)  
    history_df = history_df.drop(columns=['header', 'products', 'details','description'])
    history_df = history_df.dropna().reset_index(drop=True)
    history_df = history_df.rename(columns={'titleUrl':'url', 'subtitles':'channel'})
    history_df['title'] = history_df.apply(lambda row: row['title'][8:], axis=1)  
    history_df['channel_url'] = history_df.apply(lambda row: row['channel'][0]['url'], axis=1)
    history_df['channel'] = history_df.apply(lambda row: row['channel'][0]['name'], axis=1)
    history_df['id'] = history_df.apply(lambda row: row['url'][32:43], axis=1)
    history_df['date'] = history_df.apply(lambda row: row['time'][0:10], axis=1)
    history_df['time'] = history_df.apply(lambda row: row['time'][11:13], axis=1).astype('int64')
    history_df['date'] = pd.to_datetime(history_df['date'], format='%Y-%m-%d')

    category_dict = {}
    video_ids = []
    video_categories = []
    video_durations = []

    category_list_url = 'https://www.googleapis.com/youtube/v3/videoCategories'
    cateogry_list_params = {
        'part' : 'snippet',
        'regionCode' : 'US',
        'key' : settings.YOUTUBE_DATA_API_KEY
    }
    category_list_response = requests.get(category_list_url, params=cateogry_list_params)
    category_results = category_list_response.json()['items']

    for category in category_results:
        category_dict[category['id']] = category['snippet']['title']

    
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    for current_id in history_df['id']:
        video_ids.append(current_id)
    video_ids_chunks = list(chunks(video_ids, 50))
    
    for video_ids in video_ids_chunks:
        video_params = {
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'key' : settings.YOUTUBE_DATA_API_KEY
        }
        video_response = requests.get(video_url, params=video_params)
        results = video_response.json()['items']
        for result in results:
            video_categories.append(category_dict.get(result['snippet']['categoryId']))
            video_durations.append(parse_duration(result['contentDetails']['duration']))
    
    history_df['category'] = video_categories
    history_df['duration'] = video_durations
    history_df = history_df[['title','channel','id','category','duration','date','time','url','channel_url']]

    return history_df



def time_series_data(timeframe, bucket, today, history_df):
    time_series_dict = {}
    for i in range(timeframe//bucket): # maybe extra bucket here, fix range
        to_date = today - pd.Timedelta(i*bucket, unit='D')
        bucket_df = history_df[(history_df['date'] > to_date - pd.Timedelta(bucket+1, unit='D')) & (history_df['date'] < to_date)]
        time_series_dict[to_date] = bucket_df.groupby(['category']).size().to_dict()
    time_series_df = pd.DataFrame.from_dict(time_series_dict, orient='index').fillna(0).astype('int64')
    # print(time_series_df.to_numpy().sum())
    # print(time_series_df)
    # print(time_series_df.info())
    return time_series_df

