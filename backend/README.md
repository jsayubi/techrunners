# B2B Sales Support Chatbot - Backend

This is the backend service for the B2B Sales Support Chatbot. It provides the API and processing logic for the AI-powered sales support system.

## Core Capabilities

- **Smart Greetings:** Instant, friendly welcome in the client's preferred language.
- **Product Expertise:** Answers detailed product questions with up‑to‑date information.
- **Requirements Gathering:** Clarifies client needs and requirements.
- **Dynamic Pricing:** Leverages historical deal data to recommend initial quotes.
- **Confirmation & Negotiation:** Handles order approval or connects with human sales reps.
- **Seamless Multilingual Support:** Translates both inbound and outbound messages in real time.

## Technology Stack

- **Backend Framework:** FastAPI
- **AI Services:** AWS Bedrock
- **Translation:** AWS Translate
- **Database:** PostgreSQL (simulated with in-memory storage for demo)
- **Integration:** CRM API integration for order creation

## Setup

1. Create and activate a virtual environment:

   ```
   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Configure environment variables (create a `.env` file):

   ```
   DEBUG=True
   AWS_REGION=eu-central-1
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   BEDROCK_MODEL_ID=eu.anthropic.claude-3-7-sonnet-20250219-v1:0
   ```

4. Run the application:
   ```
   python run.py
   ```

## API Endpoints

- `GET /` - Root endpoint
- `POST /chat` - Process chat messages
- `POST /pricing` - Calculate pricing based on requirements
- `POST /create-order` - Create an order inquiry in the CRM system

## Development

The application uses FastAPI with automatic API documentation. Once running, you can access the API docs at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
