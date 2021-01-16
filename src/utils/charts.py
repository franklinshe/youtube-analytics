import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from io import BytesIO
import base64


def get_image():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_time_series_graph(x, y, labels):
    # print(x)
    # print(y)
    # print(labels)
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,4))
    plt.title("Categories Over Time")
    # x = kwargs.get('x')
    # y = kwargs.get('y')
    # labels = kwargs.get('labels')
    plt.stackplot(x,y,labels=labels)
    plt.legend(loc='upper left')
    # df.plot.area()
    
    graph = get_image()
    return graph

def get_pie_chart(labels, sizes):
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    graph = get_image()
    return graph