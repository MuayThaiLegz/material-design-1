from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil import *
import anvil.server
# from io import BytesIO

# class home(homeTemplate):
#     def __init__(self, **properties):
#         self.init_components(**properties)
#         # Initialize UI components including feedback label, connection, dataset, and file controls
#         self.setup_ui()

#     def setup_ui(self):
#         # Setup feedback label for user messages
#         self.feedback_label = Label(text="", font_size=16, bold=True, width='100%', align='center')
#         self.add_component(self.feedback_label, slot="before")

#         # Setup MongoDB connection controls
#         self.setup_connection_controls()

#         # Setup controls for dataset selection
#         self.setup_dataset_controls()

#         # Setup file upload controls
#         self.setup_file_controls()

#     def setup_connection_controls(self):
#         # Text box for MongoDB connection string input
#         self.ip_address_box = TextBox(placeholder='Enter MongoDB connection string here', width='100%')
#         self.add_component(self.ip_address_box)

#         # Connect button
#         self.connect_button = Button(text="Connect", role="primary-color")
#         self.connect_button.set_event_handler('click', self.on_connect_clicked)
#         self.add_component(self.connect_button)

#     def setup_dataset_controls(self):
#         # Instructions label for dataset selection
#         self.dataset_instructions = Label(text="Please select a dataset:", width='100%')
#         self.add_component(self.dataset_instructions)

#         # Panel to hold dynamically created radio buttons for datasets
#         self.dataset_radio_panel = FlowPanel(width='100%')
#         self.add_component(self.dataset_radio_panel)

#     def setup_file_controls(self):
#         # FileLoader for data file upload
#         self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], enabled=True)
#         self.file_loader.set_event_handler('change', self.on_file_loader_changed)
#         self.add_component(self.file_loader)

#         # Button to process the uploaded file
#         self.process_file_button = Button(text="Process File", enabled=False, role="secondary-color")
#         self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
#         self.add_component(self.process_file_button)
class home(homeTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Enhanced Layout Setup
        self.title = Label(text="Data Processing Portal", font_size=24, bold=True, align="center")
        self.nav_bar = FlowPanel(align="center")
        self.nav_bar.add_component(Link(text="Home", align="center"))
        self.nav_bar.add_component(Link(text="Analytics", align="center"))
        self.nav_bar.add_component(Link(text="Settings", align="center"))
        self.content_panel = ColumnPanel()
        
        self.add_component(self.title)
        self.add_component(self.nav_bar)
        self.add_component(self.content_panel)
        
        self.setup_connection_controls()
        self.setup_dataset_controls()
        self.setup_file_controls()
        
        # Feedback Label Setup
        self.feedback_label = Label(text="", font_size=16, bold=True, width='100%', align='center', visible=False)
        self.content_panel.add_component(self.feedback_label, width='100%')
    
    def setup_connection_controls(self):
        self.content_panel.add_component(Label(text="MongoDB Connection String:", italic=True))
        self.ip_address_box = TextBox(placeholder="mongodb://localhost:27017", width="fill")
        self.content_panel.add_component(self.ip_address_box)
        
        self.connect_button = Button(text="Connect", icon="fas fa-plug", role="primary-color", width=120)
        self.connect_button.set_event_handler('click', self.on_connect_clicked)
        self.content_panel.add_component(self.connect_button, width='fill')
    
    def setup_dataset_controls(self):
        self.content_panel.add_component(Label(text="Select a Dataset:", italic=True))
        self.dataset_radio_panel = FlowPanel(width='fill')
        self.content_panel.add_component(self.dataset_radio_panel)
    
    def setup_file_controls(self):
        self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], tooltip="Upload your data file here", width="fill")
        self.file_loader.set_event_handler('change', self.on_file_loader_changed)
        self.content_panel.add_component(self.file_loader)
        
        self.process_file_button = Button(text="Process File", icon="fas fa-cogs", role="secondary-color", enabled=False, width=120)
        self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
        self.content_panel.add_component(self.process_file_button, width='fill')
    
    # Event Handlers and Method Definitions Follow

    def on_connect_clicked(self, **event_args):
        connString = self.ip_address_box.text
        success, db_names_or_error = anvil.server.call('get_database_names', connString)
        if success:
            self.update_dataset_radios(db_names_or_error)
        else:
            self.display_feedback(False, db_names_or_error)

    def update_dataset_radios(self, db_names):
        # Clear existing radio buttons
        self.dataset_radio_panel.clear()
        # Add a radio button for each database name
        for db_name in db_names:
            radio = RadioButton(text=db_name, group_name="datasets")
            radio.set_event_handler('change', self.on_dataset_selected)
            self.dataset_radio_panel.add_component(radio)

    def on_dataset_selected(self, sender, **event_args):
        if sender.selected:
            self.selected_dataset = sender.text
            self.display_feedback(True, f"Selected dataset: {self.selected_dataset}")

    def on_file_loader_changed(self, **event_args):
        # Enable the process file button when a file is selected
        self.process_file_button.enabled = bool(self.file_loader.file)

    def on_process_file_clicked(self, **event_args):
        if self.file_loader.file:
            success, message = anvil.server.call('store_data', self.selected_dataset, self.file_loader.file.name, self.file_loader.file, self.ip_address_box.text)
            self.display_feedback(success, message)

    def display_feedback(self, success, message):
        # Display feedback message to the user
        self.feedback_label.text = message
        self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
      
