import json
import openai
import time
from utils.file_pro import *
#openai setting
with open('./resources/api_key.txt', 'r') as f:
    openai.api_key = f.read()
parameters = {
    'engine': 'gpt-3.5-turbo',
    'max_tokens': 400,
    'stop': None,
}
enhance_prompt_temp="""
Task requirements: Given the object detection results of an image with dimensions (720, 1280, 3), your task is to generate MCQ questions with answers.

Input: You'll be provided with a list of dictionaries, each dictionary has three keys: 'idx' for the object index in the image, 'object' for the type of the specific object, noting that encountering the object 'person' often implies 'hand', and 'coordinate': a tuple in the form ((x1, y1), (x2, y2)), containing the upper-left (x1, y1) and bottom-right (x2, y2) coordinates of each object in the image. Remember, for an image, (x, y) = (0, 0) is the top left point, with the x-axis running horizontally along the rows and the y-axis running vertically along the columns.

Output Requirements:
1. Generate MCQ questions in the form, such as 'How should the hand move to obtain the apple? A. Left B. Right C. Up D. Down.'
2. For each input (in the form of a list of dictionaries), please generate 5 to 10 different questions with answers.
3. The output should be in the form of a list of dictionaries, [{"question index": 0, "question": 'How should the hand move to obtain the apple?', "options": { "A": "left", "B": "right", "C": "up", "D": "down"}, "answer": the correct answer}, ...].
4. Since you have the coordinates, despite the boundary coordinate, you can also calculate the center coordinate of each object, and by comparing the x and y values (boundary and center), you can create questions and answers.
5. Return the output purely without additional text.

Here is a demonstration:
Demo input: [{'idx': 0, 'object': 'laptop', 'coordinate': ((0, 295), (612, 710))}, {'idx': 1, 'object': 'banana', 'coordinate': ((960, 276), (1078, 436))}, {'idx': 2, 'object': 'bottle', 'coordinate': ((320, 172), (418, 321))}, {'idx': 3, 'object': 'clock', 'coordinate': ((629, 173), (689, 237))}]
Demo output: [{"question index": 0, "question": 'How should the hand move to obtain the banana?', "options": { "A": "toward the top left", "B": "toward the bottom right", "C": "toward the top right", "D": "down"}, "answer": "C"}, {"question index": 1, "question": 'How should the hand move to obtain the laptop?', "options": { "A": "left", "B": "right", "C": "up", "D": "down"}, "answer": "A"}, {"question index": 2, "question": 'What is the position of the laptop relative to the clock?', "options": { "A": "left", "B": "bottom left", "C": "right", "D": "above"}, "answer": "A"}]
"""
#load data and images
#mark="banana_grap"
mark_list=['broccoli_grab','carrot_grab','orange_grab','pizza_appear']
for mark in mark_list:
    data_dir='./data'
    jf_list=get_json_files(data_dir)
    mark_json_file=get_mark_json_file(mark, jf_list)
    data=load_json_file(mark_json_file)
    img_dir=get_img_dir(mark, data_dir)

    for index in range(len(data)):
        #processing obj_list
        obj_list,img=get_obj_list(img_dir, data, index)
        #show_img(img, obj_list)
        #print(obj_list)
        prompt = "The input list of dictionary is: " + str(obj_list)
        print(prompt)
        response = openai.ChatCompletion.create(
            model=parameters['engine'],
            messages=[
                {"role": "system", "content": enhance_prompt_temp},
                {"role": "user", "content": prompt}
            ],
            max_tokens=parameters['max_tokens'],
            stop=parameters['stop'],
        )

        res_desc=response['choices'][0]['message']['content']

        save_form={"input": obj_list, "output": res_desc}
        if res_desc:
            res_file=f"{mark}_{index}_res.json"
            with open("./responses/{}".format(res_file), "w") as f:
                json.dump(save_form,f)
        time.sleep(10)





#in_list_dict=[{'idx': 0, 'object': 'person', 'coordinate': ((818, 325), (1095, 712))}, {'idx': 1, 'object': 'sink', 'coordinate': ((56, 160), (787, 710))}, {'idx': 2, 'object': 'banana', 'coordinate': ((651, 97), (957, 180))}, {'idx': 3, 'object': 'cell phone', 'coordinate': ((0, 483), (287, 714))}, {'idx': 4, 'object': 'banana', 'coordinate': ((866, 228), (963, 408))}]

