import cv2
import pyrealsense2 as rs
import numpy as np
import time
import pdb
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

#打开 RealSense 摄像头
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 10)

pipeline.start(config)
def get_obj_list_from_cv(cv_results):
    # Processing frame_data
    cls_dict = cv_results[0].names

    cls = cv_results[0].boxes.cls.cpu().numpy()
    cls_dict_img = {}
    for idx, c in enumerate(cls):
        cls_dict_img[idx] = cls_dict[int(c)]

    boxxyxy = cv_results[0].boxes.xyxy.cpu().numpy()
    obj_list = []
    for idx, elm in enumerate(boxxyxy):
        obj = {}
        x1, y1, x2, y2 = elm
        coord = ((int(x1), int(y1)), (int(x2), int(y2)))
        obj['idx'] = idx
        obj['object'] = cls_dict_img[idx]
        obj['coordinate'] = coord
        obj_list.append(obj)

    annotated_frame = cv_results[0].plot()
    # show img annotation
    cv2.imshow("YOLOv8 Inference", annotated_frame)
    cv2.waitKey(1)
    time.sleep(3)  # 等待3秒钟
    cv2.destroyWindow("YOLOv8 Inference")  # 销毁 YOLOv8 Inference 窗口

    return obj_list

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
            obj_list=get_obj_list_from_cv(results)
            prin10(obj_list)


            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

except KeyboardInterrupt:
    pass
finally:
    pipeline.stop()