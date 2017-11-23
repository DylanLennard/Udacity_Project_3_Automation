"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    NOTE: You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
    
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "improving_street_names.xml"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]


# note: for now you're just making changes for what you see in the test function below  
mapping = { "St"  : "Street",
            "St." : "Street", 
            "Rd." : "Road", 
            "Ave" : "Avenue",
            "N."  : "North", 
            "Rd"  : "Road", 
            "Dr"  : "Drive",
            "Hwy.": "Highway", 
            "st"  : "Street"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                    
    osm_file.close()
    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE
    name_split = name.split(" ")
    for i, val in enumerate(name_split):
        if val in mapping.keys():
            name_split[i] = mapping[val]
    name = " ".join(name_split)
    
    return name 

## added this for data to access 
def check_and_fix_street_name(elem):
    for tag in elem.iter("tag"):
        if is_street_name(tag):
            update_name(tag.attrib['v'], mapping)

'''
def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.items(): # changed this method from .iteritems() from 2.7 to 3.6's .items()  
        for name in ways:
            better_name = update_name(name, mapping)
            print (name, "=>", better_name) # cleaned up this print statement 
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()
'''