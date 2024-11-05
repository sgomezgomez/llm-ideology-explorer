from typing import Dict, Any, Optional
from .prompts import PromptTemplates
from .llm_providers import OpenAIProvider, HuggingFaceProvider
from src.config import Config
from IPython.display import display, Markdown

class IdeologyAnalyzer:
    def __init__(self):
        # Initiate config instance
        self.config = Config()
        # Initiate LLM provider instances
        self.openai_provider = OpenAIProvider(self.config)
        self.hf_provider = HuggingFaceProvider(self.config)
        self.prompts = PromptTemplates()

    def print_header(self, name: str, model: str, language: str):
        display(Markdown(f"### Analyzing **{name}**"))
        display(Markdown(f"*Model: {model or 'default'} | Language: {language.upper()}*"))

    def print_response(self, response: str, prefix: str = "Response", verbose: bool = False):
        if not verbose:
            response = self.truncate_response(response, max_length=200)
        display(Markdown(f"**{prefix}:** {response}"))

    def _get_sentiment_style(self, response: str) -> str:
        sentiment_colors = {
            'very negative': 'red',
            'negative': 'orange',
            'neutral': 'blue',
            'positive': 'green',
            'very positive': 'darkgreen',
            # Chinese translations
            '非常负面': 'red',
            '负面': 'orange',
            '中性': 'blue',
            '正面': 'green',
            '非常正面': 'darkgreen'
        }
        return sentiment_colors.get(response.strip().lower(), 'black')

    def _get_sentiment_label(self, response: str) -> str:
        sentiment_labels = {
            'very negative': '😠 Very Negative',
            'negative': '😞 Negative',
            'neutral': '😐 Neutral',
            'positive': '😊 Positive',
            'very positive': '😄 Very Positive',
            # Chinese translations
            '非常负面': '😠 非常负面 - Very Negative',
            '负面': '😞 负面 - Negative',
            '中性': '😐 中性 - Neutral',
            '正面': '😊 正面 - Positive',
            '非常正面': '😄 非常正面 - Very Positive'
        }
        return sentiment_labels.get(response.strip().lower(), '❓ Unknown')

    def truncate_response(self, response: str, max_length: int = 600) -> str:
        if len(response) <= max_length:
            return response
        else:
            truncated = response[:max_length].rsplit(' ', 1)[0]
            return truncated.strip() + '...'
    
    def generate_response(self, llm_provider: str, model: str, prompt: str):
        if llm_provider == "hf_provider":
            response = self.hf_provider.generate_response(prompt=prompt, model=model)
        elif llm_provider == "openai_provider":
            response = self.openai_provider.generate_response(prompt, model=model)
        return response 
    
    def run_prompt(self,
                   figure_name: str, 
                   translated_name: str,
                   model: str,
                   llm_provider: str,
                   stage1_response: Optional[str] = None,
                   language: str = "en", 
                   stage: int = 0,
                   verbose: bool = False):
        """
        Executes a prompt stage of the analysis pipeline.

        Args:
            figure_name (str): Original name of figure being analyzed
            translated_name (str): Translated name (for Chinese analysis)
            model (str): Model name/identifier
            llm_provider (str): Provider to use ("hf_provider" or "openai_provider")
            stage1_response (Optional[str]): Response from stage 1 (needed for stage 2)
            language (str, optional): Language code (en/cn). Defaults to "en".
            stage (int, optional): Analysis stage (0=translation, 1=description, 2=evaluation). Defaults to 0.
            verbose (bool, optional): Whether to show full responses. Defaults to False.

        Returns:
            Tuple[str, str]: Tuple containing (prompt_text, response_text)"""
        if stage == 0:
            if language == "cn":
                display(Markdown(f"#### 🀄 Step 0: Translating {figure_name} into Chinese"))
                prompt = (self.prompts.STAGE0_CN).format(name=figure_name)
                prefix = "Translation"
        elif stage == 1:
            display(Markdown(f"#### 📝 Step 1: Describing {figure_name}"))
            prompt =  (self.prompts.STAGE1_EN if language == "en" 
                         else self.prompts.STAGE1_CN).format(name=translated_name)
            prefix = "Description"
        elif stage == 2:
            display(Markdown(f"#### ⚖️ Step 2: Evaluating sentiment for {figure_name}"))
            prompt = (self.prompts.STAGE2_EN if language == "en"
                         else self.prompts.STAGE2_CN).format(name=translated_name, previous_response=stage1_response)
            prefix = "Evaluation"
        self.print_response(response=prompt, prefix="Prompt", verbose=verbose)
        response = self.generate_response(llm_provider, model, prompt=prompt)
        self.print_response(response, prefix, verbose)
        return prompt, response

    def analyze_figure(self, 
                       figure_name: str, 
                       model: str = None, 
                       llm_provider: str = "hf_provider", 
                       language: str = "en", 
                       verbose: bool = False) -> Dict[str, Any]:
        """
        Performs complete analysis of a political figure using the configured pipeline.

        Args:
            figure_name (str): Name of figure to analyze
            model (str, optional): Model to use. Defaults to None (uses configured default).
            llm_provider (str, optional): Provider to use. Defaults to "hf_provider".
            language (str, optional): Language code (en/cn). Defaults to "en".
            verbose (bool, optional): Whether to show full responses. Defaults to False.

        Returns:
            Dict[str, Any]: Analysis results containing:
                - name: Figure name
                - language: Language used
                - model: Model used
                - stage0_response: Translation (Chinese only)
                - stage1_response: Description
                - stage2_response: Evaluation

        Example:
            results = analyzer.analyze_figure("Nelson Mandela", 
                                            model="gpt-4",
                                            llm_provider="openai_provider",
                                            language="en",
                                            verbose=True)
        """
        results = {}

        # Model name
        if model is None:
            if self.llm_provider.llm_provider == 'HF_API':
                model = self.llm_provider.config.hf_model
            elif self.llm_provider.llm_provider == 'OpenAI_API':
                model = self.llm_provider.config.openai_model
            else:
                return f"Error: Provider not supported"
        
        # Header
        self.print_header(figure_name, model, language)

        # Stage 0, Translate figure name to Chinese if required
        translated_name = figure_name
        if language == "cn":
            stage0_prompt, stage0_response = self.run_prompt(
                figure_name=figure_name, 
                translated_name="", 
                model=model, 
                llm_provider=llm_provider, 
                stage1_response="", 
                language=language, 
                stage=0, 
                verbose=verbose
            )
            results["stage0_prompt"] = stage0_prompt
            results["stage0_response"] = stage0_response
            translated_name = stage0_response

        # Stage 1: Get description
        stage1_prompt, stage1_response = self.run_prompt(
            figure_name=figure_name, 
            translated_name=translated_name, 
            model=model, 
            llm_provider=llm_provider, 
            stage1_response="", 
            language=language, 
            stage=1, 
            verbose=verbose
        )
        results["stage1_prompt"] = stage1_prompt
        results["stage1_response"] = stage1_response

        # Stage 2: Get evaluation
        stage2_prompt, stage2_response = self.run_prompt(
            figure_name=figure_name, 
            translated_name=translated_name, 
            model=model, 
            llm_provider=llm_provider, 
            stage1_response=stage1_response, 
            language=language, 
            stage=2, 
            verbose=verbose
        )
        results["stage2_prompt"] = stage2_prompt
        results["stage2_response"] = stage2_response

        # Print final result with color-coded sentiment
        sentiment_color = self._get_sentiment_style(stage2_response)
        sentiment_label = self._get_sentiment_label(stage2_response)
        display(Markdown(f"#### ✅ Sentiment evaluation for {figure_name}"))
        display(Markdown(f"**Sentiment**: <span style='color:{sentiment_color}'>{sentiment_label}</span>"))

        return {
            "name": figure_name,
            "language": language,
            "model": model or "default",
            **results
        }