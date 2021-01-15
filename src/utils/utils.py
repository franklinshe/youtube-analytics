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
    history_df = pd.DataFrame(history)                                              # turns json to panda dataframe
    history_df = history_df.dropna()
    history_df = history_df.drop(columns=['header', 'products'])                    # deletes header and products column
    history_df = history_df.rename(columns={'titleUrl':'url', 'subtitles':'channel'})  # renames columns
    history_df['title'] = history_df.apply(lambda row: row['title'][8:], axis=1)    # reformates title column
    history_df['channel_url'] = history_df.apply(lambda row: row['channel'][0]['url'], axis=1)
    history_df['channel'] = history_df.apply(lambda row: row['channel'][0]['name'], axis=1)
    history_df['id'] = history_df.apply(lambda row: row['url'][32:43], axis=1)      # creates videoID column

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
    return history_df