from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.server

from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server

from ..analytics import analytics
from ..anomalydetection import anomalydetection
from ..edgevectors import edgevectors
from ..multisense import multisense

from anvil import *
import anvil.server

from ._anvil_designer import homeTemplate

from anvil import *
import anvil.server

class home():
    def __init__(self, mongoConnect):
        self.mongoConnect = mongoConnect
        
        # Main panel setup
        self.content_panel = ColumnPanel()
        
        # Feedback label setup
        self.feedback_label = Label(text="", font_size=16, bold=True, align='center', visible=False)
        self.content_panel.add_component(self.feedback_label)

        # Dataset and collection dropdown setup
        self.setup_dataset_and_collection_dropdowns()

        # Data grid placeholder setup
        self.data_grid_placeholder = FlowPanel()
        self.content_panel.add_component(self.data_grid_placeholder)

        # Fetch datasets from server
        self.fetch_datasets()

    def setup_dataset_and_collection_dropdowns(self):
        self.dataset_dropdown = DropDown()
        self.dataset_dropdown.set_event_handler('change', self.on_dataset_selected)
        self.content_panel.add_component(self.dataset_dropdown)

        self.collection_dropdown = DropDown(visible=False)
        self.collection_dropdown.set_event_handler('change', self.on_collection_selected)
        self.content_panel.add_component(self.collection_dropdown)

    def fetch_datasets(self):
        success, datasets = anvil.server.call('get_database_names', self.mongoConnect)
        if success:
            self.dataset_dropdown.items = [(dataset, dataset) for dataset in datasets]
            self.dataset_dropdown.visible = True
        else:
            self.display_feedback(False, "Failed to fetch datasets.")

    def on_dataset_selected(self, sender, **event_args):
        selected_dataset = sender.selected_value
        self.collection_dropdown.visible = True
        collections = anvil.server.call('list_collections', self.mongoConnect, selected_dataset)
        self.collection_dropdown.items = [(c, c) for c in collections]
        self.display_feedback(True, f"Dataset '{selected_dataset}' selected. Now select a collection.")

    def on_collection_selected(self, sender, **event_args):
        collection_name = sender.selected_value
        data, columns = anvil.server.call('fetch_collection_data', self.mongoConnect, self.dataset_dropdown.selected_value, collection_name)
        if data:
            self.display_data_in_grid(data[:10], columns)  # Only display the first 10 records
        else:
            self.display_feedback(False, f"No data found for the collection '{collection_name}'.")

    def display_data_in_grid(self, data, columns):
        self.data_grid_placeholder.clear()
        # Create headers
        header = FlowPanel()
        for col in columns:
            header.add_component(Label(text=col, bold=True))
        self.data_grid_placeholder.add_component(header)

        # Add data rows
        for row in data:
            row_panel = FlowPanel()
            for col in columns:
                row_panel.add_component(Label(text=str(row[col]), width=200))
            self.data_grid_placeholder.add_component(row_panel)

    def display_feedback(self, success, message):
        self.feedback_label.text = message
        self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
        self.feedback_label.visible = True

# class home(homeTemplate):
#     def __init__(self, mongoConnect, **properties):
#         self.init_components(**properties)
#         self.mongoConnect = mongoConnect

#         # Initialize components for the form
#         self.nav_links = self.setup_nav_links()
#         self.title = self.setup_title()
#         self.content_panel = self.setup_content_panel()
#         self.dataset_dropdown = self.setup_dataset_dropdown()
#         self.file_loader, self.process_file_button = self.setup_file_controls()
#         self.feedback_label = self.setup_feedback_label()
#         self.data_grid_placeholder = self.setup_data_grid_placeholder()
        
#         # Fetch initial data
#         self.fetch_datasets()

#     def setup_nav_links(self):
#         # Links for navigation
#         nav_links = {'Analytics': analytics, 'Anomaly Detection': anomalydetection,
#                      'Edge Vectors': edgevectors, 'Multi Sense': multisense}
#         for name, form in nav_links.items():
#             link = Link(text=name, align="center")
#             link.set_event_handler('click', lambda sender, form=form: self.open_feature_form(form))
#             self.add_component(link)
#         return nav_links

#     def setup_title(self):
#         # Title for the application
#         return Label(text="Cognitive Data Portal", font_size=24, bold=True, align="center")

#     def setup_content_panel(self):
#         # Main content area
#         content_panel = ColumnPanel()
#         self.add_component(content_panel)
#         return content_panel

#     def setup_dataset_dropdown(self):
#         # Dropdown for selecting datasets
#         dataset_dropdown = DropDown()
#         dataset_dropdown.set_event_handler('change', self.on_dataset_selected)
#         self.content_panel.add_component(dataset_dropdown, width='fill')
#         return dataset_dropdown

#     def setup_file_controls(self):
#         # Controls for file uploading and processing
#         file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], 
#                                  tooltip="Upload your data file here", width="fill")
#         file_loader.set_event_handler('change', self.on_file_loader_changed)
#         self.content_panel.add_component(file_loader)
        
#         process_file_button = Button(text="Process File", icon="fa:cogs", enabled=False, width=120)
#         process_file_button.set_event_handler('click', self.on_process_file_clicked)
#         self.content_panel.add_component(process_file_button, width='fill')
        
#         return file_loader, process_file_button

#     def setup_feedback_label(self):
#         # Label for user feedback
#         feedback_label = Label(text="", font_size=16, bold=True, align='center', visible=False)
#         self.content_panel.add_component(feedback_label, width='fill')
#         return feedback_label

#     def setup_data_grid_placeholder(self):
#         # Placeholder for the data grid
#         data_grid_placeholder = FlowPanel()
#         self.content_panel.add_component(data_grid_placeholder)
#         return data_grid_placeholder

#     def on_dataset_selected(self, sender, **event_args):
#         # Logic to handle dataset selection
#         selected_dataset = sender.selected_value
#         self.display_feedback(True, f"Dataset '{selected_dataset}' selected. Now upload a file.")

#     def on_file_loader_changed(self, **event_args):
#         # Enable the process file button when a file is selected
#         self.process_file_button.enabled = bool(self.file_loader.file)

#     def on_process_file_clicked(self, **event_args):
#         # Process the selected file
#         if self.file_loader.file:
#             success, message = anvil.server.call('process_file', self.file_loader.file, 
#                                                  self.dataset_dropdown.selected_value)
#             self.display_feedback(success, message)
#             if success:
#                 data, columns = anvil.server.call('get_processed_data', 
#                                                   self.dataset_dropdown.selected_value)
#                 if data:
#                     self.display_data(data, columns)
#                 else:
#                     self.display_feedback(False, "No data to display.")
                  
#     # def on_process_file_clicked(self, **event_args):
#     #     # Logic to handle file processing
#     #     if self.file_loader.file:
#     #         self.display_feedback(True, "Processing file...")
#             # ... existing logic for file processing ...

#     def fetch_datasets(self):
#         # Logic to fetch dataset names from the server
#         success, datasets = anvil.server.call('get_database_names', self.mongoConnect)
#         if success:
#             self.dataset_dropdown.items = [(dataset, dataset) for dataset in datasets]
#         else:
#             self.display_feedback(False, "Failed to fetch datasets.")

#     def display_feedback(self, success, message):
#         # Display a feedback message to the user
#         self.feedback_label.text = message
#         self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
#         self.feedback_label.visible = True

#     def open_feature_form(self, form_class):
#         # Logic to open different feature forms
#         self.content_panel.clear()
#         self.content_panel.add_component(form_class())



# class home(homeTemplate):
#     def __init__(self, mongoConnect, **properties):
#         self.init_components(**properties)
#         self.mongoConnect = mongoConnect
        
#         self.setup_nav_bar()
#         self.setup_content_panel()
#         self.fetch_and_display_datasets()

#     def setup_nav_bar(self):
#         # Define links for the navigation bar
#         self.nav_links = {
#             'Home':home,
#             'Analytics': analytics,
#             'Anomaly Detection': anomalydetection,
#             'Edge Vectors': edgevectors,
#             'Multi Sense': multisense
#         }
#         # Create and add the navigation bar links
#         for text, form in self.nav_links.items():
#             link = Link(text=text, align="center")
#             link.set_event_handler('click', lambda **e, form=form: self.open_feature_form(form))
#             self.add_component(link, slot="nav-bar") # Add the link to the nav-bar slot

#     def setup_content_panel(self):
#         # Initialize components for dataset selection and file processing
#         self.dataset_dropdown = DropDown()
#         self.file_loader = FileLoader(multiple=False, 
#                                       file_types=[".csv", ".xlsx", ".json", ".parquet"], 
#                                       tooltip="Upload your data file here", 
#                                       visible=False, width="fill")
#         self.process_file_button = Button(text="Process File", icon="fa:cogs", 
#                                           enabled=False, visible=False, width=120)
        
#         # Setup event handlers
#         self.dataset_dropdown.set_event_handler('change', self.on_dataset_selected)
#         self.file_loader.set_event_handler('change', self.on_file_loader_changed)
#         self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
        
#         # Add components to the content panel
#         self.add_component(self.dataset_dropdown)
#         self.add_component(self.file_loader)
#         self.add_component(self.process_file_button)

#     def fetch_and_display_datasets(self):
#         # Fetch dataset names from the server and populate the dropdown
#         success, datasets = anvil.server.call('get_database_names', self.mongoConnect)
#         if success:
#             self.dataset_dropdown.items = [(dataset, dataset) for dataset in datasets]
#         else:
#             self.display_feedback(False, "Failed to fetch datasets.")
    
#     def on_dataset_selected(self, sender, **event_args):
#         # Update UI based on selected dataset
#         selected_dataset = sender.selected_value
#         self.file_loader.visible = True
#         self.process_file_button.visible = False
#         self.display_feedback(True, f"Dataset '{selected_dataset}' selected. You can now upload a file.")
        
#     def on_file_loader_changed(self, **event_args):
#         # Enable the process button when a file is selected
#         self.process_file_button.enabled = bool(self.file_loader.file)
#         self.process_file_button.visible = True

#     def on_process_file_clicked(self, **event_args):
#         # Process the selected file
#         if self.file_loader.file:
#             success, message = anvil.server.call('process_file', self.file_loader.file, 
#                                                  self.dataset_dropdown.selected_value)
#             self.display_feedback(success, message)
#             if success:
#                 data, columns = anvil.server.call('get_processed_data', 
#                                                   self.dataset_dropdown.selected_value)
#                 if data:
#                     self.display_data(data, columns)
#                 else:
#                     self.display_feedback(False, "No data to display.")

#     def display_data(self, data, columns):
#         # Function to display data in a grid-like format
#         self.content_panel.clear()  # Clear the content panel for new data
#         header = FlowPanel()
#         for col in columns:
#             header.add_component(Label(text=col, bold=True))
#         self.content_panel.add_component(header)
        
#         for row in data:
#             row_panel = FlowPanel()
#             for col in columns:
#                 row_panel.add_component(Label(text=str(row[col])))
#             self.content_panel.add_component(row_panel)

#     def display_feedback(self, success, message):
#         # Function to display feedback to the user
#         self.feedback_label.text = message
#         self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
#         self.feedback_label.visible = True

#     def open_feature_form(self, form):
#         # Function to open different forms within the app
#         self.content_panel.clear()
#         self.content_panel.add_component(form())
      
# class home(homeTemplate):
#     def __init__(self, mongoConnect, **properties):
#         self.init_components(**properties)
#         self.mongoConnect = mongoConnect
#         # Setup UI and fetch initial data
#         self.setup_ui()
#         self.fetch_datasets()

#     def setup_ui(self):
#         self.content_panel = ColumnPanel()
#         self.data_grid_placeholder = FlowPanel()
#         self.add_component(self.content_panel)
#         self.content_panel.add_component(self.data_grid_placeholder)
        
#         self.setup_feedback_label()
#         self.setup_nav_links()
#         self.setup_dataset_controls()
#         self.setup_collection_dropdown()
#         self.setup_file_controls()

#     def setup_feedback_label(self):
#         self.feedback_label = Label(text="", font_size=16, bold=True, align='center', visible=False)
#         self.content_panel.add_component(self.feedback_label)

#     def setup_nav_links(self):
#         self.nav_links = {'Analytics': analytics, 'Anomaly Detection': anomalydetection,
#                           'Edge Vectors': edgevectors, 'Multi Sense': multisense}
#         for name, form in self.nav_links.items():
#             link = Link(text=name, align="center")
#             link.set_event_handler('click', lambda sender, **e: self.open_feature_form(form))
#             self.add_component(link)

#     def setup_dataset_controls(self):
#         self.dataset_radio_panel = FlowPanel(width='fill')
#         self.content_panel.add_component(self.dataset_radio_panel)

#     def setup_collection_dropdown(self):
#         self.collection_dropdown = DropDown(visible=False)  # Initially hidden
#         self.collection_dropdown.set_event_handler('change', self.on_collection_selected)
#         self.content_panel.add_component(self.collection_dropdown)

#     def setup_file_controls(self):
#         self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], tooltip="Upload data file", width="fill")
#         self.file_loader.set_event_handler('change', self.on_file_loader_changed)
#         self.content_panel.add_component(self.file_loader)
        
#         self.process_file_button = Button(text="Process File", icon="fa:cogs", enabled=False, width=120)
#         self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
#         self.content_panel.add_component(self.process_file_button)

#     def on_file_loader_changed(self, **event_args):
#         self.process_file_button.enabled = bool(self.file_loader.file)

#     def on_process_file_clicked(self, **event_args):
#         if self.file_loader.file:
#             # Example logic for handling file processing
#             self.display_feedback(True, "File processed successfully.")

#     def fetch_datasets(self):
#         success, datasets = anvil.server.call('get_database_names', self.mongoConnect)
#         if success:
#             self.update_dataset_radios(datasets)
#         else:
#             self.display_feedback(False, "Failed to fetch datasets.")

#     def update_dataset_radios(self, datasets):
#         for dataset in datasets:
#             radio = RadioButton(text=dataset, group_name="datasets")
#             radio.set_event_handler('change', self.on_dataset_selected)
#             self.dataset_radio_panel.add_component(radio)

#     def on_dataset_selected(self, sender, **event_args):
#         if sender.selected:
#             self.selected_dataset = sender.text
#             collections = anvil.server.call('list_collections', self.mongoConnect, self.selected_dataset)
#             self.collection_dropdown.items = [(c, c) for c in collections]
#             self.collection_dropdown.visible = True

  
#     def on_collection_selected(self, sender, **event_args):
#       collection_name = sender.selected_value
#       data, columns = anvil.server.call('fetch_collection_data', self.mongoConnect, self.selected_dataset, collection_name)
#       if data:
#           self.populate_data_simulated_grid(data[:10], columns)
#       else:
#           self.display_feedback(False, "No data found for the selected collection.")

#     def populate_data_simulated_grid(self, data, columns):
      
#         self.data_grid_placeholder.clear()  # Clear previous content
#         for row_data in data:
#             row_panel = FlowPanel()  # This will represent a row
#             for column_name in columns:
#                 cell_label = Label(text=str(row_data[column_name]), width=200)  # Create a label for each cell
#                 row_panel.add_component(cell_label)
#             self.data_grid_placeholder.add_component(row_panel)  # Add the row to the placeholder

  
#     def create_and_populate_data_grid(self, data, columns):
#       self.data_grid_placeholder.clear()
#       data_grid = DataGrid(auto_header=True)
#       data_grid.columns = [DataGridColumn(title=col, data_key=col) for col in columns]  # Corrected typo here from data_gird to data_grid and fixed parenthesis
#       data_grid.items = data
#       self.data_grid_placeholder.add_component(data_grid)

#     def open_feature_form(self, form):
#         self.content_panel.clear()
#         self.content_panel.add_component(form())

#     def display_feedback(self, success, message):
#         self.feedback_label.text = message
#         self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
#         self.feedback_label.visible = True



    