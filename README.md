# ShopEase AI Customer Support Agent

An AI-powered customer support assistant for **ShopEase**, built using FastAPI, LangChain, Groq, ChromaDB, and Sentence Transformers.

The assistant uses an LLM with tool calling to understand customer queries and select the appropriate support functionality, including policy lookup, order tracking, and product availability.

## 🚀 Features

- **Policy & FAQ Assistance:** Answers customer questions using Retrieval-Augmented Generation (RAG).
- **Order Tracking:** Retrieves order status and expected delivery details.
- **Product Availability:** Checks product stock and pricing.
- **AI Agent:** Uses an LLM to understand customer intent and select the appropriate tool.
- **RAG Pipeline:** Retrieves relevant information from company documents.
- **Vector Database:** Stores document embeddings using ChromaDB.
- **REST API:** Provides a FastAPI endpoint for customer conversations.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| LLM | Groq (gpt-oss-120b) |
| Agent Framework | LangChain |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Document Processing | PyPDF / LangChain |
| Language | Python |

## 🏗️ Architecture

1. Customer sends a message through the chat API.
2. The Groq-hosted LLM understands the customer's intent.
3. The agent selects the appropriate tool.
4. The selected tool performs the required operation:
   - `lookup_policy` – Retrieves relevant company policies using ChromaDB.
   - `track_order` – Retrieves order information.
   - `check_product_availability` – Checks product stock and pricing.
5. The tool returns the result to the LLM.
6. The LLM generates a natural-language response.
7. FastAPI returns the response to the customer.

## 📚 RAG Pipeline

The RAG pipeline allows the assistant to answer questions using company-specific documents.

**Workflow:**

1. Load PDF and TXT documents from `data/documents/`.
2. Extract text from documents.
3. Split documents into smaller chunks.
4. Generate embeddings using `all-MiniLM-L6-v2`.
5. Store embeddings in ChromaDB.
6. Retrieve relevant chunks using similarity search.
7. Provide retrieved context to the LLM to generate an answer.

## 📂 Project Structure

```text
Customer-Support-Agent/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── agent_v2.py
│   │   ├── config.py
│   │   │
│   │   ├── rag/
│   │   │   └── ingest.py
│   │   │
│   │   └── tools/
│   │       ├── order_tools.py
│   │       ├── product_tools.py
│   │       ├── rag_tools.py
│   │       └── mock_data.py
│   │
│   └── requirements.txt
│
├── data/
│   ├── documents/
│   └── vector_store/
│
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AbhijeetSingh293/Customer-Support-Agent.git

cd Customer-Support-Agent
```

### 2. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd backend

pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside the `backend/` directory.

```env
GROQ_API_KEY=your_groq_api_key
CHROMA_PERSIST_DIR=../data/vector_store
DATABASE_URL=sqlite:///./database/support.db
```

Get your API key from [Groq Console](https://console.groq.com/keys).

### 5. Add Company Documents

Add your company policy and FAQ documents (`.pdf` or `.txt`) inside:

```text
data/documents/
```

Examples:
- Return and refund policies
- Shipping and delivery timelines
- Cancellation policies
- Warranty information
- Payment FAQs
- Company contact information

### 6. Run Document Ingestion

From the `backend/` directory:

```bash
python -m app.rag.ingest
```

This processes the documents, generates embeddings, and stores them in ChromaDB.

Run ingestion again whenever you add or update company documents.

### 7. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

### 8. API Documentation

Open the interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔌 API Usage

### Chat Endpoint

**POST** `/api/chat`

Example request:

```json
{
  "message": "What is your return policy?"
}
```

Example response:

```json
{
  "reply": "..."
}
```

## 🧰 Available Agent Tools

| Tool | Description |
|---|---|
| `lookup_policy` | Searches company documents using RAG. |
| `track_order` | Retrieves order status and delivery information. |
| `check_product_availability` | Checks product availability and pricing. |

**Note:** Order and product lookups currently use sample data. Production deployment requires integration with real backend data sources.

## 🔐 Security Considerations

- Keep API keys in environment variables.
- Never commit `.env` files or sensitive credentials.
- Avoid exposing customer passwords, OTPs, CVVs, or payment credentials to the LLM.
- Configure appropriate CORS restrictions before production deployment.
- Use authenticated and access-controlled services when integrating real customer data.

## 🔮 Future Improvements

- Customer authentication and role-based access control.
- Integration with live order-management systems.
- Persistent conversation history.
- React-based customer chat interface.
- Automated testing and CI/CD.
- Human-agent escalation for complex queries.

## 👨‍💻 Author

**Abhijeet Kumar Singh**

- GitHub: [@AbhijeetSingh293](https://github.com/AbhijeetSingh293)

---

⭐ If you find this project useful, consider giving it a star!
