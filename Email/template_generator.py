def Email_template(state):
    issue_id=state["issue_id"]
    issue_type = state["issue_type"]
    Address=state["metadata"]["Address"]
    similar_issue=state["similar_count"]
    Subject=f"Civic Issue Report – {issue_id} – {Address['city']}"
    Body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6;">
        <p>Dear <strong>sir</strong>,</p>

        <p>
          We are reaching out to bring a civic issue to your attention. The report was submitted by a citizen through the <strong>CivicSpotter</strong> platform.
        </p>

        <h3 style="margin-top: 20px;">📝 Issue Details</h3>
        <ul>
          <li><strong>🔹 Issue ID:</strong> {issue_id}</li>
          <li><strong>🔹 Issue type:</strong> {issue_type}</li>
          <li><strong>🔹 Similar issue reported nearby:</strong> {similar_issue}</li>
          <li><strong>📍 Location:</strong> {Address.get('road', 'N/A')}, {Address.get('suburb', 'N/A')}, {Address.get('city', 'N/A')}, {Address.get('postcode', 'N/A')}, {Address.get('country', 'N/A')}</li>
          <li><strong>📅 Date Reported:</strong> {state['metadata'].get('datetime', 'Unknown')}</li>
          <li><strong>🌐 Coordinates:</strong> Latitude {state['metadata'].get('latitude', 'N/A')}, Longitude {state['metadata'].get('longitude', 'N/A')}</li>
        </ul>

        <p>
          The issue was identified through a geotagged image submission. We kindly request you to review and initiate appropriate action to resolve this matter.
        </p>

        <p style="color: #b30000; font-weight: bold;">
          ⚠️ Please note: If this issue remains unaddressed beyond the expected timeframe, it may be escalated to higher authorities.
        </p>

        <p>
          We appreciate your prompt attention to this civic concern and thank you for your continued service to the community.
        </p>

        <p>
          Sincerely,<br>
          <strong>CivicSpotter System</strong><br>
          
        </p>

        <hr style="margin-top: 30px;">

        </body>
    </html>
    """

    return Subject, Body
