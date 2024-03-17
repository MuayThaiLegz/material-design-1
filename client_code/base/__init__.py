# baseTemplate.py

from ._anvil_designer import baseTemplate
from anvil import *
import anvil.server
from anvil import open_url
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..home import home
from ..signup import signup

class base(baseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
 
  def link_signup_click(self, **event_args):
    """This method is called when the link is clicked"""
    # Brings up sign up page
    # self.content_panel.clear()
    self.content_panel.add_component(signup())

        
  def button_login_click(self, **event_args):
    email = self.useremail.text
    password = self.password.text
    message = anvil.server.call('login', email, password)
    alert(message)
    if message == "Login successful!":
        # Optionally, redirect to another form upon successful login
        self.content_panel.clear()
        self.content_panel.add_component(home())

  def websitelink_click(self, **event_args):
    """This method is called when the link is clicked"""
     open_url("https://connectivialabs.com/")
    # https://connectivialabs.com/
    pass


    

  

