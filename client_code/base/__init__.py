from ._anvil_designer import baseTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..home import home

class base(baseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
      
    # self.content_panel.add_component((home()))

  def button_signup_click(self, **event_args):
    email = self.useremail.text
    password = self.password.text
    message = anvil.server.call('sign_up', email, password)
    alert(message)

  def button_login_click(self, **event_args):
    email = self.useremail.text
    password = self.password.text
    message = anvil.server.call('login', email, password)
    alert(message)
    if message == "Login successful!":
        # Optionally, redirect to another form upon successful login
        self.content_panel.clear()
        self.content_panel.add_component(home())

  

