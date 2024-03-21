# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# import anvil.server
# import pandas as pd
# from pandas.api.types import is_string_dtype, is_numeric_dtype, is_datetime64_any_dtype, is_categorical_dtype

# @anvil.server.callable
# def filter_dataframe(df_json, filters, case):
#     df = pd.read_json(df_json, orient='split')
    

#     for column, filter_info in filters.items():
#         if filter_info['type'] == 'text':
#             if case:
#                 df = df[df[column].str.contains(filter_info['value'], na=False)]
#             else:
#                 df = df[df[column].str.contains(filter_info['value'], case=False, na=False)]
#         elif filter_info['type'] == 'numeric':
#             df = df[(df[column] >= filter_info['min']) & (df[column] <= filter_info['max'])]
#         elif filter_info['type'] == 'datetime':
#             df = df[(df[column] >= pd.to_datetime(filter_info['start_date'])) & 
#                     (df[column] <= pd.to_datetime(filter_info['end_date']))]
#         elif filter_info['type'] == 'categorical':
#             df = df[df[column].isin(filter_info['values'])]

#     return df.to_json(orient='split')


# import anvil.server
# from anvil import *
# import pandas as pd

# class MainForm(Form):
#     def __init__(self, **properties):
#         self.init_components(**properties)
#         self.df_json = self.load_initial_dataframe()

#         # Dictionary to hold filters
#         self.filters = {}

#     def load_initial_dataframe(self):
#         # Load your initial DataFrame and convert it to JSON
#         df = pd.DataFrame() # Replace with your actual DataFrame loading
#         return df.to_json(orient='split')

#     def apply_filters_button_click(self, **event_args):
#         # Call the
#       filtered_df_json = anvil.server.call('filter_dataframe', self.df_json, self.filters, case=True)
#       filtered_df = pd.read_json(filtered_df_json, orient='split')
#       # Update the UI with the filtered DataFrame
#       self.update_data_grid(filtered_df)

#     def update_data_grid(self, df):
#         # Assuming you have a DataGrid component named data_grid
#         # Convert the DataFrame to a list of dictionaries for the DataGrid
#         self.data_grid.items = df.to_dict(orient='records')
    
#     def add_filter(self, column_name, filter_type, **kwargs):
#         # Store filter information in the self.filters dictionary
#         if filter_type == 'text':
#             self.filters[column_name] = {'type': 'text', 'value': kwargs['pattern']}
#         elif filter_type == 'numeric':
#             self.filters[column_name] = {'type': 'numeric', 'min': kwargs['min_value'], 'max': kwargs['max_value']}
#         elif filter_type == 'datetime':
#             self.filters[column_name] = {'type': 'datetime', 'start_date': kwargs['start_date'], 'end_date': kwargs['end_date']}
#         elif filter_type == 'categorical':
#             self.filters[column_name] = {'type': 'categorical', 'values': kwargs['values']}