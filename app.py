#!/usr/bin/env python3
"""
SIMPLE WEB FRONTEND FOR HACKATHON DEMO
======================================

Clean, simple interface for judges to see the platform in action.
Real AI validation + real email sending!
"""

from flask import Flask, render_template, request, jsonify, flash
import asyncio
import json
from datetime import datetime
from real_resend_integration import RealResendMCP
from real_ai_validator import RealAIValidator
from typing import Dict

app = Flask(__name__)
app.secret_key = 'hackathon_demo_key'

# Initialize real components
resend_client = None
ai_validator = None

try:
    resend_client = RealResendMCP()
    ai_validator = RealAIValidator()
    print("✅ Real integrations initialized!")
except Exception as e:
    print(f"⚠️  Integration error: {e}")

@app.route('/')
def home():
    """Main demo page"""
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate_code():
    """Handle code validation requests"""
    try:
        data = request.json
        code = data.get('code', '')
        email = data.get('email', '')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Run validation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Real AI validation
            if ai_validator:
                validation_result = loop.run_until_complete(ai_validator.quick_validate(code))
            else:
                validation_result = {"error": "AI validator not available"}
            
            response = {
                'validation_id': f"val_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'timestamp': datetime.now().isoformat(),
                'validation_result': validation_result
            }
            
            # Send email if requested and email provided
            if email and resend_client and validation_result.get('risk_score', 0) > 0:
                email_result = loop.run_until_complete(send_validation_email(
                    email, code, validation_result
                ))
                response['email_sent'] = email_result
            
            return jsonify(response)
            
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

async def send_validation_email(email: str, code: str, validation: Dict):
    """Send real validation email"""
    if not resend_client:
        return {"error": "Email client not available"}
    
    risk_score = validation.get('risk_score', 0)
    issues = validation.get('issues', [])
    
    # Generate email content
    if risk_score >= 0.7:
        subject = f"🚨 HIGH RISK - Code Validation Alert (Score: {risk_score:.2f})"
        urgency = "🚨 HIGH RISK"
        color = "#ff4444"
    elif risk_score >= 0.4:
        subject = f"⚠️ MEDIUM RISK - Code Validation Report (Score: {risk_score:.2f})"
        urgency = "⚠️ MEDIUM RISK"
        color = "#ff8800"
    else:
        subject = f"✅ LOW RISK - Code Validation Complete (Score: {risk_score:.2f})"
        urgency = "✅ LOW RISK"
        color = "#44ff44"
    
    # Text version
    text_content = f"""
🤖 AI CODE VALIDATION REPORT
============================

Risk Level: {urgency}
Risk Score: {risk_score:.2f}/1.0
Validation Agent: {validation.get('agent', 'AI Validator')}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

ISSUES DETECTED:
"""
    
    if issues:
        for i, issue in enumerate(issues, 1):
            text_content += f"{i}. {issue}\n"
    else:
        text_content += "No security issues detected.\n"
    
    text_content += f"""
CODE ANALYZED:
{'-' * 40}
{code[:200]}{'...' if len(code) > 200 else ''}
{'-' * 40}

🚀 Powered by AI Validation Suite + Resend MCP
Built for #ResendMCPHackathon
"""
    
    # HTML version
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Arial', sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #eee; }}
        .risk-badge {{ display: inline-block; padding: 10px 20px; border-radius: 25px; color: white; font-weight: bold; background: {color}; }}
        .issues {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .code-preview {{ background: #f1f3f4; padding: 15px; border-radius: 5px; font-family: monospace; overflow-x: auto; }}
        .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Code Validation Report</h1>
            <div class="risk-badge">{urgency} - Score: {risk_score:.2f}</div>
        </div>
        
        <div style="margin: 20px 0;">
            <strong>Agent:</strong> {validation.get('agent', 'AI Validator')}<br>
            <strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            <strong>Confidence:</strong> {validation.get('confidence', 0.8):.1%}
        </div>
        
        <div class="issues">
            <h3>🛡️ Security Analysis</h3>
            {"<ul>" + "".join(f"<li>{issue}</li>" for issue in issues) + "</ul>" if issues else "<p style='color: #28a745;'>✅ No security issues detected</p>"}
        </div>
        
        <div class="code-preview">
            <h4>📝 Code Analyzed:</h4>
            <pre>{code[:300]}{'...' if len(code) > 300 else ''}</pre>
        </div>
        
        <div class="footer">
            <p><strong>🚀 Powered by AI Validation Suite + Resend MCP</strong></p>
            <p>Built for <strong>#ResendMCPHackathon</strong></p>
        </div>
    </div>
</body>
</html>
"""
    
    # Send the email
    return await resend_client.send_email(
        to=email,
        subject=subject,
        text=text_content,
        html=html_content
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'resend_available': resend_client is not None,
        'ai_available': ai_validator is not None,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting AI Validation Demo Server...")
    print("🌐 Open http://localhost:5000 to see the demo")
    app.run(debug=True, host='0.0.0.0', port=5000)