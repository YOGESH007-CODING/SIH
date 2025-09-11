import os
import math
import json
from geopy.geocoders import Nominatim
class SimilarIssueFinder:
    def __init__(self, active_path="issues/active", completed_path="issues/completed", threshold_meters=2500):
        self.active_path = active_path
        self.completed_path = completed_path
        self.threshold = threshold_meters

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def _load_state(self, file_path):
        with open(file_path, "r") as f:
            return json.load(f)



    def get_pincode_from_coords(self, lat, lon):
        geolocator = Nominatim(user_agent="my-civic-app")
        location = geolocator.reverse((lat, lon), exactly_one=True)

        if location and location.raw.get("address"):
            return location.raw["address"].get("postcode")
        return None

    def _get_location(self, state):
        try:
            loc = state["metadata"]
            return float(loc["latitude"]), float(loc["longitude"])
        except:
            return None, None

    def check_and_group(self, new_state, external_metadata):
        if external_metadata:
            new_lat = external_metadata["latitude"]
            new_lon = external_metadata["longitude"]
        else:
            new_lat, new_lon = self._get_location(new_state)
        new_type = new_state.get("issue_type", "").strip().lower()
        new_pin = self.get_pincode_from_coords(new_lat, new_lon)

        if not new_lat or not new_lon:
            print("Location missing in new issue. Skipping similarity check.")
            return False, None



        # 1. Check Active Issues
        for file in os.listdir(self.active_path):
            path = os.path.join(self.active_path, file)
            state = self._load_state(path)
            pin1 = state.get("metadata", {}).get("Address", {}).get("postcode")


            lat, lon = self._get_location(state)
            if not lat or not lon:
                continue

            dist = self._haversine(new_lat, new_lon, lat, lon)
            issue_type_existing = state.get("issue_type", "").strip().lower()

            if dist <= self.threshold and issue_type_existing == new_type:
                print(f"Match found in active: {file}, dist={dist:.2f} meters")

                # Update existing state
                # state.setdefault("similar_count", 1)
                # simi_count=state["similar_count"]
                # state["similar_count"] = int(simi_count) + 1
                state["similar_count"] = (int(state.get("similar_count")) if state.get(
                    "similar_count") is not None else 0) + 1

                state.setdefault("similar_image_paths", [])
                for img in new_state.get("image_paths", []):
                    if img not in state["similar_image_paths"]:
                        state["similar_image_paths"].append(img)
                self._save_state(state, path)

                return True, state.get("issue_id")
            elif pin1 and new_pin and pin1 == new_pin:
                return True, state.get("issue_id")

        # 2. Check Completed Issues
        for file in os.listdir(self.completed_path):
            path = os.path.join(self.completed_path, file)
            state = self._load_state(path)
            pin1 = state.get("metadata", {}).get("Address", {}).get("postcode")

            lat, lon = self._get_location(state)
            if not lat or not lon:
                continue

            dist = self._haversine(new_lat, new_lon, lat, lon)
            issue_type_existing = state.get("issue_type", "").strip().lower()

            if dist <= self.threshold and issue_type_existing == new_type:
                print(f"Already reported in completed: {file}, dist={dist:.2f} meters")
                return True, state.get("issue_id")
            elif pin1 and new_pin and pin1 == new_pin:
                return True, state.get("issue_id")

        # No match found
        print("No similar issue found.")
        return False, None

    def _save_state(self, state, path):
        with open(path, "w") as f:
            json.dump(state, f, indent=2)
