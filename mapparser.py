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
