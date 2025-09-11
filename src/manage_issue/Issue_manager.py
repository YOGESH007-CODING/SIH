import json
import os

from src.manage_issue.state_template import Blank_state


class IssueState():
    def __init__(self):
        self.state_temp=Blank_state

    def from_blank(self, img_paths):
        new_state=self.state_temp
        new_state['image_paths']=img_paths
        return new_state

    def update_issue(self, state):
        issue_id = state['issue_id']
        metadata = state['metadata']
        os.makedirs("issues", exist_ok=True)
        file_path = os.path.join("issues/active", f"{issue_id}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=4)
        # 4. Optionally add status = "stored" to state
        state['stored'] = True
        # 5. Return updated state
        print("Issue stored or Updated")

    def load_json_as_dict(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    def get_all_active_ids(self):
        return [f.split('.')[0] for f in os.listdir("issues/active") if f.endswith(".json")]

    def get_all_completed_ids(self):
        return [f.split('.')[0] for f in os.listdir("issues/completed") if f.endswith(".json")]

    def get_data(self, issue_id):
        # file_path = os.path.join("issues/active/", f"{issue_id}.json")
        base_dir = os.path.join("issues", "active")
        # print("Current working directory:", os.getcwd())
        filename=f"{issue_id}.json"
        file_path = os.path.join(base_dir, filename)
        # print(file_path)
        return self.load_json_as_dict(file_path)



