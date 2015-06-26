"""
Current module have functions for establishing connection with
API Servers
"""
from urllib.request import *
import http.client
from requestHeaderConstructor import *
import json
__author__ = 'aleksandrlazarenko'
def make_info_request():
    connection = http.client.HTTPConnection(APIRoot)                    # opening connection
    api_sub_root = construct_find_artist_req_str(artist_name)           # getting sub root
    connection.request('GET', api_sub_root)                             # making request
    response = connection.getresponse()                                 # getting response
    byte_data_about_artist = response.read()                            # reading response
    json_data_about_artist = byte_data_about_artist.decode('utf-8')     # getting string from bytes
    connection.close()                                                  # closing connection