import cv2

image = cv2.imread("data/raw/Sample_1.mp4")
video = cv2.VideoCapture("data/raw/Sample_1.mp4")
success, frame = video.read()
video.release()

if not success:
    raise RuntimeError("Could not read traffic video.")

regions = {
    "Region A": ((5, 334), (973, 1080)),
    "Region B": ((1003, 370), (1907, 1077))
}

for name, (p1, p2) in regions.items():
    cv2.rectangle(frame, p1, p2, (0, 255, 0), 3)
    cv2.putText(frame, name, (p1[0] + 5, max(30, p1[1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

output = "evidence/roi_verification.jpg"
cv2.imwrite(output, frame)
print("Saved:", output)
