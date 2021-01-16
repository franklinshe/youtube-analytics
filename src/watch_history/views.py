import pandas as pd
import json
import requests
from datetime import date, timedelta
from utils.utils import reformat_history, time_series_data, get_time_series_graph
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
    history = request.session['history']
    history_df = pd.read_json(history)
    history_df_truncated = history_df
    if request.method == 'POST':
        timeframe = request.POST.get('timeframe')
        today = pd.Timestamp('today').floor('D')
        history_df_truncated = history_df[(history_df['date'] > today - pd.Timedelta(int(timeframe), unit='D')) & (history_df['date'] < today)]
        
        time_series_df = time_series_data(timeframe, today, history_df_truncated)
        time_series_graph = get_time_series_graph(x=list(time_series_df.index.values),y=time_series_df.transpose().to_numpy(),labels=list(time_series_df.columns.values))

    context = {
        'history': history_df_truncated.to_html(),
        'graph': time_series_graph
    }
    return render(request, 'watch_history/charts.html', context)