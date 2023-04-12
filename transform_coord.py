from area import area


def toKMLFolder(area):
    coorList = area["coordinates"].split(" ")
    coorList.pop()
    coorString = f"{coorList[1]},{coorList[0]},0 {coorList[7]},{coorList[6]},0 {coorList[5]},{coorList[4]},0 {coorList[3]},{coorList[2]},0 {coorList[1]},{coorList[0]},0"
    kmlFolder = f"<Folder><name>{area['code']}</name><description>Date: {area['acquisition_date']}, Satellite: {area['satellite']}, Incidence angle: {area['incidence_angle']}, Area: {area['area']}</description><Placemark><Polygon><outerBoundaryIs><LinearRing><coordinates>{coorString}</coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark><GroundOverlay><Icon><href>{area['quicklook_url']}</href></Icon><gx:LatLonQuad xmlns:gx='http://www.google.com/kml/ext/2.2'><coordinates>{coorString}</coordinates></gx:LatLonQuad></GroundOverlay></Folder>"
    return kmlFolder


def areasToKML(from_, to, areaList):
    kmlFolders = ""
    for area in areaList:
        areasKMLFolder = toKMLFolder(area)
        kmlFolders += areasKMLFolder
    kml = f"<?xml version='1.0' encoding='UTF-8'?><kml xmlns='http://www.opengis.net/kml/2.2'><Folder><name>Quicklooks: from {from_.isoformat().split('T')[0]}, to {to.isoformat().split('T')[0]}</name>{kmlFolders}</Folder></kml>"
    return kml


def transform(images):
    for image in images:
        image["area"] = area(image["geometry"])
        list_of_lists = image["geometry"]["coordinates"][0]
        coord_string = ""
        for list in list_of_lists:
            coord_string = coord_string + str(list[1]) + " " + str(list[0]) + " "
        image["coordinates"] = coord_string
    return images


def convert_to_kml(images, from_date, to_date):
    if images == None:
        return f"<?xml version='1.0' encoding='UTF-8'?><kml xmlns='http://www.opengis.net/kml/2.2'><Folder>Search yielded no results</Folder></kml>"
    images = transform(images)
    kml = areasToKML(from_date, to_date, images)
    return kml
