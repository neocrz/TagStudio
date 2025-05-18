# Copyright (C) 2024 Travis Abendshien (CyanVoxel).
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio


from collections.abc import Callable

import sys

from PySide6.QtCore import QObject, Signal


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
        try:
            # Call the function to get the generator object
            generator = self.generator_function()
            # Iterate over the generator, emitting yielded values
            for yield_value in generator:
                self.value.emit(yield_value)
        except StopIteration as e:
            # This exception is raised when the generator finishes.
            # The return value of the generator function is in e.value (Python 3.3+)
            result = e.value
        except Exception as e:
            result = None # Or handle error result differently
        finally:
            # Emit the final result when the generator is exhausted (or an error occurred)
            self.finished_with_result.emit(result)
            # The CustomRunnable's 'done' signal will be emitted *after* this method finishes.
