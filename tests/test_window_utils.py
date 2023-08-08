import os
import signal
import subprocess
import time

import keyboard
import pytest
import win32gui

from window_utils import *

pids = []


def setup_module():
    global pids
    pids = [
        subprocess.Popen(["notepad"]).pid,
        subprocess.Popen(["mspaint"]).pid,
    ]
    time.sleep(2)


def teardown_module():
    global pids
    for pid in pids:
        os.kill(pid, signal.SIGTERM)


@pytest.fixture(autouse=True)
def notepad():
    hwnd = win32gui.FindWindow("Notepad", "Untitled - Notepad")
    return Window(hwnd)


@pytest.fixture(autouse=True)
def paint():
    hwnd = win32gui.FindWindow("MSPaintApp", "Untitled - Paint")
    return Window(hwnd)


def test_move(notepad: Window, paint: Window):
    notepad.move(0, 0, 400, 400)
    paint.move(200, 200, 400, 400)


def test_flash(notepad: Window, paint: Window):
    notepad.flash()
    time.sleep(2)


def test_activate(notepad: Window, paint: Window):
    notepad.activate()
    assert notepad.hwnd == win32gui.GetForegroundWindow()
    paint.activate()
    assert paint.hwnd == win32gui.GetForegroundWindow()


def test_is_active(notepad: Window, paint: Window):
    notepad.activate()
    assert notepad.is_active()
    assert not paint.is_active()
    paint.activate()
    assert paint.is_active()
    assert not notepad.is_active()


def test_get_rect(notepad: Window, paint: Window):
    x, y, w, h = (-7, 3, 163, 142)
    rect = (x, y, x + w, y + h)
    notepad.move(x, y, w, h)
    assert notepad.get_rect() == rect


def test_get_bbox(notepad: Window, paint: Window):
    x, y, w, h = (-7, 3, 163, 142)
    bbox = (x, y, w, h)
    notepad.move(x, y, w, h)
    assert notepad.get_bbox() == bbox


def test_get_size(notepad: Window, paint: Window):
    x, y, w, h = (-7, 3, 163, 142)
    size = (w, h)
    notepad.move(x, y, w, h)
    assert notepad.get_size() == size


def test_activate_momentarily(notepad: Window, paint: Window):
    paint.activate()
    assert paint.is_active()
    with notepad.activate_momentarily():
        keyboard.write("Hello World!")
        assert notepad.is_active()
    assert paint.is_active()


def test_get_foreground_window(notepad: Window, paint: Window):
    notepad.activate()
    assert get_foreground_window().hwnd == notepad.hwnd
    paint.activate()
    assert get_foreground_window().hwnd == paint.hwnd


def test_find_window(notepad: Window, paint: Window):
    pass


def test_find_window_noclass(notepad: Window, paint: Window):
    expected = notepad.hwnd
    actual = find_window(None, "Untitled - Notepad").hwnd
    assert actual == expected


def test_find_window_notitle(notepad: Window, paint: Window):
    pass
