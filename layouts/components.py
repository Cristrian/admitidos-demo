from dash import dcc, html
import dash_bootstrap_components as dbc

def generate_dropdown(id: str, title: str, dropdown_data: dict, 
                            default_label = 'All', default_value = None):
    """Generates a dropdown component.
    
    Retrieves a dropdown element from dash_core_components,
    including it's labels and values
    
    Args:
        id: The component identifier.
        title: The dropdown title.
        dropdown_data: A dictionarie with the dropdown data.
            The keys are the dropdown labels and the values are 
            the dropdown values.
        default_label: The label that is going to be displayed by default.
        default_value: The dropdown default value.
        
    Returns: 
        A dropdown component ready to be used and connected to some graphs"""

    dropdown_options = [{'label': i, 'value': dropdown_data[i]}
                        for i in dropdown_data
                       ]
    dropdown = dcc.Dropdown(
        id=id,
        options=dropdown_options,
        placeholder=default_label,
        value=default_value
    )
    return dropdown

def generate_card(id, color, card_title, card_text):
    
    card = html.Div([
        dbc.CardBody([
            html.H5(card_title, className="card-title"),
            html.P(card_text ,className="card-text")]
        ),
        ],
        className="card text-center"
    )

    return card
    
