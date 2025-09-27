#!/usr/bin/env python3
"""
🚀 MULTI-AGENT VALIDATION GUI 
The fucking ultimate interface for the DeepSeek AI Validation Suite's multi-LLM capabilities.

This beast lets users:
- Select validation chains (free, pro, enterprise)
- Mix and match AI models like a DJ
- Monitor costs in real-time
- View consensus scores and individual agent responses
- Fallback management and performance monitoring

Author: DeepSeek AI Validation Suite Team
Version: 2.0.0 - The Multi-LLM Monster GUI
"""

import asyncio
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from datetime import datetime
import os
import sys

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from multi_agent_orchestrator import MultiAgentOrchestrator, ValidationResult
except ImportError as e:
    print(f"❌ Failed to import MultiAgentOrchestrator: {e}")
    print("Make sure multi_agent_orchestrator.py is in the same directory")
    sys.exit(1)

class MultiAgentValidationGUI:
    """
    The fucking ultimate GUI for multi-agent AI validation.
    Makes Guardrails.ai look like a toy.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 DeepSeek AI Validation Suite - Multi-Agent Monster")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Initialize orchestrator
        try:
            self.orchestrator = MultiAgentOrchestrator("agent_config.yaml")
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Failed to load configuration: {e}")
            sys.exit(1)
        
        # GUI state
        self.current_user_tier = tk.StringVar(value="free")
        self.selected_chain = tk.StringVar(value="free_basic")
        self.validation_type = tk.StringVar(value="code_validation")
        self.auto_refresh_costs = tk.BooleanVar(value=True)
        
        # Results storage
        self.validation_history = []
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.start_cost_monitor()
        
        print("🚀 Multi-Agent Validation GUI initialized successfully!")
    
    def setup_styles(self):
        """Configure custom styles for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme
        style.configure('Title.TLabel', 
                       background='#1e1e1e', 
                       foreground='#00ff41',
                       font=('Consolas', 16, 'bold'))
        
        style.configure('Header.TLabel',
                       background='#1e1e1e',
                       foreground='#ffffff',
                       font=('Consolas', 12, 'bold'))
        
        style.configure('Info.TLabel',
                       background='#1e1e1e',
                       foreground='#cccccc',
                       font=('Consolas', 10))
        
        style.configure('Success.TLabel',
                       background='#1e1e1e',
                       foreground='#00ff41',
                       font=('Consolas', 10, 'bold'))
        
        style.configure('Warning.TLabel',
                       background='#1e1e1e',
                       foreground='#ffaa00',
                       font=('Consolas', 10, 'bold'))
        
        style.configure('Error.TLabel',
                       background='#1e1e1e',
                       foreground='#ff0040',
                       font=('Consolas', 10, 'bold'))
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        
        # Main title
        title_frame = tk.Frame(self.root, bg='#1e1e1e')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = ttk.Label(title_frame, 
                               text="🚀 DeepSeek AI Validation Suite - Multi-Agent Edition",
                               style='Title.TLabel')
        title_label.pack(side='left')
        
        # Status indicators
        self.status_frame = tk.Frame(title_frame, bg='#1e1e1e')
        self.status_frame.pack(side='right')
        
        self.cost_label = ttk.Label(self.status_frame, text="Cost: $0.00", style='Success.TLabel')
        self.cost_label.pack(side='right', padx=10)
        
        # Create main sections
        self.create_config_section()
        self.create_input_section()
        self.create_results_section()
        self.create_monitoring_section()
        
    def create_config_section(self):
        """Create configuration section with model and chain selection"""
        
        config_frame = tk.LabelFrame(self.root, text="🔧 Configuration", 
                                   bg='#2d2d2d', fg='#ffffff', font=('Consolas', 12, 'bold'))
        config_frame.pack(fill='x', padx=10, pady=5)
        
        # User tier selection
        tier_frame = tk.Frame(config_frame, bg='#2d2d2d')
        tier_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(tier_frame, text="User Tier:", style='Header.TLabel').pack(side='left')
        
        tier_combo = ttk.Combobox(tier_frame, textvariable=self.current_user_tier,
                                 values=['free', 'professional', 'enterprise'],
                                 state='readonly', width=15)
        tier_combo.pack(side='left', padx=10)
        tier_combo.bind('<<ComboboxSelected>>', self.on_tier_changed)
        
        # Validation chain selection
        chain_frame = tk.Frame(config_frame, bg='#2d2d2d')
        chain_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(chain_frame, text="Validation Chain:", style='Header.TLabel').pack(side='left')
        
        self.chain_combo = ttk.Combobox(chain_frame, textvariable=self.selected_chain,
                                       state='readonly', width=25)
        self.chain_combo.pack(side='left', padx=10)
        self.chain_combo.bind('<<ComboboxSelected>>', self.on_chain_changed)
        
        # Chain info label
        self.chain_info_label = ttk.Label(chain_frame, text="", style='Info.TLabel')
        self.chain_info_label.pack(side='left', padx=20)
        
        # Validation type selection
        type_frame = tk.Frame(config_frame, bg='#2d2d2d')
        type_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(type_frame, text="Validation Type:", style='Header.TLabel').pack(side='left')
        
        type_combo = ttk.Combobox(type_frame, textvariable=self.validation_type,
                                 values=['code_validation', 'content_neutrality_check', 'consensus_arbitration'],
                                 state='readonly', width=25)
        type_combo.pack(side='left', padx=10)
        
        # Update available chains initially
        self.update_available_chains()
    
    def create_input_section(self):
        """Create input section for code/content to validate"""
        
        input_frame = tk.LabelFrame(self.root, text="💻 Input Content", 
                                   bg='#2d2d2d', fg='#ffffff', font=('Consolas', 12, 'bold'))
        input_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Input text area
        input_container = tk.Frame(input_frame, bg='#2d2d2d')
        input_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_container,
                                                   height=8,
                                                   bg='#000000',
                                                   fg='#00ff41',
                                                   font=('Consolas', 11),
                                                   insertbackground='#00ff41')
        self.input_text.pack(fill='both', expand=True)
        
        # Example code button and validate button
        button_frame = tk.Frame(input_frame, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        load_example_btn = tk.Button(button_frame, text="📝 Load Example",
                                   command=self.load_example_code,
                                   bg='#404040', fg='#ffffff',
                                   font=('Consolas', 10, 'bold'))
        load_example_btn.pack(side='left', padx=5)
        
        load_file_btn = tk.Button(button_frame, text="📁 Load File",
                                command=self.load_file,
                                bg='#404040', fg='#ffffff',
                                font=('Consolas', 10, 'bold'))
        load_file_btn.pack(side='left', padx=5)
        
        self.validate_btn = tk.Button(button_frame, text="🚀 VALIDATE",
                                    command=self.start_validation,
                                    bg='#00aa00', fg='#ffffff',
                                    font=('Consolas', 12, 'bold'),
                                    state='normal')
        self.validate_btn.pack(side='right', padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(button_frame, variable=self.progress_var,
                                          mode='indeterminate')
        self.progress_bar.pack(side='right', padx=10, fill='x', expand=True)
