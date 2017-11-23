import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus
import schema # note: refers to the schema.py file attached in this directory 

# these are custom made functions  
from audit import check_and_fix_street_name
 

# changed this  
CSV_PATH = "./CSV_files/"
NODES_PATH = CSV_PATH+"nodes.csv"
NODE_TAGS_PATH =CSV_PATH+ "nodes_tags.csv"
WAYS_PATH = CSV_PATH+"ways.csv"
WAY_NODES_PATH = CSV_PATH+"ways_nodes.csv"
WAY_TAGS_PATH = CSV_PATH+"ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Be sure fields order in the csvs matches the field order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp'] 
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type'] 
WAY_NODES_FIELDS = ['id', 'node_id', 'position'] 


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    def get_tags(element, tags):
        for child in element.iter('tag'): 
            
            attr = child.attrib
            
            # check for problematic characters first and skip if matches
            if PROBLEMCHARS.search(attr['k']):
                continue
                
            child_dict = {}
            child_dict['id'] = element.attrib['id']
            child_dict['value'] = attr['v']
            
        
            child_dict['key'] = attr['k'].split(':', 1)[-1] 
            
            # Check that the k tag is regular or has addr in it. 
            # Treat it according to specs
            if LOWER_COLON.search(attr['k']):
                child_dict['type'] = attr['k'].split(':')[0]
            
            else: 
                child_dict['type'] = 'regular' 
                
            tags.append(child_dict)
            
        return tags
    
    if element.tag == 'node':
        
        attr = element.attrib
        node_attribs['id'] = attr['id']
        node_attribs['user'] = attr['user']
        node_attribs['uid'] = attr['uid']
        node_attribs['version'] = attr['version']
        node_attribs['lat'] = attr['lat']
        node_attribs['lon'] = attr['lon']
        node_attribs['timestamp'] = attr['timestamp']
        node_attribs['changeset'] = attr['changeset'] 
        
        # tags list 
        tags = get_tags(element, [])
        return {'node': node_attribs, 'node_tags': tags}
    
    elif element.tag == 'way':
        
        attr = element.attrib
        way_attribs['id'] = attr['id']
        way_attribs['user'] = attr['user']
        way_attribs['uid'] = attr['uid']
        way_attribs['version'] = attr['version']
        way_attribs['timestamp'] = attr['timestamp']
        way_attribs['changeset'] = attr['changeset']
        
        # set up way nodes 
        for i, child in enumerate(element.iter('nd')):
            way_node_dict = {}
            way_node_dict['id'] = attr['id']
            way_node_dict['node_id'] = child.attrib['ref']
            way_node_dict['position'] = i
            
            way_nodes.append(way_node_dict)
            
        # tags list 
        tags = get_tags(element, [])

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string)) 


class UnicodeDictWriter(csv.DictWriter, object):
    # note: this was unnecessary and done strictly for python 2 since it doesn't automatically read unicode
    # commented out writerow since it's overriding an existing method which should work fine in python 3 
    # if using windows and data doesn't write as unicode, you can find a way on your own or use original 
    # python 2 code
    """Extend csv.DictWriter to handle Unicode input"""

    """ def writerow(self, row):
        # change .iteritems() method to .items() (python 3 uses .items()) and figure out how to enforce unicode
        # note: the following is dictionary comprehension, similar to list comprehension but for dicts
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        }) 
    """
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'w') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:
    
        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader() 
        node_tags_writer.writeheader() 
        ways_writer.writeheader() 
        way_nodes_writer.writeheader() 
        way_tags_writer.writeheader() 

        validator = cerberus.Validator() 
        
        
        #added this
        count = 0
        for element in get_element(file_in, tags=('node', 'way')):
            
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    # call function from audit 
                    check_and_fix_street_name(element)
                    # then finish original functions   
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                    
                elif element.tag == 'way':
                    # call function from audit
                    check_and_fix_street_name(element)
                    # then finish original functions
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags']) 
