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

 
  def link_signup_click(self, **event_args):
    """This method is called when the link is clicked"""
    # Brings up sign up page
    self.content_panel.clear()
    self.basesidebar.visible = False
    self.content_panel.add_component(signup())

        
  def button_login_click(self, **event_args):
    email = self.useremail.text
    password = self.password.text
    mongoConnect = self.mongoConnect.text
    
    # message = anvil.server.call('login', email, password)
    user = anvil.users.login_with_form()
    if user:
      success, message = anvil.server.call('connect_to_mongodb', mongoConnect)
      if success:
          # If MongoDB connection is successful, proceed to the home form.
          self.content_panel.clear()
          self.basesidebar.visible = True
          self.content_panel.add_component(home(mongoConnect=mongoConnect))
          alert("Login and MongoDB connection successful.")
      else:
          # If MongoDB connection fails, show an error message.
        alert("MongoDB connection failed: " + message)
    else:
      alert("Login failed. Please check your credentials.")

    # if get_user() is None:
    #   login_with_form()

    self.content_panel.clear()
    self.basesidebar.visible = False
    self.content_panel.add_component(home(mongoConnect))
    # alert(message)
    # if message == "Login successful.":
        # Optionally, redirect to another form upon successful login
        # self.content_panel.clear()
  
  # def setup_connection_controls(self):
  #   self.content_panel.add_component(Label(text="MongoDB Connection String:", italic=True))
  #   self.ip_address_box = TextBox(placeholder="mongodb://localhost:27017", width="fill")
  #   self.content_panel.add_component(self.ip_address_box)
    
  #   self.connect_button = Button(text="Connect", icon="fa:plug", role="primary-color", width=120)
    
  #   self.connect_button.set_event_handler('click', self.on_connect_clicked)
    
  #   self.content_panel.add_component(self.connect_button, width='fill')

  
  def on_connect_clicked(self, **event_args):
    # connString = self.ip_address_box.text
    email = self.useremail.text
    password = self.password.text
    connString = self.mongoConnect.text
    
    success, message = anvil.server.call('connect_to_mongodb', connString)
    message = anvil.server.call('login', email, password)
    alert(message)
    if message:
      alert("Signup successful.")
      open_form(home(mongoConnect))
    else:
        alert("Signup failed.")
          
  def websitelink_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.js.window.location.href = "https://connectivialabs.com/"

