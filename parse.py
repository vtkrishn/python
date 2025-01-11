import os
import sys

from xml.dom import minidom, Node
from faker import Faker
import random

import argparse

parser = argparse.ArgumentParser(
                    prog='python3 parser.py',
                    description='Feed this file with the template location, tags to be modified and how many times the template to be repeated ')

parser.add_argument('-l', '--location')      # template location
parser.add_argument('-o', '--output')      # output location
parser.add_argument('-r', '--repeat')      # repeat the template no of times range form 1 to 100
parser.add_argument('-m', '--tags')      # template location

args = parser.parse_args()

#TODO
# if not os.path.exists(args.location):
#    print('Template Path does not exist')

# if not os.path.exists(args.output):
#     print('Output Path does not exist')

# if args.repeat:
#     print('Output Path does not exist')


# take template location if left blank take from template folder
LOCATION=args.location

# take output location if left blank take from output folder
OUTPUT_LOCATION=args.output

# take the number of things to process e.g 50
REPEATS=int(args.repeat)

# take list of tags for randomized
MODIFY_TAGS=args.tags



if LOCATION is None or len(LOCATION) == 0:
    TEMPLATE_NAME='Put_Applicant_001_of_001.xml'
    TEMPLATE_NAME='test.xml'
    LOCATION = "template/" + TEMPLATE_NAME



if OUTPUT_LOCATION is None or len(OUTPUT_LOCATION) == 0:
    OUTPUT_NAME='Output.xml'
    OUTPUT_LOCATION = "output/" + OUTPUT_NAME

if REPEATS is None:
    REPEATS=1

if MODIFY_TAGS is None or len(MODIFY_TAGS) == 0:
    MODIFY_TAGS=['Applicant_ID','First_Name','Last_Name','Address_Line_Data','Municipality','Postal_Code']
    MODIFY_TAGS=['price','name','title','author']
else:
    MODIFY_TAGS = [i for i in MODIFY_TAGS.split(',')]


print(LOCATION)
print(OUTPUT_LOCATION)
print(REPEATS)
print(MODIFY_TAGS)


SIZE=5
output = minidom.Document()

def write_output():
    with open(OUTPUT_LOCATION, 'w') as f:
        output.writexml(f,encoding="utf-8") 

def set_all_attributes(root, node):
    if root.attributes is not None:
        for k, v in root.attributes.items():
            value = v
            if k in MODIFY_TAGS:
                value = get_random_characters()
            node.setAttribute(k,value)

def set_specific_values(tag):
    if tag == 'Applicant_ID':
        value = 'A' + get_random_nums() + '-' + get_random_caps()
    elif tag == 'Address_Line_Data':
        value = f.address()

    elif tag == 'Address_Line_Data':
        value = f.address()
    else:
        value = f.first_name() #get_random_characters()
    return value
def walk_xml(root, node):
    nodeList = root.childNodes
    for child in nodeList:
        if child.nodeType == Node.TEXT_NODE:
            value = child.data
            strippedList = child.parentNode.tagName.split(':')
            if len(strippedList) == 2:
                stripped_tag = strippedList[1]
                if stripped_tag in MODIFY_TAGS:
                    # value = set_specific_values(stripped_tag)
                    value = get_random_characters()
            item = output.createTextNode(value)
        if child.nodeType == Node.ELEMENT_NODE:
            item = output.createElementNS(child.namespaceURI, child.tagName)
            set_all_attributes(child, item)
        node.appendChild(item)
        walk_xml(child, item)


def add_nodes(root, node):
    [walk_xml(root, node) for _ in range(REPEATS)]
        

def get_random(chars, size):
        return ''.join(random.choice(chars) for _ in range(size))

def get_random_nums(size=5):
    num = get_random([chr(i) for i in range(48,58)], size)
    return num

def get_random_caps(size=5):
    caps = get_random([chr(i) for i in range(65,91)], size)
    return caps

def get_random_characters(size=5):
    num = get_random([chr(i) for i in range(48,58)], size)
    small = get_random([chr(i) for i in range(97,123)], size)
    caps = get_random([chr(i) for i in range(65,91)], size)
    specials = get_random([chr(i) for i in [33,35,36,37,38,42,59,61,63] + list(range(43,47))], size)
    return random.choice([num, small, caps, specials])

def read_template():
    try:
        template = minidom.parse(LOCATION)
    except Exception as e:
        print('not well-formed (invalid token)')
        print(e)
        sys.exit(1)
    
    try: 
        rootList = template.getElementsByTagName("w:root")
        if len(rootList) == 1:
            root = rootList[0]
        else:
            raise Exception('No Root Element')
    except Exception as e:
        print(e)
        sys.exit(1)
    
    node = output.createElementNS(root.namespaceURI, root.tagName)
    set_all_attributes(root, node)
    add_nodes(root, node)
    output.appendChild(node)

f = Faker()
read_template()
write_output()





