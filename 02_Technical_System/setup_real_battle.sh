#!/bin/bash
# 🔥 REAL LLM BATTLE ARENA SETUP
# Configure API keys for genuine LLM battles

echo "🔥 REAL LLM BATTLE ARENA SETUP"
echo "=============================="
echo ""
echo "To enable REAL LLM battles (not mock), set your API keys:"
echo ""

echo "📋 AVAILABLE LLMS FOR BATTLE:"
echo "  1. OpenAI GPT-4 (Perfectionist) - OPENAI_API_KEY"
echo "  2. Anthropic Claude-3 (Optimistic) - ANTHROPIC_API_KEY" 
echo "  3. DeepSeek Coder (Security Paranoid) - DEEPSEEK_API_KEY"
echo "  4. Google Gemini Pro (Philosophical) - GEMINI_API_KEY"
echo "  5. Local LLM via Ollama (Chaotic) - No key needed"
echo ""

echo "🔧 HOW TO SET API KEYS:"
echo "  export OPENAI_API_KEY='your-openai-api-key-here'"
echo "  export ANTHROPIC_API_KEY='your-anthropic-api-key-here'"
echo "  export DEEPSEEK_API_KEY='your-deepseek-api-key-here'"
echo "  export GEMINI_API_KEY='your-gemini-api-key-here'"
echo ""

echo "🚀 TESTING THE REAL BATTLE:"
echo "  # Test with current API keys:"
echo "  python3 real_llm_battle.py 'def test(): return True' general_validation"
echo ""
echo "  # Or test via the full validation system:"
echo "  echo '{\"code\": \"def test(): return True\", \"type\": \"general_validation\", \"unhinged_mode\": true}' | python3 validation_api.py"
echo ""

echo "⚠️  CURRENT API KEY STATUS:"
if [ -n "$OPENAI_API_KEY" ]; then
    echo "  ✅ OPENAI_API_KEY: Set (${OPENAI_API_KEY:0:8}...)"
else
    echo "  ❌ OPENAI_API_KEY: Not set"
fi

if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "  ✅ ANTHROPIC_API_KEY: Set (${ANTHROPIC_API_KEY:0:8}...)"
else
    echo "  ❌ ANTHROPIC_API_KEY: Not set"
fi

if [ -n "$DEEPSEEK_API_KEY" ]; then
    echo "  ✅ DEEPSEEK_API_KEY: Set (${DEEPSEEK_API_KEY:0:8}...)"
else
    echo "  ❌ DEEPSEEK_API_KEY: Not set"
fi

if [ -n "$GEMINI_API_KEY" ]; then
    echo "  ✅ GEMINI_API_KEY: Set (${GEMINI_API_KEY:0:8}...)"
else
    echo "  ❌ GEMINI_API_KEY: Not set"
fi

# Check if Ollama is running for local LLM
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  ✅ LOCAL LLM (Ollama): Running"
else
    echo "  ⚠️ LOCAL LLM (Ollama): Not running (install with: curl -fsSL https://ollama.ai/install.sh | sh)"
fi

echo ""
echo "💡 TIP: You need at least 2 API keys for real battles!"
echo "     If no keys are available, the system falls back to mock battles."
echo ""

# Count available LLMs
available_count=0
if [ -n "$OPENAI_API_KEY" ]; then ((available_count++)); fi
if [ -n "$ANTHROPIC_API_KEY" ]; then ((available_count++)); fi
if [ -n "$DEEPSEEK_API_KEY" ]; then ((available_count++)); fi
if [ -n "$GEMINI_API_KEY" ]; then ((available_count++)); fi
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then ((available_count++)); fi

if [ $available_count -ge 2 ]; then
    echo "🎉 READY FOR REAL BATTLES! ($available_count LLMs available)"
else
    echo "🤖 Only $available_count LLM(s) available - will use mock battles"
fi

echo ""
echo "🔥 LET THE BATTLE BEGIN!"