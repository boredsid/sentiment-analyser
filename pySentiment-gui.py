import dash
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
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

    html.Td(dash_table.DataTable(id='tweet-data',columns=[{'name':col,'id':col} for col in ['Serial No.','Subject','Positive','Negative','# Tweets']],data=[])),
    html.Td(html.Div(id='top-tweets',children=[]))

    ])])

    ])


@app.callback([Output('tweet-data','data'),Output('top-tweets','children')],
                [Input('submit-button','n_clicks')],
                [State('search-term','value'),
                State('tweet-data','data')
                ])
def update_tweet_data(n_clicks,search_term,rows):
    if n_clicks!=0:
        new_data = pySentiment.TweetAnalyse(search_term)
        posShare = str(round(new_data[1]*100,2)) + "%"
        negShare = str(round(new_data[2]*100,2)) + "%"
        if rows!=[]:
            df = pd.DataFrame(rows,columns=['Serial No.','Subject','Positive','Negative','# Tweets'])
            count = df['Serial No.'].iloc[-1]
            df = df.append({'Serial No.':count+1,'Subject':search_term,'Positive':posShare,'Negative':negShare,'# Tweets':new_data[0]},ignore_index=True)
            table = df.to_dict('records')
        else:
            table = [{'Serial No.':1,'Subject':search_term,'Positive':posShare,'Negative':negShare,'# Tweets':new_data[0]}]
        top_tweets = [html.H3('Top Tweets for '+search_term+':')] + [html.P(x['text']) for x in new_data[3]] + [html.P(x['text']) for x in new_data[4]]
        return table,top_tweets
    else:
        return [],[]

if __name__ == '__main__':
    app.run_server()