import datetime
from search import search_images
from transform_coord import convert_to_kml
import argparse
from convert_to_json import convert_to_geojson
from kmz_to_kml import unzip_kmz

parser = argparse.ArgumentParser(
    prog="KML Generator By AOI", description="It generates KML based on AOI"
)

parser.add_argument("kml")
parser.add_argument("-f", "--date_from")
parser.add_argument("-t", "--date_to", required=False)
parser.add_argument("-r", "--angle", required=False)
parser.add_argument("-o", "--output", required=False)
parsed_args = parser.parse_args()


def form_request(polygons, from_date, to_date, angle_range):
    body = {
        "polygons": polygons,
        "from_date": f"{from_date}T00:00:00+00:00",
        "to_date": f"{to_date}T23:59:59+00:00",
        "include_kazeosat1": True,
        "include_kazeosat2": False,
        "cloud_coverage_max": 100,
        "cloud_coverage_include_null": True,
        "incidence_angle_from": angle_range[0] if angle_range[0] is not None else 0,
        "incidence_angle_to": angle_range[1] if angle_range[1] is not None else 360,
        "incidence_angle_include_null": True,
    }
    return body


def get_angle_query():
    if parsed_args.angle is not None:
        angle_range = parsed_args.angle.split(":")
        return angle_range
    return None


def main():
    from_date = datetime.datetime.strptime(parsed_args.date_from, "%Y-%m-%d").date()
    try:
        to_date = datetime.datetime.strptime(parsed_args.date_to, "%Y-%m-%d").date()
    except:
        to_date = datetime.datetime.now().date()

    angle_range = get_angle_query()
    if parsed_args.kml.endswith(".kmz"):
        unzip_kmz(parsed_args.kml)
        parsed_args.kml = parsed_args.kml.split(".")[0] + ".kml"
    # convert kml to geojson
    geojson_data = convert_to_geojson(parsed_args.kml)

    # prepare data for searching
    body = form_request(geojson_data, from_date, to_date, angle_range)

    # feed json to api, get answers
    images = search_images(body)

    # transform coordinates and convert to kml
    kml = convert_to_kml(images, from_date, to_date)

    # create file
    resulting_file = "results/"
    if parsed_args.output == None:
        filename = parsed_args.kml.split("/")[1]
        resulting_file += "Покрытия " + filename
    else:
        resulting_file += parsed_args.output + ".kml"
    with open(resulting_file, "w") as file:
        file.write(kml)
        if images != None:
            print(f"Успешный поиск!\n Количество найденных снимков: {len(images)}")
        else:
            print("По вашему запросу снимки не найдены.")


if __name__ == "__main__":
    main()
