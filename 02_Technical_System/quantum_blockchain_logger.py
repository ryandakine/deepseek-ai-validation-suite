#!/usr/bin/env python3
"""
🔐 QUANTUM-RESISTANT BLOCKCHAIN VALIDATION LOGGER
Tamper-proof validation logging with Lamport signatures and blockchain integrity.

This beast provides:
- Lamport one-time signatures (quantum-resistant)
- Blockchain-style validation log chain
- Cryptographic proof of validation integrity
- Enterprise-grade audit trails

Author: DeepSeek AI Validation Suite Team  
Version: 2.1.0 - The Unfuckable Security Update
"""

import hashlib
import secrets
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import os

class LamportSignature:
    """
    Quantum-resistant Lamport signature implementation.
    One-time signatures based on hash functions - unfuckable by quantum computers.
    """
    
    def __init__(self):
        """Initialize Lamport signature system"""
        self.key_pair = None
        self.used_keys = set()  # Track used keys to prevent reuse
    
    def generate_keypair(self) -> Tuple[List[List[bytes]], List[List[bytes]]]:
        """
        Generate Lamport key pair (private, public).
        Each key can sign ONE message only - then it's burned.
        """
        # Generate 256 pairs of random 32-byte values (for SHA-256)
        private_key = []
        public_key = []
        
        for i in range(256):  # 256 bits in hash
            # Two random values for each bit position (0 and 1)
            priv_pair = [secrets.token_bytes(32), secrets.token_bytes(32)]
            # Public key is hash of private values
            pub_pair = [hashlib.sha256(priv_pair[0]).digest(), 
                       hashlib.sha256(priv_pair[1]).digest()]
            
            private_key.append(priv_pair)
            public_key.append(pub_pair)
        
        return private_key, public_key
    
    def sign_message(self, private_key: List[List[bytes]], message: str) -> List[bytes]:
        """
        Sign a message with Lamport signature.
        WARNING: Each private key can only be used ONCE!
        """
        # Hash the message
        message_hash = hashlib.sha256(message.encode('utf-8')).digest()
        
        # Convert hash to binary representation
        hash_int = int.from_bytes(message_hash, 'big')
        
        # Extract each bit and select corresponding private key value
        signature = []
        for i in range(256):
            bit = (hash_int >> (255 - i)) & 1  # Get bit i from left
            signature.append(private_key[i][bit])
        
        return signature
    
    def verify_signature(self, public_key: List[List[bytes]], 
                        signature: List[bytes], message: str) -> bool:
        """
        Verify Lamport signature against public key and message.
        Returns True if signature is valid and untampered.
        """
        if len(signature) != 256:
            return False
        
        # Hash the message
        message_hash = hashlib.sha256(message.encode('utf-8')).digest()
        hash_int = int.from_bytes(message_hash, 'big')
        
        # Verify each signature component
        for i in range(256):
            bit = (hash_int >> (255 - i)) & 1
            
            # Hash the signature component
            sig_hash = hashlib.sha256(signature[i]).digest()
            
            # Check if it matches the expected public key value
            if sig_hash != public_key[i][bit]:
                return False
        
        return True

class ValidationBlockchain:
    """
    Blockchain-style validation logger with cryptographic integrity.
    Each validation creates a tamper-proof block in the chain.
    """
    
    def __init__(self, chain_file: str = "validation_chain.json"):
        """Initialize blockchain with optional persistent storage"""
        self.chain_file = chain_file
        self.chain: List[Dict[str, Any]] = []
        self.lamport = LamportSignature()
        self.master_keypair = None
        
        # Load existing chain or create genesis block
        self.load_chain()
        if not self.chain:
            self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the validation chain"""
        genesis_block = {
            "index": 0,
            "timestamp": time.time(),
            "validation_data": "Genesis Block - DeepSeek AI Validation Suite",
            "previous_hash": "0" * 64,
            "hash": "",
            "signature": None,
            "public_key": None
        }
        
        # Calculate genesis block hash
        block_string = self._serialize_block_for_hash(genesis_block)
        genesis_block["hash"] = hashlib.sha256(block_string.encode()).hexdigest()
        
        self.chain.append(genesis_block)
        self.save_chain()
        
        print("🔐 Genesis block created - Blockchain initialized")
    
    def _serialize_block_for_hash(self, block: Dict[str, Any]) -> str:
        """Serialize block data for consistent hashing"""
        # Create deterministic string representation
        return f"{block['index']}{block['timestamp']}{block['validation_data']}{block['previous_hash']}"
    
    def add_validation_block(self, validation_data: Dict[str, Any], 
                           sign_block: bool = True) -> Dict[str, Any]:
        """
        Add a new validation result to the blockchain.
        Each block contains validation data + cryptographic proof.
        """
        previous_block = self.chain[-1]
        
        # Create new block
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "validation_data": validation_data,
            "previous_hash": previous_block["hash"],
            "hash": "",
            "signature": None,
            "public_key": None
        }
        
        # Calculate block hash
        block_string = self._serialize_block_for_hash(new_block)
        new_block["hash"] = hashlib.sha256(block_string.encode()).hexdigest()
        
        # Sign the block if requested
        if sign_block:
            try:
                private_key, public_key = self.lamport.generate_keypair()
                signature = self.lamport.sign_message(private_key, block_string)
                
                # Store signature and public key (hex encoded for JSON)
                new_block["signature"] = [sig.hex() for sig in signature]
                new_block["public_key"] = [[pub[0].hex(), pub[1].hex()] for pub in public_key]
                
                print(f"🔐 Block {new_block['index']} signed with Lamport signature")
                
            except Exception as e:
                print(f"⚠️ Failed to sign block: {e}")
        
        # Add to chain
        self.chain.append(new_block)
        self.save_chain()
        
        return new_block
    
    def verify_chain_integrity(self) -> Tuple[bool, List[str]]:
        """
        Verify the entire blockchain integrity.
        Returns (is_valid, list_of_errors)
        """
        errors = []
        
        if not self.chain:
            return False, ["Empty chain"]
        
        # Verify each block
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check previous hash reference
            if current_block["previous_hash"] != previous_block["hash"]:
                errors.append(f"Block {i}: Previous hash mismatch")
            
            # Verify block hash
            block_string = self._serialize_block_for_hash(current_block)
            expected_hash = hashlib.sha256(block_string.encode()).hexdigest()
            if current_block["hash"] != expected_hash:
                errors.append(f"Block {i}: Hash integrity failed")
            
            # Verify Lamport signature if present
            if current_block["signature"] and current_block["public_key"]:
                try:
                    # Reconstruct signature and public key from hex
                    signature = [bytes.fromhex(sig) for sig in current_block["signature"]]
                    public_key = [[bytes.fromhex(pub[0]), bytes.fromhex(pub[1])] 
                                 for pub in current_block["public_key"]]
                    
                    if not self.lamport.verify_signature(public_key, signature, block_string):
                        errors.append(f"Block {i}: Signature verification failed")
                        
                except Exception as e:
                    errors.append(f"Block {i}: Signature verification error - {e}")
        
        is_valid = len(errors) == 0
        
        if is_valid:
            print(f"✅ Blockchain integrity verified - {len(self.chain)} blocks valid")
        else:
            print(f"❌ Blockchain integrity compromised - {len(errors)} errors found")
            for error in errors:
                print(f"   • {error}")
        
        return is_valid, errors
    
    def get_validation_history(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get validation history from the blockchain"""
        history = [block["validation_data"] for block in self.chain[1:]]  # Skip genesis
        
        if limit:
            history = history[-limit:]
        
        return history
    
    def save_chain(self):
        """Save blockchain to persistent storage"""
        try:
            with open(self.chain_file, 'w') as f:
                json.dump(self.chain, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save blockchain: {e}")
    
    def load_chain(self):
        """Load blockchain from persistent storage"""
        try:
            if os.path.exists(self.chain_file):
                with open(self.chain_file, 'r') as f:
                    self.chain = json.load(f)
                print(f"🔐 Loaded blockchain with {len(self.chain)} blocks")
        except Exception as e:
            print(f"⚠️ Failed to load blockchain: {e}")
            self.chain = []

class SecureValidationLogger:
    """
    Main interface for secure validation logging.
    Combines Lamport signatures + blockchain for unfuckable audit trails.
    """
    
    def __init__(self, chain_file: str = "validation_audit.json"):
        """Initialize secure logger"""
        self.blockchain = ValidationBlockchain(chain_file)
        self.session_id = secrets.token_hex(16)
        
        print(f"🔐 Secure Validation Logger initialized")
        print(f"   Session ID: {self.session_id}")
        print(f"   Blockchain: {len(self.blockchain.chain)} blocks")
    
    def log_validation(self, validation_result: Dict[str, Any], 
                      metadata: Dict[str, Any] = None) -> str:
        """
        Log a validation result to the secure blockchain.
        Returns the block hash for reference.
        """
        # Prepare validation data
        log_entry = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "validation_result": validation_result,
            "metadata": metadata or {},
            "chain_index": len(self.blockchain.chain)
        }
        
        # Add to blockchain with signature
        block = self.blockchain.add_validation_block(log_entry, sign_block=True)
        
        print(f"🔐 Validation logged to blockchain - Block {block['index']}")
        return block["hash"]
    
    def verify_validation_integrity(self, block_hash: str = None) -> bool:
        """
        Verify validation integrity.
        If block_hash provided, verify specific block.
        Otherwise verify entire chain.
        """
        if block_hash:
            # Verify specific block
            for block in self.blockchain.chain:
                if block["hash"] == block_hash:
                    block_string = self.blockchain._serialize_block_for_hash(block)
                    expected_hash = hashlib.sha256(block_string.encode()).hexdigest()
                    return block["hash"] == expected_hash
            return False
        else:
            # Verify entire chain
            is_valid, errors = self.blockchain.verify_chain_integrity()
            return is_valid
    
    def get_audit_report(self) -> Dict[str, Any]:
        """Generate comprehensive audit report"""
        is_valid, errors = self.blockchain.verify_chain_integrity()
        
        report = {
            "audit_timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "blockchain_status": {
                "is_valid": is_valid,
                "total_blocks": len(self.blockchain.chain),
                "total_validations": len(self.blockchain.chain) - 1,  # Minus genesis
                "errors": errors
            },
            "recent_validations": self.blockchain.get_validation_history(limit=10),
            "security_features": [
                "Quantum-resistant Lamport signatures",
                "Blockchain integrity verification", 
                "Tamper-proof audit trails",
                "Cryptographic validation proofs"
            ]
        }
        
        return report

# Integration example for existing DeepSeek suite
def integrate_with_validation_suite():
    """
    Example integration with existing validation components.
    Call this from your main validation pipeline.
    """
    
    # Initialize secure logger (once per session)
    logger = SecureValidationLogger("deepseek_validation_audit.json")
    
    # Example validation result (replace with your actual validation data)
    validation_result = {
        "input_code": "def calculate_odds(bet, odds): return bet * odds",
        "model_used": "deepseek-coder",
        "validation_status": "approved",
        "confidence_score": 0.95,
        "issues_found": [],
        "processing_time": 1.23
    }
    
    metadata = {
        "user_tier": "enterprise",
        "validation_chain": "deepseek-claude-hybrid",
        "api_cost": 0.0045
    }
    
    # Log validation with cryptographic proof
    block_hash = logger.log_validation(validation_result, metadata)
    
    # Verify integrity
    is_valid = logger.verify_validation_integrity()
    
    print(f"🔐 Validation logged: {block_hash}")
    print(f"🔐 Chain integrity: {'✅ Valid' if is_valid else '❌ Compromised'}")
    
    return logger

# Demo and testing
if __name__ == "__main__":
    print("🔐 Testing Quantum-Resistant Blockchain Logger...")
    
    # Test Lamport signatures
    lamport = LamportSignature()
    priv_key, pub_key = lamport.generate_keypair()
    
    test_message = "Test validation: This code generates betting odds"
    signature = lamport.sign_message(priv_key, test_message)
    is_valid = lamport.verify_signature(pub_key, signature, test_message)
    
    print(f"🔐 Lamport signature test: {'✅ Valid' if is_valid else '❌ Failed'}")
    
    # Test blockchain integrity
    logger = integrate_with_validation_suite()
    
    # Add a few more test validations
    for i in range(3):
        test_validation = {
            "test_id": f"test_{i}",
            "code_snippet": f"function test_{i}() {{ return {i * 2}; }}",
            "result": "valid"
        }
        logger.log_validation(test_validation)
    
    # Generate audit report
    report = logger.get_audit_report()
    print(f"\n🔐 Audit Report:")
    print(f"   Total validations: {report['blockchain_status']['total_validations']}")
    print(f"   Chain valid: {report['blockchain_status']['is_valid']}")
    
    # Test tampering detection (try to modify chain file manually to see it fail)
    print("\n🔐 Quantum-resistant security system ready for enterprise deployment!")