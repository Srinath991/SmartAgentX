from langchain.tools import BaseTool
from typing import Optional, Type, Any
from pydantic import BaseModel, Field
import PyPDF2
import io

class PDFReaderInput(BaseModel):
    file_path: str = Field(description="Path to the PDF file to read")
    page_number: Optional[int] = Field(default=None, description="Specific page number to read (optional)")

class PDFReaderTool(BaseTool):
    name: str = "pdf_reader"
    description: str = "Useful for reading and extracting text from PDF files"
    args_schema: Type[BaseModel] = PDFReaderInput

    def _run(self, file_path: str, page_number: Optional[int] = None) -> str:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if page_number is not None:
                    if page_number < 0 or page_number >= len(pdf_reader.pages):
                        return f"Error: Page number {page_number} is out of range. PDF has {len(pdf_reader.pages)} pages."
                    return pdf_reader.pages[page_number].extract_text()
                
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    async def _arun(self, file_path: str, page_number: Optional[int] = None) -> str:
        return self._run(file_path, page_number) 