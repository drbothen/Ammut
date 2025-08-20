RATE_LIMIT_INDICATORS = [
    "rate limit",
    "too many requests",
    "429",
    "throttle",
    "slow down",
    "retry after",
    "quota exceeded",
    "api limit",
    "request limit"
]

TIMING_PROFILES = {
    "aggressive": {"delay": 0.1, "threads": 50, "timeout": 5},
    "normal": {"delay": 0.5, "threads": 20, "timeout": 10},
    "conservative": {"delay": 1.0, "threads": 10, "timeout": 15},
    "stealth": {"delay": 2.0, "threads": 5, "timeout": 30}
}
