# -*- coding: utf-8 -*-

# sample.py (this creates a sample of your data for practice and code is below)
import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow


def sample_data(OSM_FILE, SAMPLE_FILE, k=10):

    
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
    
    
    with open(SAMPLE_FILE, 'w') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')
    
        # Write every kth top level element
        for i, element in enumerate(get_element(OSM_FILE)):
            if i % k == 0:
                # added 'encoding="unicode"'to get this to work in python 3 
                output.write(ET.tostring(element, encoding="unicode"))
    
        output.write('</osm>')
