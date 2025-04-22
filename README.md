# B2B Sales Support Chatbot

An AI-powered B2B sales support chatbot that automates the early stages of sales dialogues—rapidly capturing client requirements, proposing initial pricing, and seamlessly handing off to human sales representatives when needed.

## Project Overview

This project implements an intelligent, multilingual chatbot designed to improve the B2B sales process by:

- Providing instant responses to client inquiries in their preferred language
- Answering detailed product questions with up-to-date information
- Gathering client requirements through natural conversation
- Generating data-driven pricing quotes with optimal margins
- Creating order inquiries or facilitating handoffs to human sales reps

## Core Capabilities

1. **Smart Greetings:**

   - Instant, friendly welcome in the client's preferred language.

2. **Product Expertise:**

   - Answers detailed product questions with up‑to‑date information.

3. **Requirements Gathering:**

   - Clarifies:
     - "What do you need?"
     - "What features aren't required?"

4. **Dynamic Pricing:**

   - Leverages historical deal data.
   - Recommends an initial quote ~15% above the company's minimum threshold.

5. **Confirmation & Negotiation:**

   - Summarizes the client's request and proposed price for approval.
   - If accepted → Automatically generates an order inquiry.
   - If declined → Offers to connect with a human sales representative.

6. **Seamless Multilingual Support:**
   - Translates both inbound and outbound messages in real time.

## Technology Stack

- **Backend:** Python with FastAPI
- **Frontend:** Vue.js with Vuex
- **AI Services:** AWS Bedrock
- **Translation:** AWS Translate
- **API Gateway:** Kong Konnect
- **Database:** PostgreSQL (simulated with in-memory storage for demo)

## Project Structure

```
.
├── backend/                # Python backend with FastAPI
│   ├── app/                # Application code
│   │   ├── config/         # Configuration
│   │   ├── database/       # Database models and functions
│   │   ├── models/         # Pydantic models
│   │   └── services/       # Business logic services
│   ├── data/               # Data files
│   └── tests/              # Test files
└── frontend/               # Vue.js frontend
    ├── public/             # Static assets
    └── src/                # Source code
        ├── assets/         # Images and styles
        ├── components/     # Vue components
        ├── router/         # Vue Router configuration
        ├── store/          # Vuex store
        └── views/          # Page components
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:

   ```
   cd backend
   ```

2. Create and activate a virtual environment:

   ```
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory:

   ```
   DEBUG=True
   AWS_REGION=eu-central-1
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   BEDROCK_MODEL_ID=eu.anthropic.claude-3-7-sonnet-20250219-v1:0
   ```

5. Run the backend server:
   ```
   python run.py
   ```

The API will be available at http://localhost:8000.

### Frontend Setup

1. Navigate to the frontend directory:

   ```
   cd frontend
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Create a `.env` file in the frontend directory:

   ```
   VUE_APP_API_URL=http://localhost:8000
   ```

4. Run the development server:
   ```
   npm run serve
   ```

The frontend will be available at http://localhost:8080.

## Key Benefits

- **Accelerated Response:** 24/7 instant engagement reduces lead response time.
- **Workload Reduction:** AI handles routine inquiries, freeing sales staff for high‑value tasks.
- **Global Reach:** Multilingual support breaks down language barriers.
- **Consistent Experience:** Standardized pricing and tone across all client interactions.
- **Smooth Handoff:** Escalation to human reps only when needed, ensuring professionalism throughout.
