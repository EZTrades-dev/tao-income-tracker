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

def reproduce_balance_table(data):
    """Reproduce the exact same calculations as the frontend Balance History Table"""
    if not data or not isinstance(data, list):
        print("No data received")
        return
    
    # Filter for last 24 hours (same as frontend)
    now = datetime.now()
    one_day_ago = now - timedelta(hours=24)
    
    print(f"Filtering data from: {one_day_ago} to {now}")
    
    # Process data exactly like frontend
    processed_data = []
    
    for entry in data:
        timestamp = entry['timestamp']
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        # Only include data from the last 24 hours (same as frontend)
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
    
    # Sort each subnet's data by timestamp (newest first) - same as frontend
    for netuid in subnet_data:
        subnet_data[netuid].sort(key=lambda x: x['timestamp'], reverse=True)
    
    print(f"Subnets with data: {len(subnet_data)}")
    
    # Reproduce the Balance History Table calculations
    print(f"\n{'='*80}")
    print("BALANCE HISTORY TABLE REPRODUCTION")
    print(f"{'='*80}")
    print(f"{'Timestamp':<20} {'Subnet':<8} {'Token Amount':<15} {'Token Price (TAO)':<18} {'Balance Value (TAO)':<20} {'Rewards Earned (Tokens)':<25} {'Rewards Value (USD)':<20}")
    print("-" * 120)
    
    table_entries = []
    
    # Process each entry exactly like the frontend table
    for entry in processed_data:
        # Calculate rewards for this subnet (same as frontend displayBalanceTable)
        subnet_entries = subnet_data[entry['netuid']]
        rewards_earned = 0
        rewards_value_usd = 0
        
        if len(subnet_entries) >= 2:
            # Find the current entry's position and calculate hourly change (same as frontend)
            current_index = None
            for i, e in enumerate(subnet_entries):
                if e['timestamp'] == entry['timestamp']:
                    current_index = i
                    break
            
            if current_index is not None and current_index < len(subnet_entries) - 1:
                next_entry = subnet_entries[current_index + 1]  # Next older entry
                
                # Calculate token amount change for this specific hour (same as frontend)
                rewards_earned = entry['tokenAmount'] - next_entry['tokenAmount']
                
                # For subnet 0 (TAO), use TAO USD price; for other subnets, use subnet token price
                if entry['netuid'] == 0:
                    # Subnet 0 uses TAO tokens, so multiply by TAO USD price
                    rewards_value_usd = rewards_earned * entry['taoPrice']
                else:
                    # Other subnets use their own token prices
                    rewards_value_usd = rewards_earned * entry['tokenPrice']
        
        # Format timestamp like frontend
        timestamp_str = entry['timestamp'].strftime('%m/%d/%Y, %I:%M:%S %p')
        
        # Create table row (same format as frontend)
        table_row = {
            'timestamp': timestamp_str,
            'subnet': f"Subnet {entry['netuid']}",
            'token_amount': f"{entry['tokenAmount']:.6f}",
            'token_price': f"${entry['tokenPrice']:.6f}",
            'balance_value': f"${entry['balanceValue']:.2f}",
            'rewards_earned': f"{rewards_earned:.6f} tokens",
            'rewards_value_usd': f"${rewards_value_usd:.2f}"
        }
        
        table_entries.append(table_row)
        
        # Print formatted row
        print(f"{table_row['timestamp']:<20} {table_row['subnet']:<8} {table_row['token_amount']:<15} {table_row['token_price']:<18} {table_row['balance_value']:<20} {table_row['rewards_earned']:<25} {table_row['rewards_value_usd']:<20}")
    
    print(f"\n{'='*80}")
    print("TABLE SUMMARY")
    print(f"{'='*80}")
    print(f"Total table entries: {len(table_entries)}")
    print(f"Unique subnets: {len(subnet_data)}")
    
    # Calculate totals from table data
    total_rewards_earned = 0
    total_rewards_value_usd = 0
    total_balance_value = 0
    
    for entry in processed_data:
        subnet_entries = subnet_data[entry['netuid']]
        if len(subnet_entries) >= 2:
            newest = subnet_entries[0]
            oldest = subnet_entries[-1]
            rewards_earned = newest['tokenAmount'] - oldest['tokenAmount']
            
            # For subnet 0 (TAO), use TAO USD price; for other subnets, use subnet token price
            if newest['netuid'] == 0:
                # Subnet 0 uses TAO tokens, so multiply by TAO USD price
                rewards_value_usd = rewards_earned * newest['taoPrice']
            else:
                # Other subnets use their own token prices
                rewards_value_usd = rewards_earned * newest['tokenPrice']
            
            total_rewards_earned += rewards_earned
            total_rewards_value_usd += rewards_value_usd
        
        total_balance_value += entry['balanceValue']
    
    print(f"Total Rewards Earned (Tokens): {total_rewards_earned:.6f}")
    print(f"Total Rewards Value (USD): ${total_rewards_value_usd:.2f}")
    print(f"Total Balance Value (TAO): ${total_balance_value:.2f}")
    
    # Show sample of first few entries
    print(f"\n{'='*80}")
    print("SAMPLE TABLE ENTRIES (First 5)")
    print(f"{'='*80}")
    for i, entry in enumerate(table_entries[:5]):
        print(f"Entry {i+1}:")
        print(f"  Timestamp: {entry['timestamp']}")
        print(f"  Subnet: {entry['subnet']}")
        print(f"  Token Amount: {entry['token_amount']}")
        print(f"  Token Price: {entry['token_price']}")
        print(f"  Balance Value: {entry['balance_value']}")
        print(f"  Rewards Earned: {entry['rewards_earned']}")
        print(f"  Rewards Value USD: {entry['rewards_value_usd']}")
        print()
    
    return {
        'table_entries': table_entries,
        'total_rewards_earned': total_rewards_earned,
        'total_rewards_value_usd': total_rewards_value_usd,
        'total_balance_value': total_balance_value,
        'data_points': len(processed_data),
        'subnets': len(subnet_data)
    }

if __name__ == "__main__":
    coldkey = "5H6Hecx18JknhSubE2ewEJMvHb2N5TL1LVYXL6EENoCoLHW2"
    
    print("Reproducing Balance History Table calculations...")
    data = fetch_portfolio_balance(coldkey)
    
    if data:
        print(f"Received {len(data)} total data points")
        results = reproduce_balance_table(data)
        
        print(f"\n{'='*80}")
        print("FINAL SUMMARY")
        print(f"{'='*80}")
        print(f"Table entries generated: {len(results['table_entries'])}")
        print(f"Data points processed: {results['data_points']}")
        print(f"Subnets analyzed: {results['subnets']}")
        print(f"Total Rewards Earned: {results['total_rewards_earned']:.6f} tokens")
        print(f"Total Rewards Value: ${results['total_rewards_value_usd']:.2f}")
        print(f"Total Balance Value: ${results['total_balance_value']:.2f}")
    else:
        print("Failed to fetch data")
