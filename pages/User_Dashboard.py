from datetime import datetime

import streamlit as st


import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from coordinator.orchestrator import TheBrain

brain = TheBrain()
ISSUE_TYPES = ["Pothole", "Garbage", "Water Leakage", "Streetlight", "Road Damage", "Other"]

st.set_page_config(page_title="CivicSpotter", layout="centered")
from streamlit_js_eval import streamlit_js_eval, get_geolocation
st.title("🧾 Report a Civic Issue")

# Sidebar: Active and Completed Issues
st.sidebar.title("📋 Issue Tracker")
active_issues, completed_issues = brain.get_issue_lists()

st.sidebar.subheader("🟢 Active Issues")
if not active_issues:
    st.sidebar.info("No active issues yet.")
else:
    for issue in active_issues:
        st.sidebar.write(f"• {issue['id']} ({issue['type']})")

st.sidebar.subheader("✅ Completed Issues")
if not completed_issues:
    st.sidebar.info("No completed issues.")
else:
    for issue in completed_issues:
        tweet_url = issue.get("tweet_url")
        if tweet_url:
            st.sidebar.markdown(f"• [{issue['id']}]({tweet_url}) ({issue['type']})")
        else:
            st.sidebar.write(f"• {issue['id']} ({issue['type']}) - No Tweet")

# Upload mode selection
upload_mode = st.radio("📤 How would you like to upload your photo?",
                       ["📸 Take photo", "🖼️ Upload from gallery"])
if upload_mode == "📸 Take photo":
    uploaded_files = st.file_uploader("Click below to capture photo",
                                      type=["jpg", "jpeg", "png"],
                                      accept_multiple_files=True,
                                      key="camera_upload",
                                      label_visibility="collapsed")
    location = streamlit_js_eval(js_expressions=get_geolocation(), key="get_location")

    if location and location.get("coords"):
        coords = location["coords"]
        st.success("📍 Location fetched from browser:")
        st.write(f"**Latitude:** {coords['latitude']}")
        st.write(f"**Longitude:** {coords['longitude']}")
    else:
        st.warning("📍 Location not available yet. Allow location access in your browser.")
    # print(location)
else:
    uploaded_files = st.file_uploader("Upload from device",
                                      type=["jpg", "jpeg", "png"],
                                      accept_multiple_files=True,
                                      key="gallery_upload")
    location = None  # We'll rely on EXIF in brain.new_issue()

issue_type = st.selectbox("Select Issue Type", ISSUE_TYPES)

if st.button("Submit"):
    if not uploaded_files:
        st.error("Please upload at least one image.")
    else:
        os.makedirs("temp_uploads", exist_ok=True)
        image_paths = []
        for file in uploaded_files:
            save_path = f"temp_uploads/{file.name}"
            with open(save_path, "wb") as f:
                f.write(file.read())
            image_paths.append(save_path)

        # If browser GPS is available, pass it manually to override metadata fallback
        gps_metadata = None
        if upload_mode == "📸 Take photo" and location and location.get("coords"):
            coords = location["coords"]
            now = datetime.now()
            formatted_datetime = now.strftime("%Y:%m:%d %H:%M:%S")
            gps_metadata = {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "datetime": formatted_datetime # brain can still use EXIF timestamp if available
            }

        # Submit issue
        issue_id, merge_status, metadata = brain.new_issue(image_paths, issue_type, external_metadata=gps_metadata)

        # Handle response
        if not issue_id:
            st.error("❌ Could not extract metadata from the image choose the GPS feature.")
        else:
            if merge_status:
                st.success(f"✅ Issue merged with existing active issue: {issue_id}")
            else:
                st.success("✅ New issue submitted successfully!")
            st.code(issue_id, language="text")

            # Show map if location found
            try:
                lat = float(metadata["latitude"])
                lon = float(metadata["longitude"])
                st.subheader("📍 Issue Location")
                st.map({"lat": [lat], "lon": [lon]})
            except Exception as e:
                st.warning("⚠️ Could not load location on map.")
                st.text(f"Error: {e}")


# # Footer

# st.markdown("---", unsafe_allow_html=True)

# st.markdown("""
# <div style="margin: 2rem 0; text-align: center;">
#     <a href="https://bolt.new" target="_blank" style="text-decoration: none;">
#         <img src="https://img.shields.io/badge/Built%20with-Bolt.new-FF6B6B?style=for-the-badge&logo=thunderstorm&logoColor=white" 
#              alt="Built with Bolt.new" 
#              style="border-radius: 8px; box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3); height: 40px;">
#     </a>
# </div>

# <p style="margin-top: 1rem; font-size: 0.9rem; color: #888; font-style: italic; text-align: center;">
#     ⚡ Powered by AI • 🎯 Built for Impact • 🚀 Deployed with Bolt
# </p>
# """, unsafe_allow_html=True)