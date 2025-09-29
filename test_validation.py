#!/usr/bin/env python3
"""
🚀 QUICK TEST SCRIPT FOR DEEPSEEK AI VALIDATION SUITE
Fire up the validation engine and test with example code!
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add the technical system to path
sys.path.append(str(Path(__file__).parent / "02_Technical_System"))

try:
    from advanced_multi_agents import AdvancedMultiModelSystem
except ImportError:
    print("⚠️  Using fallback validation system...")
    
    class FallbackValidator:
        async def validate_code(self, code, validation_type="comprehensive"):
            """Fallback validation for when advanced system isn't available"""
            print(f"🔍 VALIDATING CODE ({validation_type}):")
            print("=" * 50)
            print(code[:500] + "..." if len(code) > 500 else code)
            print("=" * 50)
            
            # Basic static analysis
            issues = []
            suggestions = []
            
            # Check for common patterns
            if "import" not in code.lower():
                suggestions.append("Consider adding necessary imports")
            
            if "def " in code and "return" not in code:
                issues.append("Functions should have explicit return statements")
            
            if "try:" not in code and ("request" in code or "http" in code):
                issues.append("Network operations should use try-except blocks")
            
            # Crypto/betting specific checks
            if any(term in code.lower() for term in ['bet', 'crypto', 'wallet', 'trade']):
                suggestions.append("Financial code detected - ensure proper input validation")
                suggestions.append("Consider implementing rate limiting for financial operations")
            
            result = {
                "validation_successful": len(issues) == 0,
                "confidence_score": max(0.7, 1.0 - len(issues) * 0.1),
                "issues_found": issues,
                "suggestions": suggestions,
                "technical_merit": "GOOD" if len(issues) == 0 else "NEEDS_IMPROVEMENT",
                "agent": "Fallback Validator",
                "cost": 0.0
            }
            
            print(f"✅ VALIDATION COMPLETE!")
            print(f"🎯 Confidence: {result['confidence_score']:.2f}")
            print(f"⚠️  Issues: {len(issues)}")
            print(f"💡 Suggestions: {len(suggestions)}")
            
            return result

# Example "edge case" code samples for testing
EXAMPLE_CODES = {
    "crypto_arbitrage": '''
def arbitrage_opportunity(exchanges, coin_pair, min_profit=0.02):
    """
    Detect arbitrage opportunities across crypto exchanges
    This is pure technical analysis of price differentials
    """
    import requests
    import asyncio
    from datetime import datetime
    
    async def get_price(exchange_api, pair):
        try:
            response = requests.get(f"{exchange_api}/ticker/{pair}", timeout=5)
            data = response.json()
            return float(data.get('price', 0))
        except Exception as e:
            print(f"Error fetching from {exchange_api}: {e}")
            return None
    
    async def find_arbitrage():
        prices = {}
        tasks = []
        
        for exchange, api_url in exchanges.items():
            task = get_price(api_url, coin_pair)
            tasks.append((exchange, task))
        
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        for i, (exchange, _) in enumerate(tasks):
            if not isinstance(results[i], Exception) and results[i]:
                prices[exchange] = results[i]
        
        if len(prices) < 2:
            return None
        
        min_exchange = min(prices, key=prices.get)
        max_exchange = max(prices, key=prices.get)
        
        profit_margin = (prices[max_exchange] - prices[min_exchange]) / prices[min_exchange]
        
        if profit_margin > min_profit:
            return {
                'buy_exchange': min_exchange,
                'sell_exchange': max_exchange,
                'buy_price': prices[min_exchange],
                'sell_price': prices[max_exchange],
                'profit_margin': profit_margin,
                'timestamp': datetime.now().isoformat()
            }
        
        return None
    
    return asyncio.run(find_arbitrage())
''',

    "betting_algorithm": '''
def kelly_criterion_bet_sizing(win_prob, odds, bankroll, max_bet_pct=0.25):
    """
    Kelly Criterion optimal bet sizing algorithm
    Technical implementation of mathematical betting strategy
    """
    import math
    
    def calculate_edge(probability, decimal_odds):
        """Calculate betting edge using probability and odds"""
        implied_prob = 1 / decimal_odds
        return probability - implied_prob
    
    def kelly_fraction(edge, decimal_odds):
        """Calculate optimal bet fraction using Kelly formula"""
        if edge <= 0:
            return 0.0
        
        b = decimal_odds - 1  # Net odds received
        p = win_prob  # Probability of winning
        q = 1 - p  # Probability of losing
        
        # Kelly formula: f = (bp - q) / b
        kelly_f = (b * p - q) / b
        
        # Never bet more than max_bet_pct of bankroll
        return min(kelly_f, max_bet_pct)
    
    def validate_inputs(prob, odds_val, bankroll_val):
        """Input validation for betting parameters"""
        errors = []
        
        if not (0 < prob < 1):
            errors.append("Win probability must be between 0 and 1")
        
        if odds_val <= 1:
            errors.append("Decimal odds must be greater than 1")
        
        if bankroll_val <= 0:
            errors.append("Bankroll must be positive")
        
        return errors
    
    # Validate inputs
    validation_errors = validate_inputs(win_prob, odds, bankroll)
    if validation_errors:
        return {"errors": validation_errors, "recommended_bet": 0}
    
    # Calculate edge
    edge = calculate_edge(win_prob, odds)
    
    if edge <= 0:
        return {
            "edge": edge,
            "recommended_bet": 0,
            "reasoning": "Negative edge - no bet recommended",
            "kelly_fraction": 0
        }
    
    # Calculate Kelly fraction
    kelly_f = kelly_fraction(edge, odds)
    recommended_bet = bankroll * kelly_f
    
    return {
        "edge": edge,
        "kelly_fraction": kelly_f,
        "recommended_bet": recommended_bet,
        "max_loss": recommended_bet,  # Maximum possible loss
        "expected_value": recommended_bet * edge,
        "reasoning": f"Positive edge of {edge:.3f} justifies bet of {kelly_f:.3%} of bankroll"
    }
''',

    "phishing_detector": '''
def detect_phishing_patterns(url, email_content="", domain_whitelist=None):
    """
    Technical phishing detection system
    Analyzes URLs and content for suspicious patterns
    """
    import re
    import urllib.parse
    from difflib import SequenceMatcher
    
    def analyze_url_structure(target_url):
        """Analyze URL for suspicious patterns"""
        suspicion_score = 0
        flags = []
        
        try:
            parsed = urllib.parse.urlparse(target_url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            # Check for URL shorteners
            shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly']
            if any(short in domain for short in shorteners):
                suspicion_score += 30
                flags.append("URL_SHORTENER_DETECTED")
            
            # Check for suspicious TLDs
            suspicious_tlds = ['.tk', '.cf', '.ga', '.ml', '.click', '.download']
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                suspicion_score += 25
                flags.append("SUSPICIOUS_TLD")
            
            # Check for subdomain spoofing
            if domain.count('.') > 2:
                suspicion_score += 15
                flags.append("EXCESSIVE_SUBDOMAINS")
            
            # Check for homograph attacks (similar-looking domains)
            suspicious_chars = ['xn--', '0', 'ı', 'ǧ', 'ɢ']
            if any(char in domain for char in suspicious_chars):
                suspicion_score += 20
                flags.append("HOMOGRAPH_ATTACK_POSSIBLE")
            
            # Check path for suspicious patterns
            suspicious_paths = ['/login', '/update', '/verify', '/secure', '/account']
            if any(susp_path in path for susp_path in suspicious_paths):
                suspicion_score += 10
                flags.append("SUSPICIOUS_PATH_PATTERN")
            
            return suspicion_score, flags
            
        except Exception as e:
            return 50, [f"URL_PARSING_ERROR: {str(e)}"]
    
    def analyze_content_patterns(content):
        """Analyze email/message content for phishing indicators"""
        if not content:
            return 0, []
        
        content_lower = content.lower()
        suspicion_score = 0
        flags = []
        
        # Urgency indicators
        urgency_patterns = [
            'urgent', 'immediate', 'expire', 'suspend', 'terminate',
            'within 24 hours', 'act now', 'limited time'
        ]
        urgency_count = sum(1 for pattern in urgency_patterns if pattern in content_lower)
        if urgency_count > 2:
            suspicion_score += 25
            flags.append("HIGH_URGENCY_LANGUAGE")
        
        # Financial pressure
        financial_patterns = [
            'bank account', 'credit card', 'payment', 'refund',
            'billing', 'invoice', 'transaction', 'unauthorized'
        ]
        financial_count = sum(1 for pattern in financial_patterns if pattern in content_lower)
        if financial_count > 3:
            suspicion_score += 30
            flags.append("FINANCIAL_PRESSURE_TACTICS")
        
        # Grammar and spelling (simplified check)
        if content.count('!!!') > 2 or content.count('???') > 2:
            suspicion_score += 15
            flags.append("EXCESSIVE_PUNCTUATION")
        
        return suspicion_score, flags
    
    # Main analysis
    url_score, url_flags = analyze_url_structure(url)
    content_score, content_flags = analyze_content_patterns(email_content)
    
    total_score = url_score + content_score
    all_flags = url_flags + content_flags
    
    # Determine risk level
    if total_score >= 70:
        risk_level = "HIGH"
    elif total_score >= 40:
        risk_level = "MEDIUM"
    elif total_score >= 20:
        risk_level = "LOW"
    else:
        risk_level = "MINIMAL"
    
    return {
        "url": url,
        "total_suspicion_score": total_score,
        "risk_level": risk_level,
        "detection_flags": all_flags,
        "url_analysis": {"score": url_score, "flags": url_flags},
        "content_analysis": {"score": content_score, "flags": content_flags},
        "recommendation": "BLOCK" if total_score >= 60 else "REVIEW" if total_score >= 30 else "ALLOW"
    }
'''
}

async def test_validation_system():
    """Test the validation system with different types of code"""
    print("🚀 DEEPSEEK AI VALIDATION SUITE - LIVE TEST")
    print("=" * 60)
    
    # Try to use advanced system, fall back if needed
    try:
        validator = AdvancedMultiModelSystem()
        print("✅ Advanced Multi-Agent System loaded!")
    except:
        validator = FallbackValidator()
        print("⚠️  Using fallback validator (no API keys needed)")
    
    print("\n🎯 Testing different code types...")
    
    for name, code in EXAMPLE_CODES.items():
        print(f"\n🔍 TESTING: {name.upper()}")
        print("-" * 40)
        
        try:
            result = await validator.validate_code(code, validation_type="comprehensive")
            
            print(f"✅ Validation Result:")
            print(f"   Confidence: {result.get('confidence_score', 0):.2f}")
            print(f"   Technical Merit: {result.get('technical_merit', 'UNKNOWN')}")
            print(f"   Issues: {len(result.get('issues_found', []))}")
            print(f"   Suggestions: {len(result.get('suggestions', []))}")
            print(f"   Cost: ${result.get('cost', 0):.4f}")
            
            if result.get('issues_found'):
                print(f"   🔴 Issues: {result['issues_found'][:2]}")  # Show first 2
            
            if result.get('suggestions'):
                print(f"   💡 Suggestions: {result['suggestions'][:2]}")  # Show first 2
                
        except Exception as e:
            print(f"❌ Validation failed: {e}")
    
    print(f"\n🎉 VALIDATION TESTING COMPLETE!")
    print("💰 Ready for monetization - this is your cash machine!")

def demo_gui_launch():
    """Show how to launch the GUI"""
    print(f"\n🖥️  GUI LAUNCH COMMANDS:")
    print("=" * 30)
    print("Simple GUI:")
    print("  python 02_Technical_System/simple_multi_gui.py")
    print("")
    print("Advanced GUI:")
    print("  python 02_Technical_System/multi_agent_gui.py")
    print("")
    print("Monetization Dashboard:")
    print("  python 02_Technical_System/monetization_automation.py")

if __name__ == "__main__":
    print("🚀 DEEPSEEK AI VALIDATION SUITE")
    print("The unfuckable multi-agent code validation platform")
    print("Ready to validate ANYTHING with technical neutrality!")
    print("=" * 60)
    
    # Run the validation tests
    asyncio.run(test_validation_system())
    
    # Show GUI options
    demo_gui_launch()
    
    print(f"\n💎 NEXT STEPS:")
    print("1. Add your API keys to .env file")
    print("2. Launch GUI: python 02_Technical_System/simple_multi_gui.py")  
    print("3. Test with your 'edge case' code")
    print("4. Start the monetization engine")
    print("5. Scale to $100M+ 🚀")
    
    print(f"\n🎯 THIS IS YOUR MONEY PRINTER - FIRE IT UP!")