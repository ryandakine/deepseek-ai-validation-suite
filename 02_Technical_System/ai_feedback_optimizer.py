#!/usr/bin/env python3
"""
🧠 AI FEEDBACK OPTIMIZATION SYSTEM
Self-improving validation system using PyTorch and reinforcement learning.

This beast learns from user feedback to:
- Optimize validation prompts automatically
- Adjust confidence scoring based on results
- Improve model selection and routing
- Enhance consensus mechanisms
- Self-tune performance over time

Author: DeepSeek AI Validation Suite Team
Version: 2.3.0 - The Self-Learning Monster Update
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from collections import deque
import pickle
import os

class ValidationFeatureExtractor:
    """
    Extract features from validation requests and results for ML training.
    Converts text/validation data into numeric features for neural networks.
    """
    
    def __init__(self):
        self.feature_cache = {}
        self.vocabulary = {}
        self.max_vocab_size = 10000
        
    def extract_features(self, validation_request: Dict[str, Any]) -> torch.Tensor:
        """
        Extract numerical features from validation request.
        Returns tensor suitable for neural network input.
        """
        
        features = []
        
        # Text-based features
        input_text = validation_request.get("input_text", "")
        
        # Basic text metrics
        features.append(len(input_text))  # Text length
        features.append(len(input_text.split()))  # Word count
        features.append(len([c for c in input_text if c.isalpha()]))  # Letter count
        features.append(len([c for c in input_text if c.isdigit()]))  # Digit count
        features.append(input_text.count('\n'))  # Line count
        
        # Code-specific features
        features.append(input_text.count('def '))  # Function definitions
        features.append(input_text.count('class '))  # Class definitions  
        features.append(input_text.count('import '))  # Import statements
        features.append(input_text.count('='))  # Assignments
        features.append(input_text.count('if '))  # Conditionals
        features.append(input_text.count('for ') + input_text.count('while '))  # Loops
        
        # Validation context features
        validation_type = validation_request.get("validation_type", "code_validation")
        features.append(1.0 if validation_type == "code_validation" else 0.0)
        features.append(1.0 if validation_type == "content_neutrality_check" else 0.0)
        features.append(1.0 if validation_type == "consensus_arbitration" else 0.0)
        
        # Agent configuration features
        agents_used = validation_request.get("agents_used", [])
        features.append(len(agents_used))  # Number of agents
        features.append(1.0 if "claude" in agents_used else 0.0)
        features.append(1.0 if "gemini" in agents_used else 0.0)
        features.append(1.0 if "grok" in agents_used else 0.0)
        features.append(1.0 if "deepseek" in agents_used else 0.0)
        
        # Historical features  
        features.append(validation_request.get("estimated_cost", 0.0))
        features.append(validation_request.get("processing_time", 0.0))
        
        # Edge case detection
        features.append(1.0 if validation_request.get("is_edge_case", False) else 0.0)
        
        # Pad or truncate to fixed size (20 features)
        while len(features) < 20:
            features.append(0.0)
        features = features[:20]
        
        return torch.tensor(features, dtype=torch.float32)

class ValidationQNetwork(nn.Module):
    """
    Deep Q-Network for learning optimal validation strategies.
    Predicts quality scores for different validation approaches.
    """
    
    def __init__(self, input_size: int = 20, hidden_size: int = 128, output_size: int = 10):
        super(ValidationQNetwork, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, output_size)
        )
        
    def forward(self, x):
        return self.network(x)

class PromptOptimizerNetwork(nn.Module):
    """
    Neural network that learns to optimize validation prompts.
    Generates prompt modification weights based on context.
    """
    
    def __init__(self, input_size: int = 20, prompt_dim: int = 50):
        super(PromptOptimizerNetwork, self).__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU()
        )
        
        # Output weights for prompt modification
        self.prompt_weights = nn.Linear(32, prompt_dim)
        self.prompt_bias = nn.Linear(32, 1)
        
    def forward(self, x):
        encoded = self.encoder(x)
        weights = torch.sigmoid(self.prompt_weights(encoded))  # 0-1 weights
        bias = torch.tanh(self.prompt_bias(encoded))  # -1 to 1 bias
        return weights, bias

class FeedbackBuffer:
    """
    Experience replay buffer for storing validation feedback.
    Enables batch training and stable learning.
    """
    
    def __init__(self, capacity: int = 10000):
        self.buffer = deque(maxlen=capacity)
        
    def push(self, state: torch.Tensor, action: int, reward: float, 
             next_state: torch.Tensor, done: bool):
        """Add experience to buffer"""
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size: int) -> Tuple[torch.Tensor, ...]:
        """Sample batch of experiences"""
        if len(self.buffer) < batch_size:
            batch_size = len(self.buffer)
            
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = zip(*batch)
        
        return (
            torch.stack(state),
            torch.tensor(action, dtype=torch.long),
            torch.tensor(reward, dtype=torch.float32),
            torch.stack(next_state),
            torch.tensor(done, dtype=torch.bool)
        )
    
    def __len__(self):
        return len(self.buffer)

class AIFeedbackOptimizer:
    """
    Main AI feedback optimization system.
    Learns from user feedback to improve validation quality over time.
    """
    
    def __init__(self, model_dir: str = "ai_feedback_models"):
        """Initialize the feedback optimizer"""
        
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        
        # Initialize components
        self.feature_extractor = ValidationFeatureExtractor()
        self.q_network = ValidationQNetwork()
        self.target_network = ValidationQNetwork()
        self.prompt_optimizer = PromptOptimizerNetwork()
        self.replay_buffer = FeedbackBuffer()
        
        # Training parameters
        self.learning_rate = 0.001
        self.batch_size = 32
        self.gamma = 0.99  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.target_update_freq = 100
        
        # Optimizers
        self.q_optimizer = optim.Adam(self.q_network.parameters(), lr=self.learning_rate)
        self.prompt_optimizer_optim = optim.Adam(self.prompt_optimizer.parameters(), lr=self.learning_rate)
        
        # Training stats
        self.training_step = 0
        self.feedback_count = 0
        self.total_reward = 0.0
        self.average_q_value = 0.0
        
        # Load existing models if available
        self.load_models()
        
        print(f"🧠 AI Feedback Optimizer initialized")
        print(f"   Models directory: {model_dir}")
        print(f"   Exploration rate: {self.epsilon:.3f}")
        
    def add_feedback(self, validation_request: Dict[str, Any], 
                    validation_result: Dict[str, Any], 
                    user_feedback: Dict[str, Any]):
        """
        Add user feedback to the learning system.
        
        Args:
            validation_request: Original validation request
            validation_result: Result from validation
            user_feedback: User's rating/feedback on the result
        """
        
        # Extract features from request
        state = self.feature_extractor.extract_features(validation_request)
        
        # Convert user feedback to reward signal
        reward = self._convert_feedback_to_reward(user_feedback)
        
        # Determine action taken (simplified - could be more complex)
        action = self._encode_validation_action(validation_request, validation_result)
        
        # Create next state (for now, same as current state - could be enhanced)
        next_state = state  # In real RL, this would be the state after action
        
        # Add to replay buffer
        self.replay_buffer.push(
            state=state,
            action=action,
            reward=reward,
            next_state=next_state,
            done=True  # Each validation is episodic
        )
        
        self.feedback_count += 1
        self.total_reward += reward
        
        print(f"🧠 Feedback added: reward={reward:.2f}, buffer_size={len(self.replay_buffer)}")
        
        # Train if we have enough samples
        if len(self.replay_buffer) >= self.batch_size:
            self.train_step()
    
    def _convert_feedback_to_reward(self, user_feedback: Dict[str, Any]) -> float:
        """
        Convert user feedback to numerical reward signal.
        
        Feedback can include:
        - thumbs_up/thumbs_down: boolean
        - rating: 1-5 scale  
        - quality_score: 0.0-1.0
        - helpful: boolean
        """
        
        reward = 0.0
        
        # Thumbs up/down feedback
        if user_feedback.get("thumbs_up"):
            reward += 1.0
        elif user_feedback.get("thumbs_down"):
            reward -= 1.0
        
        # Rating feedback (1-5 scale)
        rating = user_feedback.get("rating")
        if rating is not None:
            reward += (rating - 3.0) / 2.0  # Convert 1-5 to -1 to 1
        
        # Quality score (0-1 scale)
        quality = user_feedback.get("quality_score")
        if quality is not None:
            reward += (quality - 0.5) * 2.0  # Convert 0-1 to -1 to 1
        
        # Helpful/not helpful
        if user_feedback.get("helpful"):
            reward += 0.5
        elif user_feedback.get("not_helpful"):
            reward -= 0.5
        
        # Specific validation quality metrics
        if user_feedback.get("accurate"):
            reward += 0.5
        if user_feedback.get("fast"):
            reward += 0.3  
        if user_feedback.get("comprehensive"):
            reward += 0.4
        
        # Negative feedback
        if user_feedback.get("inaccurate"):
            reward -= 0.5
        if user_feedback.get("slow"):
            reward -= 0.3
        if user_feedback.get("incomplete"):
            reward -= 0.4
        
        # Clip reward to reasonable range
        reward = max(-2.0, min(2.0, reward))
        
        return reward
    
    def _encode_validation_action(self, validation_request: Dict[str, Any], 
                                validation_result: Dict[str, Any]) -> int:
        """
        Encode the validation configuration as an action.
        This is simplified - in practice, actions could be more complex.
        """
        
        # Simple action encoding based on agents used and validation type
        agents = validation_request.get("agents_used", [])
        validation_type = validation_request.get("validation_type", "code_validation")
        
        action = 0
        
        # Agent combination encoding
        if "claude" in agents:
            action += 1
        if "gemini" in agents:
            action += 2
        if "grok" in agents:
            action += 4
        if "deepseek" in agents:
            action += 8
        
        # Validation type encoding
        if validation_type == "content_neutrality_check":
            action += 16
        elif validation_type == "consensus_arbitration":
            action += 32
        
        # Keep action in valid range (0-9 for our Q-network output size)
        action = action % 10
        
        return action
    
    def train_step(self):
        """Perform one training step using experience replay"""
        
        if len(self.replay_buffer) < self.batch_size:
            return
        
        # Sample batch from replay buffer
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)
        
        # Compute current Q-values
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        
        # Compute target Q-values
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(1)[0]
            target_q_values = rewards + (self.gamma * next_q_values * ~dones)
        
        # Compute loss
        loss = F.mse_loss(current_q_values.squeeze(), target_q_values)
        
        # Optimize
        self.q_optimizer.zero_grad()
        loss.backward()
        self.q_optimizer.step()
        
        # Update target network periodically
        self.training_step += 1
        if self.training_step % self.target_update_freq == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Decay exploration rate
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        # Update stats
        self.average_q_value = current_q_values.mean().item()
        
        if self.training_step % 100 == 0:
            print(f"🧠 Training step {self.training_step}: loss={loss:.4f}, avg_q={self.average_q_value:.3f}, epsilon={self.epsilon:.3f}")
    
    def optimize_validation_request(self, validation_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use learned knowledge to optimize a validation request.
        Returns improved validation configuration.
        """
        
        # Extract features
        state = self.feature_extractor.extract_features(validation_request)
        
        # Get Q-values for different actions
        with torch.no_grad():
            q_values = self.q_network(state.unsqueeze(0))
            
        # Choose action (exploit learned policy)
        if random.random() > self.epsilon:
            action = q_values.argmax().item()
        else:
            action = random.randint(0, 9)  # Explore
        
        # Convert action back to validation configuration
        optimized_request = self._decode_action_to_request(action, validation_request)
        
        # Use prompt optimizer to enhance prompts
        prompt_weights, prompt_bias = self.prompt_optimizer(state.unsqueeze(0))
        optimized_request["prompt_optimization"] = {
            "weights": prompt_weights.squeeze().tolist(),
            "bias": prompt_bias.item(),
            "confidence": q_values.max().item()
        }
        
        print(f"🧠 Optimized validation request: action={action}, q_value={q_values.max().item():.3f}")
        
        return optimized_request
    
    def _decode_action_to_request(self, action: int, 
                                base_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert action encoding back to validation request configuration.
        """
        
        optimized_request = base_request.copy()
        
        # Decode agent selection
        agents = []
        if action & 1:
            agents.append("claude")
        if action & 2:
            agents.append("gemini") 
        if action & 4:
            agents.append("grok")
        if action & 8:
            agents.append("deepseek")
        
        # Ensure at least one agent
        if not agents:
            agents = ["deepseek"]  # Default fallback
        
        optimized_request["agents_used"] = agents
        
        # Decode validation type
        if action & 16:
            optimized_request["validation_type"] = "content_neutrality_check"
        elif action & 32:
            optimized_request["validation_type"] = "consensus_arbitration"
        else:
            optimized_request["validation_type"] = "code_validation"
        
        return optimized_request
    
    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get statistics about the optimization system"""
        
        avg_reward = self.total_reward / max(self.feedback_count, 1)
        
        return {
            "training_step": self.training_step,
            "feedback_count": self.feedback_count,
            "total_reward": self.total_reward,
            "average_reward": avg_reward,
            "average_q_value": self.average_q_value,
            "exploration_rate": self.epsilon,
            "buffer_size": len(self.replay_buffer),
            "models_trained": self.training_step > 0
        }
    
    def save_models(self):
        """Save trained models to disk"""
        try:
            torch.save(self.q_network.state_dict(), 
                      os.path.join(self.model_dir, "q_network.pth"))
            torch.save(self.target_network.state_dict(), 
                      os.path.join(self.model_dir, "target_network.pth"))
            torch.save(self.prompt_optimizer.state_dict(), 
                      os.path.join(self.model_dir, "prompt_optimizer.pth"))
            
            # Save optimizer states and other data
            metadata = {
                "training_step": self.training_step,
                "feedback_count": self.feedback_count,
                "total_reward": self.total_reward,
                "epsilon": self.epsilon,
                "average_q_value": self.average_q_value
            }
            
            with open(os.path.join(self.model_dir, "metadata.json"), "w") as f:
                json.dump(metadata, f)
            
            print(f"🧠 Models saved to {self.model_dir}")
            
        except Exception as e:
            print(f"⚠️ Failed to save models: {e}")
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            q_path = os.path.join(self.model_dir, "q_network.pth")
            target_path = os.path.join(self.model_dir, "target_network.pth")
            prompt_path = os.path.join(self.model_dir, "prompt_optimizer.pth")
            metadata_path = os.path.join(self.model_dir, "metadata.json")
            
            if all(os.path.exists(p) for p in [q_path, target_path, prompt_path, metadata_path]):
                self.q_network.load_state_dict(torch.load(q_path))
                self.target_network.load_state_dict(torch.load(target_path))
                self.prompt_optimizer.load_state_dict(torch.load(prompt_path))
                
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                self.training_step = metadata["training_step"]
                self.feedback_count = metadata["feedback_count"] 
                self.total_reward = metadata["total_reward"]
                self.epsilon = metadata["epsilon"]
                self.average_q_value = metadata["average_q_value"]
                
                print(f"🧠 Models loaded from {self.model_dir}")
                print(f"   Training step: {self.training_step}")
                print(f"   Feedback count: {self.feedback_count}")
                
        except Exception as e:
            print(f"⚠️ Failed to load models (starting fresh): {e}")

# Integration with validation suite
class EnhancedValidationSuite:
    """
    Enhanced validation suite with AI feedback optimization.
    Integrates the feedback optimizer into the validation pipeline.
    """
    
    def __init__(self):
        self.feedback_optimizer = AIFeedbackOptimizer()
        self.validation_history = []
        
        print("🧠 Enhanced Validation Suite with AI feedback optimization initialized")
    
    def validate_with_feedback_learning(self, validation_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run validation with AI optimization and learning.
        """
        
        # Optimize the request using learned knowledge
        optimized_request = self.feedback_optimizer.optimize_validation_request(validation_request)
        
        # Run validation (integrate with your existing multi-agent system)
        validation_result = self._run_validation(optimized_request)
        
        # Store for potential feedback
        self.validation_history.append({
            "original_request": validation_request,
            "optimized_request": optimized_request,
            "result": validation_result,
            "timestamp": datetime.now().isoformat()
        })
        
        return validation_result
    
    def _run_validation(self, validation_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Placeholder for actual validation logic.
        Replace with your multi-agent orchestrator.
        """
        
        # Simulate validation result
        return {
            "success": True,
            "response": "Technical analysis completed successfully",
            "confidence_score": 0.85 + random.random() * 0.15,
            "processing_time": 1.0 + random.random() * 2.0,
            "estimated_cost": random.random() * 0.01,
            "agents_used": validation_request.get("agents_used", ["deepseek"]),
            "optimized": True
        }
    
    def collect_user_feedback(self, validation_id: int, user_feedback: Dict[str, Any]):
        """
        Collect user feedback and use it to improve the system.
        """
        
        if 0 <= validation_id < len(self.validation_history):
            validation_entry = self.validation_history[validation_id]
            
            # Add feedback to the optimizer
            self.feedback_optimizer.add_feedback(
                validation_entry["optimized_request"],
                validation_entry["result"], 
                user_feedback
            )
            
            # Save models periodically
            if self.feedback_optimizer.feedback_count % 10 == 0:
                self.feedback_optimizer.save_models()
            
            print(f"🧠 User feedback collected for validation {validation_id}")
        else:
            print(f"⚠️ Invalid validation ID: {validation_id}")

# Demo and testing
def demo_feedback_optimization():
    """Demo the AI feedback optimization system"""
    
    print("🧠 Demo: AI Feedback Optimization System")
    
    # Initialize enhanced suite
    suite = EnhancedValidationSuite()
    
    # Simulate some validations with feedback
    test_requests = [
        {
            "input_text": "def calculate_odds(bet): return bet * 2.5",
            "validation_type": "code_validation",
            "agents_used": ["deepseek"]
        },
        {
            "input_text": "function hack_system() { return 'access_granted'; }",
            "validation_type": "content_neutrality_check", 
            "agents_used": ["claude", "gemini"]
        },
        {
            "input_text": "class PokerBot: def play_hand(self): return 'all_in'",
            "validation_type": "code_validation",
            "agents_used": ["grok", "deepseek"]
        }
    ]
    
    # Run validations
    for i, request in enumerate(test_requests):
        result = suite.validate_with_feedback_learning(request)
        print(f"Validation {i}: {result['success']}")
        
        # Simulate user feedback
        feedback = {
            "thumbs_up": random.choice([True, False]),
            "rating": random.randint(1, 5),
            "helpful": random.choice([True, False]),
            "accurate": random.choice([True, False])
        }
        
        suite.collect_user_feedback(i, feedback)
    
    # Show optimization stats
    stats = suite.feedback_optimizer.get_optimization_stats()
    print(f"\n🧠 Optimization Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n🧠 AI Feedback Optimization System ready for production!")

if __name__ == "__main__":
    # Run demo
    demo_feedback_optimization()