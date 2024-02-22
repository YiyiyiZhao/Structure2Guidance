import json
import os
prompt_tem="turn the following dataset into a structured data structure, and return a json file can be processed by python, output the json file only for download. The input data is: {}. If the last item of output is not complete, you can delete the last item. Please write the output json file with name {}.json"


for root, dirs, files in os.walk("./"):
    for file in files:
        if ".json" in file:
            with open(os.path.join(root,file), 'r') as f:
                data = json.load(f)

                file_list=file.split(".")
                name=file_list[0]
                prompt = prompt_tem.format(data,name)
                with open(name+".txt", "w") as f:
                    f.write(prompt)

