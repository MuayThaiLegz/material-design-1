

# # base.py

# from ._anvil_designer import baseTemplate
# from anvil import *
# import anvil.server
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# from ..home import home

# class base(baseTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)
      
#     # self.content_panel.add_component((home()))

#   def button_signup_click(self, **event_args):
#     anvil.server.call('create_db')
#     email = self.useremail.text
#     password = self.password.text
#     if email and password:  # Simple check to ensure fields are not empty
#             result = anvil.server.call('sign_up', email, password)
#             alert(result)
#     else:
#         alert("Please enter both email and password")
      

#   def button_login_click(self, **event_args):
#     email = self.useremail.text
#     password = self.password.text

#     if email and password:  # Simple check to ensure fields are not empty
#       result = anvil.server.call('login', email, password)
#       if result == "Login successful!":
#         # Optionally, redirect to another form upon successful login
#         self.content_panel.clear()
#         self.content_panel.add_component(home())
#       else:
#         alert(result)        
#     else:
#         alert("Please enter both email and password")  

# base.py

from ._anvil_designer import baseTemplate
from anvil import *
import anvil.server
from ..home import home

class base(baseTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Optionally, load the home component or any other initial setup as needed
        # self.content_panel.add_component(home())

    def button_signup_click(self, **event_args):
        # Ensure the database exists before trying to sign up a new user
        anvil.server.call('create_db')
        
        email = self.useremail.text  # Assuming 'useremail' is the name of your TextBox for email input
        password = self.password.text  # Assuming 'password' is the name of your TextBox for password input
        
        # Simple check to ensure fields are not empty
        if email and password:
            result = anvil.server.call('sign_up', email, password)
            alert(result)
        else:
            alert("Please enter both email and password")

    def button_login_click(self, **event_args):
        email = self.useremail.text
        password = self.password.text
        
        # Simple check to ensure fields are not empty
        if email and password:
            result = anvil.server.call('login', email, password)
            if result == "Login successful!":
                # Clear the content panel and redirect to another form upon successful login
                self.content_panel.clear()
                self.content_panel.add_component(home())
            else:
                alert(result)
        else:
            alert("Please enter both email and password")
