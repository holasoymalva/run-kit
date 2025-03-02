# {{ project_name }}

An AI application generated with RunKit.

## Features

- LLM Provider: {{ provider }}
{% for feature in features %}
- {{ feature }}
{% endfor %}
- Project Type: {{ project_type }}

## Getting Started

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file to add your API keys.

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
{{ project_name }}/
├── app.py                 # Entry point
├── .env                   # Environment variables
├── .env.example           # Example environment variables
├── requirements.txt       # Dependencies
├── app/
│   ├── components/        # UI components
│   ├── llm/               # LLM connection logic
│   ├── utils/             # General utilities
│   ├── data/              # Data and resources
│   └── styles/            # Custom CSS
└── tests/                 # Unit tests
```

## Customization

This project is a starting point. Feel free to modify the code to suit your needs.

## License

This project is licensed under the MIT License.