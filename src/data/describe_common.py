from openai import OpenAI
import base64
import json
import os

# OpenAI API Key
client = OpenAI(api_key="")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Call to openAI using the images as multi image input
def find_common_story(image_list):
    prompt = [{
        "type": "input_text", "text": "You are a detective, reviewing these handwritten clues by a people who had an experience together. Without commentary or additional text, create a brief 1-2 sentence story about these people, and the commonalities across the notes they wrote. Keep the tone casual."
    }]
    image_input = []
    for image in image_list:
        image_input.append({
            "type": "input_image", 
            "image_url": f"data:image/jpeg;base64,{image}",
            "detail": "high",
        })

    common_story = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": prompt + image_input
            }
        ],
    )

    return common_story.output_text


# List to hold encoded images
encoded_images = []

# Path to the image directory
image_dir = '/Users/juliamatthews/Documents/CCC/etch-stories/public/images'

# Supported image extensions
image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')

for filename in os.listdir(image_dir):

    if filename.lower().endswith(image_extensions):
        image_path = os.path.join(image_dir, filename)
        base64_image = encode_image(image_path)
        encoded_images.append(base64_image)

common_story = {
    "common_story": find_common_story(encoded_images)
}

with open('/Users/juliamatthews/Documents/CCC/etch-stories/src/data/common_story.json', 'w') as json_file:
    json.dump(common_story, json_file, indent=4)
