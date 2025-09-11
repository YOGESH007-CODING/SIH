
# 🏙️ FixMyCity

**A Smart Civic Issue Reporting & Management Platform**

FixMyCity is an intelligent crowdsourced platform that empowers citizens to report local infrastructure issues through simple photo uploads, providing administrators with powerful tools to manage, track, and resolve these issues efficiently. Every small fix makes a big difference.

## 🌟 Key Features

### 👥 For Citizens

  - **📸 Photo-Based Reporting**: Upload photos directly from your camera or gallery.
  - **🗺️ Automatic Location Detection**: Use GPS to automatically get location data from photos or your browser.
  - **🔍 Issue Tracking**: Track the progress of your submitted issues with a unique ID.
  - **📱 Mobile-Friendly Interface**: A responsive design that works on any device.
  - **🤝 Smart Duplicate Detection**: The platform automatically groups similar, nearby issues to prevent redundancy.

### 🛠️ For Administrators

  - **📋 Comprehensive Dashboard**: Review and manage all reported issues from a single, centralized dashboard.
  - **✅ Multi-Stage Approval Process**: A clear workflow from metadata verification to authority contact and social media approval.
  - **📧 Automated Email Generation**: Smartly discovers and composes emails to the correct authority contacts.
  - **🐦 Social Media Integration**: Automatically generate and post tweets to raise awareness and amplify issues.
  - **🔍 Advanced Filtering**: Quickly sort issues by their stage, city, and current status.
  - **📊 Real-time Status Tracking**: Monitor issue progress live, from submission to resolution.

### 📊 Analytics & Insights

  - **📈 Interactive Analytics Dashboard**: A comprehensive dashboard for data visualization and insights.
  - **🗺️ Geographic Mapping**: Visually see where issues are concentrated on an interactive map.
  - **📅 Trend Analysis**: Analyze reporting patterns over time to identify hot spots and trends.
  - **🔥 Heatmap Visualization**: See the geographic distribution of issue types by city.
  - **📤 Data Export**: Download analytics data for external analysis and reporting.

### 🎬 Live Demo Features

  - **🎯 Interactive Demo Simulation**: A complete, step-by-step demonstration of the entire workflow.
  - **🎭 Humorous Tweet Generation**: Engaging and appropriately humorous social media content to get attention.
  - **⚡ Real-time Processing**: A live simulation of the platform's processing pipeline.
  - **📊 Impact Metrics**: See a breakdown of processing time, accuracy, and automation statistics.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Upload   │───▶│  Metadata        │───▶│  Admin Review   │
│   (Photo +      │    │  Extraction      │    │  & Approval     │
│    Location)    │    │  & Processing    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Similar       │    │   Authority      │    │   Email &       │
│   Issue         │    │   Contact        │    │   Tweet         │
│   Detection     │    │   Discovery      │    │   Generation    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

  - Python 3.8+
  - Required API keys (see Configuration section)

### Installation

1.  **Clone the repository**
    ` bash git clone [https://github.com/YOGESH007-CODING/SIH.git](https://github.com/YOGESH007-CODING/SIH.git) cd SIH  `

2.  **Install dependencies**
    ` bash pip install -r requirements.txt  `

3.  **Set up environment variables**
    \`bash
    cp .env.example .env

    # Edit .env with your API keys and credentials

    \`

4.  **Create required directories**
    ` bash mkdir -p issues/active issues/completed temp_uploads  `

5.  **Run the application**
    ` bash streamlit run main.py  `

## ⚙️ Configuration

### Required API Keys

Create a `.env` file with the following credentials:

```env
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Twitter API (for social media integration)
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET=your-api-secret
TWITTER_ACCESS_TOKEN=your-access-token
TWITTER_ACCESS_SECRET=your-access-secret
TWITTER_BEARER_TOKEN=your-bearer-token

# Google AI (for content generation)
GOOGLE_API_KEY=your-google-ai-key

# Tavily Search (for authority discovery)
TAVILY_API_KEY=your-tavily-key

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD_HASH=your-sha256-hashed-password
```

### API Setup Instructions

1.  **Google AI API**: Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2.  **Twitter API**: Apply for developer access at [Twitter Developer Portal](https://developer.twitter.com/)
3.  **Tavily Search**: Sign up at [Tavily](https://tavily.com/) for web search capabilities
4.  **Email**: Use Gmail with App Password or configure your SMTP provider

## 📱 Usage Guide

### For Citizens

1.  **Report an Issue**

      - Navigate to the User Dashboard.
      - Choose "Take photo" or "Upload from gallery."
      - Select the issue type (Pothole, Garbage, Water Leakage, etc.).
      - Submit the report, and let the system handle automatic location detection.

2.  **Track Your Issue**

      - Use the Issue ID provided after submission to track its progress.
      - Search on the main page to see the current status.
      - See if your report was merged with similar issues.

### For Administrators

1.  **Login**

      - Use your admin credentials on the sidebar to access the Admin Dashboard.

2.  **Review Process**

      - **Metadata Review**: Verify and edit the extracted location data.
      - **Authority Review**: Confirm the contact information for the relevant authority.
      - **Tweet Review**: Review and edit the automatically generated social media content.

3.  **Approval Workflow**

      - Approve each stage to move the issue forward.
      - The system automatically processes approved stages.
      - Monitor for errors and retry failed operations.

4.  **Analytics & Insights**

      - Access the Analytics Dashboard for comprehensive data visualization.
      - View geographic distribution, trend analysis, and performance metrics.
      - Export data for further analysis.

## 🔧 Core Components

### 📊 Issue Management (`src/manage_issue/`)

  - **IssueState**: Manages the issue lifecycle and storage.
  - **SimilarIssueFinder**: Detects and groups related issues.
  - **StateTemplate**: Defines the issue data structure.

### 📍 Metadata Extraction (`src/photo_extractor.py`)

  - Extracts GPS coordinates from EXIF data.
  - Uses reverse geocoding for addresses.
  - Falls back to browser GPS for camera uploads.

### 🔍 Authority Discovery (`authority_finder/`)

  - **TavilySearch**: Performs web searches for authority contacts.
  - **AuthorityFinder**: Uses AI to extract contacts.
  - Generates smart, location-specific queries for local authorities.

### 📧 Communication (`Email/`, `Social_platforms/`)

  - **EmailNotifier**: Handles automated email composition and sending.
  - **TwitterIntegration**: Generates and posts tweets to get attention.
  - Uses professional templates with embedded images.

### 🧠 Orchestration (`coordinator/orchestrator.py`)

  - **TheBrain**: The central coordinator that manages the entire workflow.
  - Handles stage management and approval processing.
  - Includes error handling and retry mechanisms.

### 📊 Analytics & Visualization (`pages/_3_Analytics_Dashboard.py`)

  - **Interactive Charts**: Provides charts, maps, and heatmaps for visualization.
  - **Real-time Metrics**: Tracks performance and key insights.
  - **Data Export**: Allows downloading data as a CSV.
  - **Responsive Design**: Optimized for all screen sizes.

### 🎬 Live Demo (`pages/_4_Live_Demo.py`)

  - **Interactive Simulation**: A full, interactive demonstration of the workflow.
  - **Humorous Content**: Features engaging and fun tweet examples.
  - **Technical Showcase**: Highlights the architecture and features.
  - **Real-time Processing**: Simulates the pipeline live.

## 📁 Project Structure

```
SIH/
├── 📁 src/                     # Core application logic
│   ├── manage_issue/           # Issue lifecycle management
│   ├── photo_extractor.py      # Metadata extraction
│   └── unique_id.py           # ID generation
├── 📁 authority_finder/        # Authority contact discovery
├── 📁 Email/                   # Email communication
├── 📁 Social_platforms/        # Social media integration
├── 📁 coordinator/             # Workflow orchestration
├── 📁 pages/                   # Streamlit UI pages
│   ├── _1_User_Dashboard.py    # Citizen reporting interface
│   ├── _2_Admin_Dashboard.py   # Administrative management
│   ├── _3_Analytics_Dashboard.py # Data visualization & insights
│   └── _4_Live_Demo.py         # Interactive demonstration
├── 📁 issues/                  # Issue storage
│   ├── active/                 # Pending issues
│   └── completed/              # Resolved issues
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies
└── HACKATHON_SUBMISSION.md     # Submission guidelines
```

## 🔄 Workflow Process

1.  **Issue Submission**

      - A user uploads a photo with location data.
      - The system extracts metadata and generates a unique ID.
      - Smart duplicate detection prevents multiple reports of the same issue.

2.  **Admin Review Stages**

      - **Stage 1**: Verify and edit the extracted metadata.
      - **Stage 2**: Confirm the authority contact information.
      - **Stage 3**: Review and edit the social media content before it's posted.

3.  **Automated Actions**

      - An email is sent to the relevant civic authority.
      - A tweet is posted to amplify the issue.
      - The issue is automatically moved to "completed" status.

4.  **Tracking & Follow-up**

      - Citizens can track the progress of their issue with their Issue ID.
      - Admins can monitor the resolution status.
      - Public social media posts provide transparency and accountability.

## 🛡️ Security Features

  - **Admin Authentication**: Secure login with SHA-256 password hashing.
  - **Data Validation**: Input sanitization and validation to prevent vulnerabilities.
  - **File Security**: Secure handling of image uploads.
  - **API Security**: All credentials are managed via environment variables.

## 🔧 Advanced Features

### Smart Duplicate Detection

  - Analyzes geographic proximity with a configurable radius.
  - Matches issue types.
  - Groups issues based on postal codes.
  - Automatically aggregates images for similar issues.

### AI-Powered Content Generation

  - Creates context-aware email templates.
  - Composes professional tweets with appropriate humor.
  - Discovers authority contacts.
  - Generates location-specific search queries.

### Robust Error Handling

  - Retry mechanisms for failed operations.
  - Comprehensive error logging for easy debugging.
  - Graceful degradation for missing data.
  - User-friendly error messages.

### Analytics & Insights

  - **Interactive Visualizations**: Charts, maps, and heatmaps for easy analysis.
  - **Trend Analysis**: Analyze time series data to spot patterns.
  - **Geographic Clustering**: Understand issue distribution by location.
  - **Performance Metrics**: Monitor system efficiency and response times.
  - **Data Export**: Download data as a CSV for deeper analysis.

## 🎯 Hackathon Highlights

### Technical Innovation

  - **Multi-Modal AI**: Combines image processing, GPS data, and AI-powered content generation.
  - **Smart Automation**: Automates authority discovery, email generation, and social media posting.
  - **Real-time Processing**: Features live location detection and metadata extraction.
  - **Intelligent Clustering**: Automatically detects and groups duplicate issues.

### User Experience Excellence

  - **Mobile-First Design**: A responsive interface optimized for all devices.
  - **Intuitive Workflow**: A simple flow from photo upload to automated processing.
  - **Real-time Feedback**: Live progress tracking and status updates for users.
  - **Accessibility**: Works with both camera and gallery uploads.

### Social Impact

  - **Civic Engagement**: Empowers citizens to be part of the solution.
  - **Government Efficiency**: Streamlines the issue management process for authorities.
  - **Transparency**: Public social media posting for greater accountability.
  - **Scalability**: Designed to work across multiple cities and issue types.

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

## 🆘 Support

  - **Issues**: Report bugs or request features via GitHub Issues.
  - **Documentation**: Check the code comments for detailed implementation notes.
  - **Community**: Join discussions in the repository.

## 🙏 Acknowledgments

  - **Streamlit** for the amazing web framework.
  - **Google AI** for intelligent content generation.
  - **Twitter API** for social media integration.
  - **OpenStreetMap/Nominatim** for geocoding services.
  - **Tavily** for web search capabilities.
  - **Plotly** for interactive data visualizations.
