#!/usr/bin/env python3
"""
🤖 Free HuggingFace Technical Validator
100% free, uncensored technical code analysis using HuggingFace models
No API keys required, focuses only on technical issues

Usage:
  ./huggingface_validator.py --code "code here"
  ./huggingface_validator.py --interactive
"""

import requests
import json
import argparse
import time
from typing import Dict, List


class HuggingFaceValidator:
    """Free technical code validator using HuggingFace models"""
    
    def __init__(self):
        self.models = {
            "codebert": "https://api-inference.huggingface.co/models/microsoft/codebert-base",
            "codet5": "https://api-inference.huggingface.co/models/Salesforce/codet5-small", 
            "codegen": "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-mono",
        }
        
        print("🤖 Free HuggingFace Technical Validator")
        print("   ✅ 100% Free - No API keys required")
        print("   ✅ Completely uncensored")
        print("   ✅ Technical focus only")
        print("   🔄 Using multiple HF models for validation")
    
    def validate_with_model(self, code: str, model_name: str, model_url: str) -> Dict:
        """Validate code with specific HuggingFace model"""
        
        prompt = f"""Technical code review - find bugs, security issues, performance problems:

```python
{code}
```

Issues found:"""

        try:
            print(f"   🔍 Checking with {model_name}...")
            
            response = requests.post(
                model_url,
                headers={"Content-Type": "application/json"},
                json={"inputs": prompt[:800]},  # HF free tier limit
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Parse model response
                if isinstance(result, list) and result:
                    generated_text = result[0].get('generated_text', str(result))
                else:
                    generated_text = str(result)
                
                # Extract issues from response
                issues = self.parse_model_response(generated_text, code)
                
                return {
                    "model": model_name,
                    "success": True,
                    "issues": issues,
                    "raw_response": generated_text[:300] + "..." if len(generated_text) > 300 else generated_text
                }
            else:
                return {
                    "model": model_name,
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "issues": []
                }
                
        except Exception as e:
            return {
                "model": model_name,
                "success": False,
                "error": str(e),
                "issues": []
            }
    
    def parse_model_response(self, response: str, original_code: str) -> List[str]:
        """Parse model response to extract technical issues"""
        issues = []
        
        # Common issue indicators
        issue_keywords = [
            "error", "bug", "issue", "problem", "vulnerability", "security",
            "performance", "inefficient", "missing", "undefined", "null",
            "exception", "leak", "unsafe", "deprecated", "warning"
        ]
        
        # Split response into sentences
        sentences = response.replace('.', '.\n').replace('!', '!\n').split('\n')
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Skip very short phrases
                # Check if sentence mentions technical issues
                if any(keyword in sentence.lower() for keyword in issue_keywords):
                    # Clean up the sentence
                    if not sentence.endswith(('.', '!', '?')):
                        sentence += '.'
                    issues.append(sentence)
        
        # If no specific issues found, add general assessment
        if not issues:
            if len(original_code.strip()) > 0:
                issues.append("Code structure appears technically sound based on automated analysis")
            else:
                issues.append("No code provided for analysis")
        
        return issues[:5]  # Limit to 5 most relevant issues
    
    def validate_code(self, code: str) -> Dict:
        """Validate code using multiple HuggingFace models"""
        
        print("🔧 Starting free HuggingFace validation...")
        print(f"   📝 Code length: {len(code)} characters")
        
        all_results = []
        all_issues = []
        
        # Try each model
        for model_name, model_url in self.models.items():
            result = self.validate_with_model(code, model_name, model_url)
            all_results.append(result)
            
            if result["success"]:
                all_issues.extend(result["issues"])
            
            # Small delay between API calls
            time.sleep(1)
        
        # Consolidate results
        unique_issues = list(set(all_issues))  # Remove duplicates
        successful_models = [r["model"] for r in all_results if r["success"]]
        
        # Calculate simple technical score
        total_models = len(self.models)
        successful_models_count = len(successful_models)
        issue_count = len(unique_issues)
        
        # Simple scoring: fewer issues = higher score, more models = more confidence
        base_score = max(0.3, 1.0 - (issue_count * 0.1))
        confidence_bonus = (successful_models_count / total_models) * 0.2
        technical_score = min(1.0, base_score + confidence_bonus)
        
        result = {
            "technical_score": technical_score,
            "models_used": successful_models,
            "total_models": total_models,
            "issues_found": unique_issues,
            "issue_count": issue_count,
            "all_results": all_results,
            "summary": f"Free HuggingFace analysis using {successful_models_count}/{total_models} models"
        }
        
        self.display_result(result, code)
        return result
    
    def display_result(self, result: Dict, code: str):
        """Display validation results"""
        
        print("\n" + "="*70)
        print("🤖 FREE HUGGINGFACE TECHNICAL VALIDATION")
        print("="*70)
        
        # Score and summary
        score_pct = result["technical_score"] * 100
        print(f"\n📊 TECHNICAL SCORE: {score_pct:.1f}%")
        print(f"   🔍 Models Used: {len(result['models_used'])}/{result['total_models']}")
        print(f"   🎯 Issues Found: {result['issue_count']}")
        
        # Issues
        if result["issues_found"]:
            print(f"\n🔍 TECHNICAL ISSUES DETECTED:")
            for i, issue in enumerate(result["issues_found"], 1):
                print(f"   {i}. {issue}")
        else:
            print(f"\n✅ No obvious technical issues detected")
        
        # Model results
        print(f"\n📋 MODEL RESULTS:")
        for model_result in result["all_results"]:
            status = "✅" if model_result["success"] else "❌"
            print(f"   {status} {model_result['model']}")
            if not model_result["success"]:
                print(f"      Error: {model_result.get('error', 'Unknown error')}")
        
        # Limitations
        print(f"\n⚠️ LIMITATIONS:")
        print(f"   • Free tier models have limited analysis depth")
        print(f"   • Best for basic syntax and obvious issues")
        print(f"   • For advanced analysis, use Claude or GLM validators")
        
        print(f"\n💡 100% FREE & UNCENSORED - No content judgment applied")
        print("="*70)
    
    def interactive_mode(self):
        """Interactive validation mode"""
        
        print("🤖 FREE HUGGINGFACE VALIDATOR - INTERACTIVE MODE")
        print("="*50)
        print("Commands:")
        print("  validate - Validate code snippet")
        print("  paste    - Paste code for validation")
        print("  help     - Show help")
        print("  quit     - Exit")
        print()
        
        while True:
            try:
                command = input("🤖 hf> ").strip().lower()
                
                if command in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif command == 'help':
                    print("Available commands: validate, paste, help, quit")
                    print("Focus: Free technical analysis with HuggingFace models")
                
                elif command == 'validate':
                    print("📝 Enter your code (press Ctrl+D when done):")
                    code_lines = []
                    try:
                        while True:
                            line = input()
                            code_lines.append(line)
                    except EOFError:
                        pass
                    
                    if code_lines:
                        code = '\n'.join(code_lines)
                        self.validate_code(code)
                    else:
                        print("❌ No code provided")
                
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
                        code = '\n'.join(lines)
                        self.validate_code(code)
                    else:
                        print("❌ No code provided")
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main function"""
    
    parser = argparse.ArgumentParser(description="Free HuggingFace Technical Validator")
    parser.add_argument("--code", help="Validate code snippet")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    try:
        validator = HuggingFaceValidator()
        
        if args.code:
            validator.validate_code(args.code)
        else:
            # Default to interactive mode
            validator.interactive_mode()
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()