from utils.file_pro import *
mark="banana_grap"
data_dir='./data'
jf_list=get_json_files(data_dir)
mark_json_file=get_mark_json_file(mark, jf_list)
data=load_json_file(mark_json_file)
img_dir=get_img_dir(mark, data_dir)



for index in range(len(data)):
    obj_list,img=get_obj_list(img_dir, data, index)
    show_img(img, obj_list)
    print(obj_list)
    print('********************************')