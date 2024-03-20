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
        # Initialize components from the design template
        self.init_components(**properties)
        
        # Store the MongoDB connection string for use in other parts of the app
        self.mongoConnect = mongoConnect

        # Initialize UI components and fetch datasets
        self.setup_ui_elements()
        self.fetch_datasets()

    def setup_ui_elements(self):
        """Initializes UI elements including the title, navigation bar, and content panel."""
        # Title setup
        self.title = Label(text="Data Processing Portal", font_size=24, bold=True, align="center")
        
        # Navigation bar setup
        self.nav_bar = FlowPanel(align="center")
        self.add_nav_links()
        
        # Content panel setup
        self.content_panel = ColumnPanel()
        
        # Add UI elements to the form
        self.add_component(self.title)
        self.add_component(self.nav_bar)
        self.add_component(self.content_panel)
        
        # Feedback label setup
        self.setup_feedback_label()

    def add_nav_links(self):
        """Adds navigation links to the navigation bar with event handlers."""
        features = [
            ("Analytics", self.open_analytics),
            ("Anomaly Detection", self.open_anomaly_detection),
            ("Edge Vectors", self.open_edge_vectors),
            ("Multi Sense", self.open_multi_sense)
        ]
        
        for text, event_handler in features:
            link = Link(text=text, align="center")
            link.set_event_handler('click', event_handler)
            self.nav_bar.add_component(link)

    def setup_feedback_label(self):
        """Sets up the feedback label for displaying messages to the user."""
        self.feedback_label = Label(text="", font_size=16, bold=True, width='100%', align='center', visible=False)
        self.content_panel.add_component(self.feedback_label, width='100%')

    def fetch_datasets(self):
        """Fetches dataset names from the server using the MongoDB connection string."""
        success, db_names_or_error = anvil.server.call('get_database_names', self.mongoConnect)
        if success:
            self.update_dataset_radios(db_names_or_error)
        else:
            self.display_feedback(False, db_names_or_error)

    def update_dataset_radios(self, db_names):
        """Updates the dataset selection options based on available datasets."""
        # Example placeholder for dataset selection logic

    def display_feedback(self, success, message):
        """Displays a feedback message to the user."""
        self.feedback_label.text = message
        self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
        self.feedback_label.visible = True

    # Navigation methods
    def open_analytics(self, **event_args):
        self.content_panel.clear()
        self.content_panel.add_component(analytics())

    def open_anomaly_detection(self, **event_args):
        self.content_panel.clear()
        self.content_panel.add_component(anomalydetection())

    def open_edge_vectors(self, **event_args):
        self.content_panel.clear()
        self.content_panel.add_component(edgevectors())

    def open_multi_sense(self, **event_args):
        self.content_panel.clear()
        self.content_panel.add_component(multisense())
      

# class home(homeTemplate):
#     def __init__(self, mongoConnect, **properties):
#         # super().__init__(**properties)
#         self.init_components(**properties)
#         self.mongoConnect = mongoConnect
#         # Setup UI Elements
#         self.setup_ui_elements()

#         # Attempt to automatically fetch datasets after initialization
#         self.fetch_datasets()

#     def setup_ui_elements(self):
#         """Sets up UI components including title, navigation bar, and feedback label."""
#         self.title = Label(text="Data Processing Portal", font_size=24, bold=True, align="center")
#         self.nav_bar = FlowPanel(align="center")
        
#         # Adding links to the navigation bar
#         for feature in ["Analytics", "Anomaly Detection", "Edge Vectors", "Multi Sense"]:
#             self.nav_bar.add_component(Link(text=feature, align="center"))
            
            
#         self.content_panel = ColumnPanel()
#         self.add_component(self.title)
#         self.add_component(self.nav_bar)
#         self.add_component(self.content_panel)

#         # Feedback label for user notifications
#         self.feedback_label = Label(text="", font_size=16, bold=True, width='100%', align='center', visible=True)
#         self.content_panel.add_component(self.feedback_label, width='100%')

#         # Setup for dataset selection and file uploading
#         self.setup_dataset_controls()
#         self.setup_file_controls()

#     def setup_dataset_controls(self):
#         """Sets up UI components for dataset selection."""
#         # label = Label(text="Select a Dataset:", italic=True, background='#023645')
#         self.dataset_radio_panel = FlowPanel(width='fill')
        
#         # self.content_panel.add_component(label)
#         self.content_panel.add_component(self.dataset_radio_panel)

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

#     def fetch_datasets(self):
#         """Fetches dataset names from the server and updates the UI."""
#         success, db_names_or_error = anvil.server.call('get_database_names', self.mongoConnect)
#         if success:
#             self.update_dataset_radios(db_names_or_error)
#         else:
#             self.display_feedback(False, db_names_or_error)

#     def update_dataset_radios(self, db_names):
#         """Updates the dataset selection radio buttons based on available datasets."""
#         self.dataset_radio_panel.clear()
#         for db_name in db_names:
#             radio = RadioButton(text=db_name, group_name="datasets")
#             radio.set_event_handler('change', self.on_dataset_selected)
#             self.dataset_radio_panel.add_component(radio)

#     def on_dataset_selected(self, sender, **event_args):
#         """Handles dataset selection, enabling file processing based on selection."""
#         if sender.selected:
#             self.selected_dataset = sender.text
#             self.display_feedback(True, f"Selected dataset: {self.selected_dataset}")

#     def on_file_loader_changed(self, **event_args):
#         """Enables the process file button when a file is selected."""
#         self.process_file_button.enabled = bool(self.file_loader.file)

#     def on_process_file_clicked(self, **event_args):
#         """Processes the selected file against the selected dataset."""
#         if self.file_loader.file:
#             success, message = anvil.server.call('process_datafile', self.selected_dataset, 
#                                                  self.file_loader.file.name, self.file_loader.file)
#             self.display_feedback(success, message)

#     def display_feedback(self, success, message):
#         """Displays feedback to the user."""
#         self.feedback_label.text = message
#         self.feedback_label.foreground = "#4CAF50" if success else "#F44336"

# class home(homeTemplate):
#     def __init__(self, **properties):
#         self.init_components(**properties)

#         # Enhanced Layout Setup
#         self.title = Label(text="Data Processing Portal", font_size=24, bold=True, align="center")
#         self.nav_bar = FlowPanel(align="center")
#         # self.nav_bar.add_component(Link(text="Verticals", align="center"))
#         self.nav_bar.add_component(Link(text="Analytics", align="center"))
#         self.nav_bar.add_component(Link(text="Anomaly Detection", align="center"))
#         self.nav_bar.add_component(Link(text="Anomaly Detection", align="center"))
#         self.nav_bar.add_component(Link(text="Multi Sense", align="center"))
#         self.content_panel = ColumnPanel()
        
#         self.add_component(self.title)
#         self.add_component(self.nav_bar)
#         self.add_component(self.content_panel)
        
#         self.setup_dataset_controls()
#         self.setup_file_controls()
        
#         # Feedback Label Setup
#         self.feedback_label = Label(text="", font_size=16, bold=True, width='100%', align='center', visible=False)
#         self.content_panel.add_component(self.feedback_label, width='100%')
    
    
#     def setup_dataset_controls(self):
#         self.content_panel.add_component(Label(text="Select a Dataset:", italic=True))
#         self.dataset_radio_panel = FlowPanel(width='fill')
#         self.content_panel.add_component(self.dataset_radio_panel)
    
#     def setup_file_controls(self):
#         self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], tooltip="Upload your data file here", width="fill")
#         self.file_loader.set_event_handler('change', self.on_file_loader_changed)
#         self.content_panel.add_component(self.file_loader)
        
#         self.process_file_button = Button(text="Process File", icon="fa:cogs", role="secondary-color", enabled=False, width=120)
#         self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
#         self.content_panel.add_component(self.process_file_button, width='fill')
    
#     # Event Handlers and Method Definitions Follow

#     def on_connect_clicked(self, **event_args):
#         connString = self.ip_address_box.text
#         success, db_names_or_error = anvil.server.call('get_database_names', connString)
#         if success:
#             self.update_dataset_radios(db_names_or_error)
#         else:
#             self.display_feedback(False, db_names_or_error)

#     def update_dataset_radios(self, db_names):
#         self.dataset_radio_panel.clear()
        
#         for db_name in db_names:
#             radio = RadioButton(text=db_name, group_name="datasets")
#             radio.set_event_handler('change', self.on_dataset_selected)
#             self.dataset_radio_panel.add_component(radio)

#     def on_dataset_selected(self, sender, **event_args):
#         if sender.selected:
#             self.selected_dataset = sender.text
#             self.display_feedback(True, f"Selected dataset: {self.selected_dataset}")

#     def on_file_loader_changed(self, **event_args):
#         # Enable the process file button when a file is selected
#         self.process_file_button.enabled = bool(self.file_loader.file)

#     def on_process_file_clicked(self, **event_args):
#       if self.file_loader.file:
#         success, message = anvil.server.call('store_data', self.selected_dataset, self.file_loader.file.name, self.file_loader.file, self.ip_address_box.text)
#         alert(message)
#         self.display_feedback(success, message)

#     def setup_data_grid(self):
#         self.data_selection = TextBox(placeholder="mongodb://localhost:27017", width="fill")
#         self.content_panel.add_component(self.data_selection)
        
        
#         self.data_grid = DataGrid()
#         self.data_grid.show_header = True
#         self.data_grid.columns = [
#             # Define columns based on your DataFrame structure
#             # Example:
#             DataGridColumn(title='Name', data_key='Name', width=200),
#             DataGridColumn(title='Age', data_key='Age', width=100),
#             DataGridColumn(title='City', data_key='City', width=200),
#         ]
        
#     def display_feedback(self, success, message):
#       # Display feedback message to the user
#       self.feedback_label.text = message
#       self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
      
