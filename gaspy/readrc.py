'''
The function in this module is used to read the GASpy rc file. It is separated
from the rest of the module so that we don't need any non-native Python modules
to read the file.
'''

import os
from os.path import join
import json


def read_rc(key=None):
    '''
    This function will pull out keys from the .gaspyrc file for you

    Input:
        key     [Optional] The string indicating the configuration you want
    Output:
        configs A dictionary whose keys are the input keys and whose values
                are the values that we found in the .gaspyrc file
    '''
    # Pull out the PYTHONPATH environment variable
    # so that we know where to look for the .gaspyrc file
    try:
        python_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    except KeyError:
        raise KeyError('You do not have the PYTHONPATH environment variable. You need to add GASpy to it')

    # Initializating our search for the .gaspyrc file
    rc_file = '.gaspyrc.json'
    found_config = False
    # Search our PYTHONPATH one-by-one
    for path in python_paths:
        for root, dirs, files in os.walk(path):
            if rc_file in files:
                rc_file = join(root, rc_file)
                found_config = True
                break
        # Stop looking through the files if we've found it
        if found_config:
            break
    if not found_config:
        raise EnvironmentError('Could not find .gaspyrc.json; please add it to your PYTHONPATH')

    # Now that we've found it, open it up and read from it
    with open(rc_file, 'r') as rc:
        configs = json.load(rc)

    # Return out the keys you asked for. If the user did not specif the key, then return it all
    if key:
        try:
            return configs[key]
        except KeyError as err:
            err.message += "; Check the spelling/capitalization of the config you're looking for"
            raise
    else:
        return configs