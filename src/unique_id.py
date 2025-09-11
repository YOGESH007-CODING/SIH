import json
from datetime import datetime
import os
from filelock import FileLock, Timeout

class IssueIDGenerator:
    def __init__(self, counter_file='issue_counter.json', issues_dir="/issues/active", lock_timeout=5):
        self.counter_file = counter_file
        self.date_str = datetime.now().strftime("%Y%m%d")
        self.counter = 0
        self.issues_dir = issues_dir  # Directory to check existing issue IDs (optional)
        self.lock = FileLock(f"{self.counter_file}.lock")
        self.lock_timeout = lock_timeout
        self._load_counter()

    def _load_counter(self):
        try:
            with self.lock.acquire(timeout=self.lock_timeout):
                if os.path.exists(self.counter_file):
                    with open(self.counter_file, 'r') as f:
                        data = json.load(f)
                    if data.get('date') == self.date_str:
                        self.counter = data.get('counter', 0)
                    else:
                        self.counter = 0  # New day, reset counter
                else:
                    self.counter = 0
        except Timeout:
            print("Could not acquire lock on counter file, proceeding cautiously.")
        except Exception as e:
            print(f"Error loading counter: {e}")
            self.counter = 0

    def _save_counter(self):
        try:
            with self.lock.acquire(timeout=self.lock_timeout):
                data = {'date': self.date_str, 'counter': self.counter}
                with open(self.counter_file, 'w') as f:
                    json.dump(data, f)
        except Timeout:
            print("Could not acquire lock to save counter.")
        except Exception as e:
            print(f"Error saving counter: {e}")

    def _id_exists(self, issue_id):
        if not self.issues_dir:
            return False
        # Customize this check depending on how your issues are stored
        # For example, if issues saved as files: check if file exists
        filename = os.path.join(self.issues_dir, issue_id + ".txt")
        return os.path.exists(filename)

    def generate_id(self, prefix=None):
        # Try generating unique ID (if issues_dir given)
        for _ in range(1000):  # safety max retries
            self.counter += 1
            issue_id = f"{prefix}_{self.date_str}_{str(self.counter).zfill(3)}"
            if not self._id_exists(issue_id):
                self._save_counter()
                return issue_id
        raise RuntimeError("Failed to generate unique issue ID after 1000 attempts.")

# Usage example
if __name__ == "__main__":
    generator = IssueIDGenerator(counter_file="issue_counter.json", prefix="FR")
    new_id = generator.generate_id()
    print("New Issue ID:", new_id)
