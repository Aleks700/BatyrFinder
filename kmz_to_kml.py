import os
from zipfile import ZipFile


def unzip_kmz(file):
    filename = file.split(".")[0]
    os.rename(file, filename + ".zip")
    file = filename + ".zip"
    folder = ""
    if "/" in file:
        list = file.split("/")
        list.pop()
        folder = "/".join(list)
    # loading the temp.zip and creating a zip object
    with ZipFile(file, "r") as archive:

        # Extracting specific file in the zip
        # into a specific location.
        archive.extract("doc.kml", path=folder)
        os.rename(folder + "/doc.kml", filename + ".kml")
    archive.close()
    os.remove(file)
