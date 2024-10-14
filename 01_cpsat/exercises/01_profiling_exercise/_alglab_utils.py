"""
This file contains utils for checking the correctness of the solutions.
Do not modify this file!

Author: Dominik Krupke
Version: 2024-06-18
Changelog:
    - 2024-06-18: Only checking argv for >=2 and taking last argument for specific test execution. This way it can be used directly with scalene.
"""

import inspect
import os
import subprocess
import sys
import time
import typing

from tqdm import tqdm  # pip install tqdm

# A dictionary with all tests that should be run.
_check_list = {}


class _TestCase:
    def __init__(self, func, max_runtime_s):
        self.func_name = func.__name__
        self.func = func
        # extract full path of function file
        self.func_file = os.path.abspath(inspect.getfile(func))

        self.max_runtime_s = max_runtime_s

    def run(self):
        """
        Direct call of the test case.
        """
        self.func()

    def _on_timeout(self, proc):
        proc.kill()
        outs, errs = proc.communicate()
        # decode output
        outs = outs.decode("utf-8")
        errs = errs.decode("utf-8")
        # print output
        print(outs)
        print(errs)
        print(f"Test '{self.func_name}' timed out after {self.max_runtime_s} seconds.")

    def _on_error(self, outs, errs):
        # decode output
        outs = outs.decode("utf-8")
        errs = errs.decode("utf-8")
        # print output
        print(outs)
        print(errs)
        print(f"Test '{self.func_name}' failed.")

    def _create_subprocess(self):
        cmd = [
            sys.executable,
            os.path.abspath(__file__),
            self.func_file,
            self.func_name,
        ]
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def run_in_subprocess(self):
        """
        Run in subprocess with time limit. Return True if the function
        terminates without error in time. Capture the output of the
        function and print it in case of an error.
        """
        print(f"Running test '{self.func_name}'...")
        assert os.path.exists(self.func_file)
        # create subprocess
        proc = self._create_subprocess()
        # wait for process to terminate
        try:
            outs, errs = proc.communicate(timeout=self.max_runtime_s)
        except subprocess.TimeoutExpired:
            self._on_timeout(proc)
            return False
        # check if there was an error
        if proc.returncode != 0:
            self._on_error(outs, errs)
            return False
        return True


def FAIL(msg):
    """
    Print a message and exit.
    """
    print(f"Check failed: {msg}")
    exit(1)


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
        # the should only be one function with this name
        assert func_name not in _check_list
        _check_list[func_name] = _TestCase(func, max_runtime_s)
        return func
        # return _TestCase(func, max_runtime_s)

    return decorator


def _run_with_runtime_measurement(func_name) -> typing.Tuple[bool, float]:
    start_time = time.time()
    succ = _check_list[func_name].run_in_subprocess()
    end_time = time.time()
    execution_time = end_time - start_time
    return succ, execution_time


def run_all_checks():
    """
    Run all checks in subprocesses with a timeout.
    """
    print("Running all checks...")
    for func_name in tqdm(_check_list, desc="Progress"):
        succ, exc_time = _run_with_runtime_measurement(func_name)
        while not succ:
            print("========================================")
            print(
                "Please fix the error and press enter to try again. Press Ctrl+C to abort."
            )
            input()
            succ, exc_time = _run_with_runtime_measurement(func_name)
        print(f"Test '{func_name}' passed in {exc_time:.1f}s.")
    print("All checks passed.")


def main():
    """
    This function is the entry point for running tests.
    If a single test name is provided as a command line argument, only that test will be run.
    Otherwise, all available tests will be run.
    """
    if len(sys.argv) >= 2:
        func_name = sys.argv[-1]
        if func_name not in _check_list:
            print(f"Test '{func_name}' not found.")
            print("Available tests:")
            for func_name in _check_list:
                print(f"  {func_name}")
            exit(1)
        else:
            _check_list[func_name].run()
    else:
        print_how_to_test_individually()
        run_all_checks()


def print_how_to_test_individually():
    print("-" * 80)
    print("You can run a single test by passing the name of the test as an argument.")
    print("Use this to debug a single test. It will also show the output of the test.")
    print("Available tests:")
    for func_name in _check_list:
        print(f"  {func_name}")
    print("-" * 80)


if __name__ == "__main__":
    # run the function specified by the second command line argument
    # this is the entry point for running tests in a subprocess
    path_to_py = sys.argv[1]  # path to python file with function
    func_name = sys.argv[2]  # name of function to run
    glob = dict(globals())  # copy globals
    # set __name__ to None such that the file is not executed
    glob["__name__"] = None
    # if the function imports other files, they must be in the path
    sys.path.append(os.path.dirname(path_to_py))
    # read file and append function call
    exc_file = f"{open(path_to_py).read()}\n{func_name}()"
    # execute the modified file
    exec(exc_file, glob)
