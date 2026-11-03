import cv2

image = cv2.imread("evidence/roi_coordinate_grid.jpg")
if image is None:
    raise FileNotFoundError("ROI image not found.")

H, W = image.shape[:2]
display_w, display_h = 1200, 675

preview = cv2.resize(image, (display_w, display_h))
original_preview = preview.copy()

start = None
end = None
drawing = False
rectangles = []

def mouse_callback(event, x, y, flags, param):
    global start, end, drawing, preview

    if event == cv2.EVENT_LBUTTONDOWN:
        start = (x, y)
        end = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        end = (x, y)
        preview = original_preview.copy()
        for a, b in rectangles:
            cv2.rectangle(preview, a, b, (0, 255, 0), 2)
        cv2.rectangle(preview, start, end, (0, 0, 255), 2)
        cv2.imshow("ROI Selector", preview)

    elif event == cv2.EVENT_LBUTTONUP and drawing:
        end = (x, y)
        drawing = False

        x1, x2 = sorted([start[0], end[0]])
        y1, y2 = sorted([start[1], end[1]])

        if x2 - x1 < 5 or y2 - y1 < 5:
            print("Rectangle too small. Try again.")
            return

        rectangles.append(((x1, y1), (x2, y2)))

        preview = original_preview.copy()
        for a, b in rectangles:
            cv2.rectangle(preview, a, b, (0, 255, 0), 2)
        cv2.imshow("ROI Selector", preview)

        scale_x = W / display_w
        scale_y = H / display_h

        print("Original image coordinates:",
              (round(x1 * scale_x), round(y1 * scale_y)),
              (round(x2 * scale_x), round(y2 * scale_y)))

cv2.namedWindow("ROI Selector")
cv2.setMouseCallback("ROI Selector", mouse_callback)

print("Drag around each traffic region.")
print("U = undo, R = reset, Q = finish.")

cv2.imshow("ROI Selector", preview)

while True:
    key = cv2.waitKey(1) & 0xFF

    if key == ord("u") and rectangles:
        rectangles.pop()
        preview = original_preview.copy()
        for a, b in rectangles:
            cv2.rectangle(preview, a, b, (0, 255, 0), 2)
        cv2.imshow("ROI Selector", preview)

    elif key == ord("r"):
        rectangles.clear()
        preview = original_preview.copy()
        cv2.imshow("ROI Selector", preview)

    elif key == ord("q"):
        break

cv2.destroyAllWindows()
print("Total regions selected:", len(rectangles))
