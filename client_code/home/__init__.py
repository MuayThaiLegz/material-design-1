from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.server

# class home(homeTemplate):
#     def __init__(self, **properties):
#         self.init_components(**properties)
        
#         # Initialize UI components
#         self.setup_ui()

#     def setup_ui(self):
#         # Connection Controls
#         self.ip_address_box = TextBox(placeholder='Enter MongoDB connection string here', width='100%')
#         self.add_component(self.ip_address_box)
        
#         self.connect_button = Button(text="Connect", role="primary-color")
#         self.connect_button.set_event_handler('click', self.on_connect_clicked)
#         self.add_component(self.connect_button)

#         # Dataset Controls
#         self.dataset_instructions = Label(text="Please select a dataset:", width='100%')
#         self.add_component(self.dataset_instructions)
        
#         self.dataset_radio_panel = FlowPanel(width='100%')
#         self.add_component(self.dataset_radio_panel)

#         # Collection Controls
#         self.collection_instructions = Label(text="Select a collection:", width='100%', visible=False)
#         self.add_component(self.collection_instructions)

#         self.collection_dropdown = DropDown(width='100%', visible=False)
#         self.add_component(self.collection_dropdown)
#         self.collection_dropdown.set_event_handler('change', self.on_collection_selected)

#         # Data Display Controls
#         self.setup_data_display_controls()

#     def on_connect_clicked(self, **event_args):
#         conn_string = self.ip_address_box.text
#         success, db_names_or_error = anvil.server.call('get_verticals', conn_string)
#         self.verticals = db_names_or_error
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
#             self.fetch_and_display_collections(self.selected_dataset)

#     def fetch_and_display_collections(self, dataset_name):
#         collections = anvil.server.call('get_collection_names', dataset_name, self.vertical)
#         self.collection_dropdown.items = [(c, c) for c in collections]
#         self.collection_instructions.visible = True
#         self.collection_dropdown.visible = True

#     def on_collection_selected(self, sender, **event_args):
#         selected_collection = sender.selected_value
#         if selected_collection:
#             data = anvil.server.call('fetch_collection_data', self.selected_dataset, selected_collection)
#             if data:
#                 self.display_data_table(data)

#     def setup_data_display_controls(self):
#         self.data_display_container = FlowPanel(width='100%', spacing=5, visible=False)
#         self.add_component(self.data_display_container)

#     def display_data_table(self, data):
#         self.data_display_container.clear_components()
#         self.data_display_container.visible = True

#         if not data:
#             self.display_feedback(False, "No data to display.")
#             return
        
#         header_row = FlowPanel(width='100%', background='lightgrey', align='left')
#         for column in data[0].keys():
#             header_label = Label(text=column, bold=True)
#             header_row.add_component(header_label)
#         self.data_display_container.add_component(header_row)
        
#         for row_data in data:
#             row_panel = FlowPanel(width='100%', align='left')
#             for value in row_data.values():
#                 cell_label = Label(text=str(value))
#                 row_panel.add_component(cell_label)
#             self.data_display_container.add_component(row_panel)

#     def display_feedback(self, success, message):
#         self.feedback_label.text = message
#         self.feedback_label.foreground = "#4CAF50" if success else "#F44336"


    

class home(homeTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Enhanced Layout Setup
        self.title = Label(text="Data Processing Portal", font_size=24, bold=True, align="center")
        self.nav_bar = FlowPanel(align="center")
        # self.nav_bar.add_component(Link(text="Verticals", align="center"))
        self.nav_bar.add_component(Link(text="Analytics", align="center"))
        self.nav_bar.add_component(Link(text="Anomaly Detection", align="center"))
        self.nav_bar.add_component(Link(text="Anomaly Detection", align="center"))
        self.nav_bar.add_component(Link(text="Multi Sense", align="center"))
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
        
        self.connect_button = Button(text="Connect", icon="fa:plug", role="primary-color", width=120)
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
        
        self.process_file_button = Button(text="Process File", icon="fa:cogs", role="secondary-color", enabled=False, width=120)
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
      
