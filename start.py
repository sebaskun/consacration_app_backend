#!/usr/bin/env python3
"""
Startup script for the Totus Tuus Backend API
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False,
        log_level="info"
    ) 