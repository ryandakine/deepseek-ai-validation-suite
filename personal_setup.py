#!/usr/bin/env python3
"""
🏠 PERSONAL SETUP FOR RYAN'S DAILY USE
=====================================

This sets up the AI validation suite for your personal daily workflow.
No pressure, no public launch - just a powerful tool for YOUR code.

Usage:
  python3 personal_setup.py
"""

import os
import sys
from pathlib import Path

def setup_personal_environment():
    """Set up the environment for personal daily use"""
    print("🏠 Setting up your personal AI code validation environment...")
    
    # Check if we're in the right directory
    if not Path("winning_demo.py").exists():
        print("❌ Please run this from the deepseek-ai-validation-suite directory")
        sys.exit(1)
    
    # Create personal config directory
    personal_dir = Path.home() / ".ai-validator"
    personal_dir.mkdir(exist_ok=True)
    print(f"✅ Created personal config directory: {personal_dir}")
    
    # Create a simple daily usage script
    daily_script = personal_dir / "daily_validate.py"
    
    daily_script_content = '''#!/usr/bin/env python3
"""
🛡️ DAILY CODE VALIDATOR - Your Personal AI Assistant
===================================================

Quick validation for your daily coding work.
"""

import sys
import asyncio
from pathlib import Path

# Add the main directory to path
sys.path.append("''' + str(Path.cwd()) + '''")

from winning_demo import WinningDemo

async def validate_my_code():
    """Quick validation without emails - just for you"""
    if len(sys.argv) < 2:
        print("Usage: python3 daily_validate.py <path_to_your_code.py>")
        print("Example: python3 daily_validate.py ~/my_project/main.py")
        return
    
    code_file = Path(sys.argv[1])
    if not code_file.exists():
        print(f"❌ File not found: {code_file}")
        return
    
    # Read your code
    with open(code_file, 'r') as f:
        code_content = f.read()
    
    print(f"🔍 Analyzing your code: {code_file.name}")
    print("=" * 50)
    
    # Initialize the validator (no emails, just analysis)
    demo = WinningDemo()
    
    # Quick validation
    from real_ai_validator import RealAIValidator
    validator = RealAIValidator()
    
    result = await validator.quick_validate(code_content)
    
    # Show results
    risk_score = result.get('risk_score', 0)
    issues = result.get('issues', [])
    agent = result.get('agent', 'AI Validator')
    
    print(f"🤖 Agent: {agent}")
    print(f"⚡ Risk Score: {risk_score:.2f}/1.0")
    
    if risk_score > 0.7:
        print("🚨 HIGH RISK - Review recommended")
    elif risk_score > 0.4:
        print("⚠️  MEDIUM RISK - Some issues found")
    else:
        print("✅ LOW RISK - Looking good!")
    
    if issues:
        print(f"\\n🛡️ Issues found ({len(issues)}):")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print("\\n🎉 No issues detected!")
    
    print("\\n" + "="*50)
    print("💡 This is your personal AI validator - use it daily!")

if __name__ == "__main__":
    asyncio.run(validate_my_code())
'''
    
    with open(daily_script, 'w') as f:
        f.write(daily_script_content)
    
    # Make it executable
    os.chmod(daily_script, 0o755)
    print(f"✅ Created daily validation script: {daily_script}")
    
    # Create alias setup
    alias_setup = personal_dir / "setup_aliases.sh"
    alias_content = f'''#!/bin/bash
# Add these aliases to your ~/.zshrc for easy access

echo "Adding AI validator aliases to your shell..."

# Add to zshrc
cat >> ~/.zshrc << 'EOF'

# 🛡️ AI Code Validator Aliases
alias validate="python3 {daily_script}"
alias ai-check="python3 {daily_script}"
alias code-check="cd {Path.cwd()} && python3 winning_demo.py"
alias ai-demo="cd {Path.cwd()} && python3 claude_45_showcase_demo.py"

EOF

echo "✅ Aliases added! Restart your terminal or run: source ~/.zshrc"
echo ""
echo "🚀 Your new commands:"
echo "  validate ~/my_code.py    # Quick validation of any file"
echo "  ai-check ~/project.py    # Same as validate"
echo "  code-check              # Full demo mode"
echo "  ai-demo                 # Claude 4.5 showcase"
'''
    
    with open(alias_setup, 'w') as f:
        f.write(alias_content)
    
    os.chmod(alias_setup, 0o755)
    print(f"✅ Created alias setup script: {alias_setup}")
    
    # Create a simple README for personal use
    personal_readme = personal_dir / "README.md"
    readme_content = '''# 🏠 Your Personal AI Code Validator

This is YOUR private AI validation suite. No pressure, no public launch - just a powerful tool for your daily coding.

## Quick Start

### Daily Validation
```bash
# Validate any Python file
validate ~/my_project/main.py
ai-check ~/code/script.py
```

### Full Demo Mode
```bash
code-check    # Run the full demo
ai-demo       # Claude 4.5 showcase
```

## What It Does

- ✅ **Security Analysis**: Finds vulnerabilities in your code
- ✅ **Bug Detection**: Spots potential issues before they bite you
- ✅ **Performance Tips**: Suggests optimizations
- ✅ **Best Practices**: Keeps your code clean and professional
- ✅ **Multi-AI Analysis**: Uses different AI models for comprehensive review

## Your Personal Benefits

1. **Catch Issues Early**: Before they become problems
2. **Learn Better Practices**: Each analysis teaches you something
3. **Confidence Boost**: Know your code is solid before deployment
4. **Time Saver**: Automated review instead of manual checking
5. **Private & Safe**: Everything stays on your machine

## No Pressure Zone

This is your personal tool. Use it when you want, how you want. If it helps your daily coding, great! If not, no worries. It's here when you need it.

## API Keys (Optional)

If you want to use premium features:
- Set `CLAUDE_API_KEY` for Claude 4.5 analysis
- Set `OPENAI_API_KEY` for GPT-4 analysis
- Set `GOOGLE_API_KEY` for Gemini analysis

But the free version works great too!
'''
    
    with open(personal_readme, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Created personal README: {personal_readme}")
    
    # Final setup
    print("\n🎉 PERSONAL SETUP COMPLETE!")
    print("=" * 40)
    print(f"📁 Your config: {personal_dir}")
    print(f"🛡️ Daily validator: {daily_script}")
    print(f"📖 Personal guide: {personal_readme}")
    
    print(f"\n🚀 To complete setup, run:")
    print(f"   bash {alias_setup}")
    
    print(f"\n💡 Then you can use:")
    print(f"   validate ~/my_code.py")
    print(f"   ai-check ~/project.py")
    print(f"   code-check")
    
    print(f"\n🏠 This is YOUR tool now. Use it however helps YOU most!")

if __name__ == "__main__":
    setup_personal_environment()