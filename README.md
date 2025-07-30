# 🚗 Ask MTO - AI-Powered Ontario Driver's Handbook Assistant

*Get instant, accurate answers about Ontario driving rules from the official MTO Driver's Handbook using advanced AI and semantic search.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Railway](https://img.shields.io/badge/Deployed%20on-Railway-blueviolet)](https://railway.app)

---

## 🎯 What is Ask MTO?

**Ask MTO** is an intelligent chatbot that provides instant, accurate answers about Ontario driving rules using advanced **Retrieval-Augmented Generation (RAG)** technology. Instead of manually searching through the 200+ page MTO Driver's Handbook, simply ask your question in plain English and get precise answers.

### 🧠 **How It Works**
1. **Enhanced Document Processing**: Uses OCR + TF-IDF analysis to extract and organize the MTO handbook content
2. **Semantic Search**: FAISS vector database enables lightning-fast similarity search through 72 smart chunks
3. **AI Generation**: OpenAI GPT generates natural, helpful answers based on the retrieved content


### 💡 **Perfect For**
- **New Drivers**: G1/G2 license requirements and rules
- **Road Test Prep**: Specific driving procedures and regulations  
- **Quick References**: Speed limits, right-of-way, traffic signs
- **Driving Instructors**: Accurate, source-backed teaching material

---

## ✨ **Live Demo**

🚀 **Try it now**: https://mto-ai.up.railway.app/
📚 **API Docs**: https://ask-mto.up.railway.app/docs

### **Example Questions**
- "What is a G1 license and how do I get one?"
- "What should I do at a four-way stop?"
- "What are the speed limits in residential areas?"
- "When can I turn right on a red light?"

---

## 🏗️ **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │  AI/Database    │
│   (Next.js)     │───▶│   (FastAPI)     │───▶│     Stack       │
│                 │    │                 │    │                 │
│ • Chat UI       │    │ • RAG Pipeline  │    │ • OpenAI GPT    │
│ • Question      │    │ • API Endpoints │    │ • FAISS Vector  │
│ • Responses     │    │ • Error Handling│    │ • TF-IDF Search │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **🔬 Technical Stack**

**Frontend**
- **Next.js 15** - Modern React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Railway** - Deployment platform

**Backend** 
- **FastAPI** - High-performance Python API
- **LangChain** - RAG pipeline orchestration
- **FAISS** - Vector similarity search
- **OpenAI GPT** - Language generation
- **Railway** - Cloud deployment

**Data Processing**
- **OCR + TF-IDF** - Enhanced text extraction and analysis
- **Semantic Chunking** - Smart content segmentation
- **Vector Embeddings** - Semantic search capabilities

---

## 📁 **Project Structure**

```
ask-mto/
├── apps/
│   ├── backend/                    # FastAPI Backend
│   │   ├── app/
│   │   │   ├── main.py            # API endpoints & RAG system
│   │   │   ├── config.py          # Configuration management
│   │   │   ├── cosmosdb.py        # Session storage
│   │   │   ├── monitoring.py      # Performance tracking
│   │   │   ├── semantic_kernel.py # AI orchestration
│   │   │   └── utils.py           # PDF processing utilities
│   │   ├── data/
│   │   │   └── mto_drive.pdf      # Official MTO handbook
│   │   ├── vectorstore/           # FAISS database
│   │   │   ├── index.faiss        # Vector index (72 chunks)
│   │   │   └── index.pkl          # Metadata
│   │   ├── scripts/
│   │   │   └── rebuild_vectorstore_ocr_tfidf.py  # Database builder
│   │   ├── Dockerfile             # Container configuration
│   │   ├── requirements.txt       # Python dependencies
│   │   ├── prompt.yaml            # AI prompt templates
│   │   └── railway.toml           # Railway deployment config
│   └── frontend/                   # Next.js Frontend
│       ├── src/app/
│       │   ├── page.tsx           # Main chat interface
│       │   ├── layout.tsx         # App layout
│       │   └── globals.css        # Styling
│       ├── package.json           # Node dependencies
│       └── railway.toml           # Railway deployment config
├── Dockerfile                     # Root container (legacy)
├── railway.toml                   # Root Railway config
└── README.md                      # This guide
```

---

## 🚀 **Quick Start**

### **🌐 Option 1: Use the Live Version**
Just visit https://mto-ai.up.railway.app/ - no setup required!

### **💻 Option 2: Local Development**

#### **Prerequisites**
- Python 3.11+
- Node.js 20+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

#### **1. Clone & Setup Backend**
```bash
# Clone the repository
git clone https://github.com/Tobidx/ask-mto.git
cd ask-mto/apps/backend

# Install Python dependencies
pip install -r requirements.txt

# Set your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# The vectorstore is already built and included in the repo
# Backend starts on http://localhost:8000
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### **2. Setup Frontend**
```bash
# Open new terminal
cd ask-mto/apps/frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Frontend starts on http://localhost:3000
```

#### **3. Test the System**
```bash
# Test the API
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a G1 license?"}'

# Visit http://localhost:3000 for the chat interface
```

---

## 🔧 **Configuration**

### **Environment Variables**

Create `.env` in `apps/backend/`:
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
AZURE_MONITOR_CONNECTION_STRING=your_azure_monitor_string
DEBUG=false
PORT=8000
CORS_ORIGINS=http://localhost:3000,https://your-frontend-url.com
```

### **Building Your Own Vectorstore**

If you want to rebuild the knowledge base:

```bash
cd apps/backend

# 1. Place your PDF in data/mto_drive.pdf
# 2. Ensure OPENAI_API_KEY is set
# 3. Run the rebuild script
python scripts/rebuild_vectorstore_ocr_tfidf.py
```

This will:
- Extract text using enhanced OCR
- Analyze content with TF-IDF for important terms
- Create 72 smart chunks optimized for driving questions
- Build FAISS vector index with OpenAI embeddings
- Save to `vectorstore/` directory

---

## 🚀 **Railway Deployment** 

This project is configured for **Railway** - a modern deployment platform.

### **Backend Deployment**

1. **Connect Repository**
   - Fork this repo to your GitHub
   - Connect to Railway (railway.app)
   - Deploy from `apps/backend`

2. **Set Environment Variables**
   ```bash
   # In Railway dashboard → Backend service → Variables
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Deploy**
   - Railway auto-deploys on git push
   - Uses `apps/backend/Dockerfile`
   - Includes pre-built vectorstore

### **Frontend Deployment**

1. **Deploy Frontend**
   - Create new Railway service from `apps/frontend`
   - Set environment variable:
   ```bash
   NEXT_PUBLIC_API_URL=https://your-backend-service.up.railway.app
   ```

2. **Custom Domains** (Optional)
   - Add custom domain in Railway dashboard
   - Configure DNS as instructed

### **🔗 Railway Configuration Files**

The project includes Railway configuration:
- `apps/backend/railway.toml` - Backend deployment
- `apps/frontend/railway.toml` - Frontend deployment  
- `railway.toml` - Root configuration

---



## 🧪 **Testing & Quality**

### **Manual Testing**
```bash
# Test basic functionality
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What should I do at a stop sign?"}'

# Test enhanced features  
curl -X POST "http://localhost:8000/ask-enhanced" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the G2 license restrictions?"}'
```


---

## 🛠️ **Development Guide**

### **Adding New Features**

**Backend (FastAPI):**
1. Add endpoints in `apps/backend/app/main.py`
2. Extend RAG pipeline functionality
3. Update configuration in `app/config.py`
4. Add monitoring in `app/monitoring.py`

**Frontend (Next.js):**
1. Update chat interface in `src/app/page.tsx`
2. Add new components in `src/components/`
3. Modify styles in `src/app/globals.css`

### **Updating the Knowledge Base**

When the MTO handbook is updated:
1. Replace `apps/backend/data/mto_drive.pdf`
2. Run `python scripts/rebuild_vectorstore_ocr_tfidf.py`
3. Commit and push the new `vectorstore/` files
4. Deploy to Railway

---


### **📚 Data Sources**
- **Official MTO content only** - no external or unofficial sources
- **Unmodified handbook content** - preserves official information
- **Source verification** - every answer includes handbook references

---


### **💻 Code Contributions**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Commit with clear messages
5. Push and create Pull Request

### **📝 Documentation**
- Improve this README
- Add code comments
- Create tutorials
- Update API documentation

---


## 📄 **License**

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

**What this means:**
- ✅ Free to use for personal/commercial projects
- ✅ Modify and distribute as needed  
- ✅ Private use allowed
- ❗ Include license notice in distributions

---

## 🚨 **Important Disclaimers**

### **⚖️ Legal Notice**
This application provides information from the Ontario MTO Driver's Handbook for **educational purposes only**. 

**Always:**
- Refer to the [official MTO website](https://www.ontario.ca/document/official-mto-drivers-handbook) for current regulations
- Verify information with licensed driving instructors
- Check for recent updates to traffic laws

### **🏢 Affiliation**
This project is **NOT affiliated** with:
- The Ontario Ministry of Transportation (MTO)
- The Government of Ontario
- Any official government agency

This is an independent educational tool using publicly available materials.

---


### **📚 Official Resources**
- **MTO Driver's Handbook**: [ontario.ca/document/official-mto-drivers-handbook](https://www.ontario.ca/document/official-mto-drivers-handbook)
- **Drive Test Booking**: [drivetest.ca](https://drivetest.ca)

### **🛠️ Tech Stack**
- **Railway**: [railway.app](https://railway.app)
- **OpenAI**: [platform.openai.com](https://platform.openai.com)
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Next.js**: [nextjs.org](https://nextjs.org)

---


---

**Ready to become a safer, more knowledgeable Ontario driver?** 

🚀 **[Try Ask MTO Now →](Your-Railway-Frontend-URL)**

*Built with ❤️ for the Ontario driving community* 
