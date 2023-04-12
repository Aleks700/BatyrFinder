import xml.etree.ElementTree as ET
import json


def convert_to_geojson(filename):
    # parse the KML file
    tree = ET.parse(filename)
    root = tree.getroot()
    root.tag = root.tag.replace("}kml", "}")

    # create a GeoJSON feature collection
    feature_collection = {"type": "FeatureCollection", "features": []}
    # if no folder in root, then, else
    if root.find(f".//{root.tag}Folder") != None:
        for folder in root.iter(f"{root.tag}Folder"):
            for placemark in folder.iter(f"{root.tag}Placemark"):
                properties = {}
                for data in placemark.iter(f"{root.tag}SimpleData"):
                    properties[data.attrib["name"]] = data.text
                multigeom = ""
                if placemark.find(f"{root.tag}MultiGeometry/") != None:
                    multigeom = f"{root.tag}MultiGeometry/"
                coords = placemark.find(
                    multigeom
                    + f"{root.tag}Polygon/{root.tag}outerBoundaryIs/{root.tag}LinearRing/{root.tag}coordinates"
                ).text
                coords = [
                    [float(x) for x in coord.split(",")[:2]]
                    for coord in coords.strip().split()
                ]

                feature = {
                    "type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [coords]},
                    "properties": properties,
                }
                feature_collection["features"].append(feature)

    else:
        for placemark in root.iter(f"{root.tag}Placemark"):
            properties = {}
            for data in placemark.iter(f"{root.tag}SimpleData"):
                properties[data.attrib["name"]] = data.text
            multigeom = ""
            if placemark.find(f"{root.tag}MultiGeometry/") != None:
                multigeom = f"{root.tag}MultiGeometry/"
            coords = placemark.find(
                multigeom
                + f"{root.tag}Polygon/{root.tag}outerBoundaryIs/{root.tag}LinearRing/{root.tag}coordinates"
            ).text
            coords = [
                [float(x) for x in coord.split(",")[:2]]
                for coord in coords.strip().split()
            ]

            feature = {
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": [coords]},
                "properties": properties,
            }
            feature_collection["features"].append(feature)

    # write the GeoJSON file
    with open("converted_kml.geojson", "w") as f:
        json.dump(feature_collection, f)

    return feature_collection
