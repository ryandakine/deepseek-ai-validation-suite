#!/bin/bash

# 🚀 DEEPSEEK AI VALIDATION SUITE - ONE-CLICK DEPLOYMENT SCRIPT
# The ultimate deployment tool for the unfuckable AI validation platform

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}
🚀 ========================================== 🚀
   DEEPSEEK AI VALIDATION SUITE DEPLOYMENT
   The Ultimate Multi-Agent AI Validation Platform
🚀 ========================================== 🚀
${NC}"

# Configuration
SUITE_DIR="deepseek-ai-validation-suite"
PYTHON_MIN_VERSION="3.8"
NODE_MIN_VERSION="16"

# Functions
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        log "Python ${PYTHON_VERSION} detected"
        
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            log "✅ Python version check passed"
            return 0
        else
            error "❌ Python ${PYTHON_MIN_VERSION}+ required (found ${PYTHON_VERSION})"
        fi
    else
        error "❌ Python 3 not found. Please install Python ${PYTHON_MIN_VERSION}+"
    fi
}

check_docker() {
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d ' ' -f3 | cut -d ',' -f1)
        log "Docker ${DOCKER_VERSION} detected"
        log "✅ Docker check passed"
        return 0
    else
        warn "Docker not found. Docker deployment will not be available."
        return 1
    fi
}

check_system_dependencies() {
    log "🔍 Checking system dependencies..."
    
    # Check OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        log "OS: Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        log "OS: macOS"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
        log "OS: Windows"
    else
        warn "Unknown OS: $OSTYPE"
        OS="unknown"
    fi
    
    # Check required tools
    local missing_tools=()
    
    if ! command -v git &> /dev/null; then
        missing_tools+=("git")
    fi
    
    if ! command -v curl &> /dev/null && ! command -v wget &> /dev/null; then
        missing_tools+=("curl or wget")
    fi
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        error "❌ Missing required tools: ${missing_tools[*]}"
    fi
    
    log "✅ System dependencies check passed"
}

setup_environment() {
    log "🔧 Setting up environment..."
    
    # Create directories
    mkdir -p data logs models monitoring/grafana monitoring db nginx/ssl
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        log "📝 Creating .env configuration file..."
        cat > .env << 'EOF'
# DeepSeek AI Validation Suite Configuration
# Copy this file to .env and fill in your API keys

# API Keys (get these from respective providers)
DEEPSEEK_API_KEY=your_deepseek_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROK_API_KEY=your_grok_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_TOKEN=your_huggingface_token_here

# License and Security
LICENSE_SECRET_KEY=your_license_secret_key_here

# Database Configuration (for enterprise deployment)
POSTGRES_PASSWORD=deepseek_secure_password_123
GRAFANA_PASSWORD=grafana_admin_password_123

# Deployment Configuration
DEPLOYMENT_MODE=development
LOG_LEVEL=INFO
CACHE_ENABLED=true
MONITORING_ENABLED=false
EOF
        warn "📋 Please edit .env file with your API keys before running the suite"
    fi
    
    log "✅ Environment setup complete"
}

install_python_version() {
    log "🐍 Installing Python dependencies..."
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log "Created virtual environment"
    fi
    
    # Activate venv and install
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install the package
    pip install -e .[all]
    
    log "✅ Python installation complete"
}

install_docker_version() {
    log "🐳 Setting up Docker deployment..."
    
    # Build images
    docker-compose build
    
    # Create necessary directories
    mkdir -p data logs models
    
    log "✅ Docker setup complete"
}

run_tests() {
    log "🧪 Running system tests..."
    
    if [ -d "venv" ]; then
        source venv/bin/activate
        
        # Test imports
        python -c "
import sys
sys.path.append('02_Technical_System')
try:
    from multi_agent_orchestrator import MultiAgentOrchestrator
    from quantum_blockchain_logger import SecureValidationLogger
    from ai_feedback_optimizer import AIFeedbackOptimizer
    from enterprise_licensing import LicenseManager
    print('✅ All core modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"
        
        # Test basic functionality
        python -c "
import sys
sys.path.append('02_Technical_System')
from quantum_blockchain_logger import SecureValidationLogger

try:
    logger = SecureValidationLogger()
    print('✅ Quantum blockchain logger initialized')
except Exception as e:
    print(f'❌ Logger initialization failed: {e}')
    sys.exit(1)
"
        
        log "✅ Core tests passed"
    else
        warn "Skipping tests (virtual environment not found)"
    fi
}

display_usage_instructions() {
    echo -e "\n${CYAN}
🎉 DEPLOYMENT COMPLETE! 🎉

Your DeepSeek AI Validation Suite is ready to use!

📋 NEXT STEPS:
${NC}"

    if [ -f ".env" ]; then
        echo -e "${YELLOW}1. Configure API Keys:${NC}"
        echo "   Edit .env file with your API keys:"
        echo "   - DeepSeek API key"
        echo "   - Claude API key (optional)"
        echo "   - Gemini API key (optional)"
        echo "   - Grok API key (optional)"
        echo ""
    fi

    if [ -d "venv" ]; then
        echo -e "${YELLOW}2. Python Usage:${NC}"
        echo "   source venv/bin/activate"
        echo "   deepseek-validate          # Command-line validation"
        echo "   deepseek-gui               # Launch GUI interface"
        echo "   deepseek-license           # License management"
        echo "   deepseek-blockchain        # Blockchain logging demo"
        echo "   deepseek-feedback          # AI feedback optimization"
        echo ""
    fi

    if command -v docker &> /dev/null; then
        echo -e "${YELLOW}3. Docker Usage:${NC}"
        echo "   docker-compose up          # Start basic services"
        echo "   docker-compose --profile enterprise up  # Enterprise mode"
        echo "   docker-compose --profile monitoring up  # With monitoring"
        echo ""
    fi

    echo -e "${YELLOW}4. Testing:${NC}"
    echo "   python 02_Technical_System/simple_multi_gui.py  # Test GUI"
    echo "   python -m pytest tests/    # Run full test suite"
    echo ""

    echo -e "${YELLOW}5. Documentation:${NC}"
    echo "   README.md                   # Main documentation"
    echo "   BUSINESS_MODEL_V2_MULTI_AGENT.md  # Business model"
    echo "   06_Supporting_Documentation/  # Technical guides"
    echo ""

    echo -e "${GREEN}💰 REVENUE POTENTIAL:${NC}"
    echo "   Year 1: $850K+ projected revenue"
    echo "   Year 3: $4.7M+ projected revenue"
    echo "   Target market: $17B+ (AI developer tools)"
    echo ""

    echo -e "${PURPLE}🚀 Ready to dominate the AI validation market!${NC}"
}

# Main deployment flow
main() {
    log "🚀 Starting DeepSeek AI Validation Suite deployment..."
    
    # Check system
    check_system_dependencies
    check_python
    
    # Docker is optional
    DOCKER_AVAILABLE=false
    if check_docker; then
        DOCKER_AVAILABLE=true
    fi
    
    # Setup
    setup_environment
    
    # Installation method selection
    echo -e "\n${BLUE}🔧 Choose installation method:${NC}"
    echo "1) Python installation (recommended for development)"
    echo "2) Docker installation (recommended for production)"
    echo "3) Both installations"
    
    read -p "Enter your choice (1-3): " INSTALL_CHOICE
    
    case $INSTALL_CHOICE in
        1)
            install_python_version
            ;;
        2)
            if [ "$DOCKER_AVAILABLE" = true ]; then
                install_docker_version
            else
                error "Docker not available. Please install Docker or choose Python installation."
            fi
            ;;
        3)
            install_python_version
            if [ "$DOCKER_AVAILABLE" = true ]; then
                install_docker_version
            else
                warn "Docker not available, skipping Docker installation"
            fi
            ;;
        *)
            error "Invalid choice. Please run the script again."
            ;;
    esac
    
    # Run tests
    run_tests
    
    # Show usage instructions
    display_usage_instructions
    
    log "🎉 Deployment completed successfully!"
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "DeepSeek AI Validation Suite Deployment Script"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h          Show this help message"
        echo "  --python-only       Install Python version only"
        echo "  --docker-only       Install Docker version only"
        echo "  --test              Run tests only"
        echo "  --setup-only        Setup environment only"
        echo ""
        exit 0
        ;;
    --python-only)
        check_system_dependencies
        check_python
        setup_environment
        install_python_version
        run_tests
        display_usage_instructions
        ;;
    --docker-only)
        check_system_dependencies
        check_docker
        setup_environment
        install_docker_version
        display_usage_instructions
        ;;
    --test)
        run_tests
        ;;
    --setup-only)
        setup_environment
        ;;
    *)
        main
        ;;
esac