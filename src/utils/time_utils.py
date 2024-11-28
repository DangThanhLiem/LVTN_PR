from datetime import datetime, timedelta

class TimeUtils:
    @staticmethod
    def calculate_hours(check_in: str, check_out: str) -> float:
        """Calculate hours between check-in and check-out times"""
        try:
            time_in = datetime.strptime(check_in, '%H:%M:%S')
            time_out = datetime.strptime(check_out, '%H:%M:%S')
            
            # If check-out is earlier than check-in, assume it's next day
            if time_out < time_in:
                time_out += timedelta(days=1)
                
            duration = time_out - time_in
            hours = duration.total_seconds() / 3600
            return round(hours, 2)
        except Exception as e:
            print(f"Error calculating hours: {str(e)}")
            return 0.0

    @staticmethod
    def format_time(time_str: str) -> str:
        """Format time string to HH:MM:SS"""
        try:
            time_obj = datetime.strptime(time_str, '%H:%M:%S')
            return time_obj.strftime('%H:%M:%S')
        except:
            return time_str

    @staticmethod
    def get_current_time() -> str:
        """Get current time in HH:MM:SS format"""
        return datetime.now().strftime('%H:%M:%S')

    @staticmethod
    def get_current_date() -> str:
        """Get current date in YYYY-MM-DD format"""
        return datetime.now().strftime('%Y-%m-%d')

    @staticmethod
    def is_valid_time(time_str: str) -> bool:
        """Check if time string is valid"""
        try:
            datetime.strptime(time_str, '%H:%M:%S')
            return True
        except:
            return False
