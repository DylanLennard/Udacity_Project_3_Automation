# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    """simply return the uid attribute for user id that is attributed to the tag"""
    return element.attrib['uid']

        

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        # delete pass and enter your code here
        
        '''
        we need to check that it's in a node, way, or relation 
        (got this by examining the xml file)
        '''
        if element.tag in ['node','way','relation']:
            users.add(get_user(element))

    return len(users) 

# TODO: rethink this function to return a csv file of usernames and userIDs 
