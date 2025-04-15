from openai import OpenAI
import base64
import os
import re
import json

# OpenAI API Key
client = OpenAI(api_key="")


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to the image directory
image_dir = '/Users/juliamatthews/Documents/CCC/etch-stories/public/images'

# Supported image extensions
image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')

# List to store dict results per image
raw_results = []


# Parse keywords to fix formatting and save as list of strings
def parse_keywords(raw_keywords: str) -> list[str]:
    # Split on newlines, commas, or numbered list/bullets
    split_keywords = re.split(r'[\n,]|(?:\d+\.\s*)', raw_keywords)

    clean_keywords = []
    for kw in split_keywords:
        cleaned = re.sub(r'^[\-\d\.\s"]+|["\']+$', '', kw.strip())
        if cleaned:
            clean_keywords.append(cleaned.lower())

    return clean_keywords


# Dedupe list of keywords 
def dedupe_keywords(results):
    keywords = set()
    for value in results:
        raw_keywords = value.get('keywords', '')
        for kw in raw_keywords:
             keywords.add(kw)
                    
    return sorted(keywords)

# Script:
# Send encoded images to gpt-4o for analysis 
for filename in os.listdir(image_dir):

    if filename.lower().endswith(image_extensions):
        image_path = os.path.join(image_dir, filename)
        base64_image = encode_image(image_path)

        text_transcription = client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": "Without commentary or additional text, transcribe any handwritten text in this image." },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",
                        },
                    ],
                }
            ],
        )
        drawings = client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": "Without commentary or additional text, concisely describe only any drawings or doodles that appear in this image." },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",
                        },
                    ],
                }
            ],
        ) 
        paper = client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": "Without commentary or additional text, concisely describe the quality of the paper or surface of this image." },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",
                        },
                    ],
                }
            ],
        )
        keywords = client.responses.create(
            model="gpt-4o",
            input=[
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": "Without commentary or additional text, generate 3 memorable keywords that describe the story being told within this image, based on its handwritten text, drawings, or doodles." },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high",
                        },
                    ],
                }
            ],
        ) 

        # Save results as list of dicts
        raw_results.append({
            'filename': os.path.basename(image_path),
            'transcription': text_transcription.output_text,
            'drawings': drawings.output_text,
            'paper': paper.output_text,
            'keywords': parse_keywords(keywords.output_text),
        })

# Write results to json file
with open('/Users/juliamatthews/Documents/CCC/etch-stories/src/data/analysis.json', 'w') as json_file:
    json.dump(raw_results, json_file, indent=4)

# Write deduped list of keywords for all images to json file
unique_keywords = dedupe_keywords(raw_results)
with open('/Users/juliamatthews/Documents/CCC/etch-stories/src/data/keywords.json', 'w') as json_file:
            json.dump(unique_keywords, json_file, indent=4)