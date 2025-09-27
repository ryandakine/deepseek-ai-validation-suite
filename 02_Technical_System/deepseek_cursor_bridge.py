#!/usr/bin/env python3
"""
DeepSeek Cursor Bridge
Enables DeepSeek to work inside Cursor with shell command execution
Maintains compatibility with GLM bridge while adding DeepSeek support
"""

import json
import sys
import subprocess
import os
import argparse
from pathlib import Path

class DeepSeekCursorBridge:
    """Bridge that allows both DeepSeek and GLM to work in Cursor"""
    
    def __init__(self):
        self.deepseek_path = self.find_deepseek_cli()
        self.home_path = Path.home()
        
    def find_deepseek_cli(self):
        """Find DeepSeek CLI installation"""
        # Check common locations
        possible_paths = [
            "/home/ryan/.nvm/versions/node/v22.19.0/bin/deepseek",
            "/usr/local/bin/deepseek",
            "/usr/bin/deepseek"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                return path
        
        # Try which command
        try:
            result = subprocess.run(['which', 'deepseek'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return None
    
    def is_deepseek_request(self, args):
        """Check if this is a request that should go to DeepSeek"""
        # Look for indicators this should use DeepSeek (uncensored)
        content = ' '.join(args).lower()
        
        deepseek_indicators = [
            'betting', 'gambling', 'parlay', 'odds', 'wager',
            'uncensored', 'shell command', 'execute', 'run command',
            'deepseek', 'fast coding', 'quick code'
        ]
        
        return any(indicator in content for indicator in deepseek_indicators)
    
    def execute_with_deepseek(self, prompt):
        """Execute request using DeepSeek CLI"""
        if not self.deepseek_path:
            return {"error": "DeepSeek CLI not found", "content": "Please install DeepSeek CLI first"}
        
        try:
            # Run DeepSeek CLI
            result = subprocess.run([
                self.deepseek_path, 'ask', prompt
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                response = result.stdout.strip()
                
                # Check if DeepSeek suggested shell commands
                if self.contains_shell_commands(response):
                    response = self.add_shell_execution_offer(response)
                
                return {
                    "content": response,
                    "source": "deepseek-cli",
                    "model": "deepseek-reasoner"
                }
            else:
                return {
                    "error": f"DeepSeek CLI error: {result.stderr}",
                    "content": "DeepSeek request failed"
                }
                
        except subprocess.TimeoutExpired:
            return {
                "error": "DeepSeek request timed out",
                "content": "Request took too long"
            }
        except Exception as e:
            return {
                "error": f"DeepSeek execution error: {str(e)}",
                "content": "DeepSeek bridge error"
            }
    
    def contains_shell_commands(self, response):
        """Check if response contains shell commands"""
        shell_indicators = [
            '```bash', '```sh', '```shell',
            'run this command:', 'execute:', '$',
            'npm install', 'pip install', 'sudo',
            'mkdir', 'cd ', 'ls ', 'cp ', 'mv '
        ]
        
        return any(indicator in response.lower() for indicator in shell_indicators)
    
    def add_shell_execution_offer(self, response):
        """Add shell execution capabilities to response"""
        return f"""{response}

🔧 **SHELL EXECUTION AVAILABLE**
I can execute these commands for you in Cursor. Type 'execute' to run them, or modify them first.

**Available commands:**
- Execute all suggested commands
- Execute individual commands  
- Test commands in safe mode first
- Show command explanations

Just say "execute the commands" or "run the shell commands" and I'll do it!
"""
    
    def execute_shell_commands(self, response_text, mode="safe"):
        """Extract and execute shell commands from response"""
        commands = self.extract_shell_commands(response_text)
        
        if not commands:
            return "No shell commands found in the response."
        
        results = []
        results.append(f"🔧 Executing {len(commands)} shell commands in {mode} mode:\n")
        
        for i, cmd in enumerate(commands, 1):
            results.append(f"Command {i}: {cmd}")
            
            if mode == "safe":
                results.append("⚠️  Safe mode: Command not executed (use 'execute' mode to run)")
            else:
                try:
                    result = subprocess.run(
                        cmd, shell=True, capture_output=True, 
                        text=True, timeout=30, cwd=Path.cwd()
                    )
                    
                    if result.returncode == 0:
                        results.append(f"✅ Success: {result.stdout.strip()}")
                    else:
                        results.append(f"❌ Error: {result.stderr.strip()}")
                        
                except subprocess.TimeoutExpired:
                    results.append("⏱️  Command timed out")
                except Exception as e:
                    results.append(f"💥 Error: {str(e)}")
            
            results.append("")
        
        return "\n".join(results)
    
    def extract_shell_commands(self, text):
        """Extract shell commands from text"""
        commands = []
        lines = text.split('\n')
        
        in_code_block = False
        for line in lines:
            line = line.strip()
            
            # Code block detection
            if line.startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                if line and not line.startswith('#'):
                    commands.append(line)
            elif line.startswith('$'):
                commands.append(line[1:].strip())
            elif line.startswith('sudo ') or line.startswith('npm ') or line.startswith('pip '):
                commands.append(line)
        
        return commands
    
    def forward_to_glm(self, args):
        """Forward request to GLM bridge"""
        glm_bridge = Path("/home/ryan/claude_to_glm_bridge.py")
        
        if glm_bridge.exists():
            try:
                result = subprocess.run([
                    'python', str(glm_bridge)
                ] + args, capture_output=True, text=True, timeout=60)
                
                return result.stdout if result.returncode == 0 else result.stderr
            except Exception as e:
                return f"GLM bridge error: {str(e)}"
        else:
            return "GLM bridge not found"
    
    def handle_request(self, args):
        """Main request handler - routes to DeepSeek or GLM"""
        full_prompt = ' '.join(args)
        
        # Check for special commands
        if 'execute' in full_prompt.lower() and ('command' in full_prompt.lower() or 'shell' in full_prompt.lower()):
            # This is a shell execution request
            return self.execute_shell_commands(full_prompt, mode="execute")
        
        elif 'safe mode' in full_prompt.lower():
            return self.execute_shell_commands(full_prompt, mode="safe")
        
        elif self.is_deepseek_request(args):
            # Route to DeepSeek for uncensored responses
            print("🤖 Routing to DeepSeek (uncensored mode)", file=sys.stderr)
            result = self.execute_with_deepseek(full_prompt)
            
            if 'error' in result:
                # Fallback to GLM if DeepSeek fails
                print("🔄 Falling back to GLM", file=sys.stderr)
                return self.forward_to_glm(args)
            
            return result['content']
        else:
            # Route to GLM for general requests
            print("🔄 Routing to GLM", file=sys.stderr)
            return self.forward_to_glm(args)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="DeepSeek Cursor Bridge")
    parser.add_argument('prompt', nargs='*', help='Prompt to send')
    parser.add_argument('--test', action='store_true', help='Test the bridge')
    parser.add_argument('--status', action='store_true', help='Show status')
    
    args = parser.parse_args()
    bridge = DeepSeekCursorBridge()
    
    if args.test:
        print("🧪 Testing DeepSeek Cursor Bridge...")
        test_prompt = ["Create a simple betting odds calculator in Python"]
        response = bridge.handle_request(test_prompt)
        print("✅ Test response:")
        print(response)
    
    elif args.status:
        print("📊 DeepSeek Cursor Bridge Status:")
        print(f"   DeepSeek CLI: {'✅' if bridge.deepseek_path else '❌'}")
        print(f"   Path: {bridge.deepseek_path or 'Not found'}")
        print(f"   GLM Bridge: {'✅' if Path('/home/ryan/claude_to_glm_bridge.py').exists() else '❌'}")
        
    elif args.prompt:
        response = bridge.handle_request(args.prompt)
        print(response)
    
    else:
        # Interactive mode
        print("🔌 DeepSeek Cursor Bridge - Interactive Mode")
        print("Type 'quit' to exit, 'help' for commands")
        
        while True:
            try:
                user_input = input("\n🤖 > ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    print("""
Available commands:
- Any prompt: Routes to DeepSeek (betting/uncensored) or GLM (general)
- 'execute commands': Execute shell commands from previous response
- 'safe mode': Show commands without executing
- 'status': Show bridge status
- 'quit': Exit
                    """)
                elif user_input:
                    response = bridge.handle_request([user_input])
                    print("\n" + "="*50)
                    print(response)
                    print("="*50)
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()