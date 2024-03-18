from ._anvil_designer import signupTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class signup(signupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    fp = FlowPanel(align='center', spacing='small')
    # A button determines its own width
    fp.add_component(Button(text="Click me"))

    # You set the width of a TextBox explicitly
    fp.add_component(TextBox(), width=100)
    
  def button_signup_click(self, **event_args):
    email = self.signupemail.text
    password = self.signuppassword.text
    
    anvil.server.call('create_db')
    
    message = anvil.server.call('sign_up', email, password)
    alert(message)
