from datetime import datetime, timedelta
from typing import Dict, Tuple

RATE_LIMIT = 100000

class RateLimiter:
    def __init__(self, max_requests: int = RATE_LIMIT, window_seconds: int = 300):  # 10 requests per 5 minutes
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}  # user_id -> list of timestamps
    
    def is_allowed(self, user_id: str) -> Tuple[bool, int]:
        """
        Check if user is allowed to make a request
        Returns: (is_allowed, remaining_requests)
        """
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Get user's request history
        user_requests = self.requests.get(user_id, [])
        
        # Filter requests within the current window
        recent_requests = [req_time for req_time in user_requests if req_time > window_start]
        
        # Update user's request history
        self.requests[user_id] = recent_requests
        
        # Check if user has exceeded the limit
        if len(recent_requests) >= self.max_requests:
            return False, 0
        
        # Add current request
        recent_requests.append(now)
        self.requests[user_id] = recent_requests
        
        remaining = self.max_requests - len(recent_requests)
        return True, remaining
    
    def get_retry_after(self, user_id: str) -> int:
        """Get seconds until user can make another request"""
        if user_id not in self.requests or not self.requests[user_id]:
            return 0
        
        # Find the oldest request
        oldest_request = min(self.requests[user_id])
        window_end = oldest_request + timedelta(seconds=self.window_seconds)
        now = datetime.now()
        
        if window_end > now:
            return int((window_end - now).total_seconds())
        return 0

# Global rate limiter instance
progress_rate_limiter = RateLimiter(max_requests=10, window_seconds=300)  # 10 requests per 5 minutes 