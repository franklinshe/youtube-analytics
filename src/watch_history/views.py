import pandas as pd
import json
import requests
from datetime import date, timedelta
from utils.utils import reformat_history, time_series_data
from utils.charts import get_time_series_graph, get_pie_chart
from django.shortcuts import render
from django.conf import settings

def home(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['history_json']
        history_df = reformat_history(json.loads(uploaded_file.read()))
        request.session['history'] = history_df.to_json()
        
    return render(request, 'watch_history/home.html', context)


def charts(request):
    time_series_graph = None
    pie_chart = None
    categories = None
    recent_df_html = None
    bucket = None

    history = request.session['history']
    history_df = pd.read_json(history)
    history_df_truncated = history_df
    if request.method == 'POST':
        timeframe = request.POST.get('timeframe')
        category = request.POST.get('category')
        bucket = int(request.POST.get('bucket'))
        today = pd.Timestamp('today').floor('D')
        
        if timeframe == 'all_time':
            time_delta = today - history_df['date'].iat[-1]
            time_series_df = time_series_data(time_delta.days, bucket, today, history_df)
        else:
            timeframe = int(timeframe)
            history_df_truncated = history_df[(history_df['date'] > today - pd.Timedelta(timeframe, unit='D')) & (history_df['date'] < today)]
            time_series_df = time_series_data(timeframe, bucket, today, history_df_truncated)
        
        time_series_graph = get_time_series_graph(list(time_series_df.index), time_series_df.transpose().to_numpy(), list(time_series_df.columns.values))
        
        pie_chart_df = history_df_truncated.groupby(['category']).size().reset_index(name='count')
        categories = pie_chart_df.loc[:,'category'].tolist()
        pie_chart = get_pie_chart(categories, pie_chart_df.loc[:,'count'].tolist())

        recent_df_html = history_df.loc[history_df['category'] == category].drop(columns=['url', 'channel_url', 'time', 'id']).head(20).to_html()

    context = {
        'categories': categories,
        
        'graph': time_series_graph,
        'pie': pie_chart,
        'recents': recent_df_html
    }
    return render(request, 'watch_history/charts.html', context)

#TODO both time series and pie chart are a broken...
    # fix buckets: either user chooses bucket or default value, make sure value of bucket matches days grouped by
    # fix selectors, stay on value chosen when submitted
    # create others category which groups all videos outside top 7 categories (for better visability)
    # fix time series x axis, dates are correct/match bucket size
    # fix duration format??? time delta 
    # make recents table nicer, with hyperlinks to channel and video
    # add more charts, and implement tab feature where only one chart at a time is shown and the rest hidden
    # Add summary statistics and interesting stats in column

def table(request):
    history = request.session['history']
    history_df = pd.read_json(history)
    context = {
        'history': history_df.to_html()
    }
    return render(request, 'watch_history/table.html', context)