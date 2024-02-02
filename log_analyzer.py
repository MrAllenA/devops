import re
from collections import Counter

def analyze_logs(log_file_path):
    # Initialize variables to store data
    total_requests = 0
    status_code_counts = Counter()
    requested_pages = Counter()
    ip_address_counts = Counter()

    # Regular expression for parsing CLF
    clf_pattern = re.compile(r'(\S+) (\S+) (\S+) \[([^\]]+)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)')

    # Open and read the log file
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            match = clf_pattern.match(line)
            if match:
                total_requests += 1
                status_code = int(match.group(8))
                requested_page = match.group(6)
                ip_address = match.group(1)

                # Count status codes
                status_code_counts[status_code] += 1

                # Count requested pages
                requested_pages[requested_page] += 1

                # Count IP addresses
                ip_address_counts[ip_address] += 1

    # Print summary report
    print("Total Requests:", total_requests)
    print("\nStatus Code Counts:")
    print(status_code_counts)
    for code, count in status_code_counts.items():
        print(f"{code}: {count} requests")

    print("\nMost Requested Pages:")
    for page, count in requested_pages.most_common(5):  # Change 5 to desired number of top pages
        print(f"{page}: {count} requests")

    print("\nIP Addresses with Most Requests:")
    for ip, count in ip_address_counts.most_common(5):  # Change 5 to desired number of top IP addresses
        print(f"{ip}: {count} requests")

# Example usage
log_file_path = 'access.log'
analyze_logs(log_file_path)
