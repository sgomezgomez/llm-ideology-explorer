import openai
import time
from abc import ABC, abstractmethod
from huggingface_hub import InferenceClient
from typing import Dict, Any, Optional
from requests.exceptions import HTTPError, Timeout
from src.config import Config

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_response(self, prompt: str, model: Optional[str] = None) -> str:
        """Generate a response from the LLM"""
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, config: Config):
        self.llm_provider = 'OpenAI_API'
        self.config = config
        openai.api_key = config.openai_api_key
        
    def generate_response(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Generates a response using OpenAI's API.

        Args:
            prompt (str): Prompt text to send to model
            model (Optional[str], optional): OpenAI model identifier. Defaults to configured model.

        Returns:
            str: Model's response text or error message

        Example:
            provider = OpenAIProvider(config)
            response = provider.generate_response("Tell me about...", model="gpt-4")
        """
        try:
            response = openai.chat.completions.create(
                model=model or self.config.openai_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.config.openai_max_tokens,
                temperature=self.config.openai_temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

class HuggingFaceProvider(LLMProvider):
    def __init__(self, config: Config):
        """
        Initialize HuggingFace provider using configuration
        
        Args:
            config: Configuration object containing all necessary parameters
        """
        self.llm_provider = 'HF_API'
        self.config = config
        self.client = InferenceClient(
            model=config.hf_model,
            token=config.hf_api_key,
            headers={
                "x-wait-for-model": "true",  # Wait for model to load
                "x-use-cache": "false" # Disable caching for demo purposes
            },
            timeout=60  # 60 second timeout
        )

    def generate_response(self, prompt: str, model: Optional[str] = None, max_retries: int = 3) -> str:
        """
        Generates a response using HuggingFace's Inference API with retry logic.

        Args:
            prompt (str): Prompt text to send to model
            model (Optional[str], optional): HuggingFace model identifier. Defaults to configured model.
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.

        Returns:
            str: Model's response text or error message

        Example:
            provider = HuggingFaceProvider(config)
            response = provider.generate_response("Tell me about...", 
                                            model="meta-llama/Llama-2-70b-chat-hf",
                                            max_retries=5)
        """
        for attempt in range(max_retries):
            try:
                # If model is specified, create a new client for it
                client = self.client if model is None else InferenceClient(
                    model=model,
                    token=self.config.hf_api_key,
                    headers={"x-wait-for-model": "true", "x-use-cache": "false"},
                    timeout=60
                )
                
                response = client.chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.config.hf_max_tokens,
                    temperature=self.config.hf_temperature
                )
                return response.choices[0].message.content
                
            except HTTPError as e:
                if e.response.status_code == 503:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5  # Progressive backoff
                        print(f"Model loading, waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                return f"Error: Model unavailable after {max_retries} attempts"
                
            except Timeout:
                return "Error: Request timed out"
                
            except Exception as e:
                return f"Error generating response: {str(e)}"
        
        return "Error: Maximum retries exceeded"