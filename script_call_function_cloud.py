import json
import httplib
import urllib
import sys
from settings import Settings

MODE = "agents"

def get_connection():
    url = Settings.CONFIG[MODE]['url'] + ':' + Settings.CONFIG[MODE]['port']
    if Settings.CONFIG[MODE]['type_protocol'] == 'https':
        connection = httplib.HTTPSConnection(url)
    else:
        connection = httplib.HTTPConnection(url)
    return connection

def call_function_cloud(function_name, params={}):
    connection = get_connection()
    connection.connect()
    connection.request('POST', Settings.CONFIG[MODE]['post_url'] +  '/functions/' + function_name, json.dumps(params), {
       "X-Parse-Application-Id": Settings.CONFIG[MODE]['application_id'],
       "X-Parse-REST-API-Key": Settings.CONFIG[MODE]['rest_api_key'],
       "X-Parse-Master-Key": Settings.CONFIG[MODE]['master_key'],
       "Content-Type": "application/json"
     })
    result = connection.getresponse().read()
    return result

if __name__ == "__main__":
    function_name = sys.argv[1]
    params = {}
    if (len(sys.argv) == 3):
        params = eval(sys.argv[2])
    result = call_function_cloud(function_name, params)
    print result
