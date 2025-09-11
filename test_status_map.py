# test_status_map.py
import pytest
import os
import folium
from status_map import create_status_map

@pytest.fixture
def sample_data():
    return [
        {"latitude": 28.6139, "longitude": 77.2090, "status": "completed", "label": "Site A"},
        {"latitude": 19.0760, "longitude": 72.8777, "status": "in_progress", "label": "Site B"},
        {"latitude": 13.0827, "longitude": 80.2707, "status": "rejected", "label": "Site C"},
        {"latitude": 34.0522, "longitude": -118.2437, "status": "pending", "label": "Site D"},
        {"latitude": 91.0, "longitude": 181.0, "status": "completed", "label": "Invalid Coords - skipped"}
    ]

def test_color_mapping(sample_data):
    """Test that markers are colored correctly based on status."""
    m = create_status_map(sample_data, output_html="test_colors.html")
    assert isinstance(m, folium.Map)
    
    # Access map features to check colors. This is a bit advanced, so we'll check the HTML source
    with open("test_colors.html", "r") as f:
        html_content = f.read()

    assert 'color:green' in html_content
    assert 'color:orange' in html_content
    assert 'color:red' in html_content
    assert 'color:blue' in html_content
    os.remove("test_colors.html")

def test_invalid_coordinates_skipped(sample_data, capsys):
    """Test that invalid coordinates are skipped with a warning."""
    create_status_map(sample_data, output_html="test_invalid.html")
    captured = capsys.readouterr()
    assert "Invalid coordinates skipped" in captured.err
    os.remove("test_invalid.html")

def test_html_file_creation(sample_data):
    """Test that the output HTML file is created."""
    output_filename = "test_output.html"
    create_status_map(sample_data, output_html=output_filename)
    assert os.path.exists(output_filename)
    os.remove(output_filename)