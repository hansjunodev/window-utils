Lightweight tool for handling window focus and more. Only for Windows.

```python
# Find an open Window.
window = find_window(None, "Untitled - Notepad")

# Activate the window.
window.activate()

# Move the window to coordinates (13, 13) and resize it to 600px x 400px.
window.move(13, 13, 600, 400)

# Get the window's bounding box in the form of (x, y, width, height).
window.get_bbox()

# Get whether or not the window has focus.
window.is_active()

# Activate the window, do something, then give focus back to the original window.
with window.activate_momentarily():
    # Do something here
```
