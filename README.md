# XML to JSON converter in Python

program use Python 3.7 with additional packages: json, dataclass, typing and xml

Valid XML to convert should look like:
root could be any other node like objects
```xml
  <root>
    <object>
      <obj_name> object name </obj_name>
      <field>
        <name> field name </name>
        <type> field type </type>
        <value> field value </value>
      </field>
      
      ... other fields
      
    </object>
    
    ... other objects
    
  </root>
```
  
program will produce output JSON file, example:
```json
  {
    "object 1 name" : {
      "field 1 name": "field value",
      "field 2 name": "other field value",
      "field with int val": 23
    },
    "object 2 name" : {
      "lol field": "lol",
      "pikachu": "pika pika",
      "wery stronk swort od deztruktion": 99999999
    }
  }
```
