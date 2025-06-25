# Virtual-Air-Canvas
**Air Canvas** is an AI-powered virtual drawing tool that enables users to sketch on a digital canvas using only hand gestures. Built with MediaPipe and OpenCV, the application uses real-time computer vision to detect hand landmarks via webcam and map them to drawing actions like drawing, erasing, or selecting shapes — no mouse or touchscreen needed!

---

## 🚀 Features

- ✋ Hand gesture recognition using **MediaPipe**
- 🎨 Drawing tools: Line, Rectangle, Circle, Free Draw, Eraser
- 🎨 **Color Palette** selection (Red, Green, Blue, Black)
- 💾 Save canvas by pressing **‘s’** key
- 📷 Webcam-based virtual canvas – no external hardware needed
- ✅ Displays message when drawing is successfully saved


## 🛠️ Tech Stack

| Component       | Description                             |
|----------------|-----------------------------------------|
| Python          | Programming language                   |
| OpenCV          | Image processing and visualization     |
| MediaPipe       | Hand detection via AI/ML               |
| NumPy           | Array manipulation                     |

---

### 📦 Installation

There are some prerequisites that are needed to be done to be able to run this project. It's needed to install the required libraries by running the following commend in the project's directory:

```bash
pip install opencv-python mediapipe numpy
```
now you can run the project directly from your terminal:
```bash
python canvas.py
```
