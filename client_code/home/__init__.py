from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.server
from anvil.tables import app_tables


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
        # Setup UI and fetch initial data
        self.setup_ui()
        self.fetch_datasets()

    def setup_ui(self):
        self.content_panel = ColumnPanel()
        self.data_grid_placeholder = FlowPanel()
        self.add_component(self.content_panel)
        self.content_panel.add_component(self.data_grid_placeholder)
        
        self.setup_feedback_label()
        self.setup_nav_links()
        self.setup_dataset_controls()
        self.setup_collection_dropdown()
        self.setup_file_controls()

    def setup_feedback_label(self):
        self.feedback_label = Label(text="", font_size=16, bold=True, align='center', visible=False)
        self.content_panel.add_component(self.feedback_label)

    def setup_nav_links(self):
        self.nav_links = {'Analytics': analytics, 'Anomaly Detection': anomalydetection,
                          'Edge Vectors': edgevectors, 'Multi Sense': multisense}
        for name, form in self.nav_links.items():
            link = Link(text=name, align="center")
            link.set_event_handler('click', lambda sender, **e: self.open_feature_form(form))
            self.add_component(link)

    def setup_dataset_controls(self):
        self.dataset_radio_panel = FlowPanel(width='fill')
        self.content_panel.add_component(self.dataset_radio_panel)

    def setup_collection_dropdown(self):
        self.collection_dropdown = DropDown(visible=False)  # Initially hidden
        self.collection_dropdown.set_event_handler('change', self.on_collection_selected)
        self.content_panel.add_component(self.collection_dropdown)

    def setup_file_controls(self):
        self.file_loader = FileLoader(multiple=False, file_types=[".csv", ".xlsx", ".json", ".parquet"], tooltip="Upload data file", width="fill")
        self.file_loader.set_event_handler('change', self.on_file_loader_changed)
        self.content_panel.add_component(self.file_loader)
        
        self.process_file_button = Button(text="Process File", icon="fa:cogs", enabled=False, width=120)
        self.process_file_button.set_event_handler('click', self.on_process_file_clicked)
        self.content_panel.add_component(self.process_file_button)

    def on_file_loader_changed(self, **event_args):
        self.process_file_button.enabled = bool(self.file_loader.file)

    def on_process_file_clicked(self, **event_args):
        if self.file_loader.file:
            # Example logic for handling file processing
            self.display_feedback(True, "File processed successfully.")

    def fetch_datasets(self):
        success, datasets = anvil.server.call('get_database_names', self.mongoConnect)
        if success:
            self.update_dataset_radios(datasets)
        else:
            self.display_feedback(False, "Failed to fetch datasets.")

    def update_dataset_radios(self, datasets):
        for dataset in datasets:
            radio = RadioButton(text=dataset, group_name="datasets")
            radio.set_event_handler('change', self.on_dataset_selected)
            self.dataset_radio_panel.add_component(radio)

    def on_dataset_selected(self, sender, **event_args):
        if sender.selected:
            self.selected_dataset = sender.text
            collections = anvil.server.call('list_collections', self.mongoConnect, self.selected_dataset)
            self.collection_dropdown.items = [(c, c) for c in collections]
            self.collection_dropdown.visible = True

  
    def on_collection_selected(self, sender, **event_args):
      collection_name = sender.selected_value
      data, columns = anvil.server.call('fetch_collection_data', self.mongoConnect, self.selected_dataset, collection_name)
      if data:
          self.populate_data_simulated_grid(data[:10], columns)
      else:
          self.display_feedback(False, "No data found for the selected collection.")

    def populate_data_simulated_grid(self, data, columns):
      
        self.data_grid_placeholder.clear()  # Clear previous content
        for row_data in data:
            row_panel = FlowPanel()  # This will represent a row
            for column_name in columns:
                cell_label = Label(text=str(row_data[column_name]), width=200)  # Create a label for each cell
                row_panel.add_component(cell_label)
            self.data_grid_placeholder.add_component(row_panel)  # Add the row to the placeholder

    def create_and_populate_data_grid(self, data, columns):
      self.data_grid_placeholder.clear()
      data_grid = DataGrid(auto_header=True)
      data_grid.columns = [DataGridColumn(title=col, data_key=col) for col in columns]  # Corrected typo here from data_gird to data_grid and fixed parenthesis
      data_grid.items = data
      self.data_grid_placeholder.add_component(data_grid)

    def open_feature_form(self, form):
        self.content_panel.clear()
        self.content_panel.add_component(form())

    def display_feedback(self, success, message):
        self.feedback_label.text = message
        self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
        self.feedback_label.visible = True



    