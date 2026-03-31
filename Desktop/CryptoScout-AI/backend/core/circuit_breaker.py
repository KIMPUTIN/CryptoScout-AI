
# backend/core/circuit_breaker.py

import time
import logging

logger = logging.getLogger(__name__)

CLOSED = "CLOSED"
OPEN = "OPEN"
HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_time=60):
        """
        Simple circuit breaker implementation.

        States:
        - CLOSED: normal operation
        - OPEN: all calls blocked until recovery_time
        - HALF_OPEN: allow a single trial call

        failure_threshold: number of consecutive failures before opening circuit
        recovery_time: seconds before retry allowed
        """
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time

        self.failure_count = 0
        self.last_failure_time = None
        self.state = CLOSED

    def can_execute(self):
        """
        Returns True if a request is allowed, False if circuit is open.
        """
        if self.state == OPEN:
            if self.last_failure_time and (time.time() - self.last_failure_time > self.recovery_time):
                self.state = HALF_OPEN
                logger.info("Circuit breaker HALF_OPEN")
                return True
            return False
        return True

    def record_success(self):
        """
        Call this when a request succeeds.
        Resets failure count and closes the circuit.
        """
        self.failure_count = 0
        if self.state != CLOSED:
            logger.info("Circuit breaker CLOSED")
        self.state = CLOSED

    def record_failure(self):
        """
        Call this when a request fails.
        Opens the circuit if threshold is exceeded.
        """
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            if self.state != OPEN:
                logger.warning("Circuit breaker OPEN")
            self.state = OPEN


    def snapshot(self):
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "last_failure_time": self.last_failure_time,
            "recovery_time": self.recovery_time
        }


# global circuit breaker instance
ai_circuit_breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_time=60
)