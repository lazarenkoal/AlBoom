"""
Current module contains function which allow
app to authorize via VK
"""
from selenium import webdriver
from tkinter import messagebox

"""Returns: access token
Function for getting access token from VK API
Inputs: users login, users password
"""
def get_access_token(user_login, user_password):

    try:
        # VK API oauth URL
        url = ('https://oauth.vk.com/authorize?' +
               'client_id=4973489&' +
               'scope=audio&' +
               'redirect_uri=https://oauth.vk.com/blank.html&' +
               'display=page&' +
               'v=5.34&' +
               'response_type=token')

        # Launching webdriver and opening auth page
        driver = webdriver.Chrome(executable_path='/Users//PycharmProjects/MusicScooper/chromedriver')
        driver.get(url)

        # Pasting into email field
        user_input = driver.find_element_by_name("email")
        user_input.send_keys(user_login)

        # Pasting into password field
        password_input = driver.find_element_by_name("pass")
        password_input.send_keys(user_password)

        # Clicking on Submit button
        submit = driver.find_element_by_id("install_allow")
        submit.click()

        # Getting access token
        current = driver.current_url
        access_list = (current.split("#"))[1].split("&")
        access_token = (access_list[0].split("="))[1]

        # Closing browser window
        driver.close()
        return access_token

    # Auth failed!
    except IndexError:
        messagebox.showerror('Wrong credentials', 'Please, check your email/password once again')
