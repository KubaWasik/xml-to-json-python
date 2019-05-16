import json
import unittest
from xml.etree.ElementTree import ParseError, fromstring

from converter import Field, Object


def converter(xml):
    try:
        root = fromstring(xml)
    except ParseError:
        return None

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
    return json.dumps(output)


class MyTestCase(unittest.TestCase):
    def test_empty_input(self):
        result = converter("")
        self.assertEqual(result, None)

    def test_valid_input(self):
        result = converter("""<objects>
                    <object>
                        <obj_name>object name</obj_name>
                        <field>
                            <name>int field name</name>
                            <type>int</type>
                            <value>1</value>
                        </field>
                        <field>
                            <name>string field name</name>
                            <type>string</type>
                            <value>str</value>
                        </field>
                    </object>
                </objects>""")
        correct_result = '{"object name": {"int field name": 1, "string field name": "str"}}'
        self.assertEqual(result, correct_result)

    def test_invalid_object(self):
        result = converter("""<objects>
                    <obiect>
                        <obj_name>object name</obj_name>
                        <field>
                            <name>int field name</name>
                            <type>int</type>
                            <value>1</value>
                        </field>
                        <field>
                            <name>string field name</name>
                            <type>string</type>
                            <value>str</value>
                        </field>
                    </object>
                </objects>""")
        self.assertEqual(result, None)

    def test_invalid_fields_name(self):
        result = converter("""<objects>
                    <object>
                        <obj_name>object name</obj_name>
                        <lolfield>
                            <name>int field name</name>
                            <type>int</type>
                            <value>1</value>
                        </lolfield>
                        <pokemon_field>
                            <name>string field name</name>
                            <type>string</type>
                            <value>str</value>
                        </pokemon_field>
                    </object>
                </objects>""")
        self.assertEqual(result, "{}")

    def test_invalid_field_name(self):
        result = converter("""<objects>
                    <object>
                        <obj_name>object name</obj_name>
                        <pokemon_field>
                            <name>int field name</name>
                            <type>int</type>
                            <value>1</value>
                        </pokemon_field>
                        <field>
                            <name>string field name</name>
                            <type>string</type>
                            <value>str</value>
                        </field>
                    </object>
                </objects>""")
        self.assertEqual(result, '{"object name": {"string field name": "str"}}')

    def test_invalid_field_type_name(self):
        result = converter("""<objects>
                    <object>
                        <obj_name>object name</obj_name>
                        <field>
                            <name>int field name</name>
                            <typee>int</typee>
                            <value>1</value>
                        </field>
                        <field>
                            <name>string field name</name>
                            <typee>string</typee>
                            <value>str</value>
                        </field>
                    </object>
                </objects>""")
        self.assertEqual(result, "{}")

    def test_invalid_field_type(self):
        result = converter("""<objects>
                    <object>
                        <obj_name>object name</obj_name>
                        <field>
                            <name>int field name</name>
                            <type>int</type>
                            <value>nope</value>
                        </field>
                        <field>
                            <name>string field name</name>
                            <type>tuple</type>
                            <value>(str,1)</value>
                        </field>
                    </object>
                </objects>""")
        self.assertEqual(result, "{}")

    def test_no_root(self):
        result = converter("""<object>
                        <obj_name>object name</obj_name>
                        <field>
                            <name>int field name</name>
                            <type>int</type>
                            <value>1</value>
                        </field>
                        <field>
                            <name>string field name</name>
                            <typee>string</typee>
                            <value>str</value>
                        </field>
                    </object>
                    <object>
                        <obj_name>object name</obj_name>
                        <field>
                            <name>int field name</name>
                            <type>int</type>
                            <value>1</value>
                        </field>
                        <field>
                            <name>string field name</name>
                            <typee>string</typee>
                            <value>str</value>
                        </field>
                    </object>""")
        self.assertEqual(result, None)


if __name__ == '__main__':
    unittest.main()
