from datetime import datetime

def check_license_status(license):
    current_time = datetime.now()

    # Check if the license is active and not expired
    if license['status'] == 'active' and license['end_date'] > current_time:
        return True
    return False
