import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import os
from coordinator.orchestrator import TheBrain


# Protect this page
if "admin_logged_in" not in st.session_state or not st.session_state.admin_logged_in:
    st.warning("⛔ Unauthorized access. Please log in from the Home page.")
    st.stop()

st.set_page_config(page_title="🛠️ Admin Dashboard", layout="wide")
st.title("🛠️ Civic Issue Admin Dashboard")

brain = TheBrain()

# Load all pending issues
all_issues = brain.get_pending_issue()
issue_states = [brain.issue_handler.get_data(issue_id) for issue_id in all_issues]

# ---- SIDEBAR FILTERS ---- #
st.sidebar.header("🔍 Filter Issues")

# Unique stages and cities
stages = sorted(set(state["admin_stage"] for state in issue_states))
cities = sorted(
    set(state.get("metadata", {}).get("Address", {}).get("city", "Unknown") for state in issue_states)
)

# Sidebar dropdowns
selected_stage = st.sidebar.selectbox("Filter by Stage", ["All"] + stages)
selected_city = st.sidebar.selectbox("Filter by City", ["All"] + cities)

# Filter logic
filtered_issues = []
for state in issue_states:
    stage_ok = selected_stage == "All" or state["admin_stage"] == selected_stage
    city = state.get("metadata", {}).get("Address", {}).get("city", "Unknown")
    city_ok = selected_city == "All" or city == selected_city
    if stage_ok and city_ok:
        filtered_issues.append(state)

if filtered_issues:
    issue_ids = [s["issue_id"] for s in filtered_issues]
    selected_issue_id = st.selectbox("Select an Issue to Review", issue_ids)
    selected_state = next(s for s in filtered_issues if s["issue_id"] == selected_issue_id)

    st.subheader(f"🧾 Reviewing Issue: {selected_issue_id}")
    st.write(f"**Stage:** {selected_state['admin_stage']}")

    # for img_path in selected_state.get("image_paths", []):
    #     if os.path.exists(img_path):
    #         st.image(img_path, caption="Uploaded Image", width=300)
    image_paths = selected_state.get("image_paths", [])

    # Create a column for each image (up to 4 per row for layout control)
    cols = st.columns(len(image_paths))

    for idx, img_path in enumerate(image_paths):
        if os.path.exists(img_path):
            with cols[idx]:
                st.image(img_path, caption=f"Image {idx + 1}", width=300)

    stage = selected_state["admin_stage"]

    if stage == "metadata_review":
        address = selected_state.get("metadata", {}).get("Address", {})
        # issue_type = selected_state.get("issue_type", "Not specified")
        # st.write(f"**Issue Type:** {issue_type}")
        st.markdown("### 📍 Extracted Address")
        with st.form("edit_metadata"):
            issue_type=st.text_input("Issue", value=selected_state.get("issue_type", ""))
            road = st.text_input("Road", value=address.get("road", ""))
            city = st.text_input("City", value=address.get("city", ""))
            state_name = st.text_input("State", value=address.get("state", ""))
            submitted = st.form_submit_button("💾 Save Metadata")

            if submitted:
                selected_state.update({"issue_type": issue_type})
                selected_state["metadata"]["Address"].update({"road": road, "city": city, "state": state_name})
                brain.issue_handler.update_issue(selected_state)
                st.success("Metadata updated!")
                st.rerun()

        if st.button("❌ Reject this issue"):
            selected_state.update({"status": "rejected"})
            issue_id=selected_state["issue_id"]
            source_path = f"issues/active/{issue_id}.json"
            destination_path = f"issues/rejected/{issue_id}.json"
            # Move the file
            os.rename(source_path, destination_path)
            st.rerun()


    elif stage == "authority_review":
        email_info = selected_state.get("Authority_info", {}).get("Email", "Not Available")
        st.markdown("### 📬 Authority Contact")
        with st.form("edit_email"):
            email_main = st.text_input("Main Contact", value=email_info if isinstance(email_info, str) else email_info.get("Main", ""))
            submitted = st.form_submit_button("💾 Save Email Info")
            if submitted:
                selected_state["Authority_info"]["Email"] = email_main
                brain.issue_handler.update_issue(selected_state)
                st.success("Email updated!")
                st.rerun()
        if st.button("🔁 Retry Email Lookup"):
            new_email = brain.authority_mapper.get_email_data(selected_state)
            selected_state["Authority_info"]["Email"] = new_email
            brain.issue_handler.update_issue(selected_state)
            st.success("✅ Re-fetched authority email.")
            st.rerun()



    elif stage == "tweet_review":
        st.markdown("### 🐦 Generated Tweet")
        tweet_data = selected_state.get("tweet", {})
        tweet_text = tweet_data.get("text", "No tweet prepared.")
        tweet_status = tweet_data.get("status", "Unknown")
        with st.form("edit_tweet"):
            tweet_input = st.text_area("Tweet Content", value=tweet_text, height=100)
            submitted = st.form_submit_button("💾 Save Tweet")
            if submitted:
                selected_state["tweet"]["text"] = tweet_input
                brain.issue_handler.update_issue(selected_state)
                st.success("Tweet content updated!")
                time.sleep(2)
                st.rerun()
        # Show tweet status
        st.write(f"**Tweet Status:** `{tweet_status}`")
        # Add Retry Button if tweet failed
        if tweet_status == "Failed":
            if st.button("🔁 Retry Tweet"):
                tweet_result = brain.social_handler.post_issue_to_twitter(selected_state)

                # Merge only status — preserve text
                selected_state["tweet"]["status"] = tweet_result.get("status", "Failed")

                brain.issue_handler.update_issue(selected_state)

                if tweet_result.get("status") == "Posted":
                    st.success("✅ Tweet posted successfully!")
                else:
                    st.warning("⚠️ Tweet failed again.")
                time.sleep(2)
                st.rerun()

    elif stage == "complete":
        brain.issue_handler.update_issue(selected_state)
        brain.do_stage_work(selected_state["issue_id"])

        # Display errors if any
    if "errors" in selected_state and selected_state["errors"]:
        st.markdown("### ⚠️ Errors")
        for k, v in selected_state["errors"].items():
            st.error(f"{k}: {v}")


    # Approval button
    if st.button("✅ Approve this stage"):
        stage = selected_state["admin_stage"]
        selected_state["approvals"][stage] = True
        brain.issue_handler.update_issue(selected_state)
        brain.process_pending_approvals()
        st.success(f"Approved stage: {stage} and processed next step.")
        st.rerun()



    # Option to view full JSON
    with st.expander("📦 See Full Issue JSON"):
        st.json(selected_state)
else:
    st.warning("No issues match the selected filters.")


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