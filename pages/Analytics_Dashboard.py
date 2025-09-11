import streamlit as st
import json
import os
import plotly.express as px

from datetime import datetime
import pandas as pd

st.set_page_config(page_title="📊 Analytics Dashboard", layout="wide")
st.title("📊 CivicSpotter Analytics Dashboard")


# Load all issues for analytics
def load_all_issues():
    issues = []
    for folder in ["issues/active", "issues/completed"]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.endswith(".json"):
                    with open(os.path.join(folder, file), "r") as f:
                        issue = json.load(f)
                        issue["status"] = "active" if folder.endswith("active") else "completed"
                        issues.append(issue)
    return issues


issues = load_all_issues()

if not issues:
    st.warning("No issues found for analytics.")
    st.stop()

# Convert to DataFrame for easier analysis
df_data = []
for issue in issues:
    try:
        df_data.append({
            "id": issue.get("issue_id", "unknown"),
            "type": issue.get("issue_type", "Unknown"),
            "city": issue.get("metadata", {}).get("Address", {}).get("city", "Unknown"),
            "state": issue.get("metadata", {}).get("Address", {}).get("state", "Unknown"),
            "status": issue.get("status", "unknown"),
            "similar_count": issue.get("similar_count", 0),
            "latitude": float(issue.get("metadata", {}).get("latitude", 0)),
            "longitude": float(issue.get("metadata", {}).get("longitude", 0)),
            "datetime": issue.get("metadata", {}).get("datetime", "2025:01:01 00:00:00")
        })
    except:
        continue

df = pd.DataFrame(df_data)

# Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Issues", len(df))

with col2:
    active_count = len(df[df["status"] == "active"])
    st.metric("Active Issues", active_count)

with col3:
    completed_count = len(df[df["status"] == "completed"])
    st.metric("Completed Issues", completed_count)

with col4:
    avg_similar = df["similar_count"].mean()
    st.metric("Avg Similar Reports", f"{avg_similar:.1f}")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Issues by Type")
    type_counts = df["type"].value_counts()
    fig_pie = px.pie(values=type_counts.values, names=type_counts.index,
                     title="Distribution of Issue Types")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("🏙️ Issues by City")
    city_counts = df["city"].value_counts().head(10)
    fig_bar = px.bar(x=city_counts.index, y=city_counts.values,
                     title="Top 10 Cities by Issue Count",
                     labels={"x": "City", "y": "Number of Issues"})
    # ✅ FIXED: Use update_layout instead of update_xaxis/update_yaxis
    fig_bar.update_layout(
        xaxis_title="City",
        yaxis_title="Number of Issues"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Issue Status Distribution")
    status_counts = df["status"].value_counts()
    fig_status = px.bar(x=status_counts.index, y=status_counts.values,
                        title="Active vs Completed Issues",
                        color=status_counts.index,
                        color_discrete_map={"active": "#ff6b6b", "completed": "#51cf66"},
                        labels={"x": "Status", "y": "Number of Issues"})
    fig_status.update_layout(
        xaxis_title="Status",
        yaxis_title="Number of Issues"
    )
    st.plotly_chart(fig_status, use_container_width=True)

with col2:
    st.subheader("🔄 Similar Issue Clustering")
    similar_data = df[df["similar_count"] > 0]
    if not similar_data.empty:
        fig_similar = px.histogram(similar_data, x="similar_count",
                                   title="Distribution of Similar Issue Counts",
                                   nbins=10,
                                   labels={"similar_count": "Number of Similar Reports", "count": "Frequency"})
        fig_similar.update_layout(
            xaxis_title="Number of Similar Reports",
            yaxis_title="Frequency"
        )
        st.plotly_chart(fig_similar, use_container_width=True)
    else:
        st.info("No similar issues detected yet.")

# Map Visualization
st.subheader("🗺️ Geographic Distribution of Issues")
if not df.empty and df["latitude"].sum() != 0:
    # Filter out invalid coordinates
    map_df = df[(df["latitude"] != 0) & (df["longitude"] != 0)]

    if not map_df.empty:
        fig_map = px.scatter_map(
            map_df,
            lat="latitude",
            lon="longitude",
            color="type",
            size="similar_count",
            hover_data=["id", "city", "status"],
            map_style="open-street-map",
            title="Issue Locations",
            zoom=5
        )
        fig_map.update_layout(height=500)
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("No valid coordinates found for mapping.")
else:
    st.info("No location data available for mapping.")

# Time Series Analysis (if we have datetime data)
st.subheader("📅 Issue Trends Over Time")
try:
    # Convert datetime strings to pandas datetime
    df['parsed_datetime'] = pd.to_datetime(df['datetime'], format='%Y:%m:%d %H:%M:%S', errors='coerce')
    df_with_dates = df.dropna(subset=['parsed_datetime'])

    if not df_with_dates.empty:
        # Group by date
        daily_counts = df_with_dates.groupby(df_with_dates['parsed_datetime'].dt.date).size().reset_index()
        daily_counts.columns = ['date', 'count']

        fig_timeline = px.line(daily_counts, x='date', y='count',
                               title="Issues Reported Over Time",
                               labels={"date": "Date", "count": "Number of Issues"})
        fig_timeline.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Issues"
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("No valid datetime data available for trend analysis.")
except Exception as e:
    st.info("Unable to parse datetime data for trend analysis.")

# Issue Type by City Heatmap
st.subheader("🔥 Issue Type Distribution by City")
if len(df) > 0:
    # Create a pivot table for heatmap
    heatmap_data = df.groupby(['city', 'type']).size().unstack(fill_value=0)

    if not heatmap_data.empty:
        fig_heatmap = px.imshow(
            heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            title="Issue Types by City",
            labels={"x": "Issue Type", "y": "City", "color": "Count"},
            aspect="auto"
        )
        fig_heatmap.update_layout(height=400)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.info("Not enough data for heatmap visualization.")

# Recent Activity
st.subheader("📅 Recent Activity")
recent_issues = sorted(issues, key=lambda x: x.get("metadata", {}).get("datetime", ""), reverse=True)[:5]

for issue in recent_issues:
    with st.expander(f"🆔 {issue.get('issue_id', 'Unknown')} - {issue.get('issue_type', 'Unknown')}"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Location:** {issue.get('metadata', {}).get('Address', {}).get('city', 'Unknown')}")
        with col2:
            st.write(f"**Status:** {issue.get('status', 'Unknown')}")
        with col3:
            st.write(f"**Similar Reports:** {issue.get('similar_count', 0)}")

# Summary Statistics
st.subheader("📊 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Most Common Issue", df["type"].mode().iloc[0] if not df.empty else "N/A")

with col2:
    st.metric("Most Active City", df["city"].mode().iloc[0] if not df.empty else "N/A")

with col3:
    resolution_rate = (completed_count / len(df) * 100) if len(df) > 0 else 0
    st.metric("Resolution Rate", f"{resolution_rate:.1f}%")

with col4:
    total_similar = df["similar_count"].sum()
    st.metric("Total Similar Reports", int(total_similar))

# Export Data
st.subheader("📤 Export Data")
if st.button("Download Issues as CSV"):
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"civicspotter_issues_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )



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