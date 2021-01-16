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

    history = request.session['history']
    history_df = pd.read_json(history)
    history_df_truncated = history_df
    if request.method == 'POST':
        timeframe = request.POST.get('timeframe')
        category = request.POST.get('category')
        today = pd.Timestamp('today').floor('D')
        history_df_truncated = history_df[(history_df['date'] > today - pd.Timedelta(int(timeframe), unit='D')) & (history_df['date'] < today)]
        
        time_series_df = time_series_data(timeframe, today, history_df_truncated)
        time_series_graph = get_time_series_graph(x=list(time_series_df.index.values),y=time_series_df.transpose().to_numpy(),labels=list(time_series_df.columns.values))
        
        print(category)
        pie_chart_df = history_df_truncated.groupby(['category']).size().reset_index(name='count')
        categories = pie_chart_df.loc[:,'category'].tolist()
        pie_chart = get_pie_chart(labels=categories,sizes=pie_chart_df.loc[:,'count'].tolist())
        recent_df_html = history_df.loc[history_df['category'] == category].drop(columns=['url', 'channel_url', 'time', 'id']).head(10).to_html()

    context = {
        'categories': categories,
        
        'graph': time_series_graph,
        'pie': pie_chart,
        'recents': recent_df_html
    }
    return render(request, 'watch_history/charts.html', context)

#TODO both time series and pie chart are a broken...
#     add "all_time" functionality
#     fix duration format??? time delta 
#     make recents table nicer, with hyperlinks to channel and video
#     add more charts, and implement tab feature where only one chart at a time is shown and the rest hidden
#     Add summary statistics and interesting stats in column

def table(request):
    history = request.session['history']
    history_df = pd.read_json(history)
    context = {
        'history': history_df.to_html()
    }
    return render(request, 'watch_history/table.html', context)