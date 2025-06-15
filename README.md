# Smart Agent X - Multi-Tool AI Assistant

A powerful AI assistant that can use multiple tools to help answer questions and perform tasks. Built with LangChain, FastAPI, and Google's Gemini model.

## Features

- Calculator tool for mathematical calculations
- Web search capability for finding information online
- FastAPI backend for easy integration
- Powered by Google's Gemini model

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Srinath991/SmartAgentX
cd smart-agent-x
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your Google API key:
     ```
     GOOGLE_API_KEY=your_actual_google_api_key_here
     ```

4. Run the FastAPI server:
```bash
uvicorn src.api.main:app --reload
```

## API Endpoints

- `POST /query`: Send queries to the AI assistant
  ```json
  {
    "text": "What is 2 + 2?",
    "chat_history": []
  }
  ```

- `GET /health`: Check the health status of the service

## Tools

1. Calculator
   - Performs mathematical calculations
   - Example: "Calculate 2 + 2"

3. Search
   - Searches the web for information
   - Example: "Search for information about Python programming"

## Development

The project structure is organized as follows:

```
src/
├── agents/
│   └── assistant.py
├── tools/
│   ├── calculator.py
│   └── search.py
├── api/
│   └── main.py
└── config/
    └── settings.py
```

## Environment Variables

The following environment variables can be configured in `.env`:

- `GOOGLE_API_KEY`: Your Google API key (required)
- `MODEL_NAME`: The model to use (default: gemini-pro)
- `TEMPERATURE`: Model temperature (default: 0.7)
- `MAX_TOKENS`: Maximum tokens for responses (default: 1000)

## License

MIT
