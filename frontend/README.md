# B2B Sales Support Chatbot - Frontend

This is the frontend application for the B2B Sales Support Chatbot. It provides a user interface for interacting with the AI-powered sales support system.

## Core Features

- Interactive chat interface
- Real-time conversation with AI chatbot
- Multilingual support
- Dynamic pricing display
- Order inquiry creation
- Responsive design for desktop and mobile

## Technology Stack

- **Frontend Framework:** Vue.js 3
- **State Management:** Vuex 4
- **Routing:** Vue Router 4
- **HTTP Client:** Axios
- **Styling:** CSS with custom variables

## Setup

1. Install dependencies:

   ```
   npm install
   ```

2. Configure environment variables (create a `.env` file):

   ```
   VUE_APP_API_URL=http://localhost:8000
   ```

3. Run the development server:

   ```
   npm run serve
   ```

4. Build for production:
   ```
   npm run build
   ```

## Application Structure

- `src/components/` - Reusable Vue components
- `src/views/` - Page components corresponding to routes
- `src/store/` - Vuex store modules for state management
- `src/router/` - Vue Router configuration
- `src/assets/` - Static assets and global styles

## Main Features

### Chat Interface

The chat interface allows users to communicate with the AI chatbot in real-time. Users can:

- Send messages
- Receive AI-generated responses
- View conversation history
- Start a new conversation

### Requirements Collection

The chatbot collects user requirements through natural conversation, extracting key information about what features and products they need.

### Pricing Display

Once sufficient requirements are gathered, the system displays a pricing summary including:

- Base price
- Any applicable discounts
- Final price

### Order Creation

Users can confirm their order directly from the chat interface, which creates an order inquiry in the backend system and provides an order reference number.

### Human Handoff

If users need additional assistance, they can request to speak with a human sales representative.
