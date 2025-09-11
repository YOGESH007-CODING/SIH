# 🏙️ CivicSpotter

**A Smart Civic Issue Reporting & Management Platform**

CivicSpotter is an intelligent crowdsourced platform that empowers citizens to report local infrastructure issues through simple photo uploads while providing administrators with powerful tools to manage, track, and resolve these issues efficiently.

## 🌟 Key Features

### 👥 For Citizens
- **📸 Photo-Based Reporting**: Upload photos directly from camera or gallery
- **🗺️ Automatic Location Detection**: GPS-based location extraction from photos or browser
- **🔍 Issue Tracking**: Search and track your submitted issues by ID
- **📱 Mobile-Friendly Interface**: Responsive design for all devices
- **🤝 Smart Duplicate Detection**: Automatically groups similar nearby issues

### 🛠️ For Administrators
- **📋 Comprehensive Dashboard**: Review and manage all reported issues
- **✅ Multi-Stage Approval Process**: Metadata → Authority → Tweet review workflow
- **📧 Automated Email Generation**: Smart authority contact discovery and email composition
- **🐦 Social Media Integration**: Automated tweet generation and posting to amplify issues
- **🔍 Advanced Filtering**: Filter issues by stage, city, and status
- **📊 Real-time Status Tracking**: Monitor issue progress from submission to resolution

### 📊 Analytics & Insights
- **📈 Interactive Analytics Dashboard**: Comprehensive data visualization and insights
- **🗺️ Geographic Mapping**: Visual representation of issue locations
- **📅 Trend Analysis**: Time series analysis of issue reporting patterns
- **🔥 Heatmap Visualization**: Issue type distribution by city
- **📤 Data Export**: Download analytics data for further analysis

### 🎬 Live Demo Features
- **🎯 Interactive Demo Simulation**: Complete workflow demonstration
- **🎭 Humorous Tweet Generation**: Engaging social media content with appropriate humor
- **⚡ Real-time Processing**: Live simulation of the entire pipeline
- **📊 Impact Metrics**: Processing time, accuracy, and automation statistics

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Upload   │───▶│  Metadata        │───▶│  Admin Review   │
│   (Photo +      │    │  Extraction      │    │  & Approval     │
│    Location)    │    │  & Processing    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Similar       │    │   Authority      │    │   Email &       │
│   Issue         │    │   Contact        │    │   Tweet         │
│   Detection     │    │   Discovery      │    │   Generation    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required API keys (see Configuration section)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Chaitanya782/CivicSpotter.git
   cd CivicSpotter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and credentials
   ```

4. **Create required directories**
   ```bash
   mkdir -p issues/active issues/completed temp_uploads
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

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

1. **Google AI API**: Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Twitter API**: Apply for developer access at [Twitter Developer Portal](https://developer.twitter.com/)
3. **Tavily Search**: Sign up at [Tavily](https://tavily.com/) for web search capabilities
4. **Email**: Use Gmail with App Password or configure your SMTP provider

## 📱 Usage Guide

### For Citizens

1. **Report an Issue**
   - Navigate to User Dashboard
   - Choose "Take photo" or "Upload from gallery"
   - Select issue type (Pothole, Garbage, Water Leakage, etc.)
   - Submit with automatic location detection

2. **Track Your Issue**
   - Use the Issue ID provided after submission
   - Search on the main page to see current status
   - View if your issue was merged with similar reports

### For Administrators

1. **Login**
   - Use admin credentials on the sidebar
   - Access the Admin Dashboard

2. **Review Process**
   - **Metadata Review**: Verify and edit extracted location data
   - **Authority Review**: Confirm authority contact information
   - **Tweet Review**: Review and edit generated social media content

3. **Approval Workflow**
   - Approve each stage to proceed to the next
   - System automatically processes approved stages
   - Monitor errors and retry failed operations

4. **Analytics & Insights**
   - Access the Analytics Dashboard for comprehensive data visualization
   - View geographic distribution, trend analysis, and performance metrics
   - Export data for further analysis

## 🔧 Core Components

### 📊 Issue Management (`src/manage_issue/`)
- **IssueState**: Manages issue lifecycle and storage
- **SimilarIssueFinder**: Detects and groups related issues
- **StateTemplate**: Defines issue data structure

### 📍 Metadata Extraction (`src/photo_extractor.py`)
- Extracts GPS coordinates from EXIF data
- Reverse geocoding for address information
- Fallback to browser GPS for camera uploads

### 🔍 Authority Discovery (`authority_finder/`)
- **TavilySearch**: Web search for authority contacts
- **AuthorityFinder**: AI-powered contact extraction
- Smart query generation for local authorities

### 📧 Communication (`Email/`, `Social_platforms/`)
- **EmailNotifier**: Automated email composition and sending
- **TwitterIntegration**: Tweet generation and posting
- Professional templates with embedded images

### 🧠 Orchestration (`coordinator/orchestrator.py`)
- **TheBrain**: Central coordinator managing the entire workflow
- Stage management and approval processing
- Error handling and retry mechanisms

### 📊 Analytics & Visualization (`pages/_3_Analytics_Dashboard.py`)
- **Interactive Charts**: Issue distribution, trends, and geographic mapping
- **Real-time Metrics**: Performance tracking and insights
- **Data Export**: CSV download functionality
- **Responsive Design**: Optimized for all screen sizes

### 🎬 Live Demo (`pages/_4_Live_Demo.py`)
- **Interactive Simulation**: Complete workflow demonstration
- **Humorous Content**: Engaging tweet examples with appropriate humor
- **Technical Showcase**: Architecture and feature highlights
- **Real-time Processing**: Live simulation of the entire pipeline

## 📁 Project Structure

```
CivicSpotter/
├── 📁 src/                     # Core application logic
│   ├── manage_issue/           # Issue lifecycle management
│   ├── photo_extractor.py      # Metadata extraction
│   └── unique_id.py           # ID generation
├── 📁 authority_finder/        # Authority contact discovery
├── 📁 Email/                   # Email communication
├── 📁 Social_platforms/        # Social media integration
├── 📁 coordinator/             # Workflow orchestration
├── 📁 pages/                   # Streamlit UI pages
│   ├── _1_User_Dashboard.py    # Citizen reporting interface
│   ├── _2_Admin_Dashboard.py   # Administrative management
│   ├── _3_Analytics_Dashboard.py # Data visualization & insights
│   └── _4_Live_Demo.py         # Interactive demonstration
├── 📁 issues/                  # Issue storage
│   ├── active/                 # Pending issues
│   └── completed/              # Resolved issues
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies
└── HACKATHON_SUBMISSION.md     # Submission guidelines
```

## 🔄 Workflow Process

1. **Issue Submission**
   - User uploads photo with location data
   - System extracts metadata and generates unique ID
   - Similar issue detection prevents duplicates

2. **Admin Review Stages**
   - **Stage 1**: Metadata verification and editing
   - **Stage 2**: Authority contact confirmation
   - **Stage 3**: Tweet content review and approval

3. **Automated Actions**
   - Email sent to relevant civic authority
   - Tweet posted to amplify the issue
   - Issue moved to completed status

4. **Tracking & Follow-up**
   - Citizens can track progress via Issue ID
   - Admins monitor resolution status
   - Social media provides public accountability

## 🛡️ Security Features

- **Admin Authentication**: SHA-256 password hashing
- **Data Validation**: Input sanitization and validation
- **File Security**: Secure image upload handling
- **API Security**: Environment-based credential management

## 🔧 Advanced Features

### Smart Duplicate Detection
- Geographic proximity analysis (configurable radius)
- Issue type matching
- Postal code-based grouping
- Automatic image aggregation for similar issues

### AI-Powered Content Generation
- Context-aware email templates
- Professional tweet composition with appropriate humor
- Authority contact discovery
- Location-specific query generation

### Robust Error Handling
- Retry mechanisms for failed operations
- Comprehensive error logging
- Graceful degradation for missing data
- User-friendly error messages

### Analytics & Insights
- **Interactive Visualizations**: Charts, maps, and heatmaps
- **Trend Analysis**: Time series data and patterns
- **Geographic Clustering**: Location-based issue analysis
- **Performance Metrics**: System efficiency and response times
- **Data Export**: CSV download for external analysis

## 🎯 Hackathon Highlights

### Technical Innovation
- **Multi-Modal AI**: Image processing + GPS + AI content generation
- **Smart Automation**: Authority discovery, email generation, social media posting
- **Real-time Processing**: Live location detection and metadata extraction
- **Intelligent Clustering**: Automatic duplicate detection and issue grouping

### User Experience Excellence
- **Mobile-First Design**: Responsive interface for all devices
- **Intuitive Workflow**: Simple photo upload → automatic processing
- **Real-time Feedback**: Live progress tracking and status updates
- **Accessibility**: Works with camera or gallery uploads

### Social Impact
- **Civic Engagement**: Empowers citizens to report local issues
- **Government Efficiency**: Streamlines issue management for authorities
- **Transparency**: Public social media posting for accountability
- **Scalability**: Works across multiple cities and issue types

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Check the code comments for detailed implementation notes
- **Community**: Join discussions in the repository

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **Google AI** for intelligent content generation
- **Twitter API** for social media integration
- **OpenStreetMap/Nominatim** for geocoding services
- **Tavily** for web search capabilities
- **Plotly** for interactive data visualizations

---

<!-- Built with Bolt.new Badge -->
<div align="center">
    <a href="https://bolt.new" target="_blank">
        <img src="https://img.shields.io/badge/Built%20with-Bolt.new-FF6B6B?style=for-the-badge&logo=lightning&logoColor=white" 
             alt="Built with Bolt.new" 
             style="border-radius: 8px; box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);">
    </a>
</div>

<div align="center">
    <p><strong>Built with ❤️ for better civic engagement and community empowerment</strong></p>
    <p><em>CivicSpotter - Making cities more responsive, one photo at a time.</em></p>
    <p>⚡ Powered by AI • 🎯 Built for Impact • 🚀 Deployed with Bolt</p>
</div>