# 🚗 Ask MTO - Your AI-Powered Ontario Driving Assistant

*Get instant, accurate answers about Ontario driving rules from the official MTO Driver's Handbook, powered by advanced AI technology.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

---

## 🎯 What is Ask MTO?

**Ask MTO** is an intelligent chatbot that helps Ontario drivers understand driving rules, regulations, and procedures. Instead of searching through hundreds of pages in the official MTO Driver's Handbook, simply ask your question in plain English and get instant, accurate answers with references to the source material.

### 💡 Perfect For:
- **New Drivers**: Learning the rules for G1, G2, and full G licenses
- **Experienced Drivers**: Quick refreshers on specific regulations
- **Driving Instructors**: Teaching aid with accurate, source-backed information
- **Anyone**: Preparing for knowledge tests or understanding Ontario traffic laws

---

## ✨ Key Features

### 🧠 **Smart AI Assistant**
- **Understands Context**: Remembers your conversation for follow-up questions
- **Accurate Answers**: Based entirely on the official MTO Driver's Handbook
- **Source References**: Every answer includes where to find the information in the handbook
- **Natural Language**: Ask questions the way you naturally speak

### 💬 **Modern Chat Experience**
- **Real-time Responses**: Get answers instantly
- **Voice Support**: Ask questions using speech-to-text
- **Listen to Answers**: Text-to-speech for hands-free learning
- **Conversation History**: Your chats are saved for future reference
- **Export Chats**: Download your conversation history

### 📱 **Works Everywhere**
- **Mobile-Friendly**: Responsive design for phones and tablets
- **Install as App**: Add to your home screen (PWA)
- **Offline Capable**: Basic functionality works without internet
- **Cross-Platform**: Works on iOS, Android, Windows, Mac, and Linux

### 🔧 **Enterprise-Grade Technology**
- **Quality Monitoring**: Advanced metrics ensure accurate responses
- **Performance Tracking**: Real-time monitoring of response quality
- **Scalable Architecture**: Built to handle thousands of users
- **Production Ready**: Includes monitoring, logging, and error handling

---

## 💭 Example Questions You Can Ask

**Getting Started:**
- "How do I get my G1 license?"
- "What documents do I need for a road test?"
- "How long is my G2 license valid?"

**Driving Rules:**
- "What's the speed limit in residential areas?"
- "When can I turn right on a red light?"
- "What should I do at a four-way stop?"

**Follow-up Questions:**
- You: "What should I do when I'm tired while driving?"
- Bot: "Don't drive when you are tired. Take breaks every 2 hours..."
- You: "What if I can't find a place to stop?"
- Bot: "If you can't find a proper rest area, you should..."

---

## 🏗️ How It Works (For the Curious)

### The Magic Behind the Scenes:

1. **Document Processing**: We've converted the entire MTO Driver's Handbook into a searchable format using advanced text extraction and machine learning
2. **Smart Search**: When you ask a question, AI finds the most relevant sections of the handbook
3. **Answer Generation**: Advanced language models create clear, helpful answers based on the official content
4. **Quality Control**: Every response is monitored for accuracy and helpfulness

### 🔬 **Technical Architecture**

**For Developers and Tech Enthusiasts:**

- **Frontend**: React with Next.js 15, Tailwind CSS for modern UI
- **Backend**: Python FastAPI with advanced RAG (Retrieval-Augmented Generation)
- **AI Models**: OpenAI GPT for natural language understanding and generation
- **Vector Database**: FAISS for lightning-fast document search
- **Monitoring**: Azure Application Insights for real-time performance tracking
- **Quality Assurance**: RAGAS evaluation system for answer quality metrics

---

## 📁 Project Structure

```
ask-mto/
├── ask-mto-genai/              # Main backend application
│   ├── app/                    # FastAPI application code
│   │   ├── main.py            # Main API endpoints and server
│   │   ├── config.py          # Configuration management
│   │   ├── eval_ragas.py      # Answer quality evaluation
│   │   ├── monitoring.py      # Azure monitoring integration
│   │   ├── semantic_kernel.py # AI orchestration system
│   │   ├── cosmosdb.py        # Database operations
│   │   └── utils.py           # Utility functions
│   ├── ask-mto-ui/            # Frontend React application
│   │   ├── src/app/           # Next.js app directory
│   │   │   ├── page.tsx       # Main chat interface
│   │   │   ├── layout.tsx     # App layout and metadata
│   │   │   └── globals.css    # Global styles
│   │   ├── public/            # Static assets and PWA files
│   │   │   ├── manifest.json  # PWA manifest
│   │   │   ├── sw.js          # Service worker
│   │   │   └── icons/         # App icons
│   │   └── package.json       # Frontend dependencies
│   ├── data/                  # Source documents
│   │   └── mto_drive.pdf      # Official MTO handbook
│   ├── vectorstore/           # Processed document embeddings
│   │   ├── index.faiss        # Vector index
│   │   └── index.pkl          # Metadata
│   ├── scripts/               # Setup and utility scripts
│   │   └── rebuild_vectorstore_ocr_tfidf.py
│   ├── Dockerfile             # Container configuration
│   ├── requirements.txt       # Python dependencies
│   ├── start.sh              # Production startup script
│   └── prompt.yaml           # AI prompt templates
├── azure-pipelines.yml        # CI/CD configuration
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT license
└── README.md                  # This comprehensive guide
```

---

## 🚀 Getting Started

### 📋 Prerequisites

**For Users:**
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for initial setup

**For Developers:**
- Python 3.11 or higher
- Node.js 20 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- (Optional) Azure Monitor connection string for production monitoring

### 💻 Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/Tobidx/ask-mto.git
cd ask-mto
```

#### 2. Backend Setup
```bash
# Navigate to the backend directory
cd ask-mto-genai

# Install Python dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Optional: Set Azure Monitor for production monitoring
export AZURE_MONITOR_CONNECTION_STRING="your-azure-connection-string"

# Start the backend server
./start.sh
```

The backend will start on `http://localhost:8000`

#### 3. Frontend Setup
```bash
# Open a new terminal and navigate to the frontend
cd ask-mto-genai/ask-mto-ui

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:3000`

#### 4. Access the Application
- **Main App**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000

---

## 🔧 Configuration

### 🔑 Environment Variables

Create a `.env` file in the `ask-mto-genai` directory:

```env
# Required - OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here

# Optional - Azure Services
AZURE_MONITOR_CONNECTION_STRING=your-azure-monitor-connection-string

# Application Settings
HOST=127.0.0.1
PORT=8000
DEBUG=false
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Vector Store Configuration
VECTOR_STORE_PATH=vectorstore
```

### ⚙️ Advanced Configuration

**Backend Configuration (`ask-mto-genai/app/config.py`):**
- Server host and port settings
- CORS (Cross-Origin Resource Sharing) configuration
- Debug mode settings
- Vector store location
- Monitoring and logging levels

**Frontend Configuration (`ask-mto-genai/ask-mto-ui/`):**
- API endpoint configuration
- UI theme and styling
- PWA settings
- Build optimization

---

## 📡 API Documentation

### Core Endpoints

#### 🤖 Basic Q&A
```http
POST /ask
Content-Type: application/json

{
  "question": "How do I get my G1 license?"
}
```

**Response:**
```json
{
  "answer": "To get your G1 license, you need to...",
  "sources": [
    "Section 2.1: Getting Your First License",
    "Page 15: G1 License Requirements"
  ]
}
```

#### 🧠 Enhanced AI Response
```http
POST /ask-enhanced
Content-Type: application/json

{
  "question": "What should I do when tired while driving?"
}
```

**Response includes:**
- Enhanced answer with AI orchestration
- Follow-up suggestions
- Related topics
- Conversation context

#### 📊 Quality Evaluation
```http
POST /evaluate
Content-Type: application/json

{
  "question": "What are the speed limits in Ontario?"
}
```

**Response includes:**
- The answer to your question
- Quality metrics (RAGAS scores)
- Confidence levels
- Source relevancy scores

#### 🔄 Context Management
```http
POST /clear-context
```
Resets the conversation history for a fresh start.

### 📚 Interactive API Documentation

Visit `http://localhost:8000/docs` when running locally to access:
- Complete API documentation
- Interactive testing interface
- Request/response examples
- Authentication details

---

## 🚀 Deployment Options

### 🖥️ Local Development
Perfect for testing and development:
```bash
# Backend
cd ask-mto-genai
./start.sh

# Frontend (new terminal)
cd ask-mto-genai/ask-mto-ui
npm run dev
```

### 🐳 Docker Deployment
Containerized deployment for consistency:
```bash
cd ask-mto-genai

# Build the Docker image
docker build -t ask-mto-backend .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e AZURE_MONITOR_CONNECTION_STRING=your-connection-string \
  ask-mto-backend
```

### ☁️ Production Deployment (Azure)

The project includes complete Azure deployment configuration:

**Azure Services Used:**
- **Azure App Service**: Hosts the FastAPI backend
- **Azure Static Web Apps**: Hosts the React frontend
- **Azure Application Insights**: Monitors performance and errors
- **Azure Container Registry**: Stores Docker images

**Deployment Steps:**
1. Fork this repository to your GitHub account
2. Create Azure resources using the Azure portal
3. Configure the included `azure-pipelines.yml` file
4. Set up environment variables in Azure
5. Deploy using Azure DevOps or GitHub Actions

**Environment Variables for Production:**
```env
OPENAI_API_KEY=your-production-openai-key
AZURE_MONITOR_CONNECTION_STRING=your-azure-insights-connection
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
```

---

## 📊 Monitoring and Quality Assurance

### 🎯 Answer Quality (RAGAS Metrics)

We use RAGAS (Retrieval-Augmented Generation Assessment) to ensure high-quality responses:

- **Answer Relevancy** (0-1): How well the answer addresses the question
- **Faithfulness** (0-1): How well the answer sticks to the source material
- **Context Relevancy** (0-1): How relevant the retrieved context is
- **Context Recall** (0-1): How well the system found all relevant information

**Example Quality Check:**
```bash
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"question": "What should I do at a stop sign?"}'
```

### 📈 Production Monitoring

When connected to Azure Monitor, the system automatically tracks:

**Performance Metrics:**
- Average response time
- Requests per minute
- Error rates and types
- System resource usage

**Quality Metrics:**
- RAGAS scores over time
- User satisfaction indicators
- Most popular questions
- Answer accuracy trends

**Error Tracking:**
- Failed requests with full context
- System errors and exceptions
- Integration failures
- Performance bottlenecks

---

## 🛠️ Development Guide

### 🧪 Testing the System

**Test Basic Functionality:**
```bash
# Test the main endpoint
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I renew my license?"}'

# Test enhanced features
curl -X POST "http://localhost:8000/ask-enhanced" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the rules for new drivers?"}'

# Test quality evaluation
curl -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"question": "When can I drive alone with a G2?"}'
```

**Test Frontend Features:**
1. Open http://localhost:3000
2. Try asking various questions
3. Test voice input (click microphone button)
4. Test conversation export
5. Test PWA installation (browser menu)

### 🔧 Adding New Features

**Backend (Python/FastAPI):**
1. Add new endpoints in `app/main.py`
2. Extend functionality in respective modules
3. Update configuration in `app/config.py`
4. Add monitoring in `app/monitoring.py`

**Frontend (React/Next.js):**
1. Add new components in `src/components/`
2. Update the main chat interface in `src/app/page.tsx`
3. Modify global styles in `src/app/globals.css`
4. Update PWA configuration in `public/manifest.json`

### 🧹 Code Quality

**Python (Backend):**
```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/
mypy app/

# Run tests
pytest
```

**TypeScript (Frontend):**
```bash
# Lint and format
npm run lint
npm run format

# Type checking
npm run type-check

# Run tests
npm test
```

---

## 🔒 Privacy and Security

### 🛡️ Privacy Protection

**What We DON'T Store:**
- Personal information
- Individual questions (unless you explicitly save them)
- User tracking data
- Location information

**What We DO Store:**
- Conversation history (locally in your browser only)
- Anonymous usage statistics (if monitoring is enabled)
- Error logs (for debugging purposes only)

### 🔐 Security Measures

**API Security:**
- Input validation and sanitization
- Rate limiting to prevent abuse
- CORS configuration for safe cross-origin requests
- Secure environment variable handling

**Data Security:**
- Encrypted communication (HTTPS in production)
- Secure API key management
- No sensitive data in logs
- Regular security updates

### 📚 Data Sources

**Official Content Only:**
- All answers are based on the official Ontario MTO Driver's Handbook
- No third-party or unofficial sources
- Content is processed but not modified
- Source references provided for verification

---

## 🤝 Contributing

We welcome contributions from everyone! Here's how you can help:

### 🐛 Reporting Issues
Found a bug or have a suggestion?
1. Check existing [GitHub Issues](https://github.com/Tobidx/ask-mto/issues)
2. Create a new issue with detailed information
3. Include steps to reproduce (for bugs)
4. Suggest specific improvements (for enhancements)

### 💻 Code Contributions
1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
4. **Make** your changes
5. **Test** your changes thoroughly
6. **Commit** with clear messages (`git commit -m 'Add amazing feature'`)
7. **Push** to your branch (`git push origin feature/amazing-feature`)
8. **Open** a Pull Request with detailed description

### 📝 Documentation
- Improve this README
- Add code comments
- Create tutorials or guides
- Update API documentation

### 🎨 Design and UX
- Improve the user interface
- Enhance mobile experience
- Create better icons or graphics
- Suggest UX improvements

---

## 🆘 Support and Help

### 📖 Documentation
- **This README**: Comprehensive setup and usage guide
- **API Docs**: Available at `/docs` when running locally
- **Code Comments**: Well-documented codebase
- **Configuration Examples**: See `.env` examples above

### 💬 Getting Help
- **Bug Reports**: [GitHub Issues](https://github.com/Tobidx/ask-mto/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/Tobidx/ask-mto/discussions)
- **Questions**: Check existing issues or start a discussion
- **Security Issues**: Please report privately via GitHub security advisories

### 🔧 Troubleshooting

**Common Issues:**

1. **"Module not found" errors**:
   - Ensure you're in the correct directory
   - Install dependencies: `pip install -r requirements.txt`
   - Check Python version (3.11+ required)

2. **Frontend won't start**:
   - Install Node.js dependencies: `npm install`
   - Clear Next.js cache: `rm -rf .next`
   - Check Node.js version (20+ required)

3. **API key errors**:
   - Verify your OpenAI API key is valid
   - Check environment variable setting
   - Ensure proper export syntax

4. **CORS errors**:
   - Check CORS configuration in `app/config.py`
   - Verify frontend and backend URLs match

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**What this means for you:**
- ✅ **Free to use** for personal or commercial projects
- ✅ **Modify and distribute** as needed
- ✅ **Private use** allowed
- ❗ **Include license notice** in distributions

---

## 🚨 Important Disclaimers

### ⚖️ Legal Notice
This application provides information based on the Ontario MTO Driver's Handbook for **educational purposes only**. While we strive for accuracy, you should always:
- Refer to the official MTO website for current regulations
- Consult official sources before making driving decisions
- Verify information with licensed driving instructors
- Check for recent updates to traffic laws

### 🏢 Affiliation
This project is **NOT affiliated** with:
- The Ontario Ministry of Transportation (MTO)
- The Government of Ontario
- Any official government agency

This is an independent educational tool created using publicly available materials.

### 🔄 Content Currency
The MTO Driver's Handbook content may change over time. While we aim to keep our content updated, there may be delays in reflecting the latest changes. Always verify current information through official channels.

---

## 🔗 Useful Links

### 🏠 Project Links
- **Repository**: [https://github.com/Tobidx/ask-mto](https://github.com/Tobidx/ask-mto)
- **Issues**: [GitHub Issues](https://github.com/Tobidx/ask-mto/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Tobidx/ask-mto/discussions)

### 📚 Official Resources
- **MTO Driver's Handbook**: [ontario.ca/document/official-mto-drivers-handbook](https://www.ontario.ca/document/official-mto-drivers-handbook)
- **MTO Website**: [ontario.ca/page/ministry-transportation](https://www.ontario.ca/page/ministry-transportation)
- **Drive Test Booking**: [drivetest.ca](https://drivetest.ca)

### 🛠️ Developer Resources
- **OpenAI API**: [platform.openai.com](https://platform.openai.com)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Next.js Docs**: [nextjs.org/docs](https://nextjs.org/docs)
- **Azure Docs**: [docs.microsoft.com/azure](https://docs.microsoft.com/azure)

---

## 🎉 Acknowledgments

### 💖 Built With Love
This project was created with passion for helping Ontario drivers learn and understand traffic rules safely and effectively.

### 🙏 Special Thanks
- **Ontario Ministry of Transportation** for making the Driver's Handbook publicly available
- **OpenAI** for providing advanced language models
- **Open Source Community** for the amazing tools and libraries
- **Contributors** who help make this project better
- **Users** who provide feedback and suggestions

### 🏆 Technology Credits
- **Python & FastAPI** - Backend framework
- **React & Next.js** - Frontend framework
- **OpenAI GPT** - Language understanding
- **LangChain** - RAG pipeline
- **FAISS** - Vector similarity search
- **Tailwind CSS** - UI styling
- **Azure** - Cloud hosting and monitoring

---

## 🌟 Star History

If this project helps you, please consider giving it a ⭐ on GitHub! It helps others discover the project and motivates continued development.

---

***Ready to become a safer, more knowledgeable Ontario driver? Start asking questions now!*** 🚗💨

*Built with ❤️ for the Ontario driving community* 