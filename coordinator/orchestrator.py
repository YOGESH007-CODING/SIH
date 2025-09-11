import json
import os
from Admin_task.Admin_task import AdminTasks
from Email.notifier import Email_notifier
from Social_platforms.twitter import Social_Handles
from authority_finder.get_authority import Authority_Finder
from src.manage_issue.Issue_manager import IssueState
from src.manage_issue.Similar_issue_finder import SimilarIssueFinder
from src.photo_extractor import MetadataExtractor
from src.unique_id import IssueIDGenerator
from geopy.distance import geodesic

class TheBrain():
    def __init__(self):
        self.issue_handler=IssueState()
        self.meta_extract=MetadataExtractor()
        self.issue_id=IssueIDGenerator(counter_file="../issue_counter.json")
        self.authority_mapper=Authority_Finder()
        self.Admin_work=AdminTasks()
        self.mailer=Email_notifier()
        self.similar_issue_finder=SimilarIssueFinder()
        self.social_handler=Social_Handles()
        self.next_stage_map = {
            "metadata_review": "authority_review",
            "authority_review": "tweet_review",
            "tweet_review": "complete"}

    def get_issue_lists(self):
        active_dir = "issues/active"
        completed_dir = "issues/completed"
        active_list = []
        completed_list = []

        for file in os.listdir(active_dir):
            if file.endswith(".json"):
                path = os.path.join(active_dir, file)
                with open(path, "r") as f:
                    state = json.load(f)
                active_list.append({
                    "id": state.get("issue_id", file.replace(".json", "")),
                    "type": state.get("issue_type", "Unknown"),
                })

        for file in os.listdir(completed_dir):
            if file.endswith(".json"):
                path = os.path.join(completed_dir, file)
                with open(path, "r") as f:
                    state = json.load(f)
                completed_list.append({
                    "id": state.get("issue_id", file.replace(".json", "")),
                    "type": state.get("issue_type", "Unknown"),
                    "tweet_url": state.get("tweet", {}).get("url", None)
                })

        return active_list, completed_list

    def is_similar_location(issue1, issue2, threshold_m=500):
        try:
            lat1 = float(issue1 ["latitude"])
            lon1 = float(issue1 ["longitude"])
            lat2 = float(issue2 ["latitude"])
            lon2 = float(issue2 ["longitude"])

            distance = geodesic((lat1, lon1), (lat2, lon2)).meters
            return distance < threshold_m
        except (KeyError, TypeError, ValueError):
            return False

    def new_issue(self, image_paths, issue_type, external_metadata):
        new_state = self.issue_handler.from_blank(image_paths)
        metadata = self.meta_extract.extract_metadata(image_paths[0], external_metadata)
        new_state['metadata'] = metadata
        new_state['issue_type'] = issue_type

        # Check for similar issues using SimilarIssueFinder
        print("Checking for similar issues...")
        found, matched_id = self.similar_issue_finder.check_and_group(new_state, external_metadata)
        print("Result of similarity check:", found, matched_id)


        if found:
            return matched_id, True, metadata

        # Generate new issue_id
        try:
            city = metadata['Address']['city']
        except:
            return None, False, None
        issue_id = self.issue_id.generate_id(city)
        new_state['issue_id'] = issue_id

        # Save new/merged issue
        self.issue_handler.update_issue(new_state)

        return issue_id, False, metadata

    def get_pending_issue(self):
        issues=os.listdir("issues/active")
        admin_data=[]
        for issue in issues:
            issue_id=issue.split('.')[0]
            state=self.issue_handler.get_data(issue_id)
            if state['admin_stage'] !="complete":
                admin_data.append(issue_id)
        return admin_data

    def process_pending_approvals(self):
        issues=self.get_pending_issue()
        for issue in issues:
            state = self.issue_handler.get_data(issue)
            current_stage = state["admin_stage"]
            if state["approvals"].get(current_stage) is True:
                self.do_stage_work(issue)

    def do_stage_work(self, issue_id):
        state = self.issue_handler.get_data(issue_id)
        current_stage = state["admin_stage"]
        if state["approvals"].get(current_stage) is True:
            if current_stage == "metadata_review":
                Authority_emails=self.authority_mapper.get_email_data(state)
                state['Authority_info']['Email']=Authority_emails
                state["admin_stage"]=self.next_stage_map["metadata_review"]
                self.issue_handler.update_issue(state)
            elif current_stage == "authority_review":
                # email_status=self.mailer.send_mail(state)
                # state['email']=email_status
                # state["admin_stage"] = self.next_stage_map["authority_review"]
                # tweet_text=self.social_handler.build_tweet_text(state)
                # state['tweet']['text']=tweet_text
                # self.issue_handler.update_issue(state)
                email_status = self.mailer.send_mail(state)
                if not email_status:
                    state["errors"]["email"] = "Email sending failed."
                    self.issue_handler.update_issue(state)
                    return  # Don't proceed if email fails

                state["email"] = email_status
                tweet_text = self.social_handler.build_tweet_text(state)
                if not tweet_text:
                    state["errors"]["tweet_gen"] = "Tweet generation failed."
                    self.issue_handler.update_issue(state)
                    return

                state['tweet'] = {"text": tweet_text}
                state["admin_stage"] = self.next_stage_map[current_stage]
                self.issue_handler.update_issue(state)

            elif current_stage == "tweet_review":
                # tweet_status=self.social_handler.post_issue_to_twitter(state)
                # state['tweet']=tweet_status
                # state["admin_stage"] = self.next_stage_map["tweet_review"]
                # self.issue_handler.update_issue(state)
                tweet_status = self.social_handler.post_issue_to_twitter(state)
                if not tweet_status:
                    state["errors"]["tweet_post"] = "Tweet failed to post."
                    self.issue_handler.update_issue(state)
                    return
                state['tweet']=tweet_status
                if tweet_status['status']=="Failed":
                    state["admin_stage"]="tweet_review"
                    state["approvals"]["tweet_review"]=False
                else:
                    state["admin_stage"] = self.next_stage_map["tweet_review"]
                    source_path = f"issues/active/{issue_id}.json"
                    destination_path = f"issues/completed/{issue_id}.json"
                    # Move the file
                    os.rename(source_path, destination_path)

                # self.issue_handler.update_issue(state)
                # self.do_stage_work(issue_id)
                # Workaround do it manually later will change

            # elif current_stage == "complete":
            #     source_path = f"issues/active/{issue_id}.json"
            #     destination_path = f"issues/completed/{issue_id}.json"
            #     # Move the file
            #     os.rename(source_path, destination_path)
            else:
                pass

















