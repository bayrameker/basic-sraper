# utils/save_data.py
import csv
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

def save_as_csv(data, filename):
    if not data:
        print("Kaydedilecek veri bulunamadı.")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved as CSV in {filename}")

def save_as_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Data saved as JSON in {filename}")

def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.SubElement(elem, key)
        child.text = str(val)
    return elem

def save_as_xml(data, filename, root_tag='Data', item_tag='Item'):
    root = ET.Element(root_tag)
    for entry in data:
        item_elem = dict_to_xml(item_tag, entry)
        root.append(item_elem)
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    print(f"Data saved as XML in {filename}")
