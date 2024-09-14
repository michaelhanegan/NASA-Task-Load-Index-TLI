import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_radar_chart(scores):
    """
    Create a radar chart visualization of TLX scores.
    
    :param scores: Dictionary containing scores for each TLX dimension
    :return: Plotly figure object
    """
    df = pd.DataFrame(list(scores.items()), columns=['Dimension', 'Score'])
    fig = px.line_polar(df, r='Score', theta='Dimension', line_close=True)
    fig.update_traces(fill='toself')
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False
    )
    return fig

def create_bar_chart(scores):
    """
    Create a bar chart visualization of TLX scores.
    
    :param scores: Dictionary containing scores for each TLX dimension
    :return: Plotly figure object
    """
    df = pd.DataFrame(list(scores.items()), columns=['Dimension', 'Score'])
    fig = px.bar(df, x='Dimension', y='Score', text='Score')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_yaxes(range=[0, 100])
    return fig
