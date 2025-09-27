#!/usr/bin/env python3
"""
🚀 SIMPLE MULTI-AGENT GUI
A streamlined interface for the DeepSeek AI Validation Suite's multi-LLM capabilities.
"""

import asyncio
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
import os
import sys

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from multi_agent_orchestrator import MultiAgentOrchestrator, ValidationResult
except ImportError as e:
    print(f"Error importing orchestrator: {e}")
    print("Note: Some functionality may not be available in GUI mode")

class SimpleMultiAgentGUI:
    """Simplified multi-agent validation GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DeepSeek AI Validation Suite - Multi-Agent")
        self.root.geometry("1200x800")
        
        # Try to initialize orchestrator
        self.orchestrator = None
        try:
            self.orchestrator = MultiAgentOrchestrator("agent_config.yaml")
            print("✅ Multi-agent orchestrator loaded successfully")
        except Exception as e:
            print(f"⚠️ Could not load orchestrator: {e}")
            print("GUI will run in limited mode")
        
        # GUI variables
        self.user_tier = tk.StringVar(value="free")
        self.selected_chain = tk.StringVar(value="free_basic")
        self.validation_type = tk.StringVar(value="code_validation")
        
        self.create_widgets()
        print("🚀 Simple Multi-Agent GUI initialized")
    
    def create_widgets(self):
        """Create GUI widgets"""
        
        # Title
        title_label = tk.Label(self.root, 
                             text="🚀 DeepSeek AI Validation Suite - Multi-Agent",
                             font=('Arial', 16, 'bold'),
                             fg='#00aa00')
        title_label.pack(pady=10)
        
        # Configuration frame
        config_frame = tk.LabelFrame(self.root, text="Configuration", font=('Arial', 12, 'bold'))
        config_frame.pack(fill='x', padx=10, pady=5)
        
        # User tier
        tier_frame = tk.Frame(config_frame)
        tier_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(tier_frame, text="User Tier:", font=('Arial', 10, 'bold')).pack(side='left')
        tier_combo = ttk.Combobox(tier_frame, textvariable=self.user_tier,
                                 values=['free', 'professional', 'enterprise'],
                                 state='readonly', width=15)
        tier_combo.pack(side='left', padx=10)
        tier_combo.bind('<<ComboboxSelected>>', self.on_tier_changed)
        
        # Chain selection
        chain_frame = tk.Frame(config_frame)
        chain_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(chain_frame, text="Validation Chain:", font=('Arial', 10, 'bold')).pack(side='left')
        self.chain_combo = ttk.Combobox(chain_frame, textvariable=self.selected_chain,
                                       state='readonly', width=25)
        self.chain_combo.pack(side='left', padx=10)
        
        # Update chains
        self.update_available_chains()
        
        # Input section
        input_frame = tk.LabelFrame(self.root, text="Input Code/Content", font=('Arial', 12, 'bold'))
        input_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Text area
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8,
                                                   font=('Consolas', 11),
                                                   bg='#f0f0f0')
        self.input_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(input_frame)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        example_btn = tk.Button(button_frame, text="Load Example",
                               command=self.load_example,
                               bg='#404040', fg='white')
        example_btn.pack(side='left', padx=5)
        
        self.validate_btn = tk.Button(button_frame, text="🚀 VALIDATE",
                                     command=self.start_validation,
                                     bg='#00aa00', fg='white',
                                     font=('Arial', 12, 'bold'))
        self.validate_btn.pack(side='right', padx=5)
        
        # Results section
        results_frame = tk.LabelFrame(self.root, text="Results", font=('Arial', 12, 'bold'))
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10,
                                                     font=('Consolas', 10),
                                                     state='disabled')
        self.results_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", 
                                   relief=tk.SUNKEN, anchor='w')
        self.status_label.pack(fill='x', side='bottom')
    
    def on_tier_changed(self, event=None):
        """Handle tier change"""
        self.update_available_chains()
    
    def update_available_chains(self):
        """Update available chains based on tier"""
        if not self.orchestrator:
            # Default chains when orchestrator is not available
            chains = ["free_basic", "free_consensus"]
        else:
            chains = self.orchestrator.list_available_chains(self.user_tier.get())
        
        self.chain_combo['values'] = chains
        if chains:
            self.selected_chain.set(chains[0])
    
    def load_example(self):
        """Load example code"""
        example = '''def calculate_payout(odds, bet_amount):
    """
    Calculate betting payout - for educational purposes only.
    """
    if odds <= 0 or bet_amount <= 0:
        return 0
    
    return bet_amount * odds

# Example usage
result = calculate_payout(2.5, 100)
print(f"Potential payout: ${result}")
'''
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, example)
    
    def start_validation(self):
        """Start validation in thread"""
        content = self.input_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("No Input", "Please enter code to validate.")
            return
        
        if not self.orchestrator:
            messagebox.showerror("Error", "Multi-agent orchestrator not available. Check configuration.")
            return
        
        # Disable button
        self.validate_btn.config(state='disabled', text='Validating...')
        self.status_label.config(text="Running validation...")
        
        # Start validation thread
        thread = threading.Thread(target=self.run_validation, args=(content,))
        thread.daemon = True
        thread.start()
    
    def run_validation(self, content):
        """Run validation in background thread"""
        try:
            # Create event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run validation
            result = loop.run_until_complete(
                self.orchestrator.run_validation_chain(
                    prompt=content,
                    chain_name=self.selected_chain.get(),
                    validation_type=self.validation_type.get(),
                    user_tier=self.user_tier.get()
                )
            )
            
            # Update GUI in main thread
            self.root.after(0, self.handle_success, result)
            
        except Exception as e:
            # Handle error in main thread
            self.root.after(0, self.handle_error, str(e))
        finally:
            # Re-enable button
            self.root.after(0, self.validation_finished)
    
    def handle_success(self, result):
        """Handle successful validation"""
        # Clear results
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        # Format result
        output = f"""🎯 VALIDATION RESULT: {result.result_type.value.upper()}
📊 Consensus Score: {result.consensus_score:.2f}/1.00
💰 Total Cost: ${result.total_cost:.4f}
⏱️ Processing Time: {result.processing_time:.2f}s
🔗 Chain: {result.chain_name}

📝 ANALYSIS:
{result.final_response}

🤖 INDIVIDUAL AGENTS:
"""
        
        for i, response in enumerate(result.individual_responses, 1):
            output += f"""
--- Agent {i}: {response.agent_id} ---
Provider: {response.provider}
Confidence: {response.confidence_score:.2f}
Cost: ${response.cost:.4f}
Time: {response.processing_time:.2f}s

{response.response_text[:500]}...

"""
        
        self.results_text.insert(1.0, output)
        self.results_text.config(state='disabled')
        
        self.status_label.config(text=f"Validation complete - {result.result_type.value}")
        print(f"✅ Validation completed: {result.result_type.value}")
    
    def handle_error(self, error_msg):
        """Handle validation error"""
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, f"❌ VALIDATION ERROR:\n{error_msg}")
        self.results_text.config(state='disabled')
        
        self.status_label.config(text="Validation failed")
        print(f"❌ Validation error: {error_msg}")
    
    def validation_finished(self):
        """Re-enable validation button"""
        self.validate_btn.config(state='normal', text='🚀 VALIDATE')
        if not self.status_label.cget('text').startswith('Validation'):
            self.status_label.config(text="Ready")
    
    def run(self):
        """Start the GUI"""
        print("🚀 Starting Simple Multi-Agent GUI...")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = SimpleMultiAgentGUI()
        app.run()
    except Exception as e:
        print(f"❌ GUI startup error: {e}")
        import traceback
        traceback.print_exc()