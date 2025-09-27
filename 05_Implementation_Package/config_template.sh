#!/bin/bash

# 🔐 DeepSeek AI Validation Suite Configuration
# Copy this file to config.sh and fill in your API keys

echo "🔑 Setting up API keys for DeepSeek AI Validation Suite..."

# DeepSeek API (Required for uncensored generation)
export DEEPSEEK_API_KEY="your-deepseek-api-key-here"

# Claude API (Optional - for advanced technical validation)
export ANTHROPIC_API_KEY="your-claude-api-key-here"

# GLM API (Optional - for cost-effective fallback validation)
export OPENAI_API_KEY="your-glm-api-key-here"
export OPENAI_BASE_URL="https://api.z.ai/api/paas/v4"
export OPENAI_MODEL="glm-4.5-air"

echo "✅ Configuration loaded!"
echo "💡 Run 'source config.sh' to activate these settings"

# Add to bashrc for persistence (optional)
echo ""
echo "📝 To make these settings permanent, add them to your ~/.bashrc:"
echo "   cat config.sh >> ~/.bashrc"
