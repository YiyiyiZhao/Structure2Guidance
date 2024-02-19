import json
import openai
import pdb

## settings
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
prompt_sce_desc=prompts['sce_description']
prompt_guid_step=prompts['guidance_step']
system_content="Your role involves generating descriptive scene representations from object detection results and providing guidance to help visually impaired individuals approach target objects within the described scenes."

#launch
while True:
    # get target_obj
    tar_obj = input("Please tell me the target object (please use 'q' to end): ")

    # the break condition
    if tar_obj.lower() == 'q':
        break

    #get obj_lst
    ###ToDo


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
    print(res_desc)


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
    print(res_guid)
