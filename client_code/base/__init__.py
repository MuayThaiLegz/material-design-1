# baseTemplate.py

from ._anvil_designer import baseTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..home import home
from ..signup import signup
from anvil.users import login_with_form, logout, get_user


class base(baseTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
 
  def link_signup_click(self, **event_args):
    """This method is called when the link is clicked"""
    # Brings up sign up page
    self.content_panel.clear()
    self.content_panel.add_component(signup())

        
  def button_login_click(self, **event_args):
    email = self.useremail.text
    password = self.password.text
    # message = anvil.server.call('login', email, password)
    if get_user() is None:
      login_with_form()
      self.content_panel.add_component(home())
    # alert(message)
    # if message == "Login successful.":
        # Optionally, redirect to another form upon successful login
        # self.content_panel.clear()
        

  def websitelink_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.js.window.location.href = "https://connectivialabs.com/"
