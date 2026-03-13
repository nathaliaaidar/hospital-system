# 🏥 RTCON Hospital Management System

A complete hospital compliance and alert management system built with Python, featuring automated email notifications, a Streamlit web portal, and an AI-powered chatbot for document analysis.

---

## 🚀 Features

- **Automated Alert System** — monitors expiration dates across multiple hospitals and sends email notifications automatically
- **Multi-Hospital Management** — handles different alert rules and contacts per hospital from a single codebase
- **Web Portal (Streamlit)** — interactive dashboard to visualize compliance status and trigger alerts manually
- **AI Chatbot (RAG)** — local LLM-powered chatbot that reads institutional PDFs and answers questions about their content
- **Certificate Manager** — quick-access tool for managing and opening regulatory certificate links
- **Google Sheets Integration** — downloads and processes live spreadsheet data from each hospital in real time

---

## 🛠️ Tech Stack

| Area | Technologies |
|------|-------------|
| Backend | Python, Pandas, Requests |
| Frontend | Streamlit |
| AI / NLP | LangChain, FAISS, HuggingFace Embeddings, Ollama (Llama 3.1) |
| Notifications | SMTP / Gmail |
| Data Sources | Google Sheets (export API), Excel (.xlsx) |
| Automation | GitHub Actions (scheduled runs) |

---

## 📁 Project Structure

```
rtcon-hospital-system/
│
├── app_rtcon.py              # Streamlit web portal
├── backend_rtcon.py          # Core data processing logic
├── backend_alertas.py        # Alert engine with Google Sheets integration
├── envio_automatico.py       # Multi-hospital automated email dispatcher
├── alerta_formulario.py      # Single-hospital alert script
├── certidoes.py              # Certificate link manager
├── API_RTCONnews.py          # RAG chatbot for institutional PDF analysis
│
├── hospitals_config.example.json   # Hospital config template (no real data)
├── .env.example              # Environment variables template
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/rtcon-hospital-system.git
cd rtcon-hospital-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env`:
```env
```

> ⚠️ Use a **Gmail App Password**, not your main account password.  
> Never commit real credentials to version control.

### 4. Configure hospitals
Edit `hospitals_config.json` based on the provided example template.

### 5. Run the web portal
```bash
streamlit run app_rtcon.py
```

### 6. Run the automated dispatcher
```bash
python envio_automatico.py
```

---

## 🤖 AI Chatbot (RAG Pipeline)

`API_RTCONnews.py` implements a fully **local** RAG pipeline — no external API, no cost:

1. Upload any institutional PDF via the UI
2. Content is split and indexed with **FAISS** vector store
3. Queries are answered by **Llama 3.1** running locally via **Ollama**
4. Zero data leaves the machine

```bash
# Prerequisites: install Ollama and pull the model
ollama pull llama3.1

# Run
streamlit run API_RTCONnews.py
```

---

## 📬 Alert Business Rules

| Document Type | Alert Trigger |
|--------------|--------------|
| Operating Authorization | 120 days before expiration |
| All other documents | 30 days before expiration |

Emails are sent as HTML to designated contacts per hospital, with optional CC for management.

---

## 🔒 Security

- All credentials loaded via `os.getenv()` — never hardcoded
- Hospital spreadsheet IDs stored in config file, excluded from version control via `.gitignore`
- `.env.example` provided as a safe template

---

## 📦 requirements.txt

```
streamlit
pandas
openpyxl
requests
langchain
langchain-community
langchain-text-splitters
faiss-cpu
sentence-transformers
python-dotenv
pypdf
```

---

## 👩‍💻 Author

Developed by **Nathalia** as part of an automation initiative for hospital compliance management in radiation therapy operations.
