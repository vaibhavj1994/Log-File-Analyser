from datetime import datetime
from collections import defaultdict

def process_log_file(file_path: str) -> None:
    """
    Process a log file and print user reports.

    Args:
    file_path (str): The path to the log file.

    Returns:
    None
    """
    # Initialize data structures
    sessions = defaultdict(list)  # Store user sessions
    earliest_time = None  # Store the earliest time in the log file
    latest_time = None  # Store the latest time in the log file

    # Open and read the log file
    with open(file_path, 'r') as file:
        for line in file:
            # Ignore invalid lines
            try:
                time_str, user, action = line.strip().split(maxsplit=2)  # Split each line into time, user, and action
                time = datetime.strptime(time_str, '%H:%M:%S')  # Convert time string to datetime object
            except ValueError:
                continue  # Skip invalid lines

            # Update earliest and latest times
            earliest_time = min(earliest_time, time) if earliest_time else time
            latest_time = max(latest_time, time) if latest_time else time

            # Add session start or end time
            sessions[user].append((time, action))  # Store user sessions

    # Process sessions and calculate total durations
    for user, times in sessions.items():
        times.sort()  # Sort user sessions by time
        total_duration = 0  # Initialize total duration
        start_times = []  # Store start times for sessions without end times

        for time, action in times:
            if action == 'Start':
                start_times.append(time)  # Add start time to the list
            elif action == 'End' and start_times:
                start_time = start_times.pop()  # Get the corresponding start time
                total_duration += (time - start_time).total_seconds()  # Calculate duration

        # Handle sessions without end times
        for start_time in start_times:
            total_duration += (latest_time - start_time).total_seconds()  # Calculate duration for sessions without end times

        # Print user report
        print(f'User: {user}, Sessions: {len(times) // 2}, Duration: {total_duration:.2f} seconds')  # Print user report with 2 decimal places

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python log_analyser.py <log_file>")  # Print usage message
        sys.exit(1)  # Exit with error code 1
    process_log_file(sys.argv[1])  # Process the log file