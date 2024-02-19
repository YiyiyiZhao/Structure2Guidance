import os
#os.chdir('./camera_input')

from utils.file_pro import *
import pdb
#print(os.getcwd())
mark="banana_grap"
data_dir= '../camera_input/data'
jf_list=get_json_files(data_dir)
mark_json_file=get_mark_json_file(mark, jf_list)
data=load_json_file(mark_json_file)
img_dir=get_img_dir(mark, data_dir)

index=0
item=data[index]
frame_number=item['frame_number']
cls=item['cls']
boxxywh=item['boxxywh']
boxxyxy=item['boxxyxy']
x1,y1,x2,y2=boxxyxy[0]

img = cv2.imread(os.path.join(img_dir, f'img_{frame_number}.png'))

# First line will provide resizing ability to the window

cls_dict = load_cls_dict()
cls_dict_img={}
for idx, c in enumerate(cls):
    cls_dict_img[idx]=cls_dict[str(int(c))]

for idx, elm in enumerate(boxxyxy):
    print(idx)
    x1,y1,x2,y2=elm
    ((int(x1), int(y1)), (int(x2), int(y2)))
    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    img_text = cv2.putText(img, cls_dict_img[idx], (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

pdb.set_trace()

# cv2.namedWindow('Image', cv2.WINDOW_AUTOSIZE)
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#the image's shape is (720, 1280, 3)
#for each object, its coresponding upperleft (x1, y1) and the bottomright (x2,y2) 坐标 can be expressed in the following list of dictionary
#[{"idx":,  “object”:, "(x1, y1), (x2,y2)" }]



