from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from typing import List
from ..tools.calculator import CalculatorTool
from ..tools.pdf_reader import PDFReaderTool
from ..tools.search import SearchTool
from ..config.settings import get_settings

settings = get_settings()

def create_agent() -> AgentExecutor:
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model=settings.MODEL_NAME,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=settings.TEMPERATURE,
    )

    # Initialize tools
    tools = [
        CalculatorTool(),
        PDFReaderTool(),
        SearchTool(),
    ]

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant with access to various tools.
        Use these tools to help answer user questions:
        - Calculator: For mathematical calculations
        - PDF Reader: For reading and extracting text from PDF files
        - Search: For searching information on the internet
        
        Always think step by step about which tool would be most appropriate for the task.
        If you're unsure, explain your reasoning to the user."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

    return agent_executor 