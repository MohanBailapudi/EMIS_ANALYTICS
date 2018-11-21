import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt
from collections import deque
import plotly.graph_objs as go
import random
from dash.dependencies import Input, Output, Event

app = dash.Dash()

max_length = 1440
WSHP = deque(maxlen=max_length)
format_str = '%d/%m/%Y' # The format


data_dict = {
    'CH5-A/C: WSHP1' : "",
    'CH16-DHW Gas Instant':""
}

app.layout = html.Div([
    html.Div([
        html.H2('Usage vs Time', style={'float':'left'}),
    ]),
    dcc.Dropdown(id = 'load-data-name',
                 options=[{'label':s,'value':s} for s in data_dict.keys()],
                 value=['CH5-A/C: WSHP1','CH16-DHW Gas Instant'],
                 multi=True
                 ),
    html.Div([
        html.Div([
            dcc.DatePickerSingle(
                id='my-date-picker',
                min_date_allowed=dt(1995, 8, 5),
                max_date_allowed=dt(2018, 9, 19),
                initial_visible_month=dt(2018, 1, 1),
                date=dt(2018, 1, 1)
            )
        # html.Div(id='output-container-date-picker-range'),
        ]),
        html.Button('Graph', id='button'),
        html.Div(children=html.Div(id = 'graphs'),className='row')
    ]),
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div([
        html.H2('Portfolio Accounting', style={'float': 'left'}),
    ]),
    html.Div(children=html.Div(id = 'horizontal_bar_graphs'),className='row')],
    className='container',style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000 })

# @app.callback(
#     Output(component_id='intermediate-value',component_property='children'),
#     [Input(component_id='load-data-name',component_property='value'),Input(component_id='my-date-picker',component_property='date')]
# )
# def save_inputs(data_names,date):
#     print(date)
#     return [data_names,date]


@app.callback(
    Output(component_id='graphs',component_property='children'),
    [Input(component_id='load-data-name',component_property='value'),Input(component_id='my-date-picker',component_property='date')],
    events = [Event(component_id='button',component_event='click')]
)

# @app.callback(
#     Output(component_id='graphs',component_property='children'),
#     [Input(component_id='intermediate-value',component_property='children')]
# )
def update_graph(data_names,date):
    graphs = []
    path = r"C:\Users\MohanB\Desktop\minuteData\2018\201801.csv"

    print(data_names)
    if len(data_names) > 2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'
    if date!= None:
        for data_name in data_names:
            data = pd.read_csv(path, skiprows=6, low_memory=False)
            data = data.fillna(0)
            data['date'] = pd.to_datetime(data[' Date/Time'])
            data['just_date'] = data['date'].dt.date
            print(type(data))
            data2 = data.loc[data['just_date'] == dt.strptime(date, '%Y-%m-%d').date()]
            data2[data_name].apply(int)
            trace = go.Scatter(
                # x = data.index.tolist(),
                x = data2['date'],
                y=data2[data_name].tolist(),
                mode = 'lines',
                name = data_name,
                fill = "tozeroy",
                fillcolor="#6897bb"
            )
            data = [trace]
            layout = go.Layout(
                title='{}'.format(data_name),
                # xaxis=dict(range=[min(data['time']), max(data['time'])]),
                # yaxis=dict(range=[min(data2[data_name].tolist()), max(data2[data_name].tolist())])
            )
            fig = go.Figure(data = data, layout = layout)
            graph = html.Div([dcc.Graph(
                id = data_name,
                animate = True,
                figure = fig
            )],className=class_choice)
            graphs.append(graph)
    return graphs

@app.callback(
    Output(component_id='horizontal_bar_graphs',component_property='children'),
    [Input(component_id='load-data-name',component_property='value'),Input(component_id='my-date-picker',component_property='date')],
    events = [Event(component_id='button',component_event='click')]
)

def update_graph1(data_names,date):
    graphs = []
    Y = []
    path = r"C:\Users\MohanB\Desktop\minuteData\2018\201801.csv"
    print(data_names)
    if len(data_names) > 2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'
    if date != None:
        for data_name in data_names:
            data = pd.read_csv(path, skiprows=6, low_memory=False)
            data = data.fillna(0)
            data['date'] = pd.to_datetime(data[' Date/Time'])
            data['just_date'] = data['date'].dt.date
            print(type(data))
            data2 = data.loc[data['just_date'] == dt.strptime(date, '%Y-%m-%d').date()]
            data2[data_name].apply(int)
            Y.append(data2[data_name].sum())
        trace = go.Bar(
            # x = data.index.tolist(),
            x=Y,
            y=data_names,
            orientation='h'
        )
        data = [trace]
        layout = go.Layout(
            title='Portfilo Accounting',
            autosize=False,
            # width=500,
            height=500,
            yaxis=go.layout.YAxis(
                title='Y-axis Title',
                ticktext=data_names,
                automargin=True,
                titlefont=dict(size=30),
            )
                # xaxis=dict(range=[min(data['time']), max(data['time'])]),
                # yaxis=dict(range=[min(data2[data_name].tolist()), max(data2[data_name].tolist())])
        )

        fig = go.Figure(data=data, layout=layout)
        graph = html.Div([dcc.Graph(
            id=data_name,
            animate=True,
            figure=fig
        )], className=class_choice)
        graphs.append(graph)
    return graphs



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=True)