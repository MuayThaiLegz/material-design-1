from ._anvil_designer import anomalydetectionTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class anomalydetection(anomalydetectionTemplate):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      # self.content_panel = ColumnPanel()
      self.content_panel.add_component(Label(text="Anomaly Detection", italic=True))
      
      self.back_button = Button(text="Back to Home")
      self.back_button.set_event_handler('click', self.back_to_home_clicked)
      self.add_component(self.back_button)  
        
    def back_to_home_clicked(self, **event_args):
      open_form('base')  

  
  # def __init__(self, **properties):
  #   # Set Form properties and Data Bindings.
  #   self.init_components(**properties)
  #   self.content_panel.add_component(Label(text='anomalydetection', italic=True))
  #   self.back_button = Button(text="Back to Home")
  #   self.back_button.set_event_handler('click', self.back_to_home_clicked)
  #   self.layout.add_component(self.back_button)
  #   def back_to_home_clicked(self, **event_args):
  #     open_form('home')
    

  #   # Any code you write here will run before the form opens.
