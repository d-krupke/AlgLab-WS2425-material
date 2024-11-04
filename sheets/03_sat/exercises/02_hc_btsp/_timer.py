"""
In many situations we need to measure the time. This timer makes it easy.
"""

import time
import typing


class Timer:
    """
    A simple timer for measuring time.
    """

    def __init__(self, runtime: float = 0.0):
        self.runtime = runtime
        self.start = time.time()
        self.saved_times = []

    def remaining(self) -> float:
        """
        The remaining time.
        """
        return self.runtime - self.time()

    def time(self) -> float:
        """
        Time since the creation of the timer.
        """
        return time.time() - self.start

    def reset(self, runtime: typing.Optional[float] = None):
        """
        Reset the timer.

        Args:
            runtime (float, optional): The new runtime for the timer. If provided, the timer will be set to this runtime. Defaults to None.

        Returns:
            None
        """
        if runtime is not None:
            self.runtime = runtime
        self.start = time.time()
        self.saved_times = []

    def __bool__(self):
        """
        Returns true if there is still time remaining.
        """
        return not self.is_out_of_time()

    def is_out_of_time(self) -> bool:
        """
        Check if the timer has run out of time.

        Returns:
            bool: True if the timer has run out of time, False otherwise.
        """
        return self.remaining() < 0

    def lap(self, label):
        """
        Record a lap time with a label.

        Args:
            label (Any): The label associated with the lap time.

        Returns:
            None
        """
        self.saved_times.append((self.time(), label))

    def get_laps(self):
        """
        Get the list of saved lap times.

        Returns:
            List[Tuple[float, Any]]: A list of tuples containing the lap times and their associated labels.
        """
        return list(self.saved_times)

    def check(self):
        """
        Check if the timer has expired and throw an exception if it has.

        Raises:
            TimeoutError: If the timer has expired.
        """
        if not bool(self):
            raise TimeoutError()
