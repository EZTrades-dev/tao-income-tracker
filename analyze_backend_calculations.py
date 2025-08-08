#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

def fetch_portfolio_balance(coldkey):
    """Fetch current portfolio balance data"""
    url = "http://localhost:8000/portfolio/balance"
    params = {"coldkey": coldkey}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result.get('success') and 'data' in result:
            return result['data']
        else:
            print(f"Unexpected response structure: {result}")
            return None
    else:
        print(f"Error: {response.status_code}")
        return None

def analyze_backend_calculations(data):
    """Perform the same calculations as the frontend to verify accuracy"""
    if not data or not isinstance(data, list):
        print("No data received")
        return
    
    # Filter for last 24 hours
    now = datetime.now()
    one_day_ago = now - timedelta(hours=24)
    
    print(f"Filtering data from: {one_day_ago} to {now}")
    
    # Process data similar to frontend
    processed_data = []
    
    for entry in data:
        timestamp = entry['timestamp']
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        # Only include data from the last 24 hours
        if dt >= one_day_ago:
            processed_data.append({
                'timestamp': dt,
                'netuid': entry['netuid'],
                'tokenAmount': entry['stake'],
                'tokenPrice': entry['price'],
                'balanceValue': entry['stake'] * entry['price'],
                'dtaoValue': entry['dtao_value'],
                'dtaoValueUSD': entry['dtao_value'] * entry['tao_price'],
                'taoBalance': entry['tao_balance'],
                'taoPrice': entry['tao_price']
            })
    
    print(f"Filtered data points: {len(processed_data)}")
    
    # Group data by subnet (same as frontend)
    subnet_data = defaultdict(list)
    for entry in processed_data:
        subnet_data[entry['netuid']].append(entry)
    
    # Sort each subnet's data by timestamp (newest first)
    for netuid in subnet_data:
        subnet_data[netuid].sort(key=lambda x: x['timestamp'], reverse=True)
    
    print(f"Subnets with data: {len(subnet_data)}")
    
    # Calculate totals (same as frontend)
    total_balance_change = 0
    total_rewards_usd = 0
    past_hour_rewards = 0
    past_24_hours_rewards = 0
    
    # Collect rewards arrays (same as frontend)
    most_recent_rewards = []
    daily_rewards = []
    
    # Calculate rewards for each subnet
    for netuid, subnet_entries in subnet_data.items():
        if len(subnet_entries) >= 2:
            # Data is already sorted newest first
            most_recent = subnet_entries[0]
            oldest = subnet_entries[-1]
            
            # Calculate token amount change (staking rewards)
            token_change = most_recent['tokenAmount'] - oldest['tokenAmount']
            rewards_usd = token_change * most_recent['tokenPrice']
            
            # Calculate balance value change
            balance_change = most_recent['balanceValue'] - oldest['balanceValue']
            
            total_rewards_usd += rewards_usd
            total_balance_change += balance_change
            
            print(f"\n=== Subnet {netuid} ===")
            print(f"Data period: {oldest['timestamp']} to {most_recent['timestamp']}")
            print(f"Total stake change: {token_change:.6f} tokens")
            print(f"Reward USD: ${rewards_usd:.6f}")
            
            # For each subnet, calculate rewards for consecutive time periods
            for i in range(len(subnet_entries) - 1):
                current_entry = subnet_entries[i]
                next_entry = subnet_entries[i + 1]
                
                # Calculate reward for this time period
                token_reward = current_entry['tokenAmount'] - next_entry['tokenAmount']
                reward_usd = token_reward * current_entry['tokenPrice']
                
                print(f"  Entry {i}: {current_entry['timestamp']} - Token change: {token_reward:.6f}, Reward USD: ${reward_usd:.6f}")
                
                # Only count positive rewards
                if reward_usd > 0:
                    # For hourly rewards, only count the most recent hour
                    if i == 0:
                        most_recent_rewards.append(reward_usd)
                        print(f"    -> Added to hourly rewards: ${reward_usd:.6f}")
                    
                    # For daily rewards, count all rewards in the 24-hour period
                    daily_rewards.append(reward_usd)
                    print(f"    -> Added to daily rewards: ${reward_usd:.6f}")
    
    # Sum all rewards (same as frontend)
    past_hour_rewards = sum(most_recent_rewards)
    past_24_hours_rewards = sum(daily_rewards)
    
    print(f"\n=== BACKEND CALCULATION RESULTS ===")
    print(f"Past hour rewards collected: {len(most_recent_rewards)} rewards")
    print(f"Past 24 hours rewards collected: {len(daily_rewards)} rewards")
    print(f"Past Hour Rewards: ${past_hour_rewards:.6f}")
    print(f"Past 24 Hours Rewards: ${past_24_hours_rewards:.6f}")
    print(f"Total Rewards USD: ${total_rewards_usd:.6f}")
    print(f"Total Balance Change: ${total_balance_change:.6f}")
    
    # Verify calculation logic
    print(f"\n=== VERIFICATION ===")
    print(f"Hourly rewards sum: {sum(most_recent_rewards):.6f}")
    print(f"Daily rewards sum: {sum(daily_rewards):.6f}")
    print(f"Total rewards from all subnets: {total_rewards_usd:.6f}")
    
    # Check if calculations make sense
    if past_hour_rewards >= 0 and past_24_hours_rewards >= 0:
        print("✅ Calculations appear correct")
    else:
        print("❌ Negative rewards detected - check calculation logic")
    
    return {
        'past_hour_rewards': past_hour_rewards,
        'past_24_hours_rewards': past_24_hours_rewards,
        'total_rewards_usd': total_rewards_usd,
        'total_balance_change': total_balance_change,
        'data_points': len(processed_data),
        'subnets': len(subnet_data)
    }

if __name__ == "__main__":
    coldkey = "5H6Hecx18JknhSubE2ewEJMvHb2N5TL1LVYXL6EENoCoLHW2"
    
    print("Performing backend calculations analysis...")
    data = fetch_portfolio_balance(coldkey)
    
    if data:
        print(f"Received {len(data)} total data points")
        results = analyze_backend_calculations(data)
        
        print(f"\n=== SUMMARY ===")
        print(f"Data points processed: {results['data_points']}")
        print(f"Subnets analyzed: {results['subnets']}")
        print(f"Past Hour Rewards: ${results['past_hour_rewards']:.2f}")
        print(f"Past 24 Hours Rewards: ${results['past_24_hours_rewards']:.2f}")
        print(f"Total Rewards: ${results['total_rewards_usd']:.2f}")
    else:
        print("Failed to fetch data")
