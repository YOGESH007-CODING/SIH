# status_map.py
"""
A Python script to create an interactive map with colored markers
based on the status of GPS coordinates.
"""
import folium
from folium.plugins import MarkerCluster
import warnings
import numpy as np

def create_status_map(data, output_html="map.html", start_location=None, start_zoom=6, cluster=True, show_legend=True, color_map=None):
    """
    Creates an interactive map showing user-supplied GPS coordinates as colored markers.

    Args:
        data (list of dicts): A list of dictionaries, each with keys
            'latitude', 'longitude', 'status', and optional 'label' or 'popup'.
        output_html (str): The filename for the saved HTML map.
        start_location (list, optional): The initial center of the map [latitude, longitude].
            Defaults to the mean of all coordinates.
        start_zoom (int): The initial zoom level of the map.
        cluster (bool): If True, markers will be clustered for performance.
        show_legend (bool): If True, a custom HTML legend will be added to the map.
        color_map (dict, optional): A dictionary to override the default status-to-color mapping.
    
    Returns:
        folium.Map: The Folium map object.
    """
    default_color_map = {
        'completed': 'green',
        'in progress': 'orange',
        'in_progress': 'orange',
        'progress': 'orange',
        'rejected': 'red'
    }
    status_to_color = color_map if color_map is not None else default_color_map

    valid_points = []
    for record in data:
        lat = record.get("latitude")
        lon = record.get("longitude")
        
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            warnings.warn(f"Invalid coordinates skipped: ({lat}, {lon})")
            continue
        valid_points.append(record)

    if not valid_points:
        warnings.warn("No valid coordinates found. Cannot create map.")
        return None

    # Handle large datasets
    if len(valid_points) > 2000:
        warnings.warn("Large dataset detected. Consider using clustering for better performance.")
    
    # Calculate start location if not provided
    if start_location is None:
        lats = [d['latitude'] for d in valid_points]
        lons = [d['longitude'] for d in valid_points]
        center_lat = np.mean(lats)
        center_lon = np.mean(lons)
        start_location = [center_lat, center_lon]

    m = folium.Map(location=start_location, zoom_start=start_zoom, tiles="OpenStreetMap")
    folium.TileLayer("CartoDB Positron").add_to(m) 

    if cluster:
        marker_cluster = MarkerCluster().add_to(m)
        group = marker_cluster
    else:
        group = m

    for point in valid_points:
        lat, lon = point["latitude"], point["longitude"]
        status = point["status"].lower().replace(" ", "_")
        label = point.get("label", "")
        popup_text = point.get("popup", "")

        color = status_to_color.get(status, 'blue')
        
        # Build the popup text
        if not popup_text:
            popup_text = f"<b>Status:</b> {status.replace('_', ' ').title()}<br>"
            popup_text += f"<b>Coordinates:</b> ({lat:.4f}, {lon:.4f})<br>"
            if label:
                popup_text += f"<b>Label:</b> {label}<br>"
        
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=popup_text
        ).add_to(group)

    # Add custom legend
    if show_legend:
        legend_html = """
             <div style="position: fixed; 
                         bottom: 50px; left: 50px; width: 150px; height: 120px; 
                         border:2px solid grey; z-index:9999; font-size:14px;
                         background-color: white; opacity:0.9;">
               &nbsp; <b>Status Legend</b> <br>
               &nbsp; <i style="background:green; color:green; padding: 2px; border:1px solid grey;">&nbsp;</i> Completed <br>
               &nbsp; <i style="background:orange; color:orange; padding: 2px; border:1px solid grey;">&nbsp;</i> In Progress <br>
               &nbsp; <i style="background:red; color:red; padding: 2px; border:1px solid grey;">&nbsp;</i> Rejected <br>
               &nbsp; <i style="background:blue; color:blue; padding: 2px; border:1px solid grey;">&nbsp;</i> Unknown <br>
             </div>
             """
        m.get_root().html.add_child(folium.Element(legend_html))

    folium.LayerControl().add_to(m)
    m.save(output_html)
    print(f"Map saved to {output_html}")
    return m

if __name__ == "__main__":
    sample_data = [
        {"latitude": 28.6139, "longitude": 77.2090, "status": "completed", "label": "Site A - Delhi"},
        {"latitude": 19.0760, "longitude": 72.8777, "status": "in progress", "label": "Site B - Mumbai"},
        {"latitude": 13.0827, "longitude": 80.2707, "status": "rejected", "label": "Site C - Chennai"},
        {"latitude": 12.9716, "longitude": 77.5946, "status": "Completed", "label": "Site D - Bangalore"},
        {"latitude": 22.5726, "longitude": 88.3639, "status": "in_progress", "label": "Site E - Kolkata"},
        {"latitude": 91.0, "longitude": 181.0, "status": "completed", "label": "Invalid Coords - should be skipped"},
        {"latitude": 34.0522, "longitude": -118.2437, "status": "pending", "label": "Unknown Status - LA"}
    ]
    
    # Create and save the map
    create_status_map(sample_data)