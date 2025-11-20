#!/usr/bin/env python3
"""
DeepSeek AI Validation Web App
===============================
Simple web interface for generating and validating code.
"""

from flask import Flask, render_template, request, jsonify
import asyncio
from datetime import datetime
from deepseek_client import DeepSeekClient
from ai_validator import AIValidator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'deepseek-validation-key-change-in-production'

# Initialize clients
try:
    deepseek = DeepSeekClient()
    validator = AIValidator()
    print("✅ DeepSeek and Validator initialized!")
except Exception as e:
    print(f"⚠️  Initialization error: {e}")
    deepseek = None
    validator = None


@app.route('/')
def home():
    """Main page"""
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate_code():
    """Generate code using DeepSeek"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        if not deepseek:
            return jsonify({'error': 'DeepSeek client not available'}), 500
        
        # Generate code
        result = deepseek.generate(prompt)
        
        if not result['success']:
            return jsonify({'error': result['error']}), 500
        
        return jsonify({
            'success': True,
            'code': result['content'],
            'model': result['model'],
            'usage': result['usage'],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/validate', methods=['POST'])
def validate_code():
    """Validate code for security issues"""
    try:
        data = request.json
        code = data.get('code', '')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        if not validator:
            return jsonify({'error': 'Validator not available'}), 500
        
        # Run validation in async context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            validation_result = loop.run_until_complete(validator.validate(code))
            
            return jsonify({
                'success': True,
                'validation_id': f"val_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'timestamp': datetime.now().isoformat(),
                'risk_score': validation_result['risk_score'],
                'issues': validation_result['issues'],
                'confidence': validation_result['confidence'],
                'agent': validation_result['agent']
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-and-validate', methods=['POST'])
def generate_and_validate():
    """Generate code and immediately validate it"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        if not deepseek or not validator:
            return jsonify({'error': 'Services not available'}), 500
        
        # Generate code
        gen_result = deepseek.generate(prompt)
        
        if not gen_result['success']:
            return jsonify({'error': gen_result['error']}), 500
        
        code = gen_result['content']
        
        # Validate code
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            val_result = loop.run_until_complete(validator.validate(code))
            
            return jsonify({
                'success': True,
                'code': code,
                'model': gen_result['model'],
                'usage': gen_result['usage'],
                'validation': {
                    'risk_score': val_result['risk_score'],
                    'issues': val_result['issues'],
                    'confidence': val_result['confidence'],
                    'agent': val_result['agent']
                },
                'timestamp': datetime.now().isoformat()
            })
            
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'deepseek_available': deepseek is not None,
        'validator_available': validator is not None,
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("🚀 Starting DeepSeek AI Validation Server...")
    print("🌐 Open http://localhost:5000 to use the app")
    app.run(debug=True, host='0.0.0.0', port=5000)