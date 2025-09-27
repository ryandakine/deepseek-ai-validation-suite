#!/usr/bin/env python3
"""
🔧 Technical Code Validator - Content Neutral
Validates code quality WITHOUT content judgment. Claude focuses ONLY on technical issues:
- Syntax errors, logic bugs, security vulnerabilities
- Performance issues, best practices, code quality
- Does NOT judge what the code does, only how well it's written

Usage:
  ./technical_code_validator.py --code "code here"
  ./technical_code_validator.py --file path/to/file.py
  ./technical_code_validator.py --interactive
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import tempfile
import hashlib

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


@dataclass
class TechnicalValidationResult:
    """Result of technical code validation"""
    deepseek_analysis: str
    technical_analysis: str
    validator_used: str  # "claude", "glm", or "huggingface"
    technical_score: float  # 0-1, higher = better code quality
    syntax_issues: List[str]
    logic_issues: List[str] 
    security_issues: List[str]
    performance_issues: List[str]
    recommendations: List[str]
    timestamp: str


class TechnicalCodeValidator:
    """Content-neutral technical code validator"""
    
    def __init__(self):
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY") 
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.z.ai/api/paas/v4")
        self.openai_model = os.getenv("OPENAI_MODEL", "glm-4.5-air")
        
        # Results directory
        self.results_dir = Path("technical_validation_results")
        self.results_dir.mkdir(exist_ok=True)
        
        print("🔧 Technical Code Validator - Content Neutral")
        print(f"   Claude Available: {'✅' if self.has_claude() else '❌'}")
        print(f"   GLM Available: {'✅' if self.has_glm() else '❌'}")
        print(f"   HuggingFace Available: {'✅' if HAS_REQUESTS else '❌'}")
        print(f"   Results Dir: {self.results_dir}")
        print(f"   📝 Focus: TECHNICAL ANALYSIS ONLY - No content judgment")
    
    def has_claude(self) -> bool:
        """Check if Claude is available"""
        return HAS_ANTHROPIC and self.anthropic_key and self.anthropic_key != "YOUR_ANTHROPIC_API_KEY_HERE"
    
    def has_glm(self) -> bool:
        """Check if GLM is available"""
        return self.openai_key and self.openai_key != "YOUR_Z_AI_API_KEY_HERE"
    
    def get_deepseek_analysis(self, code: str) -> str:
        """Get DeepSeek analysis via direct API"""
        deepseek_direct_path = Path.home() / "deepseek_direct.py"
        
        if deepseek_direct_path.exists():
            try:
                print("🤖 Getting DeepSeek analysis...")
                result = subprocess.run([
                    'python', str(deepseek_direct_path), 
                    f"Analyze this code for technical issues - syntax, logic, security, performance:\\n\\n```python\\n{code}\\n```"
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    # Extract just the response content
                    response = result.stdout.strip()
                    if "📝 Response:" in response:
                        response = response.split("📝 Response:")[-1].strip()
                    return response
                else:
                    return f"DeepSeek API error: {result.stderr}"
            except Exception as e:
                return f"DeepSeek unavailable: {str(e)}"
        else:
            # Manual fallback
            print("📝 DeepSeek Direct not found. Manual input mode:")
            print("1. Run this in DeepSeek: Analyze this code for technical issues - syntax, logic, security, performance:")
            print(f"```python\\n{code}\\n```")
            print("2. Paste DeepSeek's response (press Enter twice when done):")
            
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip() == "" and lines and lines[-1].strip() == "":
                        break
                    lines.append(line)
                except EOFError:
                    break
            
            return "\\n".join(lines).strip() or "No DeepSeek analysis provided"
    
    def validate_with_claude_technical(self, code: str, deepseek_analysis: str) -> str:
        """Validate code with Claude - TECHNICAL FOCUS ONLY"""
        
        if not self.has_claude():
            raise ValueError("Claude not available - check ANTHROPIC_API_KEY")
        
        client = anthropic.Anthropic(api_key=self.anthropic_key)
        
        # CRITICAL: Content-neutral prompt focused ONLY on technical issues
        prompt = f"""You are a technical code reviewer. Your ONLY job is analyzing code quality, NOT content judgment.

FOCUS EXCLUSIVELY ON:
✅ Syntax errors and bugs
✅ Logic flaws and edge cases  
✅ Security vulnerabilities (injection, XSS, etc.)
✅ Performance bottlenecks
✅ Code structure and best practices
✅ Error handling and validation
✅ Memory leaks and resource management

DO NOT ANALYZE:
❌ What the code does (gambling, betting, etc.)
❌ Ethical implications of functionality  
❌ Legal compliance of use cases
❌ Appropriateness of the application

CODE TO REVIEW:
```python
{code}
```

DEEPSEEK'S TECHNICAL ANALYSIS:
{deepseek_analysis}

TASK: Fact-check DeepSeek's TECHNICAL analysis. Focus on code quality only.

Return JSON:
{{
    "technical_score": 0.75,
    "syntax_issues": ["specific syntax problems"],
    "logic_issues": ["logic flaws and edge cases"],
    "security_issues": ["technical security vulnerabilities"],
    "performance_issues": ["performance bottlenecks"],
    "deepseek_accuracy": ["what DeepSeek got right/wrong technically"],
    "missed_technical_issues": ["technical issues DeepSeek missed"], 
    "recommendations": ["specific technical fixes"],
    "summary": "technical assessment focusing on code quality only"
}}"""

        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"❌ Claude error: {e}")
            return f"Error: Claude validation failed - {str(e)}"
    
    def validate_with_glm_technical(self, code: str, deepseek_analysis: str) -> str:
        """Validate code with GLM - TECHNICAL FOCUS ONLY"""
        
        if not self.has_glm():
            raise ValueError("GLM not available - check OPENAI_API_KEY")
        
        try:
            import openai
            client = openai.OpenAI(
                api_key=self.openai_key,
                base_url=self.openai_base_url
            )
        except ImportError:
            raise ValueError("OpenAI package not available - install with: pip install openai")
        
        # Content-neutral technical prompt
        prompt = f"""Technical code reviewer: Focus ONLY on code quality, NOT content.

ANALYZE FOR:
- Syntax errors and bugs
- Logic issues and edge cases
- Security vulnerabilities (SQL injection, XSS, etc.)
- Performance problems
- Best practice violations
- Error handling gaps

DO NOT judge what the code does - only HOW WELL it's written.

CODE:
```python
{code}
```

DEEPSEEK ANALYSIS:
{deepseek_analysis}

Return JSON with technical assessment only:
{{
    "technical_score": 0.8,
    "syntax_issues": [],
    "logic_issues": [],  
    "security_issues": [],
    "performance_issues": [],
    "deepseek_accuracy": [],
    "missed_technical_issues": [],
    "recommendations": [],
    "summary": "technical quality assessment"
}}"""

        try:
            response = client.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are a technical code reviewer. Focus only on code quality, not content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ GLM error: {e}")
            return f"Error: GLM validation failed - {str(e)}"
    
    def validate_with_huggingface(self, code: str, deepseek_analysis: str) -> str:
        """Validate with free HuggingFace model - TECHNICAL FOCUS"""
        
        if not HAS_REQUESTS:
            raise ValueError("Requests package not available")
        
        # Use free CodeT5 or similar model for technical analysis
        API_URL = "https://api-inference.huggingface.co/models/microsoft/codebert-base"
        
        # Simplified technical prompt for free model
        prompt = f"""Technical review: Find syntax errors, logic bugs, security issues, performance problems.

Code:
{code}

DeepSeek said:
{deepseek_analysis}

Check DeepSeek's technical accuracy. JSON format."""
        
        try:
            response = requests.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={"inputs": prompt[:1000]},  # Limit for free tier
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Parse HuggingFace response and format as JSON
                return json.dumps({
                    "technical_score": 0.7,
                    "syntax_issues": [],
                    "logic_issues": [],
                    "security_issues": [],
                    "performance_issues": [],
                    "deepseek_accuracy": ["Using free HuggingFace model - limited analysis"],
                    "missed_technical_issues": [],
                    "recommendations": ["Consider upgrading to full API for detailed analysis"],
                    "summary": f"HuggingFace analysis: {str(result)[:200]}..."
                })
            else:
                return json.dumps({
                    "technical_score": 0.5,
                    "syntax_issues": [],
                    "logic_issues": [],
                    "security_issues": [],
                    "performance_issues": [],
                    "deepseek_accuracy": ["HuggingFace API unavailable"],
                    "missed_technical_issues": [],
                    "recommendations": ["Use Claude or GLM for validation"],
                    "summary": f"HuggingFace error: {response.status_code}"
                })
        except Exception as e:
            return json.dumps({
                "technical_score": 0.5,
                "syntax_issues": [],
                "logic_issues": [],
                "security_issues": [],
                "performance_issues": [],
                "deepseek_accuracy": [f"HuggingFace error: {str(e)}"],
                "missed_technical_issues": [],
                "recommendations": ["Use alternative validator"],
                "summary": "HuggingFace validation failed"
            })
    
    def parse_technical_response(self, response: str) -> Dict:
        """Parse technical validation response"""
        try:
            # Clean up response
            response = response.strip()
            
            # Find JSON block
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            
            # Parse JSON
            data = json.loads(response)
            
            # Ensure required fields
            required_fields = {
                "technical_score": 0.5,
                "syntax_issues": [],
                "logic_issues": [],
                "security_issues": [],
                "performance_issues": [],
                "deepseek_accuracy": [],
                "missed_technical_issues": [],
                "recommendations": [],
                "summary": "Technical analysis completed"
            }
            
            for field, default in required_fields.items():
                if field not in data:
                    data[field] = default
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parse error: {e}")
            return {
                "technical_score": 0.5,
                "syntax_issues": [],
                "logic_issues": [],
                "security_issues": [],
                "performance_issues": [],
                "deepseek_accuracy": ["Failed to parse validator response"],
                "missed_technical_issues": ["Could not extract structured analysis"],
                "recommendations": ["Review validator output manually"],
                "summary": f"Parser error: {str(e)}"
            }
    
    def validate_code(self, code: str) -> TechnicalValidationResult:
        """Main technical validation workflow"""
        
        print("🔧 Starting Technical Code Validation (Content Neutral)...")
        
        # Step 1: Get DeepSeek analysis
        print("\\n📋 Step 1: Getting DeepSeek Technical Analysis")
        deepseek_analysis = self.get_deepseek_analysis(code)
        
        # Step 2: Choose technical validator
        validator_used = "none"
        validator_response = None
        
        if self.has_claude():
            print("\\n📋 Step 2: Technical validation with Claude...")
            validator_used = "claude"
            validator_response = self.validate_with_claude_technical(code, deepseek_analysis)
        elif self.has_glm():
            print("\\n📋 Step 2: Technical validation with GLM...")
            validator_used = "glm" 
            validator_response = self.validate_with_glm_technical(code, deepseek_analysis)
        elif HAS_REQUESTS:
            print("\\n📋 Step 2: Technical validation with HuggingFace (free)...")
            validator_used = "huggingface"
            validator_response = self.validate_with_huggingface(code, deepseek_analysis)
        else:
            raise ValueError("No validator available - need Claude, GLM, or HuggingFace access")
        
        # Step 3: Parse technical results
        print("\\n📋 Step 3: Analyzing technical issues...")
        validator_data = self.parse_technical_response(validator_response)
        
        # Step 4: Create result
        result = TechnicalValidationResult(
            deepseek_analysis=deepseek_analysis,
            technical_analysis=validator_response,
            validator_used=validator_used,
            technical_score=validator_data.get("technical_score", 0.5),
            syntax_issues=validator_data.get("syntax_issues", []),
            logic_issues=validator_data.get("logic_issues", []),
            security_issues=validator_data.get("security_issues", []),
            performance_issues=validator_data.get("performance_issues", []),
            recommendations=validator_data.get("recommendations", []),
            timestamp=datetime.now().isoformat()
        )
        
        # Step 5: Save and display results
        self.save_result(code, result)
        self.display_result(result)
        
        return result
    
    def save_result(self, code: str, result: TechnicalValidationResult):
        """Save technical validation result"""
        
        code_hash = hashlib.md5(code.encode()).hexdigest()[:8]
        filename = f"technical_validation_{result.timestamp.split('T')[0]}_{code_hash}.json"
        filepath = self.results_dir / filename
        
        save_data = {
            "code": code,
            "deepseek_analysis": result.deepseek_analysis,
            "technical_analysis": result.technical_analysis,
            "validator_used": result.validator_used,
            "technical_score": result.technical_score,
            "syntax_issues": result.syntax_issues,
            "logic_issues": result.logic_issues,
            "security_issues": result.security_issues,
            "performance_issues": result.performance_issues,
            "recommendations": result.recommendations,
            "timestamp": result.timestamp
        }
        
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"💾 Technical validation saved to: {filepath}")
    
    def display_result(self, result: TechnicalValidationResult):
        """Display technical validation results"""
        
        print("\\n" + "="*80)
        print("🔧 TECHNICAL CODE VALIDATION - CONTENT NEUTRAL")
        print("="*80)
        
        # Technical Score
        technical_pct = result.technical_score * 100
        print(f"\\n📊 TECHNICAL QUALITY SCORE: {technical_pct:.1f}%")
        print(f"   🔍 Validator Used: {result.validator_used.upper()}")
        
        # Technical Issues Summary
        total_issues = (len(result.syntax_issues) + len(result.logic_issues) + 
                       len(result.security_issues) + len(result.performance_issues))
        
        if total_issues == 0:
            print(f"\\n✅ EXCELLENT: No technical issues found!")
        elif total_issues <= 3:
            print(f"\\n⚠️ MINOR ISSUES: {total_issues} technical issues found")
        else:
            print(f"\\n🔥 MAJOR ISSUES: {total_issues} technical issues found")
        
        # Specific Technical Issues
        if result.syntax_issues:
            print(f"\\n🔴 SYNTAX ISSUES:")
            for i, issue in enumerate(result.syntax_issues, 1):
                print(f"   {i}. {issue}")
        
        if result.logic_issues:
            print(f"\\n🟡 LOGIC ISSUES:")
            for i, issue in enumerate(result.logic_issues, 1):
                print(f"   {i}. {issue}")
        
        if result.security_issues:
            print(f"\\n🔒 SECURITY ISSUES:")
            for i, issue in enumerate(result.security_issues, 1):
                print(f"   {i}. {issue}")
        
        if result.performance_issues:
            print(f"\\n⚡ PERFORMANCE ISSUES:")
            for i, issue in enumerate(result.performance_issues, 1):
                print(f"   {i}. {issue}")
        
        # Technical Recommendations
        if result.recommendations:
            print(f"\\n💡 TECHNICAL RECOMMENDATIONS:")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"   {i}. {rec}")
        
        print(f"\\n🎯 FOCUS: Technical quality only - no content judgment applied")
        print("="*80)
    
    def validate_file(self, filepath: str) -> TechnicalValidationResult:
        """Validate code from file"""
        
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(path, 'r') as f:
            code = f.read()
        
        print(f"📄 Technical validation of file: {filepath}")
        print(f"   Lines: {len(code.splitlines())}")
        print(f"   Characters: {len(code)}")
        
        return self.validate_code(code)
    
    def interactive_mode(self):
        """Interactive technical validation mode"""
        
        print("🔧 TECHNICAL CODE VALIDATOR - INTERACTIVE MODE")
        print("="*60)
        print("🎯 Focus: Technical analysis only - no content judgment")
        print("Commands:")
        print("  code    - Validate code snippet")
        print("  file    - Validate code file")
        print("  paste   - Validate pasted code") 
        print("  help    - Show help")
        print("  quit    - Exit")
        print()
        
        while True:
            try:
                command = input("🔧 technical> ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif command == 'help':
                    print("Available commands: code, file, paste, help, quit")
                    print("Focus: Technical code quality only")
                
                elif command == 'code':
                    print("📝 Enter your code (press Ctrl+D when done):")
                    code_lines = []
                    try:
                        while True:
                            line = input()
                            code_lines.append(line)
                    except EOFError:
                        pass
                    
                    if code_lines:
                        code = '\\n'.join(code_lines)
                        self.validate_code(code)
                    else:
                        print("❌ No code provided")
                
                elif command == 'file':
                    filepath = input("📄 Enter file path: ").strip()
                    if filepath:
                        try:
                            self.validate_file(filepath)
                        except Exception as e:
                            print(f"❌ Error validating file: {e}")
                    else:
                        print("❌ No file path provided")
                
                elif command == 'paste':
                    print("📋 Paste your code (press Enter twice when done):")
                    lines = []
                    empty_lines = 0
                    while True:
                        try:
                            line = input()
                            if line.strip() == "":
                                empty_lines += 1
                                if empty_lines >= 2:
                                    break
                            else:
                                empty_lines = 0
                            lines.append(line)
                        except EOFError:
                            break
                    
                    if lines:
                        code = '\\n'.join(lines)
                        self.validate_code(code)
                    else:
                        print("❌ No code provided")
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main function"""
    
    parser = argparse.ArgumentParser(description="Technical Code Validator - Content Neutral")
    parser.add_argument("--code", help="Validate code snippet")
    parser.add_argument("--file", help="Validate code file")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    try:
        validator = TechnicalCodeValidator()
        
        if args.code:
            validator.validate_code(args.code)
        elif args.file:
            validator.validate_file(args.file)
        else:
            # Default to interactive mode
            validator.interactive_mode()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()