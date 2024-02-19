import argparse
import json
import time

import cv2
import numpy as np
import openai
import pyrealsense2 as rs
from sentence_transformers import SentenceTransformer
from ultralytics import YOLO


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


def main(target_object):
    # Visual setting
    cv_model = YOLO('models/yolov8n.pt')

    # 打开 RealSense 摄像头
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 10)
    pipeline.start(config)

    # openai setting
    with open('./resources/api_key.txt', 'r') as f:
        openai.api_key = f.read()
    parameters = {'engine': 'gpt-3.5-turbo', 'max_tokens': 400, 'stop': None, }

    # similarity model
    sim_model = SentenceTransformer('./codes/models/bert-base-nli-mean-tokens')

    # load prompts
    with open('./resources/prompts.json', 'r') as f:
        prompts = json.load(f)
    prompt_sce_desc = prompts['sce_desc']
    prompt_guid_step = prompts['guid_step']
    prompt_sys_cont = prompts['sys_cont']
    prompt_comp_ref = prompts['comp_ref']
    embedding1 = sim_model.encode(prompt_comp_ref.format(target_object), convert_to_tensor=True)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            if frames.frame_number % 6 == 0:
                frame_data = np.asanyarray(color_frame.get_data())
                # print(frame_data)
                cv2.imshow("Current Frame", frame_data)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif cv2.waitKey(1) & 0xFF == ord("a"):
                    frame_data = np.asanyarray(color_frame.get_data())
                    cv_results = cv_model(frame_data)
                    obj_list = get_obj_list_from_cv(cv_results)

                    # form_question

                    # description response

                    # response_guidance


    except KeyboardInterrupt:
        pass
    finally:
        pipeline.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_object", help="Target object", type=str)
    args = parser.parse_args()
    main(args.target_object)
