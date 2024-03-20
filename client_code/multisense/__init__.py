from ._anvil_designer import multisenseTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class multisense(multisenseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.feedback_label.text = 'multisense'
    self.feedback_label.foreground = "#4CAF50" if success else "#F44336"
    self.feedback_label.visible = True


    # Any code you write here will run before the form opens.
