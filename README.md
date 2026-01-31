# Mouse From Camera

This is a Python project that allows mouse control via hand gestures through the camera.

### Requirements
- Python 3.11
- OpenCV
- MediaPipe
- PyAutoGUI
- keyboard

### Installation
```bash
pip install opencv-python mediapipe pyautogui keyboard
```

### Settings

The project starts with **default settings**.

To change settings:
- **Ctrl + Shift + "** → Opens the settings panel (HTML)
- Make the changes in the browser and press the **Save** button
- To apply the downloaded `.json` file to the project:
- **Ctrl + Shift + R**

> ⚠️ The project must be **running** for the key combinations to work.

> 🔎 **Note:** When the project is run, it accesses the camera and controls your cursor according to your right hand. Using the compiled edition is recommended.

### Gestures and Usage
#### Left Click
- Palm should face the camera
- Fingers should be spread and hand open
- Move the **index finger** forward-down

#### Right Click
- Palm should face the camera
- Fingers should be spread and hand open
- Move the **middle finger** forward-down

#### Mouse Wheel (Scroll)
- Move your hand **sideways** to the camera Turn**
- Bring your fingers together
- The distance between the **tip of your thumb** and the **tip of your index finger** determines the scroll speed
> 💡 Tip: Keeping your hand steady during scrolling gives a smoother result.

### ⚠️ Things to Note ⚠️
> While the project is not yet perfect, there are some speed and lag issues.
> Errors such as detecting another object as a hand may occur.
> Detection and processing speed will vary depending on your camera's performance.
> It also performs poorly in dark environments.
> If project settings are changed via HTML, this process must be repeated every time the project is started.
> For fixed settings, change the variable values ​​in the project code.
> The **Esc** key terminates the project.
