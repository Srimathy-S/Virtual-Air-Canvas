import mediapipe as mp
import cv2
import numpy as np
import time

# Constants
ml = 150
max_x, max_y = 250 + ml, 50
curr_tool = "select tool"
time_init = True
rad = 40
var_inits = False
thick = 4
prevx, prevy = 0, 0
save_time = 0

# Default drawing color
draw_color = (0, 0, 0)  # Black

# Color palette buttons (x1, y1, x2, y2, BGR color)
color_buttons = [
    (10, 60, 40, 90, (0, 0, 255)),   # Red
    (10, 95, 40, 125, (0, 255, 0)),  # Green
    (10, 130, 40, 160, (255, 0, 0)), # Blue
    (10, 165, 40, 195, (0, 0, 0))    # Black
]

# Get selected tool
def getTool(x):
    if x < 50 + ml:
        return "line"
    elif x < 100 + ml:
        return "rectangle"
    elif x < 150 + ml:
        return "draw"
    elif x < 200 + ml:
        return "circle"
    else:
        return "erase"

def index_raised(yi, y9):
    return (y9 - yi) > 40

hands = mp.solutions.hands
hand_landmark = hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)
draw = mp.solutions.drawing_utils

tools = cv2.imread("tools.png")
tools = tools.astype('uint8')

mask = np.ones((480, 640)) * 255
mask = mask.astype('uint8')

cap = cv2.VideoCapture(0)

while True:
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
    op = hand_landmark.process(rgb)

    if op.multi_hand_landmarks:
        for i in op.multi_hand_landmarks:
            draw.draw_landmarks(frm, i, hands.HAND_CONNECTIONS)
            x, y = int(i.landmark[8].x * 640), int(i.landmark[8].y * 480)

            # Tool selection
            if x < max_x and y < max_y and x > ml:
                if time_init:
                    ctime = time.time()
                    time_init = False
                ptime = time.time()
                cv2.circle(frm, (x, y), rad, (0, 255, 255), 2)
                rad -= 1
                if (ptime - ctime) > 0.8:
                    curr_tool = getTool(x)
                    print("Tool set to:", curr_tool)
                    time_init = True
                    rad = 40
            else:
                time_init = True
                rad = 40

            # Color selection logic
            for (x1, y1, x2, y2, color) in color_buttons:
                if x1 < x < x2 and y1 < y < y2:
                    draw_color = color

            xi, yi = int(i.landmark[12].x * 640), int(i.landmark[12].y * 480)
            y9 = int(i.landmark[9].y * 480)

            if curr_tool == "draw":
                if index_raised(yi, y9):
                    cv2.line(mask, (prevx, prevy), (x, y), draw_color[0], thick)
                    prevx, prevy = x, y
                else:
                    prevx, prevy = x, y

            elif curr_tool == "line":
                if index_raised(yi, y9):
                    if not var_inits:
                        xii, yii = x, y
                        var_inits = True
                    cv2.line(frm, (xii, yii), (x, y), draw_color, thick)
                else:
                    if var_inits:
                        cv2.line(mask, (xii, yii), (x, y), draw_color[0], thick)
                        var_inits = False

            elif curr_tool == "rectangle":
                if index_raised(yi, y9):
                    if not var_inits:
                        xii, yii = x, y
                        var_inits = True
                    cv2.rectangle(frm, (xii, yii), (x, y), draw_color, thick)
                else:
                    if var_inits:
                        cv2.rectangle(mask, (xii, yii), (x, y), draw_color[0], thick)
                        var_inits = False

            elif curr_tool == "circle":
                if index_raised(yi, y9):
                    if not var_inits:
                        xii, yii = x, y
                        var_inits = True
                    radius = int(((xii - x) ** 2 + (yii - y) ** 2) ** 0.5)
                    cv2.circle(frm, (xii, yii), radius, draw_color, thick)
                else:
                    if var_inits:
                        radius = int(((xii - x) ** 2 + (yii - y) ** 2) ** 0.5)
                        cv2.circle(mask, (xii, yii), radius, draw_color[0], thick)
                        var_inits = False

            elif curr_tool == "erase":
                if index_raised(yi, y9):
                    cv2.circle(frm, (x, y), 30, (0, 0, 0), -1)
                    cv2.circle(mask, (x, y), 30, 255, -1)

    op = cv2.bitwise_and(frm, frm, mask=mask)
    frm[:, :, 1] = op[:, :, 1]
    frm[:, :, 2] = op[:, :, 2]
    frm[:max_y, ml:max_x] = cv2.addWeighted(tools, 0.7, frm[:max_y, ml:max_x], 0.3, 0)

    # Draw vertical color palette on the left
    for (x1, y1, x2, y2, color) in color_buttons:
        cv2.rectangle(frm, (x1, y1), (x2, y2), color, -1)
        cv2.rectangle(frm, (x1, y1), (x2, y2), (255, 255, 255), 1)

    # Show tool name
    cv2.putText(frm, curr_tool, (270 + ml, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show saved message
    if time.time() - save_time < 2:
        cv2.putText(frm, "Saved!", (480, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 3)

    cv2.imshow("Virtual Canvas", frm)

    key = cv2.waitKey(1)

    if key == ord('s'):
        filename = f"drawing_{int(time.time())}.png"
        cv2.imwrite(filename, 255 - mask)
        print(f"[INFO] Drawing saved as {filename}")
        save_time = time.time()

    if key == 27:
        cv2.destroyAllWindows()
        cap.release()
        break