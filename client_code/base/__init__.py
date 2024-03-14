from ._anvil_designer import baseTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..home import home

class base(baseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
     
    # Check if a user is logged in when the app starts
    if anvil.users.get_user() is None:
      # If no user is logged in, show the login form
      self.login()
      
    self.content_panel.add_component((home()))

  def login(self):
    # This method shows the built-in Anvil login form
    user = anvil.users.login_with_form()
    if user is not None:
      # User logged in successfully
      # Here you can handle what happens after a successful login
      pass
    else:
      # The user closed the login form without logging in
      # You may want to handle this scenario, e.g., exit the app or re-show login
      anvil.server.call('anvil.server.reset_environment')
      self.login()
