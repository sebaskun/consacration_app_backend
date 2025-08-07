from datetime import datetime, timedelta
from typing import Dict, Tuple

# Rate limits for different operations
PROGRESS_RATE_LIMIT = 10      # Progress updates: 10 per 5 minutes (normal spiritual practice)
AUTH_RATE_LIMIT = 5           # Login attempts: 5 per 5 minutes (prevent brute force)
GENERAL_RATE_LIMIT = 60       # General API: 60 per 5 minutes (dashboard, content)
LIBRE_MODE_RATE_LIMIT = 2     # Libre mode toggle: 2 per hour (prevent abuse)

class RateLimiter:
    def __init__(self, max_requests: int = GENERAL_RATE_LIMIT, window_seconds: int = 300):
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

# Global rate limiter instances
progress_rate_limiter = RateLimiter(max_requests=PROGRESS_RATE_LIMIT, window_seconds=300)
auth_rate_limiter = RateLimiter(max_requests=AUTH_RATE_LIMIT, window_seconds=300)
general_rate_limiter = RateLimiter(max_requests=GENERAL_RATE_LIMIT, window_seconds=300)
libre_mode_rate_limiter = RateLimiter(max_requests=LIBRE_MODE_RATE_LIMIT, window_seconds=3600)  # 1 hour 