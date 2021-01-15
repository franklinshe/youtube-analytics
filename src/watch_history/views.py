import pandas as pd
import json
import requests
from utils.utils import reformat_history
from django.shortcuts import render
from django.conf import settings

def home(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['history_json'] # pulls uploaded file from html form
        request.session['history'] = json.loads(uploaded_file.read()) # sends json loaded file to session
        
    return render(request, 'watch_history/home.html', context)


def charts(request):
    history = request.session['history']
    history_df = reformat_history(history)

    if request.method == 'POST':
        print(request.POST)
        timeframe = request.POST.get('timeframe')
        print(timeframe)

    context = {
        'history': history_df.to_html()
    }
    return render(request, 'watch_history/charts.html', context)