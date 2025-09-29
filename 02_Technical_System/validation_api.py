#!/usr/bin/env python3
"""
🔥 VALIDATION API BRIDGE - Real-time AI validation for collaborative interface
Bridges Node.js Socket.io server with Python AI validation engine
#ResendMCPHackathon #GODTIER #RealTime
"""

import sys
import json
import asyncio
import random
import time
from mcp_email_agent_pro import EnhancedMCPEmailAgent

async def run_unhinged_llm_battle(agent, code, validation_type):
    """
    🔥 UNHINGED MODE - LLM BATTLE ARENA!
    
    Instead of consensus, LLMs fight each other with conflicting opinions.
    More dramatic, chaotic, and entertaining for demos!
    """
    
    # Define battling LLM personas with opposing views
    battling_llms = {
        "DeepSeek_Aggressive": {
            "name": "DeepSeek (Aggressive)",
            "personality": "Extremely critical, finds everything wrong, paranoid about security",
            "bias": "HARSH",
            "rating_bias": -2  # Always rates lower
        },
        "Claude_Optimistic": {
            "name": "Claude (Optimistic)", 
            "personality": "Overly positive, sees potential everywhere, minimizes risks",
            "bias": "LENIENT",
            "rating_bias": +2  # Always rates higher
        },
        "GPT_Perfectionist": {
            "name": "GPT (Perfectionist)",
            "personality": "Obsessed with code style, nitpicks everything, academic focus",
            "bias": "PEDANTIC",
            "rating_bias": -1
        },
        "Grok_Chaotic": {
            "name": "Grok (Chaotic)",
            "personality": "Unpredictable, focuses on weird edge cases, contrarian",
            "bias": "RANDOM",
            "rating_bias": random.choice([-2, -1, 0, 1, 2])
        },
        "Gemini_Philosophical": {
            "name": "Gemini (Philosophical)",
            "personality": "Questions fundamental assumptions, overthinks everything",
            "bias": "THEORETICAL", 
            "rating_bias": 0
        }
    }
    
    print("🔥 Starting LLM Battle Arena...", file=sys.stderr)
    
    # Run multiple conflicting analyses
    battle_results = []
    issues_found = []
    agent_details = []
    
    for llm_id, llm_config in battling_llms.items():
        print(f"⚔️ {llm_config['name']} entering the battle...", file=sys.stderr)
        
        # Generate biased analysis based on LLM personality
        analysis = generate_biased_analysis(code, validation_type, llm_config)
        battle_results.append(analysis)
        
        # Add to issues (with conflicts!)
        issues_found.extend(analysis['issues'])
        
        # Add agent details
        agent_details.append({
            'agent_name': llm_config['name'],
            'analysis_time': random.uniform(0.5, 2.0),
            'confidence': analysis['confidence'],
            'rating': analysis['rating'],
            'bias': llm_config['bias'],
            'personality': llm_config['personality'],
            'battle_stance': analysis['battle_stance']
        })
        
        # Simulate battle delay
        await asyncio.sleep(0.1)
    
    # Generate chaotic consensus (or lack thereof)
    ratings = [r['rating_score'] for r in battle_results]
    confidences = [r['confidence'] for r in battle_results]
    
    # Battle chaos - no real consensus!
    avg_rating = sum(ratings) / len(ratings)
    rating_variance = max(ratings) - min(ratings)  # How much they disagree
    
    if rating_variance >= 3:
        chain_type = "CHAOTIC_BATTLE" 
        consensus_confidence = 0.2  # Very low confidence due to disagreement
        overall_rating = "HIGHLY_CONTESTED"
    elif rating_variance >= 2:
        chain_type = "HEATED_DEBATE"
        consensus_confidence = 0.4
        overall_rating = "DISPUTED"
    else:
        chain_type = "MILD_DISAGREEMENT"
        consensus_confidence = 0.6
        overall_rating = get_rating_from_score(avg_rating)
    
    print(f"🔥 Battle complete! Rating variance: {rating_variance}", file=sys.stderr)
    
    return {
        "overall_rating": overall_rating,
        "consensus_confidence": consensus_confidence,
        "chain_type": chain_type,
        "agents_used": [d['agent_name'] for d in agent_details],
        "battle_results": battle_results,  # Individual battle outcomes
        "issues_found": issues_found[:10],  # Limit chaos
        "agent_details": agent_details,
        "rating_variance": rating_variance,
        "unhinged_mode": True,
        "battle_summary": generate_battle_summary(battle_results)
    }

def generate_biased_analysis(code, validation_type, llm_config):
    """
    Generate a biased analysis based on LLM personality
    """
    
    # Base analysis varies by personality
    if llm_config['bias'] == 'HARSH':
        issues = [
            "CRITICAL: This code is a security nightmare!",
            "FATAL: Memory leaks everywhere!", 
            "ERROR: Violates every best practice known to mankind!",
            "WARNING: This will definitely get hacked!"
        ]
        rating_score = max(1, 3 + llm_config['rating_bias'])
        confidence = 0.95
        battle_stance = "This code is absolutely terrible and should be burned!"
        
    elif llm_config['bias'] == 'LENIENT':
        issues = [
            "Minor: Small optimization opportunity",
            "Suggestion: Could add more comments",
            "Note: Looks pretty good overall!"
        ]
        rating_score = min(5, 4 + llm_config['rating_bias']) 
        confidence = 0.85
        battle_stance = "This code shows great potential and creativity!"
        
    elif llm_config['bias'] == 'PEDANTIC':
        issues = [
            "STYLE: Inconsistent indentation detected",
            "NAMING: Variable names not descriptive enough",
            "STRUCTURE: Function should be split into smaller functions",
            "DOCUMENTATION: Missing comprehensive docstrings"
        ]
        rating_score = max(1, 3 + llm_config['rating_bias'])
        confidence = 0.90
        battle_stance = "The code logic is fine, but the style is absolutely unacceptable!"
        
    elif llm_config['bias'] == 'RANDOM':
        issue_pool = [
            "WEIRD: This might work on Tuesdays only",
            "COSMIC: Alignment with Jupiter's moons affects performance", 
            "QUANTUM: Schrödinger's bug - exists and doesn't exist simultaneously",
            "TEMPORAL: Code works fine in the past but fails in the future",
            "INTERDIMENSIONAL: Logic only valid in parallel universe"
        ]
        issues = random.sample(issue_pool, random.randint(1, 3))
        rating_score = random.randint(1, 5)
        confidence = random.uniform(0.3, 0.9)
        battle_stance = "Nobody can predict what this code will do, including me!"
        
    else:  # THEORETICAL
        issues = [
            "PHILOSOPHICAL: What IS code, really?",
            "EXISTENTIAL: Does this function serve its true purpose?",
            "METAPHYSICAL: The variables lack deeper meaning",
            "ONTOLOGICAL: Questions the very nature of algorithms"
        ]
        rating_score = 3
        confidence = 0.7
        battle_stance = "We must question whether validation itself is meaningful..."
    
    return {
        "rating": get_rating_from_score(rating_score),
        "rating_score": rating_score,
        "confidence": confidence, 
        "issues": issues,
        "battle_stance": battle_stance,
        "personality": llm_config['personality']
    }

def get_rating_from_score(score):
    """Convert numeric score to rating string"""
    if score >= 5: return "EXCELLENT"
    elif score >= 4: return "VERY_GOOD"
    elif score >= 3: return "GOOD"
    elif score >= 2: return "SATISFACTORY"
    else: return "NEEDS_IMPROVEMENT"

def generate_battle_summary(battle_results):
    """Generate entertaining battle summary"""
    stances = [r['battle_stance'] for r in battle_results]
    
    summaries = [
        "🔥 The LLMs are at each other's throats!",
        "⚔️ Epic disagreement in the AI arena!", 
        "🤯 Complete chaos - nobody agrees!",
        "🎆 The battle was fierce and opinions flew!",
        "🎪 What a spectacular show of AI conflict!"
    ]
    
    return {
        "summary": random.choice(summaries),
        "individual_stances": stances
    }

async def validate_code_realtime(code, validation_type, unhinged_mode=False):
    """
    Real-time validation endpoint for Socket.io server
    Returns JSON result for immediate broadcast
    
    If unhinged_mode=True, LLMs will battle each other with conflicting opinions!
    """
    try:
        # Create validation agent (using demo key for real-time demo)
        agent = EnhancedMCPEmailAgent(
            resend_api_key="re_demo_key_for_realtime",
            sender_email="realtime@deepseek-ai.com"
        )
        
        if unhinged_mode:
            # 🔥 UNHINGED MODE - REAL LLM BATTLE ARENA!
            print("🔥 UNHINGED MODE ACTIVATED - REAL LLMS WILL BATTLE!", file=sys.stderr)
            from real_llm_battle import RealLLMBattleArena
            
            arena = RealLLMBattleArena()
            validation_result = await arena.start_real_battle(code, validation_type)
        else:
            # Normal consensus-based validation
            validation_result = await agent._run_enhanced_validation(code, validation_type)
        
        # Generate charts for visual display
        charts = await agent._create_validation_charts(validation_result)
        
        return {
            "validation_successful": True,
            "validation_result": validation_result,
            "charts_generated": len(charts),
            "charts": charts,  # Include base64 charts for real-time display
            "realtime": True,
            "unhinged_mode": unhinged_mode,
            "processing_time": sum(d.get('analysis_time', 0) for d in validation_result['agent_details']),
            "timestamp": "now"
        }
        
    except Exception as e:
        return {
            "validation_successful": False,
            "error": str(e),
            "realtime": True,
            "unhinged_mode": unhinged_mode,
            "timestamp": "now"
        }

def main():
    """
    Main function called by Node.js server
    Reads JSON from stdin, returns JSON to stdout
    """
    try:
        # Read input from Node.js
        input_data = json.loads(sys.stdin.read())
        code = input_data.get('code', '')
        validation_type = input_data.get('type', 'general_validation')
        unhinged_mode = input_data.get('unhinged_mode', False)
        
        if unhinged_mode:
            print("🔥 UNHINGED MODE DETECTED - PREPARING FOR BATTLE!", file=sys.stderr)
        
        # Run async validation
        result = asyncio.run(validate_code_realtime(code, validation_type, unhinged_mode))
        
        # Output JSON result
        print(json.dumps(result))
        
    except Exception as e:
        error_result = {
            "validation_successful": False,
            "error": f"API Bridge Error: {str(e)}",
            "realtime": True,
            "timestamp": "now"
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()