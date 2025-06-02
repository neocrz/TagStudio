# Copyright (C) 2024 Travis Abendshien (CyanVoxel).
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio


from collections.abc import Callable

import sys
import structlog

from PySide6.QtCore import QObject, Signal

logger = structlog.get_logger(__name__)

class FunctionIterator(QObject):
    """Iterate over a yielding function and emit progress as the 'value' signal."""

    value = Signal(object)
    # Add this new signal to emit the final result of the function
    finished_with_result = Signal(object)

    def __init__(self, function: Callable):
        super().__init__()
        # Store the generator function itself
        self.generator_function = function

    def run(self):
        result = None
        generator = None # Initialize generator
        try:
            # Call the function to get the generator object
            generator = self.generator_function()
            # Iterate over the generator using next() to capture the final return value
            while True: # Loop indefinitely until StopIteration
                try:
                    yield_value = next(generator) # Get the next yielded value
                    self.value.emit(yield_value)   # Emit the yielded value
                except StopIteration as e:
                    result = e.value # Capture the return value from StopIteration (Python 3.3+)
                    break          # Exit the loop
        except Exception as e:
            logger.error("Exception during generator execution", error=e)
            # Decide how to handle error result - perhaps return None, or emit error signal
            # For now, keeping it None as in the original traceback case.
            result = None
        finally:
            # Emit the captured result when the generator is exhausted (or an exception occurred)
            self.finished_with_result.emit(result)
            # The CustomRunnable's 'done' signal will be emitted *after* this method finishes.
