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

class home(homeTemplate):
    def __init__(self, mongoConnect, **properties):
        self.init_components(**properties)
        self.mongoConnect = mongoConnect
        # Define the data_grid_placeholder here to be used later
        self.content_panel = ColumnPanel()
        self.data_grid_placeholder = FlowPanel()
        self.content_panel.add_component(self.data_grid_placeholder)
        self.setup_ui_elements()
        self.fetch_datasets()

    def setup_ui_elements(self):
        self.add_nav_links()
        self.setup_feedback_label()
        self.setup_dataset_controls()
        self.setup_collection_dropdown()
        self.setup_file_controls()

    def add_nav_links(self):
        features = [
            ("Analytics", analytics),
            ("Anomaly Detection", anomalydetection),
            ("Edge Vectors", edgevectors),
            ("Multi Sense", multisense)
        ]
        for text, form in features:
            link = Link(text=text, align="center")
            link.tag = form
            link.set_event_handler('click', lambda **e: self.open_feature_form(e['sender'].tag))

    def setup_feedback_label(self):
        self.feedback_label = Label(text="", font_size=16, bold=True, width='100%', align='center', visible=False)
        self.content_panel.add_component(self.feedback_label, width='100%')

    def setup_dataset_controls(self):
        self.dataset_radio_panel = FlowPanel(width='fill')
        self.content_panel.add_component(self.dataset_radio_panel)

    def setup_collection_dropdown(self):
        self.collection_dropdown = DropDown()
        self.content_panel.add_component(self.collection_dropdown)
        self.collection_dropdown.set_event_handler('change', self.on_collection_selected)
    def on_file_loader_changed(self, **event_args):
      """Enables the process file button when a file is selected."""
      self.process_file_button.enabled = bool(self.file_loader.file)
      
    def setup_file_controls(self):
        self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], 
                                      tooltip="Upload your data file here", width="fill")
        self.file_loader.set_event_handler('change', self.on_file_loader_changed)
        self.content_panel.add_component(self.file_loader)
        
        self.process_file_button = Button(text="Process File", icon="fa:cogs", role="secondary-color", 
                                          enabled=False, width=120)
        self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
        self.content_panel.add_component(self.process_file_button, width='fill')

    def on_process_file_clicked(self, **event_args):
        """Processes the selected file against the selected dataset."""
        if self.file_loader.file:
            collection_name = self.file_loader.file.name
            success, message = anvil.server.call('store_data', self.selected_dataset, 
                                                 self.file_loader.file.name, self.file_loader.file, self.mongoConnect)
            self.display_feedback(success, message)

    def fetch_datasets(self):
        success, db_names_or_error = anvil.server.call('get_database_names', self.mongoConnect)
        if success:
            self.update_dataset_radios(db_names_or_error)
        else:
            self.display_feedback(False, db_names_or_error)

    def update_dataset_radios(self, db_names):
        self.dataset_radio_panel.clear()
        for db_name in db_names:
            radio = RadioButton(text=db_name, group_name="datasets")
            radio.set_event_handler('change', lambda sender, **e: self.on_dataset_selected(sender.text))
            self.dataset_radio_panel.add_component(radio)

    def on_dataset_selected(self, dataset_name):
        self.selected_dataset = dataset_name
        collections = anvil.server.call('list_collections', self.mongoConnect, self.selected_dataset)
        self.collection_dropdown.items = [(name, name) for name in collections]
        self.display_feedback(True, f"Dataset selected: {self.selected_dataset}")

    def on_collection_selected(self, sender, **event_args):
        collection_name = sender.selected_value
        data, columns = anvil.server.call('fetch_collection_data', self.mongoConnect, self.selected_dataset, collection_name)
        if data:
            self.create_and_populate_data_grid(data, columns)
        else:
            self.display_feedback(False, "No data found for the selected collection.")

    def create_and_populate_data_grid(self, data, columns):
        data_grid = DataGrid(show_header=True, columns=[DataGridColumn(title=col, data_key=col) for col in columns])
        data_grid.items = data
        self.data_grid_placeholder.clear()
        self.data_grid_placeholder.add_component(data_grid)

    def open_feature_form(self, form_class):
        self.content_panel.clear()
        self.content_panel.add_component(form_class())
      
# class home(homeTemplate):
#     def __init__(self, mongoConnect, **properties):
#         self.init_components(**properties)
#         self.mongoConnect = mongoConnect
#         self.content_panel = ColumnPanel()
#         self.setup_ui_elements()
#         self.fetch_datasets()

#     def setup_ui_elements(self):
#         # self.title.text = "Cognitive Portal"
#         self.add_nav_links()
#         self.setup_feedback_label()
#         self.setup_dataset_controls()
#         self.setup_collection_dropdown()  # Ensure this method is called
#         self.setup_file_controls()

#     def add_nav_links(self):
#         features = [
#             ("Analytics", analytics),
#             ("Anomaly Detection", anomalydetection),
#             ("Edge Vectors", edgevectors),
#             ("Multi Sense", multisense)
#         ]
#         for text, form in features:
#             link = Link(text=text, align="center")
#             link.tag = form
#             link.set_event_handler('click', lambda **e: self.open_feature_form(e['sender'].tag))

  
#     def setup_feedback_label(self):
#         """Sets up the feedback label for displaying messages to the user."""
#         self.feedback_label = Label(text="", font_size=16, bold=True, width='100%', align='center', visible=False)
#         self.content_panel.add_component(self.feedback_label, width='100%')

#     def setup_dataset_controls(self):
#         """Sets up UI components for dataset selection."""
#         self.dataset_radio_panel = FlowPanel(width='fill')  
#         self.content_panel.add_component(self.dataset_radio_panel)

#     def setup_collection_dropdown(self):
#       # Assume this dropdown is added via Anvil Editor or dynamically in code
#       self.collection_dropdown = DropDown()
#       self.content_panel.add_component(self.collection_dropdown)
#       self.collection_dropdown.set_event_handler('change', self.on_collection_selected)

#     def on_file_loader_changed(self, **event_args):
#       """Enables the process file button when a file is selected."""
#       self.process_file_button.enabled = bool(self.file_loader.file)

#     def setup_file_controls(self):
#       """Sets up UI components for file uploading and processing."""
#       self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], 
#                                     tooltip="Upload your data file here", width="fill")
#       self.file_loader.set_event_handler('change', self.on_file_loader_changed)
#       self.content_panel.add_component(self.file_loader)
      
#       self.process_file_button = Button(text="Process File", icon="fa:cogs", role="secondary-color", 
#                                         enabled=False, width=120)
#       self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
#       self.content_panel.add_component(self.process_file_button, width='fill')

#     def on_process_file_clicked(self, **event_args):
#         """Processes the selected file against the selected dataset."""
#         if self.file_loader.file:
#             collection_name = self.file_loader.file.name
#             success, message = anvil.server.call('store_data', self.selected_dataset, 
#                                                  self.file_loader.file.name, self.file_loader.file, self.mongoConnect)
#             self.display_feedback(success, message)


#     def fetch_datasets(self):
#         success, db_names_or_error = anvil.server.call('get_database_names', self.mongoConnect)
#         if success:
#             self.update_dataset_radios(db_names_or_error)
#         else:
#             self.display_feedback(False, db_names_or_error)

#     def update_dataset_radios(self, db_names):
#         self.dataset_radio_panel.clear()
#         for db_name in db_names:
#             radio = RadioButton(text=db_name, group_name="datasets")
#             radio.set_event_handler('change', lambda sender, **e: self.on_dataset_selected(sender.text))
#             self.dataset_radio_panel.add_component(radio)

#     def on_dataset_selected(self, dataset_name):
#         self.selected_dataset = dataset_name
#         # Trigger collection dropdown update based on the selected dataset
#         collections = anvil.server.call('list_collections', self.mongoConnect, self.selected_dataset)
#         self.collection_dropdown.items = [(name, name) for name in collections]
#         self.display_feedback(True, f"Dataset selected: {self.selected_dataset}")

#     def on_collection_selected(self, sender, **event_args):
#         collection_name = sender.selected_value
#         data, columns = anvil.server.call('fetch_collection_data', self.mongoConnect, self.selected_dataset, collection_name)
#         if data:
#             self.create_and_populate_data_grid(data, columns)
#         else:
#             self.display_feedback(False, "No data found for the selected collection.")

#     def create_and_populate_data_grid(self, data, columns):
#         data_grid = DataGrid(show_header=True, columns=[DataGridColumn(title=col, data_key=col) for col in columns])
#         data_grid.items = data
#         self.data_grid_placeholder.clear()
#         self.data_grid_placeholder.add_component(data_grid)

#     def open_feature_form(self, form_class):
#         self.content_panel.clear()
#         self.content_panel.add_component(form_class())

#     def display_feedback(self, success, message):
#         self.feedback_label.text = message
#         self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
#         self.feedback_label.visible = True


# class home(homeTemplate):
#     def __init__(self, mongoConnect, **properties):
#         self.init_components(**properties)
#         self.mongoConnect = mongoConnect
      
#         # Initialize UI components and fetch datasets
#         self.setup_ui_elements()
#         self.fetch_datasets()

#     def setup_ui_elements(self):
#         """Initializes UI elements including the title, navigation bar, and content panel."""
#         # Title setup
#         self.title = Label(text="Cognitivie Portal", font_size=24, bold=True, align="center")
        
#         # Navigation bar setup
#         self.nav_bar = FlowPanel(align="center")
#         self.add_nav_links()
        
#         # Content panel setup
#         self.data_grid_placeholder = FlowPanel()
#         self.content_panel = ColumnPanel()
      
#         self.content_panel.add_component(self.data_grid_placeholder)
#         # Add UI elements to the form
#         self.add_component(self.title)
#         self.add_component(self.nav_bar)
#         self.add_component(self.content_panel)
        
#         # Feedback label setup
#         self.setup_feedback_label()
#         self.setup_dataset_controls()
#         self.setup_file_controls()

#     def add_nav_links(self):
#         """Adds navigation links to the navigation bar with event handlers."""
#         features = [
#             ("Analytics", self.open_analytics),
#             ("Anomaly Detection", self.open_anomaly_detection),
#             ("Edge Vectors", self.open_edge_vectors),
#             ("Multi Sense", self.open_multi_sense)
#         ]
        
#         for text, event_handler in features:
#             link = Link(text=text, align="center")
#             link.set_event_handler('click', event_handler)
#             self.nav_bar.add_component(link)

#     def setup_feedback_label(self):
#         """Sets up the feedback label for displaying messages to the user."""
#         self.feedback_label = Label(text="", font_size=16, bold=True, width='100%', align='center', visible=False)
#         self.content_panel.add_component(self.feedback_label, width='100%')
      
#     def setup_collection_dropdown(self):
#       # Assume this dropdown is added via Anvil Editor or dynamically in code
#       self.collection_dropdown = DropDown()
#       self.content_panel.add_component(self.collection_dropdown)
#       self.collection_dropdown.set_event_handler('change', self.on_collection_selected)

#     def on_dataset_selected(self, sender, **event_args):
#       if sender.selected:
#           self.selected_dataset = sender.text
#           # Populate the collection_dropdown with collection names from the selected dataset
#           # This requires an additional server call or logic to list collections
#           collections = anvil.server.call('list_collections', self.mongoConnect, self.selected_dataset)
#           self.collection_dropdown.items = [(name, name) for name in collections]

  
#     def on_collection_selected(self, sender, **event_args):
#       collection_name = sender.selected_value
#       # Now fetch and display data for the selected collection
#       data, columns = anvil.server.call('fetch_collection_data', self.mongoConnect, self.selected_dataset, collection_name)
#       # Assuming create_and_populate_data_grid exists to dynamically create the DataGrid
#       if data:
#           self.create_and_populate_data_grid(data, columns)
#       else:
#           self.display_feedback(False, "No data found for the selected collection.")
        
#     def setup_file_controls(self):
#         """Sets up UI components for file uploading and processing."""
#         self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], 
#                                       tooltip="Upload your data file here", width="fill")
#         self.file_loader.set_event_handler('change', self.on_file_loader_changed)
#         self.content_panel.add_component(self.file_loader)
        
#         self.process_file_button = Button(text="Process File", icon="fa:cogs", role="secondary-color", 
#                                           enabled=False, width=120)
#         self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
#         self.content_panel.add_component(self.process_file_button, width='fill')

#     def on_file_loader_changed(self, **event_args):
#         """Enables the process file button when a file is selected."""
#         self.process_file_button.enabled = bool(self.file_loader.file)

#     def on_process_file_clicked(self, **event_args):
#         """Processes the selected file against the selected dataset."""
#         if self.file_loader.file:
#             collection_name = self.file_loader.file.name
#             success, message = anvil.server.call('store_data', self.selected_dataset, 
#                                                  self.file_loader.file.name, self.file_loader.file, self.mongoConnect)
#             self.display_feedback(success, message)

#     def fetch_datasets(self):
#         """Fetches dataset names from the server using the MongoDB connection string."""
#         success, db_names_or_error = anvil.server.call('get_database_names', self.mongoConnect)
      
#         if success:
#             self.update_dataset_radios(db_names_or_error)
#         else:
#             self.display_feedback(False, db_names_or_error)

#     def setup_dataset_controls(self):
#         """Sets up UI components for dataset selection."""
#         # label = Label(text="Select a Dataset:", italic=True, background='#023645')
#         self.dataset_radio_panel = FlowPanel(width='fill')
        
#         # self.content_panel.add_component(label)
#         self.content_panel.add_component(self.dataset_radio_panel)

#     def update_dataset_radios(self, db_names):
#         """Updates the dataset selection radio buttons based on available datasets."""
#         self.dataset_radio_panel.clear()
#         for db_name in db_names:
#             radio = RadioButton(text=db_name, group_name="datasets")
#             radio.set_event_handler('change', self.on_dataset_selected)
#             self.dataset_radio_panel.add_component(radio)
          
#     def create_data_grid(self, columns):
#       # Create a new DataGrid instance
#       data_grid = DataGrid()
#       data_grid.show_header = True
      
#       # Dynamically add columns based on the column names
#       for col_name in columns:
#           data_grid.columns.append(
#               DataGridColumn(title=col_name, data_key=col_name, width=200))
        
#       return data_grid
  
#     def on_dataset_selected(self, sender, **event_args):
#         """Handles dataset selection, enabling file processing based on selection."""
#         if sender.selected:
#             self.selected_dataset = sender.text
#             data, columns = anvil.server.call('fetch_collection_data', self.mongoConnect, self.selected_dataset, collection_name)
#             if data:
#               self.data_grid_placeholder.clear()
#               # self.data_grid = self.create_data_grid(columns)
#               self.create_and_populate_data_grid(data, columns)

#               # self.data_grid.items = data
#               # self.data_grid_placeholder.add_component(self.data_grid)
#               self.display_feedback(True, "Data loaded successfully.")
#             else:
#               self.display_feedback(False, "No data found for the selected dataset.")

#     def create_and_populate_data_grid(self, data, columns):
#         # Dynamically create DataGrid with columns
#         data_grid = DataGrid(show_header=True, columns=[
#             DataGridColumn(title=col, data_key=col) for col in columns])
#         # Set items for the DataGrid
      
#         data_grid.items = data  
#         # Add the new DataGrid to the placeholder
#         self.data_grid_placeholder.add_component(data_grid)
      
#     def display_feedback(self, success, message):
#         """Displays a feedback message to the user."""
#         self.feedback_label.text = message
#         self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
#         self.feedback_label.visible = True

#     # Navigation methods
#     def open_analytics(self, **event_args):
#         # self.content_panel.clear()
#         self.content_panel.add_component(analytics())

#     def open_anomaly_detection(self, **event_args):
#         # self.content_panel.clear()
#         self.content_panel.add_component(anomalydetection())

#     def open_edge_vectors(self, **event_args):
#         # self.content_panel.clear()
#         self.content_panel.add_component(edgevectors())

#     def open_multi_sense(self, **event_args):
#         # self.content_panel.clear()
#         self.content_panel.add_component(multisense())
      

