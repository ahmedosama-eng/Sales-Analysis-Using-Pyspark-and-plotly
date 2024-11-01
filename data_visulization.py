import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from data_transformer import AggOrders

# Load the data into a DataFrame
df = AggOrders.toPandas()

# Extract unique values for filtering
years = df['year'].unique()
item_types = df['ItemType'].unique()
countries = df['Country'].unique()
regions = df['Regoin'].unique()
channels = df['SalesChannel'].unique()
priorities = df['OrderPriority'].unique()

# Define metrics for the Y-axis selection
metrics = [
    'Number of orders', 'Number of Units Sold', 'Average of Unit Price',
    'Average of Unit Cost', 'Total Cost', 'Total Profit', 'Total Revenue'
]

# Define the correct order for months
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Convert 'Month' column from numeric to month names
df['Month Name'] = df['Month'].map(lambda x: month_order[x - 1])

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    style={
        'background-image': 'url("https://wallpapers.com/images/high/sales-1600-x-900-background-1gjk99udiabzoqmb.webp")',
        'background-size': 'cover',
        'background-position': 'center',
        'background-attachment': 'fixed',
        'min-height': '100vh',
        'padding': '30px',
    },
    children=[
        html.Div(
            className="content",
            style={
                'background-color': 'rgba(255, 255, 255, 0.8)',
                'border-radius': '15px',
                'padding': '20px',
                'max-width': '1200px',
                'margin': '30px auto',
            },
            children=[
                html.H1(
                    "Sales Dashboard",
                    style={
                        'text-align': 'center',
                        'color': 'white',
                        'text-shadow': '2px 2px 4px rgba(0, 0, 0, 0.8)',
                    },
                ),

                # Year selection buttons
                html.Div([
                    html.Label("Select Year:", style={'margin-right': '10px'}),
                    *[
                        html.Button(
                            str(year),
                            id=f'year-{year}',
                            n_clicks=0,
                            style={
                                'width': '80px', 'height': '40px', 'margin': '5px',
                                'background-color': '#e0e0e0', 'border-radius': '5px'
                            }
                        ) for year in years
                    ]
                ], style={'text-align': 'center', 'margin': '20px 0'}),

                # Multi-select filters
                html.Div([
                    html.Div([
                        html.Label("Item Type:", style={'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id='item-type-filter',
                            options=[{'label': i, 'value': i} for i in item_types],
                            placeholder='Select Item Type(s)',
                            multi=True,
                            style={'width': '300px'}
                        )
                    ]),
                    html.Div([
                        html.Label("Country:", style={'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id='country-filter',
                            options=[{'label': c, 'value': c} for c in countries],
                            placeholder='Select Country(s)',
                            multi=True,
                            style={'width': '300px'}
                        )
                    ]),
                    html.Div([
                        html.Label("Region:", style={'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id='region-filter',
                            options=[{'label': r, 'value': r} for r in regions],
                            placeholder='Select Region(s)',
                            multi=True,
                            style={'width': '300px'}
                        )
                    ]),
                    html.Div([
                        html.Label("Sales Channel:", style={'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id='channel-filter',
                            options=[{'label': ch, 'value': ch} for ch in channels],
                            placeholder='Select Sales Channel(s)',
                            multi=True,
                            style={'width': '300px'}
                        )
                    ]),
                    html.Div([
                        html.Label("Order Priority:", style={'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id='priority-filter',
                            options=[{'label': p, 'value': p} for p in priorities],
                            placeholder='Select Priority(s)',
                            multi=True,
                            style={'width': '300px'}
                        )
                    ]),
                ], style={
                    'display': 'flex',
                    'flex-wrap': 'wrap',
                    'gap': '20px',
                    'margin': '20px 0'
                }),

                # Metric selection radio buttons
                html.Div([
                    html.Label("Select Metric:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
                    dcc.RadioItems(
                        id='metric-selector',
                        options=[{'label': m, 'value': m} for m in metrics],
                        value='Total Revenue',
                        inline=True,
                        style={
                            'display': 'flex',
                            'justify-content': 'space-around',
                            'flex-wrap': 'wrap',
                            'margin-top': '10px',
                        },
                        labelStyle={
                            'display': 'inline-block',
                            'padding': '10px 20px',
                            'margin': '5px',
                            'border': '1px solid #ccc',
                            'border-radius': '5px',
                            'background-color': '#f9f9f9',
                            'cursor': 'pointer',
                            'transition': 'background-color 0.3s',
                        },
                        inputStyle={'margin-right': '10px'}
                    )
                ], style={'margin': '20px 0'}),

                # Line plot to display the selected metric over months
                dcc.Graph(id='line-plot')
            ]
        )
    ]
)

# Define the callback to update the line plot
@app.callback(
    [Output('line-plot', 'figure')] +
    [Output(f'year-{year}', 'style') for year in years],
    Input('metric-selector', 'value'),
    [Input(f'year-{year}', 'n_clicks') for year in years],
    Input('item-type-filter', 'value'),
    Input('country-filter', 'value'),
    Input('region-filter', 'value'),
    Input('channel-filter', 'value'),
    Input('priority-filter', 'value'),
    [State(f'year-{year}', 'style') for year in years]
)
def update_line_plot(selected_metric, *args):
    # Unpack inputs and apply filters
    year_clicks = args[:len(years)]
    selected_filters = args[len(years):len(years) + 5]  # Extract dropdown values for filters
    button_styles = args[-len(years):]

    # Determine selected year based on button clicks
    selected_year = years[year_clicks.index(max(year_clicks))] if any(year_clicks) else None

    # Filter DataFrame based on selections
    filtered_df = df.copy()
    if selected_year:
        filtered_df = filtered_df[filtered_df['year'] == selected_year]
    
    # Apply additional multi-select filters
    filter_columns = ['ItemType', 'Country', 'Regoin', 'SalesChannel', 'OrderPriority']
    for col, filter_vals in zip(filter_columns, selected_filters):
        if filter_vals:
            filtered_df = filtered_df[filtered_df[col].isin(filter_vals)]

    # Group data by month and prepare plot
    monthly_data = (
        filtered_df.groupby('Month Name').sum(numeric_only=True).reindex(month_order).reset_index()
    )

    fig = go.Figure(data=go.Scatter(
        x=monthly_data['Month Name'], y=monthly_data[selected_metric], mode='lines+markers'
    ))

    fig.update_layout(
        title=f"{selected_metric} Over the Year",
        xaxis_title="Month", yaxis_title=selected_metric,
    )

    # Update button styles to show selected year
    new_styles = [
        {**style, 'background-color': 'green' if str(year) == str(selected_year) else '#e0e0e0'}
        for year, style in zip(years, button_styles)
    ]

    return [fig] + new_styles

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
