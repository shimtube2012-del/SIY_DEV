"""Gemini Free Tier 친화 호출 유틸 — 분당 5회 제한 준수 + 429/503 재시도."""
import re
import time

# Free tier: 5 RPM per model. 안전 마진으로 13초 간격.
MIN_INTERVAL_SEC = 13.0
MAX_RETRIES = 5
BASE_BACKOFF = 15.0

_last_call_ts = 0.0


def _parse_retry_delay(err_msg: str) -> float:
    """에러 메시지에서 retryDelay 힌트 추출. 없으면 0."""
    m = re.search(r"'retryDelay': '(\d+(?:\.\d+)?)s'", err_msg)
    if m:
        return float(m.group(1))
    m = re.search(r"Please retry in ([\d.]+)s", err_msg)
    if m:
        return float(m.group(1))
    return 0.0


def _is_transient(err: Exception) -> bool:
    s = str(err)
    return any(x in s for x in ("429", "503", "UNAVAILABLE", "RESOURCE_EXHAUSTED"))


def throttle():
    """마지막 호출로부터 MIN_INTERVAL_SEC가 지나지 않았으면 대기."""
    global _last_call_ts
    now = time.time()
    elapsed = now - _last_call_ts
    if elapsed < MIN_INTERVAL_SEC:
        time.sleep(MIN_INTERVAL_SEC - elapsed)
    _last_call_ts = time.time()


def call_with_retry(fn, *args, **kwargs):
    """Gemini 호출을 페이싱+재시도로 감싼다.

    - 호출 전 throttle()로 최소 간격 유지
    - 429/503/UNAVAILABLE/RESOURCE_EXHAUSTED 발생 시 backoff 후 재시도
    """
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        throttle()
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            last_err = e
            if not _is_transient(e):
                raise
            hint = _parse_retry_delay(str(e))
            wait = max(hint, BASE_BACKOFF * attempt)
            print(f"    [retry {attempt}/{MAX_RETRIES}] transient error, wait {wait:.1f}s")
            time.sleep(wait)
    raise last_err
