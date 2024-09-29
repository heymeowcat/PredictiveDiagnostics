import csv
import random
import uuid
from datetime import datetime, timedelta

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

file_name = 'modem_diagnostics_data.csv'

fields = [
    'Customer Account ID', 'Site ID', 'Modem Serial Number', 'Model',
    'Connection Speed (Mbps)', 'Uptime (days)', 'Signal Strength (dBm)',
    'Packet Loss (%)', 'Error Rate (%)', 'SNR (Signal-to-Noise Ratio)', 
    'RSSI (Received Signal Strength Indicator)', 'Modulation Type', 
    'Error Type', 'Error Count', 'Temperature (°C)', 'Power Level (dBm)',
    'Last Checkup Date', 'Failure Date', 'Next Predicted Failure (days)'
]

modem_models = ['Arris TG2492', 'Technicolor CGM4231', 'Motorola MB7621', 'Netgear CM500', 'TP-Link Archer C7']

error_types = ['CRC Errors', 'Packet Drops', 'Signal Fading', 'Sync Loss', 'Overheating']

def generate_modem_data(num_rows):
    data = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 1, 1)
    
    for _ in range(num_rows):
        last_checkup = random_date(start_date, end_date)
        failure_date = last_checkup + timedelta(days=random.randint(1, 365))
        
        # Modem diagnostics data
        row = {
            'Customer Account ID': f'ACC-{random.randint(10000, 99999)}',
            'Site ID': f'SITE-{random.randint(1000, 9999)}',
            'Modem Serial Number': str(uuid.uuid4())[:8],  # Shortened UUID
            'Model': random.choice(modem_models),
            'Connection Speed (Mbps)': round(random.uniform(100, 1500), 2),  # Higher speeds for 5G broadband
            'Uptime (days)': random.randint(1, 365),
            'Signal Strength (dBm)': round(random.uniform(-100, -30), 1), 
            'Packet Loss (%)': round(random.uniform(0, 10), 2),  # Slightly higher range
            'Error Rate (%)': round(random.uniform(0, 5), 2),
            'SNR (Signal-to-Noise Ratio)': round(random.uniform(10, 50), 2),  # Realistic SNR values for 5G
            'RSSI (Received Signal Strength Indicator)': round(random.uniform(-120, -40), 2),
            'Modulation Type': random.choice(['QAM16', 'QAM64', 'QAM256', 'QPSK']),
            'Error Type': random.choice(error_types),
            'Error Count': random.randint(0, 500),  # Number of errors encountered
            'Temperature (°C)': round(random.uniform(30, 85), 1),  # Modem operating temperature
            'Power Level (dBm)': round(random.uniform(-10, 10), 2),
            'Last Checkup Date': last_checkup.strftime('%Y-%m-%d'),
            'Failure Date': failure_date.strftime('%Y-%m-%d'),
            'Next Predicted Failure (days)': (failure_date - last_checkup).days,
        }
        data.append(row)
    
    return data

# Write data to CSV
def write_to_csv(file_name, data):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(data)

# Main function to generate and save the dataset
if __name__ == '__main__':
    # Generate 1000 rows of modem data
    modem_data = generate_modem_data(1000)
    
    # Write data to CSV file
    write_to_csv(file_name, modem_data)
    print(f'{file_name} has been created with {len(modem_data)} rows of data.')
