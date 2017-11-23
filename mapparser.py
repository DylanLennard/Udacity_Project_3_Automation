# -*- coding: utf-8 -*-


# if you put this in your own python file, call it mapparser.py
import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):

    # YOUR CODE HERE
    tags = {}
    for _, val in ET.iterparse(filename):
        if val.tag not in tags.keys():
            tags[val.tag] = 1
        else:
            tags[val.tag] += 1
    return tags


'''
# this test is just to see that you've completed the assignment correctly,
# you won't need this in your project
def test():

    # note, you can look at an osm file by copying it
    # and changing the copied extension to .xml
    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                    'member': 3,
                    'nd': 4,
                    'node': 20,
                    'osm': 1,
                    'relation': 1,
                    'tag': 7,
                    'way': 1}

    
if __name__ == "__main__":
    test()
'''