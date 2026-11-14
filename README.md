Customer Support Agent
An AI-powered customer support assistant for ShopEase, built with
FastAPI, LangChain, Groq, ChromaDB, and Sentence Transformers.

The assistant uses an LLM with tool calling to understand customer
questions and select the appropriate support capability: retrieve
company policies, track an order, or check product availability.
Features
- Policy and FAQ assistance: Uses Retrieval-Augmented Generation
  (RAG) to retrieve relevant information from company PDF and TXT
  documents.
- Order tracking: Looks up order status and expected delivery
  details using an order ID.
- Product availability: Checks product stock and pricing from the
  available product catalog.
- Tool-augmented responses: The LLM selects and invokes the
  relevant support tool based on the customer's message.
- Local vector storage: Stores document embeddings in ChromaDB for
  semantic retrieval.
- REST API: Exposes a FastAPI chat endpoint for sending customer
  messages and receiving replies.
Tech Stack
  Component                   Technology
  API backend                 FastAPI, Uvicorn
LLM                         Groq -- openai/gpt-oss-120b
LLM integration and tools   LangChain
Embeddings                  Sentence Transformers -- all-MiniLM-L6-v2
Vector database             ChromaDB
Document processing         PyPDF, LangChain document loaders
Language                    Python
How It Works
1. A customer sends a message to the chat API.
2. The Groq-hosted language model interprets the request.
3. Based on the intent, the model can call one of the available tools:
   - lookup_policy -- searches the ShopEase knowledge base.
   - track_order -- retrieves order details and delivery status.
   - check_product_availability -- checks product price and stock.
4. The selected tool returns information to the model.
5. The model uses the tool result to prepare a customer-facing
   response.
6. FastAPI returns the reply as JSON.
RAG Workflow
Company policy documents are loaded from data/documents/, split into
smaller chunks, converted into embeddings using all-MiniLM-L6-v2, and
stored in ChromaDB. When a customer asks a policy-related question, the
assistant performs similarity search and uses the retrieved content to
answer.
Project Structure
Customer-Support-Agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application and /api/chat endpoint
│   │   ├── agent_v2.py          # LLM setup, prompt, and tool-calling loop
│   │   ├── config.py            # Environment configuration
│   │   ├── rag/
│   │   │   └── ingest.py        # Document loading, chunking, and indexing
│   │   └── tools/
│   │       ├── order_tools.py   # Order tracking tool
│   │       ├── product_tools.py # Product availability tool
│   │       ├── rag_tools.py     # Policy retrieval tool
│   │       └── mock_data.py     # Sample order and product data
│   └── requirements.txt
├── data/
│   ├── documents/               # Company policy and FAQ PDF/TXT files
│   └── vector_store/            # Generated ChromaDB data
└── README.md
Getting Started
Prerequisites
- Python 3.10 or later
- A Groq API key
- Git
1. Clone the repository
git clone https://github.com/AbhijeetSingh293/Customer-Support-Agent.git
cd Customer-Support-Agent
2. Create and activate a virtual environment
Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS / Linux:
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
cd backend
pip install -r requirements.txt
4. Configure environment variables
Create a .env file inside the backend/ directory:
GROQ_API_KEY=your_groq_api_key
CHROMA_PERSIST_DIR=../data/vector_store
DATABASE_URL=sqlite:///./database/support.db
Replace your_groq_api_key with your API key from Groq
Console. Keep .env private and never
commit API keys to Git.
5. Add company knowledge documents
Place your company policy and FAQ files (.pdf or .txt) in:
data/documents/
Examples include:
- Return and refund policies
- Shipping and delivery timelines
- Cancellation policies
- Warranty information
- Payment FAQs
- Company contact information
6. Build the knowledge base
From the backend/ directory, run:
python -m app.rag.ingest
The ingestion process loads supported documents, splits their content
into chunks, generates embeddings, and stores them in
data/vector_store/.

Run ingestion again whenever you add or update knowledge-base documents.
7. Start the API server
From the backend/ directory:
uvicorn app.main:app --reload
The API will be available at:
http://127.0.0.1:8000
Interactive API documentation:
http://127.0.0.1:8000/docs
API Usage
Chat endpoint
POST /api/chat

Request body:
{
  "message": "What is your return policy?"
}
Example response:
{
  "reply": "..."
}
You can also test the endpoint using the interactive Swagger UI at
http://127.0.0.1:8000/docs.
Available Support Tools
  Tool                           Purpose                 Example customer query
  lookup_policy                Retrieves relevant      "What is the return
policy information from policy?"
ChromaDB                

  track_order                  Checks order status and "Where is my order
expected delivery       ORD1001?"
check_product_availability   Checks product stock    "Is the wireless
and price               headphones available?"
Note: Order and product lookups currently use the sample data
defined in the project. Replace or connect these data sources to a
production database or order-management system before real-world
deployment.

Configuration
  Variable                            Purpose
  GROQ_API_KEY                      API key used to access the
Groq-hosted language model

  CHROMA_PERSIST_DIR                Configurable ChromaDB persistence
directory
DATABASE_URL                      Database connection setting
Security Notes
- Store API keys in environment variables; do not hardcode or commit
  secrets.
- Do not request or share customer passwords, OTPs, CVVs, UPI PINs, or
  complete card numbers.
- Configure restrictive CORS origins before deploying the API
  publicly. The current development configuration allows all origins.
- Connect real customer and order data only through authenticated,
  access-controlled backend services.
Future Improvements
- Add customer authentication and role-based access control.
- Integrate a production database and live order-management APIs.
- Add persistent conversation history and session management.
- Build a customer-facing React chat interface.
- Add automated tests, logging, and deployment configuration.
- Add human-agent escalation for unresolved or disputed requests.
Contributing
Contributions and suggestions are welcome. To contribute:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request describing your improvements.
License
No license is currently specified. Add a LICENSE file if you want to
define how others may use, modify, and distribute this project.
