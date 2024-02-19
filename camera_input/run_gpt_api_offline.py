import json
import openai
from utils.file_pro import *
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('bert-base-nli-mean-tokens')


#openai setting
with open('./resources/api_key.txt', 'r') as f:
    openai.api_key = f.read()
parameters = {
    'engine': 'gpt-3.5-turbo',
    'max_tokens': 400,
    'stop': None,
}

#load prompts
with open('./resources/prompts.json', 'r') as f:
    prompts=json.load(f)
prompt_sce_desc=prompts['sce_desc']
prompt_guid_step=prompts['guid_step']
system_content="Your role involves generating descriptive scene representations from object detection results and providing guidance to help visually impaired individuals approach target objects within the described scenes."



#load data and images
mark="banana_grap"
data_dir='./data'
jf_list=get_json_files(data_dir)
mark_json_file=get_mark_json_file(mark, jf_list)
data=load_json_file(mark_json_file)
img_dir=get_img_dir(mark, data_dir)


#tar_obj = input("Please tell me the target object (please use 'q' to end): ")
tar_obj='banana'
complete_ref=f"Since the person's hand has already touched the {tar_obj}, the target object has been reached. The task is completed."
embedding1 = model.encode(complete_ref, convert_to_tensor=True)

for index in range(len(data)):
    #processing obj_list
    obj_list,img=get_obj_list(img_dir, data, index)
    show_img(img, obj_list)

    #form question
    question_desc=prompt_sce_desc.format(obj_list)

    #get response
    response = openai.ChatCompletion.create(
        model=parameters['engine'],
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": question_desc}
        ],
        max_tokens=parameters['max_tokens'],
        stop=parameters['stop'],
    )

    res_desc=response['choices'][0]['message']['content']
    #print response
    print("SCENE DESCRIPTION: ", res_desc)
    print()
    #display_string(res_desc)


    question_guid=prompt_guid_step.format(res_desc, tar_obj)
    # get response
    response = openai.ChatCompletion.create(
        model=parameters['engine'],
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": question_guid}
        ],
        max_tokens=parameters['max_tokens'],
        stop=parameters['stop'],
    )

    # print response
    res_guid=response['choices'][0]['message']['content']
    print("GUIDANCE: ", res_guid)
    print()
    #display_string(res_guid)

    embedding2 = model.encode(res_guid, convert_to_tensor=True)
    cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)
    if cosine_similarity.item() > 0.85:
        break




