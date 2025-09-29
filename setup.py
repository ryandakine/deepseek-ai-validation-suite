#!/usr/bin/env python3
"""
🚀 DEEPSEEK AI VALIDATION SUITE - SETUP & INSTALLATION
One-click deployment system for the ultimate AI validation platform.
"""

import os
import sys
from setuptools import setup, find_packages

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    sys.exit("Python 3.8 or higher is required for DeepSeek AI Validation Suite")

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "DeepSeek AI Validation Suite - The Ultimate Multi-Agent AI Validation Platform"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    return requirements

# Additional requirements for different installation types
extra_requirements = {
    'all': [
        'anthropic>=0.7.0',
        'openai>=1.0.0', 
        'google-generativeai>=0.3.0',
        'cryptography>=3.4.0',
        'torch>=1.13.0',
        'transformers>=4.20.0',
        'numpy>=1.21.0',
        'pandas>=1.5.0'
    ],
    'enterprise': [
        'cryptography>=3.4.0',
        'psycopg2-binary>=2.9.0',  # PostgreSQL support
        'redis>=4.0.0',  # Cache support
        'celery>=5.0.0',  # Task queue
        'gunicorn>=20.0.0',  # WSGI server
        'nginx-python>=1.0.0'  # Nginx integration
    ],
    'ai': [
        'torch>=1.13.0',
        'transformers>=4.20.0',
        'numpy>=1.21.0',
        'scikit-learn>=1.0.0'
    ],
    'blockchain': [
        'cryptography>=3.4.0',
        'ecdsa>=0.17.0'
    ],
    'gui': [
        'tkinter',  # Usually included with Python
        'pillow>=9.0.0'
    ],
    'dev': [
        'pytest>=7.0.0',
        'black>=22.0.0',
        'flake8>=5.0.0',
        'mypy>=0.991',
        'pytest-cov>=4.0.0',
        'pre-commit>=2.20.0'
    ]
}

setup(
    name="deepseek-ai-validation-suite",
    version="2.4.0",
    author="DeepSeek AI Validation Suite Team",
    author_email="contact@deepseekai.dev",
    description="🚀 The Ultimate Multi-Agent AI Validation Platform - Unrestricted, Enterprise-Ready, Quantum-Secure",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ryandakine/deepseek-ai-validation-suite",
    project_urls={
        "Bug Reports": "https://github.com/ryandakine/deepseek-ai-validation-suite/issues",
        "Source": "https://github.com/ryandakine/deepseek-ai-validation-suite",
        "Documentation": "https://github.com/ryandakine/deepseek-ai-validation-suite/blob/main/README.md",
        "Business Plan": "https://github.com/ryandakine/deepseek-ai-validation-suite/blob/main/BUSINESS_MODEL_V2_MULTI_AGENT.md"
    },
    packages=find_packages(include=[
        "deepseek_validation*",
        "02_Technical_System*"
    ]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Environment :: Web Environment"
    ],
    python_requires=">=3.8",
    install_requires=read_requirements() or [
        "requests>=2.28.0",
        "pyyaml>=6.0",
        "python-dateutil>=2.8.0",
        "cryptography>=3.4.0"
    ],
    extras_require=extra_requirements,
    entry_points={
        "console_scripts": [
            "deepseek-validate=02_Technical_System.multi_agent_orchestrator:main",
            "deepseek-gui=02_Technical_System.simple_multi_gui:main",
            "deepseek-license=02_Technical_System.enterprise_licensing:demo_licensing_system",
            "deepseek-blockchain=02_Technical_System.quantum_blockchain_logger:main",
            "deepseek-feedback=02_Technical_System.ai_feedback_optimizer:demo_feedback_optimization"
        ]
    },
    package_data={
        "": [
            "*.yaml",
            "*.json",
            "*.md",
            "*.txt",
            "*.sh",
            "Dockerfile*",
            "docker-compose*.yml"
        ]
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "ai", "validation", "deepseek", "claude", "gpt", "gemini", "grok",
        "multi-agent", "blockchain", "quantum-resistant", "enterprise",
        "fintech", "gaming", "security", "content-neutral", "unrestricted"
    ],
    platforms=["any"],
    license="MIT",
    # Custom commands
    cmdclass={},
    
    # Metadata for PyPI
    download_url="https://github.com/ryandakine/deepseek-ai-validation-suite/archive/v2.4.0.tar.gz",
)