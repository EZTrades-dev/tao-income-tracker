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

def analyze_data_consistency(data):
    """Analyze the consistency and time range of portfolio data"""
    if not data or not isinstance(data, list):
        print("No data received")
        return
    
    # Group data by timestamp to see what time periods we have
    timestamp_data = defaultdict(list)
    
    for entry in data:
        timestamp = entry['timestamp']
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        timestamp_data[dt].append(entry)
    
    # Sort timestamps
    sorted_timestamps = sorted(timestamp_data.keys())
    
    print(f"Total data points: {len(data)}")
    print(f"Unique timestamps: {len(sorted_timestamps)}")
    print(f"Time range: {sorted_timestamps[0]} to {sorted_timestamps[-1]}")
    print(f"Duration: {sorted_timestamps[-1] - sorted_timestamps[0]}")
    
    # Check if we have recent data (last 48 hours)
    now = datetime.now()
    two_days_ago = now - timedelta(hours=48)
    
    recent_timestamps = [ts for ts in sorted_timestamps if ts >= two_days_ago]
    print(f"\nRecent data (last 48 hours): {len(recent_timestamps)} timestamps")
    
    if recent_timestamps:
        print(f"Recent time range: {recent_timestamps[0]} to {recent_timestamps[-1]}")
    else:
        print("No recent data found!")
    
    # Show sample of timestamps
    print(f"\nFirst 10 timestamps:")
    for i, ts in enumerate(sorted_timestamps[:10]):
        print(f"  {i+1}: {ts}")
    
    print(f"\nLast 10 timestamps:")
    for i, ts in enumerate(sorted_timestamps[-10:]):
        print(f"  {i+1}: {ts}")
    
    # Check data consistency per subnet
    subnet_timestamps = defaultdict(set)
    for entry in data:
        dt = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
        subnet_timestamps[entry['netuid']].add(dt)
    
    print(f"\nData consistency per subnet:")
    for netuid in sorted(subnet_timestamps.keys()):
        timestamps = sorted(subnet_timestamps[netuid])
        print(f"  Subnet {netuid}: {len(timestamps)} data points from {timestamps[0]} to {timestamps[-1]}")
    
    # Check if this data is suitable for 48-hour analysis
    if recent_timestamps:
        print(f"\n✅ SUITABLE: Data includes recent timestamps for 48-hour analysis")
        return True
    else:
        print(f"\n❌ NOT SUITABLE: No recent data for 48-hour analysis")
        return False

if __name__ == "__main__":
    coldkey = "5H6Hecx18JknhSubE2ewEJMvHb2N5TL1LVYXL6EENoCoLHW2"
    
    print("Analyzing portfolio balance data consistency...")
    data = fetch_portfolio_balance(coldkey)
    
    if data:
        print(f"Received {len(data)} data points")
        analyze_data_consistency(data)
    else:
        print("Failed to fetch data")
