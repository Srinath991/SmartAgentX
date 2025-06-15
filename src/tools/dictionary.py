from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field
import requests

class DictionaryInput(BaseModel):
    word: str = Field(description="The word to look up in the dictionary")

class DictionaryTool(BaseTool):
    name: str = "dictionary"
    description: str = "Useful for looking up definitions, synonyms, and examples of English words"
    args_schema: Type[BaseModel] = DictionaryInput

    def _run(self, word: str) -> str:
        try:
            # Using Free Dictionary API
            base_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            
            response = requests.get(base_url)
            data = response.json()
            
            if response.status_code != 200:
                return f"Error: Word '{word}' not found in dictionary"
            
            result = []
            for entry in data:
                word = entry.get("word", "")
                phonetic = entry.get("phonetic", "")
                result.append(f"Word: {word}")
                if phonetic:
                    result.append(f"Phonetic: {phonetic}")
                
                meanings = entry.get("meanings", [])
                for meaning in meanings:
                    part_of_speech = meaning.get("partOfSpeech", "")
                    result.append(f"\nPart of Speech: {part_of_speech}")
                    
                    definitions = meaning.get("definitions", [])
                    for i, definition in enumerate(definitions, 1):
                        def_text = definition.get("definition", "")
                        example = definition.get("example", "")
                        
                        result.append(f"{i}. Definition: {def_text}")
                        if example:
                            result.append(f"   Example: {example}")
                    
                    synonyms = meaning.get("synonyms", [])
                    if synonyms:
                        result.append(f"   Synonyms: {', '.join(synonyms)}")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error looking up word: {str(e)}"

    async def _arun(self, word: str) -> str:
        return self._run(word) 