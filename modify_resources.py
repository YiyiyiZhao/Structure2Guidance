import json

with open('./resources/prompts.json', 'r') as f:
    data=json.load(f)
print(data)

system_content="Your role involves generating descriptive scene representations from object detection results and providing guidance to help visually impaired individuals approach target objects within the described scenes."
data['sys_cont']=system_content

complete_ref="Since the person's hand has already touched the {}, the target object has been reached. The task is completed."
data['comp_ref']=complete_ref

with open('resources/prompts.json', 'w') as f:
    json.dump(data,f,indent=4)