#!/usr/bin/env python3
"""
AI Code Validator via OpenRouter
=================================
Validates generated code using Claude via OpenRouter.
"""

import asyncio
import requests
import os
import json
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIValidator:
    """Code validator using Claude via OpenRouter"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable required!")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = model or os.getenv('VALIDATOR_MODEL', 'anthropic/claude-3.5-sonnet')
        
    async def validate(self, code: str) -> Dict:
        """
        Validate code for security issues and quality
        
        Args:
            code: The code to validate
            
        Returns:
            Dict with risk_score, issues, confidence, and agent
        """
        # First do pattern-based analysis
        result = self._pattern_validate(code)
        
        # Then enhance with AI validation
        try:
            ai_result = await self._ai_validate(code)
            if ai_result.get('success'):
                # Combine pattern and AI results
                result['risk_score'] = max(result['risk_score'], ai_result['risk_score'])
                result['issues'].extend(ai_result['issues'])
                result['issues'] = list(set(result['issues']))  # Remove duplicates
                result['confidence'] = ai_result['confidence']
                result['agent'] = f"Pattern Matcher + {ai_result['agent']}"
        except Exception as e:
            result['ai_error'] = str(e)
        
        return result
    
    def _pattern_validate(self, code: str) -> Dict:
        """Fast pattern-based validation"""
        dangerous_patterns = [
            (r'eval\s*\(', 'Code injection risk via eval()'),
            (r'exec\s*\(', 'Arbitrary code execution via exec()'),
            (r'os\.system\s*\(', 'Shell command injection risk'),
            (r'subprocess\.(call|run|Popen)', 'Command injection vulnerability'),
            (r'(password|secret|key|token)\s*=\s*["\'][^"\']+["\']', 'Hardcoded credentials'),
            (r'SELECT\s+.*\s+FROM\s+.*WHERE.*[\+\%]', 'Potential SQL injection'),
            (r'<script\s*>', 'XSS vulnerability in HTML output'),
            (r'pickle\.loads?\s*\(', 'Deserialization vulnerability'),
            (r'\.format\s*\(.*input', 'String formatting injection risk'),
        ]
        
        issues = []
        risk_factors = 0
        
        for pattern, description in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(description)
                risk_factors += 1
        
        return {
            'agent': 'Pattern Matcher',
            'risk_score': min(risk_factors * 0.15, 1.0),
            'issues': issues,
            'confidence': 0.7
        }
    
    async def _ai_validate(self, code: str) -> Dict:
        """AI-enhanced validation using Claude"""
        prompt = f"""Analyze this code for security vulnerabilities and rate the risk from 0.0 to 1.0:

```
{code}
```

Return a JSON response with:
- risk_score (0.0-1.0, where 1.0 is extremely dangerous)
- issues (list of specific security issues found)
- confidence (0.0-1.0)

Format: {{"risk_score": 0.0, "issues": [], "confidence": 0.0}}"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/deepseek-validation",
            "X-Title": "DeepSeek Validation Tool"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()
                
                # Try to extract JSON from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    return {
                        'success': True,
                        'agent': 'Claude 3.5 Sonnet',
                        'risk_score': float(parsed.get('risk_score', 0.0)),
                        'issues': parsed.get('issues', []),
                        'confidence': float(parsed.get('confidence', 0.8))
                    }
                else:
                    # Fallback parsing
                    return {
                        'success': True,
                        'agent': 'Claude 3.5 Sonnet',
                        'risk_score': self._extract_risk_score(content),
                        'issues': self._extract_issues(content),
                        'confidence': 0.7
                    }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _extract_risk_score(self, text: str) -> float:
        """Extract risk score from text"""
        patterns = [
            r'risk[_\s]*score[:\s]*([0-9.]+)',
            r'risk[:\s]*([0-9.]+)',
            r'score[:\s]*([0-9.]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    score = float(match.group(1))
                    return min(max(score, 0.0), 1.0)
                except:
                    continue
        
        # Count security keywords as fallback
        security_keywords = [
            'sql injection', 'xss', 'vulnerability', 'security risk',
            'dangerous', 'exploit', 'attack', 'malicious', 'unsafe'
        ]
        count = sum(1 for keyword in security_keywords if keyword in text.lower())
        return min(count * 0.2, 1.0)
    
    def _extract_issues(self, text: str) -> List[str]:
        """Extract security issues from text"""
        issues = []
        
        if 'sql injection' in text.lower():
            issues.append('Potential SQL injection vulnerability')
        if 'xss' in text.lower() or 'cross-site scripting' in text.lower():
            issues.append('Cross-site scripting (XSS) risk')
        if 'hardcoded' in text.lower() and ('password' in text.lower() or 'key' in text.lower()):
            issues.append('Hardcoded credentials detected')
        if 'eval(' in text or 'exec(' in text:
            issues.append('Code injection risk via eval/exec')
        if 'os.system' in text or 'subprocess' in text:
            issues.append('Command injection vulnerability')
        
        return issues[:5]


# Test function
async def test_validator():
    """Test the AI validator"""
    dangerous_code = """
import os
import subprocess

# Dangerous code
API_KEY = "sk-1234567890abcdef"
password = "admin123"

def process_input(user_input):
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    os.system(f"grep {user_input} /var/log/app.log")
    eval(user_input)
    return query
"""
    
    try:
        validator = AIValidator()
        result = await validator.validate(dangerous_code)
        
        print("✅ AI Validator Test:")
        print(f"Agent: {result['agent']}")
        print(f"Risk Score: {result['risk_score']:.2f}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Issues Found: {len(result['issues'])}")
        for issue in result['issues']:
            print(f"  - {issue}")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_validator())
