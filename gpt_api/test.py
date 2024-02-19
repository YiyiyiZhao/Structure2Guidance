#reference 1：https://juejin.cn/post/7225126264663605309
#reference 2：https://note.com/rorosuke/n/n622a5a4b6afe


import openai
openai.api_key = "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"
parameters = {
    'engine': 'gpt-3.5-turbo',
    'max_tokens': 400,
    'stop': None,
}


while True:
    # get user input
    question = input("Please input question ( please use 'q' to end): ")

    # the break condition
    if question.lower() == 'q':
        break


    response = openai.ChatCompletion.create(
        model=parameters['engine'],
        messages=[
            {"role": "system", "content": "Your role involves generating descriptive scene representations from object detection results and providing guidance to help visually impaired individuals approach target objects within the described scenes."},
            {"role": "user", "content": question}
        ],
        max_tokens=parameters['max_tokens'],
        stop=parameters['stop'],
    )

    # 生成された反応を出力
    print(f"{response['choices'][0]['message']['content']}")
