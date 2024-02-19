import os
import json
from typing import Union
import cv2
import tkinter as tk
def get_json_files(data_dir: str) -> list:
    json_file_list=[]
    for root, dirs, files in os.walk(data_dir):
        for f in files:
            if '.json' in f:
                json_file_list.append(os.path.join(root, f))
    return json_file_list

def get_mark_json_file(mark:str, json_file_list:list) -> Union[str, None]:
    for elm in json_file_list:
        if mark in elm:
            return elm
    return None

def load_json_file(json_file:str) -> list:
    with open(json_file, 'r') as f:
        data=json.load(f)
    return data


def get_img_dir(mark:str, data_dir:str)->Union[str,None]:
    for root, dirs, files in os.walk(data_dir):
        for d in dirs:
            if mark in d:
                print(d)
                return os.path.join(root, d)
    return None


def load_cls_dict(cls_json: str = './resources/categories.json'):
    with open(cls_json, 'r') as f:
        cls_dict=json.load(f)
    return cls_dict

def get_obj_list(img_dir, data, index):
    item=data[index]
    frame_number=item['frame_number']
    cls=item['cls']
    boxxyxy=item['boxxyxy']

    img = cv2.imread(os.path.join(img_dir, f'img_{frame_number}.png'))

    cls_dict = load_cls_dict()
    cls_dict_img={}
    for idx, c in enumerate(cls):
        cls_dict_img[idx]=cls_dict[str(int(c))]

    obj_list=[]
    for idx, elm in enumerate(boxxyxy):
        obj = {}
        x1,y1,x2,y2=elm
        coord=((int(x1), int(y1)), (int(x2), int(y2)))
        obj['idx']=idx
        obj['object']=cls_dict_img[idx]
        obj['coordinate']=coord
        obj_list.append(obj)

    return obj_list, img


def show_img(img, obj_list):
    if img is not None:
        # Display the image
        cv2.imshow(f'{obj_list}', img)
        # Wait for a key press and close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error: Unable to load image.")
    return obj_list




def display_string(text_show):
    # Create a new window
    root = tk.Tk()

    # Function to destroy the root window when clicked
    def destroy_root():
        root.destroy()

    # Create a label with the specified text and large font
    label = tk.Label(root, text=text_show, font=("Helvetica", 18))
    label.pack()

    # Bind left mouse click to destroy_root function
    label.bind("<Button-1>", lambda e: destroy_root())

    # Run the main event loop to display the window
    root.mainloop()


