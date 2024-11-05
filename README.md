# LLM Ideology Explorer

Educational toolkit demonstrating a two-stage prompting methodology for analyzing ideological biases in Large Language Models (LLMs), based on research by Buyl et al. (2024).

## Overview

This project provides tools to analyze how different LLMs describe and evaluate political figures across different languages (English and Chinese). It uses a structured approach:

1. First stage prompts LLMs for factual descriptions
2. Second stage analyzes sentiment and ideological bias
3. Supports comparison across multiple models and languages

## Features

- 🌐 Multi-language support (English & Chinese)
- 🤖 Multiple LLM provider integration (OpenAI & HuggingFace)
- 📊 Structured analysis pipeline
- 🔄 Reproducible methodology
- 📝 Detailed sentiment analysis
- 💾 Dataset curation tools

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/llm-ideology-explorer.git
cd llm-ideology-explorer
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows, use: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```
OPENAI_API_KEY=your-key-here
HF_API_KEY=your-key-here
```

## Configuration

The project uses environment variables for configuration. Key settings in `.env`:

```env
# API Keys
OPENAI_API_KEY=your-key-here
HF_API_KEY=your-key-here

# OpenAI Configuration
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7

# HuggingFace Configuration
HF_MODEL=meta-llama/Meta-Llama-3-70B-Instruct
HF_MAX_TOKENS=500
HF_TEMPERATURE=0.7
```

## Usage

### Basic Analysis

```python
from src.utils import IdeologyAnalyzer

# Initialize analyzer
analyzer = IdeologyAnalyzer()

# Analyze a political figure
results = analyzer.analyze_figure(
    figure_name="Nelson Mandela",
    model="gpt-4",
    llm_provider="openai_provider",
    language="en",
    verbose=True
)
```

### Multi-Language Analysis

```python
# Analyze in Chinese
results_cn = analyzer.analyze_figure(
    figure_name="Nelson Mandela",
    model="meta-llama/Meta-Llama-3-70B-Instruct",
    llm_provider="hf_provider",
    language="cn",
    verbose=True
)
```

### Notebook Examples

Check the `notebooks/` directory for detailed examples:
- `dataset-curation-notebook.ipynb`: Dataset preparation and curation
- `llm_ideology_demo.ipynb`: Step-by-step analysis demonstrations

## Project Structure

```
llm-ideology-explorer/
├── data/                  # Dataset storage
├── notebooks/            # Example notebooks
├── src/                  # Source code
│   ├── llm_providers.py  # LLM API integrations
│   ├── prompts.py        # Prompt templates
│   ├── utils.py          # Analysis utilities
│   └── config.py         # Configuration handling
├── tests/                # Test suite
└── .env                  # Environment variables
```

## Advanced Usage

### Custom Providers

You can implement custom LLM providers by extending the `LLMProvider` base class:

```python
from src.llm_providers import LLMProvider

class CustomProvider(LLMProvider):
    def generate_response(self, prompt: str, model: Optional[str] = None) -> str:
        # Implementation here
        pass
```

### Dataset Curation

To work with your own dataset:

1. Prepare your data following the format in `data/example_data.json`
2. Use the dataset curation notebook as a template
3. Update the `DATASET_ID` in your `.env` file

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## Citation

If you use this toolkit in your research, please cite:

```bibtex
@misc{buyl2024,
  title={Analyzing Ideological Biases in Large Language Models},
  author={Buyl, et al.},
  year={2024}
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Research methodology based on work by Buyl et al. (2024)
- Thanks to OpenAI and HuggingFace for their API services

