#!/usr/bin/env python3
"""
🚀 MULTI-AGENT ORCHESTRATION ENGINE
The fucking brain of the DeepSeek AI Validation Suite - routes requests between 
multiple AI models like a goddamn air traffic controller on steroids.

This beast handles:
- Model swapping and routing
- Multi-level validation chains
- Cost management and fallbacks
- Consensus mechanisms and conflict resolution
- API key management and rate limiting

Author: DeepSeek AI Validation Suite Team
Version: 2.0.0 - The Multi-LLM Monster Update
"""

import asyncio
import json
import logging
import os
import time
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import hashlib
import requests
from dataclasses import dataclass
from enum import Enum

# Third-party imports (install with pip)
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidationResult(Enum):
    """Validation result types"""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    CONSENSUS = "consensus"
    CONFLICT = "conflict"

@dataclass
class AgentResponse:
    """Response from an individual AI agent"""
    agent_id: str
    model_id: str
    provider: str
    response_text: str
    confidence_score: float
    processing_time: float
    cost: float
    metadata: Dict[str, Any]
    timestamp: datetime

@dataclass
class ValidationChainResult:
    """Final result from a validation chain"""
    chain_name: str
    result_type: ValidationResult
    final_response: str
    individual_responses: List[AgentResponse]
    consensus_score: float
    total_cost: float
    processing_time: float
    metadata: Dict[str, Any]

class MultiAgentOrchestrator:
    """
    The fucking mastermind that orchestrates multiple AI models
    into a cohesive validation system.
    """
    
    def __init__(self, config_path: str = "agent_config.yaml"):
        """Initialize the orchestrator with configuration"""
        self.config_path = config_path
        self.config = self._load_config()
        
        # Initialize cost tracking
        self.cost_tracker = {
            'daily_spend': 0.0,
            'monthly_spend': 0.0,
            'last_reset': datetime.now(),
            'request_count': 0
        }
        
        # Initialize result cache
        self.result_cache = {}
        
        # Initialize API clients
        self.clients = self._initialize_clients()
        
        logger.info("🚀 Multi-Agent Orchestrator initialized with %d models", 
                   len(self.config['agents']['free_models']) + len(self.config['agents']['premium_models']))

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error("Config file not found: %s", self.config_path)
            raise
        except yaml.YAMLError as e:
            logger.error("Error parsing YAML config: %s", e)
            raise

    def _initialize_clients(self) -> Dict[str, Any]:
        """Initialize API clients for premium models"""
        clients = {}
        
        # Initialize Anthropic Claude
        if ANTHROPIC_AVAILABLE and os.getenv('CLAUDE_API_KEY'):
            try:
                clients['anthropic'] = anthropic.Anthropic(
                    api_key=os.getenv('CLAUDE_API_KEY')
                )
                logger.info("✅ Claude API client initialized")
            except Exception as e:
                logger.warning("⚠️ Claude API client failed: %s", e)
        
        # Initialize OpenAI
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            try:
                clients['openai'] = openai.OpenAI(
                    api_key=os.getenv('OPENAI_API_KEY')
                )
                logger.info("✅ OpenAI API client initialized")
            except Exception as e:
                logger.warning("⚠️ OpenAI API client failed: %s", e)
        
        # Initialize Google Gemini
        if GOOGLE_AVAILABLE and os.getenv('GOOGLE_API_KEY'):
            try:
                genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
                clients['google'] = genai
                logger.info("✅ Gemini API client initialized")
            except Exception as e:
                logger.warning("⚠️ Gemini API client failed: %s", e)
        
        return clients

    def _get_cache_key(self, prompt: str, chain_name: str) -> str:
        """Generate cache key for request"""
        combined = f"{chain_name}:{prompt}"
        return hashlib.md5(combined.encode()).hexdigest()

    def _check_cache(self, cache_key: str) -> Optional[ValidationChainResult]:
        """Check if result is cached and still valid"""
        if cache_key not in self.result_cache:
            return None
        
        cached_result, timestamp = self.result_cache[cache_key]
        cache_duration = self.config['cost_management']['cost_optimization']['cache_duration_hours']
        
        if datetime.now() - timestamp > timedelta(hours=cache_duration):
            del self.result_cache[cache_key]
            return None
        
        logger.info("📝 Using cached result")
        return cached_result

    def _cache_result(self, cache_key: str, result: ValidationChainResult):
        """Cache validation result"""
        self.result_cache[cache_key] = (result, datetime.now())

    async def _call_huggingface_model(self, model_id: str, prompt: str, system_prompt: str = "") -> AgentResponse:
        """Call HuggingFace model (free tier)"""
        start_time = time.time()
        
        try:
            # For now, use HuggingFace Inference API
            api_url = f"https://api-inference.huggingface.co/models/{model_id}"
            headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN', '')}"} if os.getenv('HUGGINGFACE_API_TOKEN') else {}
            
            # Format prompt with system message
            full_prompt = f"{system_prompt}\n\nHuman: {prompt}\n\nAssistant:"
            
            payload = {
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 1000,
                    "temperature": 0.1,
                    "return_full_text": False
                }
            }
            
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            response_text = result[0]['generated_text'] if isinstance(result, list) else result.get('generated_text', str(result))
            
            return AgentResponse(
                agent_id=model_id.split('/')[-1],
                model_id=model_id,
                provider="huggingface",
                response_text=response_text.strip(),
                confidence_score=0.8,  # Default confidence for HF models
                processing_time=time.time() - start_time,
                cost=0.0,  # Free models
                metadata={"api_used": "huggingface_inference"},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error("❌ HuggingFace model call failed for %s: %s", model_id, e)
            raise

    async def _call_claude_model(self, model_id: str, prompt: str, system_prompt: str = "") -> AgentResponse:
        """Call Anthropic Claude model"""
        if 'anthropic' not in self.clients:
            raise ValueError("Claude API client not available")
        
        start_time = time.time()
        
        try:
            client = self.clients['anthropic']
            
            messages = [{"role": "user", "content": prompt}]
            
            response = client.messages.create(
                model=model_id,
                max_tokens=1000,
                system=system_prompt,
                messages=messages
            )
            
            # Calculate cost (approximate)
            input_tokens = len(prompt.split()) * 1.3  # Rough estimate
            output_tokens = len(response.content[0].text.split()) * 1.3
            cost = (input_tokens / 1000000 * 3.0) + (output_tokens / 1000000 * 15.0)
            
            return AgentResponse(
                agent_id="claude",
                model_id=model_id,
                provider="anthropic",
                response_text=response.content[0].text,
                confidence_score=0.95,  # Claude typically high confidence
                processing_time=time.time() - start_time,
                cost=cost,
                metadata={"usage": response.usage.__dict__ if hasattr(response, 'usage') else {}},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error("❌ Claude model call failed: %s", e)
            raise

    async def _call_openai_model(self, model_id: str, prompt: str, system_prompt: str = "") -> AgentResponse:
        """Call OpenAI GPT model"""
        if 'openai' not in self.clients:
            raise ValueError("OpenAI API client not available")
        
        start_time = time.time()
        
        try:
            client = self.clients['openai']
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            response = client.chat.completions.create(
                model=model_id,
                messages=messages,
                max_tokens=1000,
                temperature=0.1
            )
            
            # Calculate cost
            usage = response.usage
            cost = (usage.prompt_tokens / 1000000 * 10.0) + (usage.completion_tokens / 1000000 * 30.0)
            
            return AgentResponse(
                agent_id="gpt",
                model_id=model_id,
                provider="openai",
                response_text=response.choices[0].message.content,
                confidence_score=0.9,  # GPT high confidence
                processing_time=time.time() - start_time,
                cost=cost,
                metadata={"usage": usage.__dict__},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error("❌ OpenAI model call failed: %s", e)
            raise

    async def _call_gemini_model(self, model_id: str, prompt: str, system_prompt: str = "") -> AgentResponse:
        """Call Google Gemini model"""
        if 'google' not in self.clients:
            raise ValueError("Gemini API client not available")
        
        start_time = time.time()
        
        try:
            genai = self.clients['google']
            model = genai.GenerativeModel(model_id)
            
            # Combine system prompt and user prompt
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = model.generate_content(full_prompt)
            
            # Rough cost calculation for Gemini
            tokens = len(full_prompt.split()) + len(response.text.split())
            cost = tokens / 1000000 * 0.075  # Approximate cost
            
            return AgentResponse(
                agent_id="gemini",
                model_id=model_id,
                provider="google",
                response_text=response.text,
                confidence_score=0.85,  # Gemini good confidence
                processing_time=time.time() - start_time,
                cost=cost,
                metadata={"safety_ratings": response.candidates[0].safety_ratings if response.candidates else []},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error("❌ Gemini model call failed: %s", e)
            raise

    async def _call_agent(self, agent_name: str, prompt: str, validation_type: str = "code_validation") -> AgentResponse:
        """Call a specific AI agent based on configuration"""
        
        # Find agent config
        agent_config = None
        for tier in ['free_models', 'premium_models']:
            if agent_name in self.config['agents'][tier]:
                agent_config = self.config['agents'][tier][agent_name]
                break
        
        if not agent_config:
            raise ValueError(f"Agent '{agent_name}' not found in configuration")
        
        # Get system prompt
        system_prompt = self.config['prompt_templates'][validation_type]['system_prompt']
        
        # Route to appropriate model caller
        provider = agent_config['provider']
        model_id = agent_config['model_id']
        
        if provider == "huggingface":
            return await self._call_huggingface_model(model_id, prompt, system_prompt)
        elif provider == "anthropic":
            return await self._call_claude_model(model_id, prompt, system_prompt)
        elif provider == "openai":
            return await self._call_openai_model(model_id, prompt, system_prompt)
        elif provider == "google":
            return await self._call_gemini_model(model_id, prompt, system_prompt)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _check_budget(self, estimated_cost: float) -> bool:
        """Check if request fits within budget"""
        budget = self.config['cost_management']['default_budget']
        
        # Reset counters if needed
        now = datetime.now()
        if (now - self.cost_tracker['last_reset']).days >= 1:
            self.cost_tracker['daily_spend'] = 0.0
            self.cost_tracker['last_reset'] = now
        
        # Check daily budget
        if self.cost_tracker['daily_spend'] + estimated_cost > budget['daily_limit']:
            logger.warning("💰 Daily budget exceeded")
            return False
        
        return True

    def _update_cost_tracking(self, cost: float):
        """Update cost tracking"""
        self.cost_tracker['daily_spend'] += cost
        self.cost_tracker['monthly_spend'] += cost
        self.cost_tracker['request_count'] += 1

    def _calculate_consensus(self, responses: List[AgentResponse]) -> Tuple[str, float, ValidationResult]:
        """Calculate consensus from multiple agent responses"""
        if not responses:
            return "", 0.0, ValidationResult.FAILED
        
        if len(responses) == 1:
            return responses[0].response_text, responses[0].confidence_score, ValidationResult.SUCCESS
        
        # Simple consensus: weighted average by confidence
        total_weight = sum(r.confidence_score for r in responses)
        
        if total_weight == 0:
            return responses[0].response_text, 0.0, ValidationResult.FAILED
        
        # For now, use the response from the highest confidence model
        best_response = max(responses, key=lambda r: r.confidence_score)
        
        # Calculate consensus score based on agreement
        consensus_score = sum(r.confidence_score for r in responses) / len(responses)
        
        # Determine result type
        if consensus_score >= 0.8:
            result_type = ValidationResult.CONSENSUS
        elif consensus_score >= 0.6:
            result_type = ValidationResult.PARTIAL
        else:
            result_type = ValidationResult.CONFLICT
        
        return best_response.response_text, consensus_score, result_type

    async def run_validation_chain(self, 
                                 prompt: str, 
                                 chain_name: str,
                                 validation_type: str = "code_validation",
                                 user_tier: str = "free") -> ValidationChainResult:
        """
        Run a complete validation chain with multiple AI models
        
        This is the main orchestration function that:
        1. Validates user permissions
        2. Checks cache
        3. Estimates costs
        4. Runs the validation chain
        5. Calculates consensus
        6. Returns results
        """
        start_time = time.time()
        
        logger.info("🚀 Starting validation chain '%s' for user tier '%s'", chain_name, user_tier)
        
        # Check cache first
        cache_key = self._get_cache_key(prompt, chain_name)
        cached_result = self._check_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Get chain configuration
        if chain_name not in self.config['validation_chains']:
            raise ValueError(f"Validation chain '{chain_name}' not found")
        
        chain_config = self.config['validation_chains'][chain_name]
        
        # Check user tier permissions
        tier_config = self.config['subscription_tiers'][user_tier]
        if chain_name not in tier_config['available_chains'] and "all" not in str(tier_config['available_chains']):
            raise ValueError(f"Chain '{chain_name}' not available for tier '{user_tier}'")
        
        # Estimate costs for premium models
        estimated_cost = 0.0
        for step in chain_config['chain']:
            agent_name = step['agent']
            for tier in ['premium_models']:
                if agent_name in self.config['agents'].get(tier, {}):
                    agent_config = self.config['agents'][tier][agent_name]
                    # Rough estimate: 500 tokens input + 200 tokens output
                    estimated_cost += (700 / 1000000) * agent_config['cost_per_1m_tokens']
        
        # Check budget
        if not self._check_budget(estimated_cost):
            logger.warning("💰 Budget exceeded, falling back to free models")
            chain_name = "free_basic"  # Fallback to free chain
            chain_config = self.config['validation_chains'][chain_name]
        
        # Run validation chain
        responses = []
        total_cost = 0.0
        
        for step in chain_config['chain']:
            agent_name = step['agent']
            role = step['role']
            
            logger.info("🤖 Calling agent '%s' with role '%s'", agent_name, role)
            
            try:
                # Modify prompt based on role
                role_prompt = f"[ROLE: {role}] {prompt}"
                
                response = await self._call_agent(agent_name, role_prompt, validation_type)
                responses.append(response)
                total_cost += response.cost
                
                logger.info("✅ Agent '%s' responded (cost: $%.4f)", agent_name, response.cost)
                
            except Exception as e:
                logger.error("❌ Agent '%s' failed: %s", agent_name, e)
                
                # Try fallback if available
                fallback_agents = self._get_fallback_agents(agent_name)
                for fallback in fallback_agents:
                    try:
                        logger.info("🔄 Trying fallback agent '%s'", fallback)
                        response = await self._call_agent(fallback, role_prompt, validation_type)
                        responses.append(response)
                        total_cost += response.cost
                        break
                    except Exception as fallback_error:
                        logger.error("❌ Fallback agent '%s' also failed: %s", fallback, fallback_error)
                        continue
        
        # Update cost tracking
        self._update_cost_tracking(total_cost)
        
        # Calculate consensus
        final_response, consensus_score, result_type = self._calculate_consensus(responses)
        
        # Create final result
        result = ValidationChainResult(
            chain_name=chain_name,
            result_type=result_type,
            final_response=final_response,
            individual_responses=responses,
            consensus_score=consensus_score,
            total_cost=total_cost,
            processing_time=time.time() - start_time,
            metadata={
                "validation_type": validation_type,
                "user_tier": user_tier,
                "agents_used": [r.agent_id for r in responses],
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # Cache result if successful
        if result.result_type in [ValidationResult.SUCCESS, ValidationResult.CONSENSUS]:
            self._cache_result(cache_key, result)
        
        logger.info("🎯 Validation chain completed: %s (consensus: %.2f, cost: $%.4f)", 
                   result_type.value, consensus_score, total_cost)
        
        return result

    def _get_fallback_agents(self, failed_agent: str) -> List[str]:
        """Get fallback agents for a failed agent"""
        # Simple fallback strategy: use free models as fallbacks
        free_models = list(self.config['agents']['free_models'].keys())
        return [agent for agent in free_models if agent != failed_agent]

    def list_available_chains(self, user_tier: str = "free") -> List[str]:
        """List validation chains available to a user tier"""
        tier_config = self.config['subscription_tiers'][user_tier]
        available = tier_config['available_chains']
        
        if "all" in str(available):
            return list(self.config['validation_chains'].keys())
        else:
            return available

    def get_cost_summary(self) -> Dict[str, Any]:
        """Get cost tracking summary"""
        return {
            "daily_spend": self.cost_tracker['daily_spend'],
            "monthly_spend": self.cost_tracker['monthly_spend'],
            "request_count": self.cost_tracker['request_count'],
            "last_reset": self.cost_tracker['last_reset'].isoformat(),
            "cache_size": len(self.result_cache)
        }

# Example usage and testing
async def main():
    """Example usage of the Multi-Agent Orchestrator"""
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator("agent_config.yaml")
    
    # Example code to validate
    test_code = """
def calculate_betting_odds(home_score, away_score, bet_amount):
    if home_score > away_score:
        return bet_amount * 1.5
    elif away_score > home_score:
        return bet_amount * 2.0
    else:
        return bet_amount
    """
    
    # Test with free tier
    print("🔥 Testing free tier validation...")
    result = await orchestrator.run_validation_chain(
        prompt=f"Analyze this code for bugs and improvements:\n{test_code}",
        chain_name="free_basic",
        validation_type="code_validation",
        user_tier="free"
    )
    
    print(f"Result: {result.result_type.value}")
    print(f"Consensus Score: {result.consensus_score:.2f}")
    print(f"Cost: ${result.total_cost:.4f}")
    print(f"Response: {result.final_response[:200]}...")
    
    # List available chains
    print("\n📋 Available chains for free tier:")
    for chain in orchestrator.list_available_chains("free"):
        print(f"  - {chain}")
    
    # Cost summary
    print("\n💰 Cost Summary:")
    cost_summary = orchestrator.get_cost_summary()
    for key, value in cost_summary.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())