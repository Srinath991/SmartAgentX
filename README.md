# Smart Agent X - Multi-Tool AI Assistant

A powerful AI assistant that can use multiple tools to help answer questions and perform tasks. Built with LangChain, FastAPI, and Google's Gemini model.

## Features

- Calculator tool for mathematical calculations
- PDF reader for extracting text from PDF files
- Web search capability for finding information online
- FastAPI backend for easy integration
- Powered by Google's Gemini model

## Setup

1. Install dependencies using uv:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
uv pip install -e .
```

2. Create a `.env` file in the root directory with your configuration:
```
GOOGLE_API_KEY=your_google_api_key_here
MODEL_NAME=gemini-pro
TEMPERATURE=0.7
MAX_TOKENS=1000
```

3. Run the FastAPI server:
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

## Example Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "text": "What is 2 + 2?",
        "chat_history": []
    }
)
print(response.json())
```

## Tools

1. Calculator
   - Performs mathematical calculations
   - Example: "Calculate 2 + 2"

2. PDF Reader
   - Reads and extracts text from PDF files
   - Example: "Read the first page of document.pdf"

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
│   ├── pdf_reader.py
│   └── search.py
├── api/
│   └── main.py
└── config/
    └── settings.py
```

## License

MIT
