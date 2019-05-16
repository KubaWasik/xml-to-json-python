import json
import sys
from dataclasses import dataclass
from typing import List, Union
from xml.etree.ElementTree import ParseError, parse


@dataclass
class Field:
    """
        Field class
    """
    name: str
    type: str
    value: Union[str, int]


@dataclass
class Object:
    """
        Object class
    """
    obj_name: str
    fields: List[Field]


# both classes Field and Object created for good looking code

print("Reading file 'input.xml'")
try:
    xml_file = open('input.xml', encoding='UTF-8')
except IOError:
    sys.stderr.write("\nError: 'input.xml' not found\n")
    exit(-1)
try:
    tree = parse(xml_file)
    root = tree.getroot()
except ParseError:
    sys.stderr.write("Error: Invalid XML file")
    exit(-1)

print("Creating objects list from xml tree")

objects_list = []  # list of objects

for obj in root.findall('object'):
    # xml file must have root element which contains "object" child objects
    # checking all objects, only "obj_name" and "field" filed are allowed, rest of fields are skipped

    if obj.find('obj_name') is None or obj.find('obj_name').text is None:
        # object has no name
        continue
    if obj.find('field') is None:
        # object has no fields
        continue

    object_fields = []  # list of field of current object
    for field in obj.findall('field'):
        tmp_name, tmp_type, tmp_value = field.find('name'), field.find('type'), field.find('value')
        if tmp_name is None or tmp_name.text is None:
            # field has no name
            continue
        if tmp_type is None or tmp_type.text is None:
            # field has no type
            continue
        if tmp_type.text.strip() != "int" and tmp_type.text.strip() != "string":
            # field type is not allowed
            continue
        if tmp_value is None or tmp_value.text is None:
            # field has no value
            continue
        if tmp_type.text.strip() == "int":
            try:
                tmp_value.text = int(tmp_value.text.strip())
            except ValueError:
                continue
        object_fields.append(Field(tmp_name.text.strip(), tmp_type.text.strip(),
                                   tmp_value.text if type(tmp_value.text) == int else tmp_value.text.strip()))
    if len(object_fields) == 0:
        # object has empty fields
        continue
    objects_list.append(Object(obj.find('obj_name').text.strip(), object_fields))

output = {}  # dict contains: keys - object name, value - dict of object fields
for obj in objects_list:
    item = {}
    for field in obj.fields:
        item[field.name] = field.value
    output[obj.obj_name] = item

with open("output.json", 'w') as output_file:
    print("Writing JSON file")
    output_file.write(json.dumps(output))
    print("Output: 'output.json'")
