import subprocess
import pandas as pd
import os
import time

# Function to create a chunk of the CSV
def create_chunk(df, start_idx, end_idx, chunk_num):
    chunk = df.iloc[start_idx:end_idx]
    chunk_filename = f'linkList_chunk_{chunk_num}.csv'
    chunk.to_csv(chunk_filename, index=False)
    return chunk_filename

# Load the main CSV file
main_csv = 'linkList.csv'
df = pd.read_csv(main_csv)
total_entries = len(df)
chunk_size = 20
num_chunks = (total_entries // chunk_size) + (1 if total_entries % chunk_size != 0 else 0)
num_parallel_processes = 50

# Function to start a new process
def start_process(chunk_filename):
    command = f'python scrape.py {chunk_filename}'
    return subprocess.Popen(['powershell', '-Command', command])

# Iterate over chunks and create new CSV files
current_chunk = 1387
active_processes = []
active_chunks = []

while current_chunk < num_chunks or active_processes:
    # Start new processes if there are available slots
    while len(active_processes) < num_parallel_processes and current_chunk < num_chunks:
        start_idx = current_chunk * chunk_size
        end_idx = min(start_idx + chunk_size, total_entries)
        
        chunk_filename = create_chunk(df, start_idx, end_idx, current_chunk)
        process = start_process(chunk_filename)
        active_processes.append((process, current_chunk))
        active_chunks.append(current_chunk)
        
        current_chunk += 1
    
    # Print the list of currently processing chunks
    print(f"Currently processing chunks: {active_chunks}")
    
    # Check the status of active processes and remove completed ones
    for process, chunk_num in active_processes[:]:
        if process.poll() is not None:  # Process has completed
            active_processes.remove((process, chunk_num))
            active_chunks.remove(chunk_num)
    
    # Adding a short delay to avoid busy-waiting
    time.sleep(10)

print("All tasks have been processed.")
