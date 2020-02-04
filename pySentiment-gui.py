import dash
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pySentiment

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
server.secret_key = os.environ.get('secret_key', 'secret')

app.layout = html.Div(children=[
    html.H1(children='Sentiment Analyser'),
    html.Div(children='''
        Enter Keywords to See Results
    '''),

    dcc.Input(id='search-term',value='',type='text'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),

    html.Br(),

    html.Table([html.Tr([

    html.Td(html.Table(id='tweet-data',children=[html.Tr([html.Th(col) for col in ['Serial No.','Subject','Positive','Negative','# Tweets']])])),
    html.Td(html.Div(id='top-tweets',children=[]))

    ])])

    ])

count = 0

@app.callback([Output('tweet-data','children'),Output('top-tweets','children')],
                [Input('submit-button','n_clicks')],
                [State('search-term','value'),
                State('tweet-data','children')
                ])
def update_tweet_data(n_clicks,search_term,table):
    global count
    top_tweets = []
    if n_clicks!=0:
        subs = [table[i]['props']['children'][1]['props']['children'] for i in range(len(table))]
        new_data = pySentiment.TweetAnalyse(search_term)
        if search_term in subs:
            pos = subs.index(search_term)
            table[pos]['props']['children'][2]['props']['children'] = new_data[1]
            table[pos]['props']['children'][3]['props']['children'] = new_data[2]
            table[pos]['props']['children'][4]['props']['children'] = new_data[0]
        else:
            count += 1
            table = table + [html.Tr([html.Td(x) for x in [count,search_term,new_data[1],new_data[2],new_data[0]]])]
        top_tweets = [html.H3('Top Tweets for '+search_term+':')] + [html.P(x['text']) for x in new_data[3]] + [html.P(x['text']) for x in new_data[4]]
    return table,top_tweets

if __name__ == '__main__':
    app.run_server()