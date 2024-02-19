import cv2
import pyrealsense2 as rs
import numpy as np

from ultralytics import YOLO

model = YOLO('yolov8n.pt')

#打开 RealSense 摄像头
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 10)

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        # print(frames.frame_number)
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        if frames.frame_number % 6 == 0:
            frame_data = np.asanyarray(color_frame.get_data())
            
            results = model(frame_data)

            classdef = results[0].names
            print(classdef)

            cls = results[0].boxes.cls.cpu().numpy()
            print(cls)

            boxxy = results[0].boxes.xywh.cpu().numpy()
            print(boxxy)

            annotated_frame = results[0].plot()
            
            # test(color_frame)
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

except KeyboardInterrupt:
    pass
finally:
    pipeline.stop()