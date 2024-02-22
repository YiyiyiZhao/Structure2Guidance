import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

video_path = "rtmp://158.132.255.91/live/stream_key"
# video_path = "E:/StudyAI/姚顺雨-从语言模型到语言智能体FromLanguageModelstoLanguageAgents-S hunyuYao-BV1ju4y1e7Em-h2Ni1LPYQXW2y9P1.mp4"
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
