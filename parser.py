import os
import json
import argparse
import tags
import logging
from xml.dom import minidom, Node

class Logger(object):
    def __init__(self):
        FORMAT = '%(asctime)s - %(threadName)s:%(name)s:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s :: %(message)s'
        logging.basicConfig(format=FORMAT)
        self.logger = logging.getLogger('xmlparser')
        self.logger.level = logging.INFO
    
    def get_logger(self):
        return self.logger

class Parser(object):
    def get_logger(self):
        if not hasattr(self,'logger'):
            self.logger  = Logger().get_logger()
        return self.logger
    
    def get_parser(self):
        if not hasattr(self,'parser'):
            self.parser = argparse.ArgumentParser(
                    prog='python3 parser.py',
                    description='Feed this file with the template location, tags to be modified and how many times the template to be repeated ')

            self.parser.add_argument('-t', '--template', help='template location to process, e.g template/Put_Applicant_001_of_001.xml')
            self.parser.add_argument('-o', '--output', help='output location for the processed fule, e.g output/Output.xml')
            self.parser.add_argument('-r', '--repeat', help='repetition of the template, e.g 20')
        return self.parser
    
    def log(self, message):
        self.get_logger().info(message)

    def __init__(self, debug=False):
        self.debug = debug
        self.tags_present = False
        self.get_logger().info('Logger[xmlparser] instantiated')
        self.args = self.get_parser().parse_args()
        self.get_logger().info('Arguments Processed')
        self.validate()
        self.output = minidom.Document()

    def validate(self):
        self.get_logger().info('Check if --template option provided')
        if self.args.template is not None and not os.path.exists(self.args.template):
            self.get_logger().error('Template File Path not valid')
            exit(0)
        else:
            self.TEMPLATE_FILE=self.args.template
            if self.TEMPLATE_FILE is None or len(self.TEMPLATE_FILE) == 0:
                if self.debug:
                    TEMPLATE_NAME='Put_Applicant_001_of_001.xml'
                    TEMPLATE_NAME='test.xml'
                    if not os.path.exists('template/'):
                        self.get_logger().info('Directory template/ does not exists in the current path')
                        self.get_logger().info('Creating the template/ directory')
                        os.mkdir('template/')
                    self.TEMPLATE_FILE = "template/" + TEMPLATE_NAME

        self.get_logger().info('Check if --output option provided')
        if self.args.output is not None and not os.path.exists(self.args.output):
            self.get_logger().info("Output File Path does not exist")
            self.get_logger().info('defaulting to output/Output.xml location')
            if not os.path.exists('output/'):
                self.get_logger().info('Directory output/ does not exists in the current path')
                self.get_logger().info('Creating the output/ directory')
                os.mkdir('output/')
                path = 'output/Output.xml'
                with open(path, 'w'):
                    os.utime(path, None)
        else:
            self.OUTPUT_FILE=self.args.output
        if self.OUTPUT_FILE is None or len(self.OUTPUT_FILE) == 0:
            if self.debug:
                OUTPUT_NAME='Output.xml'
                self.OUTPUT_FILE = "output/" + OUTPUT_NAME

        self.get_logger().info('Check if --repeat option provided')
        if self.args.repeat is not None and int(self.args.repeat) < 1:
            self.get_logger().error("Repeats should be between 1 to 100")
            exit(0)
        else:
            self.REPEATS=self.args.repeat
            if self.REPEATS is None:
                self.REPEATS=1
        
        if all([self.TEMPLATE_FILE, self.OUTPUT_FILE, self.REPEATS]):
            self.get_logger().info("Template File Path :: " + self.TEMPLATE_FILE)
            self.get_logger().info("Output File Path :: " + self.OUTPUT_FILE)
            self.get_logger().info("Repeat times :: " + str(self.REPEATS))
        else:
            self.get_logger().error("No arguments provided")
    
    def help(self):
        self.get_parser().print_help()

    def write_output(self):
        with open(self.OUTPUT_FILE, 'w') as f:
            self.output.writexml(f,encoding="utf-8") 

    def set_all_attributes(self, root, node, _tags):
        if root.attributes is not None:
            for k, v in root.attributes.items():
                value = v
                if k in _tags:
                    value = _tags[k]
                node.setAttribute(k,value)

    def walk_xml(self, root, node, _tags):
        nodeList = root.childNodes
        for child in nodeList:
            if child.nodeType == Node.TEXT_NODE:
                value = child.data
                strippedList = child.parentNode.tagName.split(':')
                if len(strippedList) == 2:
                    stripped_tag = strippedList[1]
                    if stripped_tag in _tags:
                        self.tags_present = True
                        # value = set_specific_values(stripped_tag)
                        value = _tags[stripped_tag]
                item = self.output.createTextNode(value)
            if child.nodeType == Node.ELEMENT_NODE:
                item = self.output.createElementNS(child.namespaceURI, child.tagName)
                self.set_all_attributes(child, item, _tags)
            node.appendChild(item)
            self.walk_xml(child, item, _tags)
            
    def add_nodes(self, root, node):
        for _ in range(int(self.REPEATS)):
            _tags = tags.get_mock_data()
            self.set_all_attributes(root, node, _tags)
            self.walk_xml(root, node, _tags)
            if self.tags_present:
                self.get_logger().info("Modified Tags and its content :: " + json.dumps(_tags, indent=4))
            else:
                self.get_logger().error("Tags Not Available for modification, please check your tags.py and template file")

    def get_namespace(self):
        with open(self.TEMPLATE_FILE, 'r') as f:
            for tag in [ i for i in f.read().splitlines()]:
                if 'root' in tag:
                    namespace = tag.split(' ')[0].split(':')[0].replace('<', '')
                    self.get_logger().info("Namespace for the template :: " + namespace)
                    return namespace
        self.get_logger().info("No Root Element for the template !!")
        exit()
            

    def read_template(self):
        try:
            template = minidom.parse(self.TEMPLATE_FILE)
        except Exception as e:
            self.get_logger().error('not well-formed (invalid token)')
            self.get_logger().error(e)
            exit(1)
        
        try: 
            rootList = template.getElementsByTagName(self.get_namespace() + ":root")
            if len(rootList) == 1:
                root = rootList[0]
            else:
                raise Exception('No Root Element')
        except Exception as e:
            self.get_logger().error(e)
            exit(1)
        
        node = self.output.createElementNS(root.namespaceURI, root.tagName)
        self.add_nodes(root, node)
        self.output.appendChild(node)
        if self.tags_present:
            self.get_logger().info("Output File Path :: " + self.OUTPUT_FILE)