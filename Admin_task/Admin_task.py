class AdminTasks:

    def __init__(self):
        pass  # optional: init logging, config, etc.

    def human_review(self, state):
        issue_id = state["issue_id"]
        address = state["metadata"]["Address"]

        print("\n📋 New Issue for Review")
        print(f"Issue ID: {issue_id}")
        print(f"Location: {address.get('road')}, {address.get('city')}")
        print(f"Time: {state['metadata']['datetime']}")
        print("-" * 40)

        choice = input("Approve issue? (y/n): ").strip().lower()
        if choice == "y":
            state["review_status"] = "approved"
        else:
            state["review_status"] = "rejected"

        return state
