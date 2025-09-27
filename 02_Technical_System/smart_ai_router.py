#!/usr/bin/env python3
"""
Smart AI Router for Cursor
Intelligently routes AI requests to:
- DeepSeek (uncensored, good for betting/gambling, shell commands)
- GLM-4.5 (general purpose, cheaper than Claude)
- Claude (high-quality validation, limited credits)

This replaces the /usr/local/bin/claude symlink for Cursor integration
"""

import sys
import json
import subprocess
from pathlib import Path
import argparse

class SmartAIRouter:
    def __init__(self):
        self.home_path = Path.home()
        self.deepseek_path = self.find_deepseek()
        self.glm_bridge_path = self.home_path / "claude_to_glm_bridge.py"
        self.deepseek_bridge_path = self.home_path / "deepseek_cursor_bridge.py"
        
    def find_deepseek(self):
        """Find DeepSeek CLI"""
        try:
            result = subprocess.run(['which', 'deepseek'], capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None
    
    def should_use_deepseek(self, prompt):
        """Determine if request should go to DeepSeek"""
        prompt_lower = prompt.lower()
        
        # DeepSeek indicators (uncensored content)
        deepseek_keywords = [
            'betting', 'gambling', 'parlay', 'odds', 'wager', 'sports betting',
            'shell command', 'execute command', 'run command', 'terminal command',
            'uncensored', 'bypass restriction', 'unrestricted',
            'install', 'setup', 'configure', 'deploy',
            'deepseek', 'fast coding', 'quick implementation'
        ]
        
        return any(keyword in prompt_lower for keyword in deepseek_keywords)
    
    def route_to_deepseek(self, args):
        """Route request to DeepSeek using direct API client"""
        full_prompt = ' '.join(args)
        deepseek_direct_path = self.home_path / "deepseek_direct.py"
        
        # Check if this is a shell execution request first
        shell_executor_path = self.home_path / "cursor_shell_executor.py"
        if ('execute' in full_prompt.lower() and 'command' in full_prompt.lower()) and shell_executor_path.exists():
            try:
                result = subprocess.run([
                    'python', str(shell_executor_path)
                ] + args, capture_output=True, text=True, timeout=60)
                
                return f"⚡ [Shell Executor]\n{result.stdout if result.returncode == 0 else result.stderr}"
            except Exception as e:
                pass  # Fall through to DeepSeek
        
        # Use direct DeepSeek API client (more reliable than CLI)
        if deepseek_direct_path.exists():
            try:
                result = subprocess.run([
                    'python', str(deepseek_direct_path), full_prompt
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    response = result.stdout.strip()
                    
                    # Check for shell commands and offer execution
                    if any(indicator in response.lower() for indicator in ['```bash', '```sh', 'npm install', 'pip install', 'sudo ', 'git ']):
                        response += "\n\n🔧 **Shell commands detected!**\n"
                        response += "💡 To execute: Type 'execute commands' in next message\n"
                        response += "🎮 Or use Ultimate DeepSeek GUI for interactive execution"
                    
                    return response
                else:
                    # DeepSeek API failed, check error and fallback to GLM
                    error_msg = result.stderr.strip()
                    if "insufficient balance" in error_msg.lower() or "402" in error_msg:
                        fallback_response = self.route_to_glm(args)
                        return f"💰 [DeepSeek Credits Exhausted - GLM Fallback]\n\n⚠️ DeepSeek is out of credits, using GLM for uncensored requests!\n\n{fallback_response}"
                    else:
                        # Try GLM fallback for any other error
                        fallback_response = self.route_to_glm(args)
                        return f"🔄 [DeepSeek Error - GLM Fallback]\n\n⚠️ DeepSeek error: {error_msg[:100]}...\n\nUsing GLM instead:\n\n{fallback_response}"
                        
            except subprocess.TimeoutExpired:
                fallback_response = self.route_to_glm(args)
                return f"⏱️ [DeepSeek Timeout - GLM Fallback]\n\n⚠️ DeepSeek took too long, using GLM instead:\n\n{fallback_response}"
            except Exception as e:
                pass  # Fall through to GLM fallback
        
        # Fallback to GLM for uncensored requests
        fallback_response = self.route_to_glm(args)
        return f"🤖 [DeepSeek Unavailable - GLM Uncensored Mode]\n\n💡 Using GLM for uncensored response (works for betting/gambling too!)\n\n{fallback_response}"
    
    def route_to_glm(self, args):
        """Route request to GLM bridge"""
        if not self.glm_bridge_path.exists():
            return "❌ GLM bridge not available"
        
        try:
            result = subprocess.run([
                'python', str(self.glm_bridge_path)
            ] + args, capture_output=True, text=True, timeout=60)
            
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"❌ GLM error: {str(e)}"
    
    def route_request(self, args):
        """Main routing logic"""
        if not args:
            return "❌ No prompt provided"
        
        full_prompt = ' '.join(args)
        
        # Check for execution requests first
        if 'execute' in full_prompt.lower() and 'command' in full_prompt.lower():
            shell_executor_path = self.home_path / "cursor_shell_executor.py"
            if shell_executor_path.exists():
                try:
                    result = subprocess.run([
                        'python', str(shell_executor_path)
                    ] + args, capture_output=True, text=True, timeout=60)
                    
                    return f"⚡ [Shell Executor]\n{result.stdout if result.returncode == 0 else result.stderr}"
                except Exception as e:
                    pass
        
        # For DeepSeek-preferred content, try DeepSeek first but fallback quickly
        if self.should_use_deepseek(full_prompt):
            response = self.route_to_deepseek(args)
            # Check if DeepSeek response indicates it worked
            if not ("credits exhausted" in response.lower() or "insufficient balance" in response.lower() or "402" in response):
                return f"🤖 [DeepSeek - Uncensored Mode]\n{response}"
            # If DeepSeek failed, the route_to_deepseek already handled GLM fallback
            return response
        else:
            # Regular requests go to GLM
            response = self.route_to_glm(args)
            return f"🔄 [GLM-4.5 - Standard Mode]\n{response}"
    
    def get_status(self):
        """Get router status"""
        status = {
            "deepseek": "✅ Available" if self.deepseek_path else "❌ Not Available",
            "glm": "✅ Available" if self.glm_bridge_path.exists() else "❌ Not Available",
            "deepseek_bridge": "✅ Available" if self.deepseek_bridge_path.exists() else "❌ Not Available",
            "routing": "Smart routing active"
        }
        
        return json.dumps(status, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Smart AI Router for Cursor")
    parser.add_argument('prompt', nargs='*', help='Prompt to route')
    parser.add_argument('--status', action='store_true', help='Show router status')
    parser.add_argument('--test', action='store_true', help='Test routing')
    
    args = parser.parse_args()
    router = SmartAIRouter()
    
    if args.status:
        print(router.get_status())
    elif args.test:
        # Test both routing paths
        print("🧪 Testing Smart AI Router\\n")
        
        print("1. Testing DeepSeek routing (betting prompt):")
        betting_test = router.route_request(["How to calculate betting odds for NFL games?"])
        print(f"   Result: {betting_test[:100]}...\\n")
        
        print("2. Testing GLM routing (general prompt):")
        general_test = router.route_request(["Explain Python list comprehensions"])
        print(f"   Result: {general_test[:100]}...\\n")
        
    elif args.prompt:
        response = router.route_request(args.prompt)
        print(response)
    else:
        # Handle Cursor's direct calls (no arguments, expects JSON response)
        if len(sys.argv) == 1:
            # This is likely a Cursor health check
            print('{"status": "Smart AI Router Active", "models": ["deepseek", "glm-4.5"]}')
        else:
            # Interactive mode
            print("🧠 Smart AI Router - Interactive Mode")
            print("Routes to DeepSeek (uncensored) or GLM (general) automatically")
            
            while True:
                try:
                    user_input = input("\\n> ").strip()
                    if user_input.lower() in ['quit', 'exit']:
                        break
                    if user_input:
                        response = router.route_request([user_input])
                        print(f"\\n{response}\\n")
                        print("-" * 50)
                except KeyboardInterrupt:
                    break

if __name__ == "__main__":
    main()