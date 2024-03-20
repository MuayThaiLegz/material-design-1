# signup.py

from ._anvil_designer import signupTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from ..home import home
# from ..base import base

class signup(signupTemplate):
    def __init__(self, **properties):
        super().__init__(**properties)
        # self.init_components(**properties)
        
        # Layout
        self.layout = ColumnPanel()
        self.add_component(self.layout)
        
        # Email
        self.email_box = TextBox(placeholder="Email")
        self.layout.add_component(self.email_box)
        
        # Password
        self.password_box = TextBox(placeholder="Password", hide_text=True)
        self.layout.add_component(self.password_box)
        
        # Password Verification
        self.password_verify_box = TextBox(placeholder="Verify Password", hide_text=True)
        self.layout.add_component(self.password_verify_box)
        
        # Signup Button
        self.signup_button = Button(text="Signup")
        self.signup_button.set_event_handler('click', self.signup_clicked)
        self.layout.add_component(self.signup_button)
        
        # Back to Home Button
        self.back_button = Button(text="Back to Home")
        self.back_button.set_event_handler('click', self.back_to_home_clicked)
        self.layout.add_component(self.back_button)
        
    def signup_clicked(self, **event_args):
        email = self.email_box.text
        password = self.password_box.text
        verify_password = self.password_verify_box.text
        
        if password != verify_password:
            alert("Passwords do not match. Please try again.")
            return
        else:
          anvil.server.call('create_db')
          message = anvil.server.call('sign_up', email, password)
          
        alert(message)
        if message:
            alert("Signup successful.")
            open_form(home())
        else:
            alert("Signup failed.")
          
      

        # Implement the rest of your signup logic here
        # For example, call a server function to handle signup
        # success = anvil.server.call('server_signup_function', email, password)
        
    def back_to_home_clicked(self, **event_args):
        open_form('base')
      

# class signup(signupTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)

#   def button_signup_click(self, **event_args):
#     email = self.signupemail.text
#     password = self.signuppassword.text
    
#     anvil.server.call('create_db')
    
#     message = anvil.server.call('sign_up', email, password)
#     alert(message)
    
#   def button_back_to_home_click(self, **event_args):
#     """This method is called when the Back to Home button is clicked."""
#     open_form('base')  # Opens the Home form