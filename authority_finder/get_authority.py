import os
import google.generativeai as genai
from authority_finder.tools.tavily_search import TavilySearchTool
from authority_finder.tools.web_crawler import WebCrawler
from dotenv import load_dotenv


class Authority_Finder():
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

        # Initialize tools
        self.search_tool = TavilySearchTool()



    def generate_search_queries(self, state, num_queries=5):
        Metadata = state['metadata']
        address = Metadata['Address']
        neighbourhood=address.get("neighbourhood","Unknown neighbourhood")
        suburb = address.get("suburb", "Unknown suburb")
        ward = address.get("ward", "Unknown ward")
        State = address.get("State", "Unknown State")
        road = address.get("road", "Unknown road")
        city = address.get("city", "Unknown city")
        country = address.get("country", "Unknown country")

        prompt = f"""
                You are assisting in identifying the correct civic authority responsible for resolving a public infrastructure issue based on the given location details.

                🗺️ Location Details:
                Road = "{road}", Neighbourhood = "{neighbourhood}", Suburb = "{suburb}", Ward = "{ward}", City = "{city}", State = "{State}", Country = "{country}"
                📌 Reported Issue: Broken road

                Generate {num_queries} **realistic Google-style search queries** that a local resident might enter to find:
                - The responsible government department or civic body
                - Official complaint registration pages or helpline numbers
                - Contact details such as emails or links to authority websites

                Each query should:
                1. Sound like a natural and practical Google search phrase
                2. Include helpful keywords like: complaint, register, contact, municipal, department, authority, road repair, etc.
                3. Be tailored to locate **official or authoritative sources** (e.g., domains ending in `.gov.in`, `.nic.in`, `.org`, or local government websites)

                Return only a Python list of strings in the following format:
                ["road repair complaint contact MCD Delhi", "how to report pothole BBMP Bangalore", ...]
                """

        response = self.model.generate_content(prompt)

        try:
            # Extract the list of queries from the response
            response_text = response.text
            # Clean up the response to extract just the list
            if "[" in response_text and "]" in response_text:
                queries_str = response_text[response_text.find("["):response_text.rfind("]") + 1]
                # Convert string representation of list to actual list
                queries = eval(queries_str)
                return queries[:num_queries]  # Ensure we have the right number
            else:
                # Fallback if parsing fails
                lines = response_text.strip().split("\n")
                queries = [line.strip().strip('"\'') for line in lines if line.strip()]
                return queries[:num_queries]
        except Exception as e:
            print(f"Error parsing queries: {e}")

    def extract_relevant_info(self, queries):
        content_blocks = []

        for query in queries:
            sources = self.search_tool.get_sources(query)  # <— cleaner than raw .search()
            for src in sources:
                content_blocks.append(src["content"])


        return content_blocks

    def find_mail(self, content, issue_type):

        prompt = f"""
                Extract the most likely **official email addresses** from the following text.
                The emails should belong to a **civic authority, municipal department, or government contact** responsible for the reported issue.
                Make sure that person is responsible for {issue_type} issue.

                If multiple relevant emails are found, categorize them clearly as:
                - Main: Primary contact to send the email to
                - CC: Secondary contact to be copied
                - Higher Authority: Escalation contact (if available)

                ✅ Only consider **valid email addresses**
                ❌ Do NOT return social media handles or unrelated personal contacts
                ❌ If no official email is found, return "None"

                Use the following format in your final output:
                Main: <main email>
                CC: <cc email>
                Higher Authority: <higher authority email>

                Text:
                \"\"\" 
                {content} 
                \"\"\"

                Return the categorized list exactly in the format shown. If none are found, return "None".
                """

        response = self.model.generate_content(prompt)
        return response.text

    def extract_email_dict(self, text):
        result = {}
        lines = text.split('\n')
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip()] = value.strip()
        print(result)
        return result


    def get_email_data(self, state):
        # print("\n🧠 Generating search queries...")
        queries = self.generate_search_queries(state, num_queries=5)
        # pprint(queries)

        print("\n🔍 Extracting content using Tavily...")
        pages = self.extract_relevant_info(queries)

        # If your WebCrawler is working correctly and source['content'] is text
        combined_content = "\n\n".join(pages)  # assuming list of strings
        issue_type=state["issue_type"]
        print("\n📬 Finding email from content...")
        mail_string=self.find_mail(combined_content, issue_type)
        return self.extract_email_dict(mail_string)






if __name__ == "__main__":
    from pprint import pprint

    agent = Authority_Finder()

    # 👇 Dummy input state to simulate a photo having this metadata
    test_state = {
        "metadata": {
            "Address": {
                "road": "Hisar Road",
                "neighbourhood": "NIT 5",
                "suburb": "New Industrial Township",
                "ward": "Ward 22",
                "city": "Faridabad",
                "state": "Haryana",
                "country": "India"
            }
        }
    }
    mails=agent.get_email_data(test_state)
    print(mails)



