#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 10:52:20 2017

@author: dlennard09
"""

# request_data.py (custom: get's data from http request)
# mapparser.py
# tags.py  
# users.py (think about adding a table of users to your db that'd be sick)
# audit.py (street name clean up)
# data.py (the final putting of tags into the csv files  ) 

# sql.py (this is one you'll make to create the sql statements needed)
# insert_data.py (custom: inserts csv data directly into sql)

# sample.py (this creates a sample of your data for practice and code is below)
'''
import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "some_osm.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample.osm"

k = 10 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')
    '''