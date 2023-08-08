import time
from contextlib import contextmanager

import win32com.client
import win32con
import win32gui


class Window:
    def __init__(self, hwnd) -> None:
        self._hwnd = hwnd

    @property
    def hwnd(self) -> int:
        return self._hwnd

    def is_active(self) -> bool:
        return self._hwnd == win32gui.GetForegroundWindow()

    def get_rect(self) -> tuple[int, int, int, int]:
        return win32gui.GetWindowRect(self._hwnd)

    def get_bbox(self) -> tuple[int, int, int, int]:
        left, top, right, bottom = win32gui.GetWindowRect(self._hwnd)
        return (left, top, right - left, bottom - top)

    def get_size(self) -> tuple[int, int]:
        left, top, right, bottom = win32gui.GetWindowRect(self._hwnd)
        return (right - left, bottom - top)

    def flash(self) -> None:
        flags = win32con.FLASHW_ALL | win32con.FLASHW_TIMERNOFG
        count = 0
        rate = 0
        win32gui.FlashWindowEx(self._hwnd, flags, count, rate)

    @contextmanager
    def activate_momentarily(self, *args, **kwargs) -> None:
        prev_window = get_foreground_window()

        if prev_window.hwnd == self.hwnd:
            yield
        else:
            try:
                # Activate the window.
                self.activate(*args, **kwargs)
                yield
            finally:
                # Return control to the original window.
                prev_window.activate(*args, **kwargs)

    def activate(self, force=True, *, ignore_errors=True, wait=True) -> bool:
        try:
            if force:
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys("%")
            win32gui.SetForegroundWindow(self._hwnd)
            if wait:
                while not self.is_active():
                    time.sleep(0.001)
        except win32gui.error:
            if ignore_errors:
                return False
            else:
                raise
        else:
            return True

    def move(self, x, y, width, height, repaint=True) -> bool:
        # TODO if width, height are none leave the window the same size
        try:
            win32gui.MoveWindow(self._hwnd, x, y, width, height, repaint)
        except Exception as e:
            raise


def get_foreground_window() -> Window:
    return Window(win32gui.GetForegroundWindow())


def find_window(_class_name, _window_title) -> Window:
    hwnd = win32gui.FindWindow(_class_name, _window_title)
    return Window(hwnd)
