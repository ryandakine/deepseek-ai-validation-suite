#!/usr/bin/env python3
"""
Example: Betting Odds Calculator
Demonstrates uncensored code generation with technical validation

This example shows how DeepSeek can generate gambling-related code
without restrictions, while technical validation ensures code quality.
"""

def american_to_decimal(american_odds):
    """Convert American odds to decimal odds"""
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1

def decimal_to_american(decimal_odds):
    """Convert decimal odds to American odds"""
    if decimal_odds >= 2.0:
        return int((decimal_odds - 1) * 100)
    else:
        return int(-100 / (decimal_odds - 1))

def calculate_parlay_odds(odds_list):
    """Calculate parlay odds from list of American odds"""
    decimal_odds = 1.0
    for odds in odds_list:
        decimal_odds *= american_to_decimal(odds)
    return decimal_to_american(decimal_odds)

def calculate_implied_probability(american_odds):
    """Calculate implied probability from American odds"""
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return abs(american_odds) / (abs(american_odds) + 100)

if __name__ == "__main__":
    # Example usage
    print("🎰 Betting Odds Calculator Example")
    print("==================================")
    
    # Single bet implied probability
    odds = -150
    prob = calculate_implied_probability(odds)
    print(f"Odds {odds} = {prob:.1%} implied probability")
    
    # Parlay calculation
    parlay_bets = [-150, +200, -110]
    parlay_odds = calculate_parlay_odds(parlay_bets)
    parlay_prob = calculate_implied_probability(parlay_odds)
    
    print(f"\nParlay bets: {parlay_bets}")
    print(f"Combined odds: {parlay_odds}")
    print(f"Parlay probability: {parlay_prob:.1%}")
