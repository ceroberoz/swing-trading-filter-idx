import random
import time
from functools import wraps
from . import config


class CircuitBreakerOpen(Exception):
    pass


class RateLimiter:
    def __init__(self):
        self.last_request_time = 0
        self.consecutive_429 = 0

    def wait(self):
        if not config.ENABLE_RATE_LIMITER:
            return

        delay = random.uniform(config.REQUEST_DELAY_MIN, config.REQUEST_DELAY_MAX)
        time_since_last_request = time.time() - self.last_request_time

        if time_since_last_request < delay:
            sleep_time = delay - time_since_last_request
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def record_success(self):
        self.consecutive_429 = 0

    def record_429(self):
        self.consecutive_429 += 1
        if self.consecutive_429 >= config.MAX_CONSECUTIVE_429:
            print(f"Circuit breaker: {config.MAX_CONSECUTIVE_429} consecutive 429 errors. Stopping.")
            raise CircuitBreakerOpen(f"Too many 429 errors ({self.consecutive_429}). Wait and try again later.")


def retry_with_backoff(max_retries=None, backoff_base=None):
    max_retries = max_retries or config.MAX_RETRIES
    backoff_base = backoff_base or config.RETRY_BACKOFF_BASE

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    _rate_limiter.record_success()
                    return result
                except Exception as e:
                    last_exception = e
                    error_str = str(e)

                    if "429" in error_str or "Too Many Requests" in error_str:
                        _rate_limiter.record_429()

                    if attempt == max_retries:
                        raise last_exception

                    backoff_time = backoff_base ** attempt
                    print(f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}. Retrying in {backoff_time}s...")
                    time.sleep(backoff_time)

            if last_exception:
                raise last_exception
            raise Exception("Max retries reached with no exception captured")
        return wrapper
    return decorator


_rate_limiter = RateLimiter()


def get_rate_limiter():
    return _rate_limiter

