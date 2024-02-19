import cv2
import pyrealsense2 as rs
import numpy as np
import pickle
import time
import json
import os
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

#打开 RealSense 摄像头
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 10)

pipeline.start(config)

try:
    results_list=[]
    img_list=[]
    snap_count = 0
    while True:
        frames = pipeline.wait_for_frames(15000)
        # print(frames.frame_number)
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        if frames.frame_number % 6 == 0:
            frame_data = np.asanyarray(color_frame.get_data())
            results = model(frame_data)
            orig_img=results[0].orig_img
            #classdef = results[0].names
            cls = results[0].boxes.cls.cpu().tolist()
            boxxywh = results[0].boxes.xywh.cpu().tolist()
            boxxyxy = results[0].boxes.xyxy.cpu().tolist()
            annotated_frame = results[0].plot()
            cv2.imshow("YOLOv8 Inference", annotated_frame)
            #print (results)
            # with open('results.pcl', 'wb') as f:
            #     pickle.dump(results, f)

            # with open('ann.pcl', 'wb') as f:
            #     pickle.dump(annotated_frame, f)
            # test(color_frame)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break
            elif key  == ord("p"):
                snap_count += 1
                # Prepare data to be saved
                snap_data = {
                    'frame_number': frames.frame_number,
                    'cls': cls,
                    'boxxywh': boxxywh,
                    'boxxyxy': boxxyxy
                    #'original_image': orig_img,
                    #'annotated_frame': annotated_frame
                }

                # Append snap data to the list
                results_list.append(snap_data)
                img_list.append({'frame_number': frames.frame_number, 'img_array':orig_img})
            elif key == ord("s"):
                # Get the current timestamp
                current_time = time.strftime('%Y-%m-%d-%H:%M:%S')

                # Allow the user to input a prefix (optional)
                prefix = input("Enter a prefix indicating the object: ")

                # Generate the filename with timestamp and prefix
                filename = f'{prefix}_{snap_count}_{current_time}.json'

                # Save results_list to a JSON file
                collections_dir='/home/aicare/workspace/collections'
                os.makedirs(collections_dir, exist_ok=True)
                with open(os.path.join(collections_dir,filename), 'w') as json_file:
                    json.dump(results_list, json_file, indent=2)


                img_dir=f'{collections_dir}/{prefix}_{current_time}'
                os.makedirs(img_dir, exist_ok=True)
                for entry in img_list:
                    frame_number = entry['frame_number']
                    img_array = entry['img_array']
                    filename = f'img_{frame_number}.png'
                    cv2.imwrite(os.path.join(img_dir,filename), img_array)

                # Log the timestamp, prefix, and the length of results_list
                log_filename = os.path.join(collections_dir, 'log.txt')
                log_entry = f'{current_time} | Prefix: {prefix} | Length of results_list: {len(results_list)}\n'
                with open(log_filename, 'a') as log_file:
                    log_file.write(log_entry)


except KeyboardInterrupt:
    pass
finally:
    pipeline.stop()