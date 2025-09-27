#!/bin/bash

echo "🚀 Installing DeepSeek AI Validation Suite..."
echo "============================================="

# Make scripts executable
chmod +x *.py
chmod +x ds
chmod +x shell-bridge 2>/dev/null
chmod +x fuckit 2>/dev/null

# Create symbolic links for easy access
echo "🔗 Creating convenient shortcuts..."

# Create ds shortcut if not exists
if [ ! -f "/usr/local/bin/ds" ]; then
    sudo ln -sf "$(pwd)/ds" /usr/local/bin/ds 2>/dev/null && echo "   ✅ ds command available globally" || echo "   ⚠️ Could not create global ds shortcut"
fi

# Setup smart router for Cursor (optional)
echo ""
echo "🎯 Optional: Setup Cursor Integration"
echo "======================================"
echo "To integrate with Cursor IDE, run:"
echo "   sudo ln -sf $(pwd)/smart_ai_router.py /usr/local/bin/claude"
echo ""
echo "⚠️  This replaces any existing 'claude' command!"
echo "   Type 'y' to proceed, 'n' to skip:"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    sudo ln -sf "$(pwd)/smart_ai_router.py" /usr/local/bin/claude && echo "   ✅ Cursor integration enabled" || echo "   ❌ Failed to setup Cursor integration"
fi

# Create results directories
mkdir -p technical_validation_results
mkdir -p deepseek_validation_results

echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "🚀 Quick Start Commands:"
echo "   ./ds 'your prompt here'                    # Quick DeepSeek access"
echo "   python technical_code_validator.py -i     # Technical validation"
echo "   python ultimate_deepseek_claude_gui.py    # Full GUI interface"
echo ""
echo "📚 Read README.md for full documentation and examples"
echo "💡 Check system_status.md for configuration help"

