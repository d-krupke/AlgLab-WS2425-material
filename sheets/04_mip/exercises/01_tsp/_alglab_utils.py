"""
This file contains utilities for checking the correctness of the solutions.
Do not modify this file!

Author: Dominik Krupke
Version: 2023-11-29

Changes:
2023-10-23: Fixed some code smells
2023-11-29: Changed to logging and printing everything by default, as too many students are too lazy to read the instructions.
"""

import inspect
import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import Tuple

from tqdm import tqdm  # pip install tqdm

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s|%(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# Prevent double logging from gurobi
logging.getLogger("gurobipy").setLevel(logging.ERROR)
DEBUG_MODE = False

# A dictionary with all tests that should be run.
_check_list = {}


class _TestCase:
    def __init__(self, func, max_runtime_s):
        self.func_name = func.__name__
        self.func = func
        # Extract full path of function file
        self.func_file = Path(inspect.getfile(func)).resolve()
        self.max_runtime_s = max_runtime_s

    def run(self):
        """
        Direct call of the test case.
        """
        self.func()

    def _create_subprocess(self):
        cmd = [
            sys.executable,
            str(Path(__file__).resolve()),
            str(self.func_file),
            self.func_name,
        ]
        if DEBUG_MODE:
            cmd.append("--debug")
        return subprocess.Popen(cmd)

    def run_in_subprocess(self):
        """
        Run in subprocess with time limit. Return True if the function
        terminates without error in time. Capture the output of the
        function and print it in case of an error.
        """
        logging.info(
            f"Running test '{self.func_name}' with time limit of {self.max_runtime_s}s ..."
        )
        assert self.func_file.exists()
        # Create subprocess
        proc = self._create_subprocess()
        try:
            stdout, _ = proc.communicate(timeout=self.max_runtime_s)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, _ = proc.communicate()
            logging.error(
                f"Test '{self.func_name}' timed out after {self.max_runtime_s} seconds."
            )
            logging.error(stdout.decode("utf-8", errors="ignore"))
            return False
        # Check if there was an error
        if proc.returncode != 0:
            logging.error(f"Test '{self.func_name}' failed.")
            logging.error(stdout.decode("utf-8", errors="ignore"))
            return False
        return True


def FAIL(msg):
    """
    Print a message and exit.
    """
    logging.error(f"Check failed: {msg}")
    sys.exit(1)


def CHECK(condition, msg):
    """
    Check a condition and print a message if it is not met.
    """
    if not condition:
        FAIL(msg)


def mandatory_testcase(max_runtime_s=900):
    """
    Decorator for marking a function as mandatory for the correctness check.
    """

    def decorator(func):
        func_name = func.__name__
        if func_name in _check_list:
            msg = f"Test case '{func_name}' is already registered."
            raise ValueError(msg)
        _check_list[func_name] = _TestCase(func, max_runtime_s)
        return func

    return decorator


def _run_with_runtime_measurement(func_name) -> Tuple[bool, float]:
    start_time = time.time()
    succ = _check_list[func_name].run_in_subprocess()
    end_time = time.time()
    execution_time = end_time - start_time
    return succ, execution_time


def run_all_checks():
    """
    Run all checks in subprocesses with a timeout.
    """
    logging.info("Running all checks...")
    history = []
    for func_name in tqdm(_check_list, desc="Progress"):
        succ, exc_time = _run_with_runtime_measurement(func_name)
        if succ:
            logging.info(f"Test '{func_name}' passed in {exc_time:.1f}s.")
            history.append((func_name, True, exc_time))
        else:
            logging.error("========================================")
            logging.error("Test failed. Please fix the error and try again.")
            sys.exit(1)
    logging.info("========================================")
    logging.info("All checks passed.")
    for func_name, succ, exc_time in history:
        logging.info(f"\tTest '{func_name}' passed in {exc_time:.1f}s.")


def print_how_to_test_individually():
    logging.info("-" * 80)
    logging.info(
        "You can run a single test by passing the name of the test as an argument."
    )
    logging.info(
        "Use this to debug a single test. It will also show the output of the test."
    )
    logging.info("Available tests:")
    for func_name in _check_list:
        logging.info(f"  {func_name}")
    logging.info("-" * 80)


def main():
    """
    Entry point for running tests.
    If a test name is provided as a command line argument, only that test will be run.
    Otherwise, all available tests will be run.
    """
    global DEBUG_MODE
    # Check if '--debug' flag is passed
    if "--debug" in sys.argv:
        logging.getLogger().setLevel(logging.DEBUG)
        sys.argv.remove("--debug")
        DEBUG_MODE = True
        logging.debug("Debug mode enabled.")
    else:
        logging.info("You can enable debug mode by passing the '--debug' flag.")

    if len(sys.argv) == 2:
        func_name = sys.argv[1]
        if func_name not in _check_list:
            logging.error(f"Test '{func_name}' not found.")
            logging.error("Available tests:")
            for name in _check_list:
                logging.error(f"  {name}")
            sys.exit(1)
        else:
            # Run the specified test in a subprocess
            succ, exc_time = _run_with_runtime_measurement(func_name)
            if succ:
                logging.info(f"Test '{func_name}' passed in {exc_time:.1f}s.")
            else:
                logging.error(f"Test '{func_name}' failed.")
                sys.exit(1)
    else:
        print_how_to_test_individually()
        run_all_checks()
    print_footer()


def print_footer():
    footer_text = """
========================================================
Use logging to print the progress of your implementation.

- Use `logging.info("Your message")` to print informational messages.
- Use `logging.debug("Your message")` for debug messages, which are shown only when debug mode is enabled (`--debug`).

To avoid unnecessary overhead, avoid building logging message strings unless necessary.
Instead of:

    logging.info(f"Value: {value}")

use:

    logging.info("Value: %s", value)

This ensures that string formatting is only performed if the message will be logged.

During development, you can run individual test cases by passing the test name as an argument.
For example:

    python verify_script.py test_name

Available tests:
"""
    test_cases = "\n".join([f"  {name}" for name in _check_list])
    footer_text += f"{test_cases}\n"
    footer_text += """
Enable debug mode by adding the `--debug` flag:

    python verify_script.py test_name --debug

========================================================
    """
    logging.info(footer_text)


if __name__ == "__main__":
    # Check if '--debug' flag is passed
    if "--debug" in sys.argv:
        logging.getLogger().setLevel(logging.DEBUG)
        sys.argv.remove("--debug")
        DEBUG_MODE = True
        logging.debug("Debug mode enabled.")

    # If there are at least 3 arguments, assume we are being called as a subprocess
    if len(sys.argv) >= 3:
        # Run the function specified by the arguments
        path_to_py = sys.argv[1]  # Path to Python file with function
        func_name = sys.argv[2]  # Name of function to run
        glob = dict(globals())  # Copy globals
        # Set __name__ to None such that the file is not executed
        glob["__name__"] = None
        # If the function imports other files, they must be in the path
        sys.path.append(str(Path(path_to_py).parent))
        # Read file and append function call
        with Path(path_to_py).open() as file:
            exc_file = f"{file.read()}\n{func_name}()"
        # Execute the modified file
        exec(exc_file, glob)
    else:
        # Otherwise, run the main function
        main()
