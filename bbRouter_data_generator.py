import csv
import random
import uuid
from datetime import datetime, timedelta
import json

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

file_name = 'bbRouter_diagnostics_data.csv'

fields = [
    'Device ID', 'Diagnostic DateTime', 'Firmware Version',
    'WAN IP', 'LAN IP', 'DNS Servers',
    'Downstream Power (dBmV)', 'Upstream Power (dBmV)',
    'Downstream SNR (dB)', 'Upstream SNR (dB)',
    'Downstream Frequency (MHz)', 'Upstream Frequency (MHz)',
    'Packet Loss (%)', 'Latency (ms)', 'Jitter (ms)',
    'WiFi 2.4GHz Channel', 'WiFi 5GHz Channel',
    'Connected Devices Count', 'CPU Usage (%)', 'Memory Usage (%)',
    'Temperature (°C)', 'Uptime (hours)',
    'ErrorCodes'
]

def generate_error_codes():
    return [f"EX{random.randint(1, 15):02d}" for _ in range(random.randint(1, 5))]

def generate_device_data(num_devices, diagnostics_per_device):
    data = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    
    for _ in range(num_devices):
        device_id = f"bbRouter-{uuid.uuid4().hex[:8]}"
        
        for _ in range(diagnostics_per_device):
            diagnostic_time = random_date(start_date, end_date)
            
            row = {
                'Device ID': device_id,
                'Diagnostic DateTime': diagnostic_time.strftime('%Y-%m-%d %H:%M:%S'),
                'Firmware Version': f"V{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,99)}",
                'WAN IP': f"192.168.{random.randint(0,255)}.{random.randint(1,254)}",
                'LAN IP': f"10.0.{random.randint(0,255)}.1",
                'DNS Servers': f"8.8.8.8, 8.8.4.4",
                'Downstream Power (dBmV)': round(random.uniform(-15, 15), 2),
                'Upstream Power (dBmV)': round(random.uniform(35, 55), 2),
                'Downstream SNR (dB)': round(random.uniform(30, 50), 2),
                'Upstream SNR (dB)': round(random.uniform(30, 50), 2),
                'Downstream Frequency (MHz)': random.choice([258, 264, 270, 276, 282]),
                'Upstream Frequency (MHz)': random.choice([37, 38, 39, 40, 41]),
                'Packet Loss (%)': round(random.uniform(0, 5), 2),
                'Latency (ms)': round(random.uniform(10, 100), 2),
                'Jitter (ms)': round(random.uniform(0, 30), 2),
                'WiFi 2.4GHz Channel': random.choice([1, 6, 11]),
                'WiFi 5GHz Channel': random.choice([36, 40, 44, 48, 149, 153, 157, 161]),
                'Connected Devices Count': random.randint(1, 20),
                'CPU Usage (%)': random.randint(10, 90),
                'Memory Usage (%)': random.randint(20, 80),
                'Temperature (°C)': round(random.uniform(30, 70), 1),
                'Uptime (hours)': random.randint(1, 8760),  # Up to 1 year
                'ErrorCodes': json.dumps(generate_error_codes())
            }
            data.append(row)
    
    return data

def write_to_csv(file_name, data):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    num_devices = 100
    diagnostics_per_device = 50
    bbRouter_data = generate_device_data(num_devices, diagnostics_per_device)
    
    write_to_csv(file_name, bbRouter_data)
    print(f'{file_name} has been created with {len(bbRouter_data)} rows of data.')