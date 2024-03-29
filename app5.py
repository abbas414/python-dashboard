import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State
import base64
import io

# Create Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1('Upload CSV File and Plot Graphs'),
    dcc.Upload(
        id='upload-data',  # Fixed the typo here
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # Allow only one file to be uploaded
    ),
    dcc.Dropdown(
        id='x-axis',
        options=[],
        placeholder='Select X-axis parameter'
    ),
    dcc.Dropdown(
        id='y-axis',
        options=[],
        placeholder='Select Y-axis parameter'
    ),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'Scatter Plot', 'value': 'scatter'},
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Bar Chart', 'value': 'bar'},
            {'label': 'Pie Chart', 'value': 'pie'}
        ],
        placeholder='Select Graph Type',
        value='scatter'
    ),
    html.Button('Plot Graph', id='plot-button', n_clicks=0),
    dcc.Graph(id='graph')
])

# Define callback to update dropdown options based on uploaded CSV file
@app.callback(
    [Output('x-axis', 'options'),
     Output('y-axis', 'options')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_dropdowns(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Assuming the uploaded file is in CSV format
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        # Get column names for dropdown options
        dropdown_options = [{'label': col, 'value': col} for col in df.columns]
        
        return [dropdown_options, dropdown_options]
    else:
        return [[], []]

# Define callback to plot graph based on dropdown selections
@app.callback(
    Output('graph', 'figure'),
    [Input('plot-button', 'n_clicks')],
    [State('x-axis', 'value'),
     State('y-axis', 'value'),
     State('graph-type', 'value'),
     State('upload-data', 'contents')]
)
def plot_graph(n_clicks, x_axis, y_axis, graph_type, contents):
    if n_clicks > 0 and contents is not None and x_axis is not None and y_axis is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Assuming the uploaded file is in CSV format
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        # Plot graph using Plotly Express based on user's choice
        if graph_type == 'scatter':
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f'{y_axis} vs {x_axis}')
        elif graph_type == 'line':
            fig = px.line(df, x=x_axis, y=y_axis, title=f'{y_axis} vs {x_axis}')
        elif graph_type == 'bar':
            fig = px.bar(df, x=x_axis, y=y_axis, title=f'{y_axis} vs {x_axis}')
        elif graph_type == 'pie':
            fig = px.pie(df, values=y_axis, names=x_axis, title=f'{y_axis} by {x_axis}')
        
        return fig
    else:
        return {}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
