import json
import pdb
import os
cnt=0
can_list=[]
for root, dirs, files in os.walk("./modi_res"):
    for file in files:
        try:
            with open(os.path.join(root,file), 'r') as f:
                data = json.load(f)
            #print(data)
            inp=data["input"]
            output = data["output"]
            print(output)
            #pdb.set_trace()
            #out_up = json.loads(output)
            for elm in output:
                can_list.append({"input":inp, "output":elm})
        except:
            cnt+=1
            continue

# print(cnt)
# with open("./can_responses/gen_up.json", "w") as f:
#     json.dump(can_list, f, indent=4)

print(can_list)

with open('can_responses/samples.json', 'w') as file:
    for data in can_list:
        # 将字典转换为 JSON 字符串，并写入文件
        json_line = json.dumps(data)
        file.write(json_line + '\n')

# with open("./camera_input/responses/banana_grap_1_res.json", "r") as f:
#     data=json.load(f)
