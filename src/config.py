import os
from dotenv import load_dotenv, find_dotenv

class Config:
    def __init__(self):
        # Load environment variables
        current_dir = os.getcwd()
        root_dir = os.path.dirname(current_dir)
        data_dir = os.path.join(root_dir, 'data')
        env_path = find_dotenv()
        load_dotenv(env_path)
        
        # API Keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.hf_api_key = os.getenv('HF_API_KEY')
        
        # OpenAI Configuration
        self.openai_model = os.getenv('OPENAI_MODEL')
        self.openai_max_tokens = int(os.getenv('OPENAI_MAX_TOKENS'))
        self.openai_temperature = float(os.getenv('OPENAI_TEMPERATURE'))
        
        # HuggingFace Configuration
        self.hf_model = os.getenv('HF_MODEL')
        self.hf_max_tokens = int(os.getenv('HF_MAX_TOKENS'))
        self.hf_temperature = float(os.getenv('HF_TEMPERATURE'))
        self.hf_wait_for_model = os.getenv('HF_WAIT_FOR_MODEL').lower() == 'true'
        self.hf_use_cache = os.getenv('HF_USE_CACHE').lower() == 'true'
        
    def validate(self):
        """Validate required configuration parameters"""
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        if not self.hf_api_key:
            raise ValueError("HF_API_KEY is required")