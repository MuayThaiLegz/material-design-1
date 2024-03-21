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
    # self.setup_connection_controls()
        
  def button_login_click(self, **event_args):
    email = self.useremail.text
    password = self.password.text
    mongoConnect = self.mongoConnect.text
    # self.connectingstring = mongoConnect
    
    # message = anvil.server.call('login', email, password)
    if get_user() is None:
      login_with_form()

    open_form(home(mongoConnect))
   
  def link_signup_click(self, **event_args):
    """This method is called when the link is clicked"""
    # Brings up sign up page
    self.content_panel.clear()
    self.basesidebar.visible = False
    self.content_panel.add_component(signup())

  
  def on_connect_clicked(self, **event_args):
    # connString = self.ip_address_box.text
    email = self.useremail.text
    password = self.password.text
    connString = self.mongoConnect.text
    # self.connectingstring = connString
    
    success, message = anvil.server.call('connect_to_mongodb', connString)
    alert(message)
    if message:
      alert("Signup successful.")
      open_form(home(connString))
    else:
        alert("Signup failed.")
          
  def websitelink_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.js.window.location.href = "https://connectivialabs.com/"


