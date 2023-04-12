from turfpy.measurement import area
from turfpy.transformation import union
from geojson import FeatureCollection
import sys, json
from convert_to_json import convert_to_geojson


def main():
    areas_kml = sys.argv[1]
    areas_geojson = convert_to_geojson(areas_kml)
    fc = union(FeatureCollection(areas_geojson, properties={"combine": "yes"}))
    calculated_area = area(fc) / 1000000
    print(f"Площадь покрытия: {round(calculated_area, 3)} кв.км.")
    # with open("unionized.geojson", "w") as f:
    #     json.dump(fc, f)


if __name__ == "__main__":
    main()
