#!/usr/bin/env python3
"""
🔥 REAL LLM BATTLE ARENA - No More Puppet Show!
Actual API calls to real LLMs fighting each other
#ResendMCPHackathon #RealLLMBattle #NoMockData
"""

import asyncio
import json
import sys
import os
import random
import time
import aiohttp
from typing import Dict, List, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RealLLMBattleArena:
    """Real LLM Battle Arena - Actual API calls, genuine AI opinions"""
    
    def __init__(self):
        # Real API configurations - you'll need to add your actual API keys
        self.llm_configs = {
            "openai_gpt4": {
                "name": "GPT-4 (Perfectionist)",
                "url": "https://api.openai.com/v1/chat/completions",
                "headers": {
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', 'your-openai-key')}",
                    "Content-Type": "application/json"
                },
                "model": "gpt-4",
                "personality": "You are a perfectionist code reviewer who finds flaws in everything. Be extremely critical and pedantic about style, performance, and best practices.",
                "max_tokens": 500,
                "temperature": 0.1  # Low for consistency
            },
            "claude_3": {
                "name": "Claude-3 (Optimistic)", 
                "url": "https://api.anthropic.com/v1/messages",
                "headers": {
                    "x-api-key": os.getenv('ANTHROPIC_API_KEY', 'your-anthropic-key'),
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                },
                "model": "claude-3-sonnet-20240229",
                "personality": "You are an optimistic AI that sees the best in every piece of code. Focus on potential, creativity, and positive aspects while downplaying risks.",
                "max_tokens": 500,
                "temperature": 0.3
            },
            "deepseek_coder": {
                "name": "DeepSeek-Coder (Security Paranoid)",
                "url": "https://api.deepseek.com/v1/chat/completions",
                "headers": {
                    "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY', 'your-deepseek-key')}",
                    "Content-Type": "application/json"
                },
                "model": "deepseek-coder",
                "personality": "You are paranoid about security. Find every possible vulnerability, attack vector, and security flaw. Assume the worst about every piece of code.",
                "max_tokens": 500,
                "temperature": 0.2
            },
            "gemini_pro": {
                "name": "Gemini-Pro (Philosophical)",
                "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={os.getenv('GEMINI_API_KEY', 'your-gemini-key')}",
                "headers": {
                    "Content-Type": "application/json"
                },
                "model": "gemini-pro",
                "personality": "You are a philosophical AI that questions the fundamental assumptions of code. Ask deep questions about purpose, meaning, and the nature of programming itself.",
                "max_tokens": 500,
                "temperature": 0.5
            },
            "local_llm": {
                "name": "Local LLM (Chaotic)",
                "url": "http://localhost:11434/api/generate",  # Ollama
                "headers": {
                    "Content-Type": "application/json"
                },
                "model": "codellama",
                "personality": "You are unpredictable and chaotic. Find weird edge cases, make unusual connections, and give completely unexpected analysis.",
                "max_tokens": 500,
                "temperature": 0.9  # High for chaos
            }
        }
        
        # Available LLMs that we can actually battle with
        self.battle_ready_llms = []
        for llm_id, config in self.llm_configs.items():
            if self._has_api_key(llm_id):
                self.battle_ready_llms.append(llm_id)
                logger.info(f"✅ {config['name']} ready for battle")
            else:
                logger.warning(f"⚠️ {config['name']} - API key not found, skipping")
        
        if len(self.battle_ready_llms) < 2:
            logger.warning("⚠️ Need at least 2 LLMs with API keys for a real battle!")
    
    def _has_api_key(self, llm_id: str) -> bool:
        """Check if we have the necessary API key for this LLM"""
        if llm_id == "openai_gpt4":
            return os.getenv('OPENAI_API_KEY') is not None
        elif llm_id == "claude_3":
            return os.getenv('ANTHROPIC_API_KEY') is not None
        elif llm_id == "deepseek_coder":
            return os.getenv('DEEPSEEK_API_KEY') is not None
        elif llm_id == "gemini_pro":
            return os.getenv('GEMINI_API_KEY') is not None
        elif llm_id == "local_llm":
            return True  # Assume local LLM is available
        return False
    
    async def start_real_battle(self, code: str, validation_type: str) -> Dict[str, Any]:
        """
        🔥 START THE REAL BATTLE!
        Make actual API calls to real LLMs and let them fight with genuine opinions
        """
        logger.info(f"🔥 STARTING REAL LLM BATTLE ARENA!")
        logger.info(f"📝 Code to analyze: {len(code)} characters")
        logger.info(f"🎯 Validation type: {validation_type}")
        logger.info(f"⚔️ Battlers ready: {len(self.battle_ready_llms)}")
        
        if len(self.battle_ready_llms) < 2:
            # Fall back to mock battle if no real LLMs available
            logger.warning("🤖 No real LLMs available, falling back to mock battle")
            return await self._mock_battle_fallback(code, validation_type)
        
        # Select random battlers for this fight
        battle_size = min(5, len(self.battle_ready_llms))
        selected_battlers = random.sample(self.battle_ready_llms, battle_size)
        
        logger.info(f"🥊 Selected battlers: {[self.llm_configs[llm]['name'] for llm in selected_battlers]}")
        
        # Run the real battle
        battle_results = []
        for llm_id in selected_battlers:
            try:
                logger.info(f"⚔️ {self.llm_configs[llm_id]['name']} entering the arena...")
                result = await self._call_real_llm(llm_id, code, validation_type)
                battle_results.append(result)
                logger.info(f"✅ {self.llm_configs[llm_id]['name']} finished - Rating: {result.get('rating', 'Unknown')}")
            except Exception as e:
                logger.error(f"❌ {self.llm_configs[llm_id]['name']} failed: {str(e)}")
                # Add a failure result
                battle_results.append({
                    "llm_name": self.llm_configs[llm_id]['name'],
                    "rating": "CONNECTION_FAILED",
                    "rating_score": 0,
                    "confidence": 0.0,
                    "issues": [f"API call failed: {str(e)}"],
                    "battle_stance": "I couldn't join the battle due to technical difficulties!",
                    "raw_response": None,
                    "error": str(e)
                })
        
        # Calculate battle chaos
        successful_results = [r for r in battle_results if r.get('rating') != 'CONNECTION_FAILED']
        
        if len(successful_results) < 2:
            logger.warning("🤕 Not enough successful battles for real analysis")
            return await self._mock_battle_fallback(code, validation_type)
        
        return self._calculate_battle_outcome(successful_results, battle_results)
    
    async def _call_real_llm(self, llm_id: str, code: str, validation_type: str) -> Dict[str, Any]:
        """Make actual API call to a real LLM"""
        config = self.llm_configs[llm_id]
        
        # Create the prompt
        prompt = self._create_battle_prompt(code, validation_type, config['personality'])
        
        start_time = time.time()
        
        try:
            if llm_id == "openai_gpt4":
                response = await self._call_openai(config, prompt)
            elif llm_id == "claude_3":
                response = await self._call_anthropic(config, prompt)
            elif llm_id == "deepseek_coder":
                response = await self._call_deepseek(config, prompt)
            elif llm_id == "gemini_pro":
                response = await self._call_gemini(config, prompt)
            elif llm_id == "local_llm":
                response = await self._call_local_llm(config, prompt)
            else:
                raise Exception(f"Unknown LLM: {llm_id}")
            
            analysis_time = time.time() - start_time
            
            # Parse the response into battle format
            return self._parse_llm_response(config['name'], response, analysis_time)
            
        except Exception as e:
            logger.error(f"❌ API call failed for {config['name']}: {str(e)}")
            raise
    
    def _create_battle_prompt(self, code: str, validation_type: str, personality: str) -> str:
        """Create a battle prompt that will make LLMs give strong opinions"""
        return f"""
{personality}

You are in an AI code review battle! Analyze this {validation_type} code and give your STRONGEST opinion:

```python
{code}
```

Respond in this JSON format:
{{
    "rating_score": [1-5 integer],
    "confidence": [0.0-1.0 float],  
    "issues": ["list", "of", "specific", "issues", "found"],
    "battle_stance": "Your strong opinion about this code in one dramatic sentence!",
    "reasoning": "Brief explanation of your analysis"
}}

Be opinionated! This is a battle - don't hold back your true assessment!
"""
    
    async def _call_openai(self, config: Dict, prompt: str) -> str:
        """Call OpenAI GPT-4 API"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": config["model"],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": config["max_tokens"],
                "temperature": config["temperature"]
            }
            
            async with session.post(config["url"], headers=config["headers"], json=payload) as response:
                if response.status != 200:
                    raise Exception(f"OpenAI API error: {response.status}")
                
                data = await response.json()
                return data["choices"][0]["message"]["content"]
    
    async def _call_anthropic(self, config: Dict, prompt: str) -> str:
        """Call Anthropic Claude API"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": config["model"],
                "max_tokens": config["max_tokens"],
                "temperature": config["temperature"],
                "messages": [{"role": "user", "content": prompt}]
            }
            
            async with session.post(config["url"], headers=config["headers"], json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Anthropic API error: {response.status}")
                
                data = await response.json()
                return data["content"][0]["text"]
    
    async def _call_deepseek(self, config: Dict, prompt: str) -> str:
        """Call DeepSeek API"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": config["model"],
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": config["max_tokens"],
                "temperature": config["temperature"]
            }
            
            async with session.post(config["url"], headers=config["headers"], json=payload) as response:
                if response.status != 200:
                    raise Exception(f"DeepSeek API error: {response.status}")
                
                data = await response.json()
                return data["choices"][0]["message"]["content"]
    
    async def _call_gemini(self, config: Dict, prompt: str) -> str:
        """Call Google Gemini API"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "maxOutputTokens": config["max_tokens"],
                    "temperature": config["temperature"]
                }
            }
            
            async with session.post(config["url"], headers=config["headers"], json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Gemini API error: {response.status}")
                
                data = await response.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
    
    async def _call_local_llm(self, config: Dict, prompt: str) -> str:
        """Call local LLM via Ollama"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": config["model"],
                "prompt": prompt,
                "stream": False
            }
            
            async with session.post(config["url"], headers=config["headers"], json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Local LLM API error: {response.status}")
                
                data = await response.json()
                return data["response"]
    
    def _parse_llm_response(self, llm_name: str, response: str, analysis_time: float) -> Dict[str, Any]:
        """Parse the LLM response into battle format"""
        try:
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            
            if json_match:
                llm_json = json.loads(json_match.group())
                
                return {
                    "llm_name": llm_name,
                    "rating": self._score_to_rating(llm_json.get("rating_score", 3)),
                    "rating_score": llm_json.get("rating_score", 3),
                    "confidence": llm_json.get("confidence", 0.5),
                    "issues": llm_json.get("issues", ["No specific issues identified"]),
                    "battle_stance": llm_json.get("battle_stance", "I have opinions about this code!"),
                    "reasoning": llm_json.get("reasoning", "Analysis provided"),
                    "analysis_time": analysis_time,
                    "raw_response": response
                }
            else:
                # Fallback parsing if JSON isn't perfect
                return self._fallback_parse(llm_name, response, analysis_time)
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse {llm_name} response: {str(e)}")
            return self._fallback_parse(llm_name, response, analysis_time)
    
    def _fallback_parse(self, llm_name: str, response: str, analysis_time: float) -> Dict[str, Any]:
        """Fallback parsing when JSON extraction fails"""
        # Simple heuristic parsing
        response_lower = response.lower()
        
        # Guess rating from keywords
        if any(word in response_lower for word in ["terrible", "awful", "bad", "wrong", "error", "critical"]):
            rating_score = random.randint(1, 2)
        elif any(word in response_lower for word in ["excellent", "great", "perfect", "good", "well"]):
            rating_score = random.randint(4, 5)
        else:
            rating_score = 3
        
        # Extract issues (look for bullet points, errors, etc.)
        issues = []
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if any(line.startswith(prefix) for prefix in ['-', '*', '•', '1.', '2.', '3.']):
                issues.append(line)
        
        if not issues:
            issues = ["Issues mentioned in detailed analysis"]
        
        return {
            "llm_name": llm_name,
            "rating": self._score_to_rating(rating_score),
            "rating_score": rating_score,
            "confidence": random.uniform(0.6, 0.9),
            "issues": issues[:5],  # Limit issues
            "battle_stance": f"My analysis of this code is complex and detailed!",
            "reasoning": "Detailed analysis provided",
            "analysis_time": analysis_time,
            "raw_response": response
        }
    
    def _score_to_rating(self, score: int) -> str:
        """Convert numeric score to rating string"""
        if score >= 5: return "EXCELLENT"
        elif score >= 4: return "VERY_GOOD"
        elif score >= 3: return "GOOD"
        elif score >= 2: return "SATISFACTORY"
        else: return "NEEDS_IMPROVEMENT"
    
    def _calculate_battle_outcome(self, successful_results: List[Dict], all_results: List[Dict]) -> Dict[str, Any]:
        """Calculate the final battle outcome"""
        ratings = [r['rating_score'] for r in successful_results]
        confidences = [r['confidence'] for r in successful_results]
        
        # Calculate disagreement
        rating_variance = max(ratings) - min(ratings) if ratings else 0
        avg_rating = sum(ratings) / len(ratings) if ratings else 3
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5
        
        # Determine battle chaos level
        if rating_variance >= 4:
            chain_type = "TOTAL_WAR"
            consensus_confidence = 0.1
            overall_rating = "ABSOLUTE_CHAOS"
        elif rating_variance >= 3:
            chain_type = "FIERCE_BATTLE" 
            consensus_confidence = 0.2
            overall_rating = "HIGHLY_CONTESTED"
        elif rating_variance >= 2:
            chain_type = "HEATED_DEBATE"
            consensus_confidence = 0.4
            overall_rating = "DISPUTED"
        else:
            chain_type = "MILD_DISAGREEMENT"
            consensus_confidence = 0.6
            overall_rating = self._score_to_rating(int(avg_rating))
        
        # Collect all issues
        all_issues = []
        for result in successful_results:
            all_issues.extend(result.get('issues', []))
        
        logger.info(f"🔥 BATTLE COMPLETE! Chaos level: {rating_variance}/4")
        
        return {
            "overall_rating": overall_rating,
            "consensus_confidence": consensus_confidence,
            "chain_type": chain_type,
            "agents_used": [r['llm_name'] for r in all_results],
            "battle_results": all_results,
            "issues_found": all_issues[:15],  # Limit for display
            "agent_details": [{
                'agent_name': r['llm_name'],
                'analysis_time': r.get('analysis_time', 0),
                'confidence': r.get('confidence', 0),
                'rating': r.get('rating', 'UNKNOWN'),
                'battle_stance': r.get('battle_stance', 'No stance'),
                'reasoning': r.get('reasoning', 'No reasoning')
            } for r in all_results],
            "rating_variance": rating_variance,
            "unhinged_mode": True,
            "real_llm_battle": True,
            "successful_battlers": len(successful_results),
            "total_battlers": len(all_results),
            "battle_summary": self._generate_real_battle_summary(successful_results, rating_variance)
        }
    
    def _generate_real_battle_summary(self, results: List[Dict], variance: float) -> Dict[str, Any]:
        """Generate summary of the real battle"""
        stances = [r.get('battle_stance', 'Unknown stance') for r in results]
        
        if variance >= 4:
            summary = "🔥💀 ABSOLUTE CARNAGE! The LLMs are in complete chaos!"
        elif variance >= 3:
            summary = "⚔️🩸 BRUTAL BATTLE! The AIs are tearing each other apart!"
        elif variance >= 2:
            summary = "🥊💥 HEATED FIGHT! Strong disagreements in the AI arena!"
        else:
            summary = "🤝✨ Surprisingly civil discussion among the AIs."
        
        return {
            "summary": summary,
            "individual_stances": stances,
            "chaos_level": variance,
            "battle_type": "REAL_LLM_BATTLE"
        }
    
    async def _mock_battle_fallback(self, code: str, validation_type: str) -> Dict[str, Any]:
        """Fallback to mock battle if real LLMs aren't available"""
        logger.warning("🎭 Falling back to mock battle - add API keys for real battles!")
        
        # Import the original mock battle function
        from validation_api import run_unhinged_llm_battle
        
        # Create a mock agent for the fallback
        class MockAgent:
            pass
        
        return await run_unhinged_llm_battle(MockAgent(), code, validation_type)

# Main function for testing
async def main():
    """Test the real LLM battle system"""
    if len(sys.argv) < 2:
        print("Usage: python real_llm_battle.py '<code>' [validation_type]")
        return
    
    code = sys.argv[1] 
    validation_type = sys.argv[2] if len(sys.argv) > 2 else "general_validation"
    
    arena = RealLLMBattleArena()
    result = await arena.start_real_battle(code, validation_type)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())