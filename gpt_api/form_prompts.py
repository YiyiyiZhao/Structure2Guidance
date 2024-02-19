import json

prompt_scene_description = """Task requirements: Given the object detection results of an image with dimensions (720, 1280, 3), your task is to generate a scene description suitable for visually impaired individuals.
Input: You'll be provided with a list of dictionaries, containing the upper-left (x1, y1) and bottom-right (x2, y2) coordinates of each object in the scene. 
Output requirements: 
1. Transform the ((x1, y1), (x2, y2)) coordinates into descriptive words like 'in front,' 'left,' 'right,' and try to be as accurate as possible. Do not return coordinate numbers; you may use clock directions (e.g., 3 o'clock direction, 9 o'clock direction, etc.). 
2. Ensure clarity and spatial understanding for the target users. You can provide additional descriptions, such as the relative position of one object to another (e.g., above, to the right), allowing visually impaired individuals to create a complete 3D spatial representation in their minds. 
3. Only return the pure descriptive text; ensure it's of an appropriate length.
4. If a 'person' has significant overlap with the coordinates of a specific object, it may indicate that the user's hand has touched the specified object. Remember to include in the description that the hand has touched an object and specify which object it has touched.
The list of object dictionaries is {}. Please return the scene description."""

prompt_guidance_step = """Task requirements: Given the description of the current scene in front of the user with objects and spatial information, your task is to provide guidance to help visually impaired individuals obtain the target object.
Output requirements: 
1. If the scene description does not contain the target object, you should suggest the user move a little (if space allows) until the scene description includes the target object.
2. ElseIf the hand has already touched the target object, you can suggest that the task is completed.
3. ElseIf the target object is in the user's field of view, you should first inform the user of the object's relative position and suggest how the user should move their hands.
4. During the process of touching objects, the user may touch different objects in sequence. You can provide tactile information about these objects to the user. For example, you might first touch an apple, which has a shape close to a sphere, a smooth surface, and feels slightly heavy. Continuing to the right, you will touch an orange, which has a shape closer to an ellipsoid, a surface that is not particularly smooth, and squeezing it may result in feeling the juice of the orange.
5. Only return the pure guidance text for this step; ensure it's of an appropriate length.
The scene description is {}, and the predefined target object is {}. Please provide guidance for this step that will help the user achieve the goal."""


prompt_dict={'sce_desc':prompt_scene_description, 'guid_step':prompt_guidance_step}

with open('prompts.json', 'w') as json_file:
    json.dump(prompt_dict, json_file, indent=4)