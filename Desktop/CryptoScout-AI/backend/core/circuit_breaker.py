
# backend/core/circuit_breaker.py

import time
import logging

logger = logging.getLogger(__name__)


class CircuitBreaker:

    def __init__(self, failure_threshold=5, recovery_time=60):
        """
        failure_threshold = number of failures before opening circuit
        recovery_time = seconds before retry allowed
        """

        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time

        self.failure_count = 0
        self.last_failure_time = None

        self.state = "CLOSED"


    def can_execute(self):

        if self.state == "OPEN":

            if time.time() - self.last_failure_time > self.recovery_time:
                self.state = "HALF_OPEN"
                logger.info("Circuit breaker HALF_OPEN")

                return True

            return False

        return True


    def record_success(self):

        self.failure_count = 0
        self.state = "CLOSED"


    def record_failure(self):

        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:

            self.state = "OPEN"

            logger.warning("Circuit breaker OPEN")


# global circuit breaker instance
ai_circuit_breaker = CircuitBreaker()