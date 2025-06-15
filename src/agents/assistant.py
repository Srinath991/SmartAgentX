from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent
from langchain import hub
from typing import List
from ..tools.calculator import CalculatorTool
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
        SearchTool(),
    ]

    # Create the prompt template
    prompt =hub.pull('hwchase17/react',api_key=settings.LANGSMITH_API_KEY)

    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )

    return agent_executor 