from ._anvil_designer import edgevectorsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class edgevectors(edgevectorsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.content_panel.add_component(Label(text='edgevectors', italic=True))
    
    # Any code you write here will run before the form opens.
