import pandas as pd
import json
import requests
from utils.utils import reformat_history
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
    history = request.session['history']
    history_df = pd.read_json(history)

    if request.method == 'POST':
        print(request.POST)
        timeframe = request.POST.get('timeframe')
        print(timeframe)

    context = {
        'history': history_df.to_html()
    }
    return render(request, 'watch_history/charts.html', context)