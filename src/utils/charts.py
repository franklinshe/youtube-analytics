import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# from io import BytesIO
# import base64
# def get_image():
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     image_png = buffer.getvalue()
#     graph = base64.b64encode(image_png)
#     graph = graph.decode('utf-8')
#     buffer.close()
#     return graph

def get_time_series_graph(x, data, labels):

    fig = go.Figure()
    for y, label in zip(data, labels):
        fig.add_trace(go.Scatter(
            x=x, y=y,
            name=label,
            hoverinfo='name+y',
            mode='lines',
            # line=dict(width=0.5, color='rgb(131, 90, 241)'),
            stackgroup='one' # define stack group
        ))
    return fig.to_html(full_html=False, default_height=800, default_width=1300)


def get_pie_chart(labels, sizes):

    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes)])

    return fig.to_html(full_html=False, default_height=800, default_width=1000)