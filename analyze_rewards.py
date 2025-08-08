#!/usr/bin/env python3
import requests
import json
from datetime import datetime
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

def analyze_rewards(data):
    """Analyze rewards from portfolio balance data"""
    if not data or not isinstance(data, list):
        print("No data received")
        return
    
    # Group data by subnet and timestamp
    subnet_data = defaultdict(lambda: defaultdict(dict))
    
    for entry in data:
        timestamp = entry['timestamp']
        netuid = entry['netuid']
        stake = entry['stake']
        price = entry['price']
        dtao_value = entry['dtao_value']
        tao_price = entry['tao_price']
        
        # Convert timestamp to datetime
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        subnet_data[netuid][timestamp] = {
            'datetime': dt,
            'stake': stake,
            'price': price,
            'dtao_value': dtao_value,
            'tao_price': tao_price,
            'balance_value_usd': stake * price * tao_price
        }
    
    print(f"Found data for {len(subnet_data)} subnets")
    print(f"Time range: {min(entry['datetime'] for subnet in subnet_data.values() for entry in subnet.values())} to {max(entry['datetime'] for subnet in subnet_data.values() for entry in subnet.values())}")
    
    # Calculate rewards for each subnet
    total_rewards = 0
    hourly_rewards = 0
    daily_rewards = 0
    
    for netuid, timestamps in subnet_data.items():
        print(f"\n=== Subnet {netuid} ===")
        
        # Sort timestamps
        sorted_timestamps = sorted(timestamps.keys())
        
        if len(sorted_timestamps) < 2:
            print(f"  Only {len(sorted_timestamps)} data point(s) - skipping")
            continue
        
        # Calculate total rewards (newest - oldest)
        newest = timestamps[sorted_timestamps[-1]]
        oldest = timestamps[sorted_timestamps[0]]
        
        stake_change = newest['stake'] - oldest['stake']
        reward_usd = stake_change * newest['price'] * newest['tao_price']
        
        print(f"  Total stake change: {stake_change:.6f} tokens")
        print(f"  Reward USD: ${reward_usd:.6f}")
        
        total_rewards += reward_usd
        
        # Calculate hourly rewards (last hour)
        current_time = newest['datetime']
        from datetime import timedelta
        one_hour_ago = current_time - timedelta(hours=1)
        
        hourly_reward = 0
        for i in range(len(sorted_timestamps) - 1):
            current_entry = timestamps[sorted_timestamps[i+1]]
            next_entry = timestamps[sorted_timestamps[i]]
            
            if current_entry['datetime'] >= one_hour_ago:
                stake_diff = next_entry['stake'] - current_entry['stake']
                if stake_diff > 0:
                    reward = stake_diff * next_entry['price'] * next_entry['tao_price']
                    hourly_reward += reward
                    print(f"    Hourly: {stake_diff:.6f} tokens = ${reward:.6f}")
        
        hourly_rewards += hourly_reward
        
        # Calculate daily rewards (last 24 hours)
        one_day_ago = current_time - timedelta(hours=24)
        
        daily_reward = 0
        for i in range(len(sorted_timestamps) - 1):
            current_entry = timestamps[sorted_timestamps[i+1]]
            next_entry = timestamps[sorted_timestamps[i]]
            
            if current_entry['datetime'] >= one_day_ago:
                stake_diff = next_entry['stake'] - current_entry['stake']
                if stake_diff > 0:
                    reward = stake_diff * next_entry['price'] * next_entry['tao_price']
                    daily_reward += reward
        
        daily_rewards += daily_reward
    
    print(f"\n=== SUMMARY ===")
    print(f"Total Historical Rewards: ${total_rewards:.6f}")
    print(f"Past Hour Rewards: ${hourly_rewards:.6f}")
    print(f"Past 24 Hours Rewards: ${daily_rewards:.6f}")

if __name__ == "__main__":
    coldkey = "5H6Hecx18JknhSubE2ewEJMvHb2N5TL1LVYXL6EENoCoLHW2"
    
    print("Fetching portfolio balance data...")
    data = fetch_portfolio_balance(coldkey)
    
    if data:
        print(f"Received {len(data)} data points")
        analyze_rewards(data)
    else:
        print("Failed to fetch data")
