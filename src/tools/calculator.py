from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(description="The mathematical expression to evaluate")

class CalculatorTool(BaseTool):
    name: str = "calculator"
    description: str = "Useful for performing mathematical calculations"
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(self, expression: str) -> str:
        try:
            # Using eval is not recommended for production, but for demo purposes
            result = eval(expression)
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Error calculating expression: {str(e)}"

    async def _arun(self, expression: str) -> str:
        return self._run(expression) 