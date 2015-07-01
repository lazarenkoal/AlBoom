import main_controller
from music_info_processing import VKApiRoot
from request_constructor import construct_vk_check_token
import http.client
import json
from main_view import TokenWindow
__author__ = 'aleksandrlazarenko'


"""Main-main-main ultra-main!!!!!
"""
def main():
    # TODO: upload data from previous users visit (token, etc)
    token = '0fb6a091be154e1330af856bf3e97a772993d76e5cb3e988a3971451a5e7cbe57b025138536cca63cf1ac'
    controller = main_controller.MainWindowViewController(token)




main()