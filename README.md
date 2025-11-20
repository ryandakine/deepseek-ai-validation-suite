# DeepSeek AI Validation Tool

A simple web application for generating code with DeepSeek and automatically validating it for security issues using Claude, both via OpenRouter.

## Features

- 🚀 **Uncensored Code Generation**: Using DeepSeek via OpenRouter
- 🛡️ **Automated Security Validation**: Using Claude 3.5 Sonnet via OpenRouter
- 🔍 **Pattern Matching**: Fast local validation for common security issues
- 🌐 **Clean Web Interface**: Simple, modern UI for easy use

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`
   - Add your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=sk-or-v1-your-key-here
     ```

3. **Run the App**:
   ```bash
   python app.py
   ```

4. **Open Browser**:
   - Navigate to http://localhost:5000

## Usage

### Generate & Validate
1. Enter a description of the code you want to generate
2. Click "Generate & Validate"
3. View the generated code and its security analysis

### Validate Only
1. Paste existing code into the text area
2. Click "Validate Code"
3. Review the security assessment

## API Endpoints

- `POST /generate` - Generate code from a prompt
- `POST /validate` - Validate code for security issues
- `POST /generate-and-validate` - Generate and validate in one call
- `GET /health` - Health check

## Security Notes

- The `.env` file is gitignored to protect your API keys
- Never commit API keys to version control
- Risk scores range from 0.0 (safe) to 1.0 (dangerous)

## License

MIT