import exifread
from geopy.geocoders import Nominatim

def get_decimal_from_dms(dms, ref):
    degrees = float(dms[0].num) / dms[0].den
    minutes = float(dms[1].num) / dms[1].den
    seconds = float(dms[2].num) / dms[2].den
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def format_address_dict(address):
    formatted = {}
    for key in [
        "house_number", "road", "neighbourhood", "suburb", "county",
        "state", "postcode", "country", "country_code","ward"
    ]:
        if key in address:
            formatted[key] = address[key]

    for city_key in ["city", "town", "village"]:
        if city_key in address:
            formatted["city"] = address[city_key]
            break
    return formatted

class MetadataExtractor:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="my-camera-app")

    def extract_metadata(self, image_source, external_metadata=None):
        # image_path=state["image_path"]
        with open(image_source, 'rb') as f:
            tags = exifread.process_file(f)
        try:
            if external_metadata:
                latitude = external_metadata["latitude"]
                longitude = external_metadata["longitude"]
                datetime = external_metadata["datetime"]
            else:
                lat = tags['GPS GPSLatitude']
                lat_ref = tags['GPS GPSLatitudeRef'].printable
                lon = tags['GPS GPSLongitude']
                lon_ref = tags['GPS GPSLongitudeRef'].printable

                latitude = get_decimal_from_dms(lat.values, lat_ref)
                longitude = get_decimal_from_dms(lon.values, lon_ref)

                datetime = str(tags['EXIF DateTimeOriginal'])

            raw_address = self.geolocator.reverse(
                (latitude, longitude), language='en', addressdetails=True, timeout=10
            ).raw.get("address", {})

            address = format_address_dict(raw_address)


            return {
                'latitude': latitude,
                'longitude': longitude,
                'datetime': datetime,
                'Address': address
            }
        except:
            print("No metadata found in the photo")
            return {}


if __name__ == "__main__":
    image_path = "E:/CivicSpotter/test/photo_extractor/test_data/test_photo.jpg"
    extractor = MetadataExtractor()
    info = extractor.extract_metadata(image_path)
    print("Metadata Extracted:")
    print(info)
