from openai import OpenAI
from PIL import Image
import base64
import json
import os
import re
import argparse

from dotenv import load_dotenv
load_dotenv()

# Retrieve OpenAI API key from env variable
api_key = ""
client = OpenAI(api_key=api_key)

# Encode an image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Get image aspect ratio
def get_aspect_ratio(width, height):
    from math import gcd
    g = gcd(width, height)
    return f"{width//g}:{height//g}"


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


# Create image list for processing
def image_list(collection_name):
    print("📂 Loading images...")
    # Path to the image directory
    image_dir = f"/Users/juliamatthews/Documents/CCC/etch-stories/public/images/{collection_name}"
    # Supported image extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    image_list = []

    for filename in os.listdir(image_dir):

        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(image_dir, filename)
            base64_image = encode_image(image_path)
            image_list.append({
                "image_path": image_path,
                "encoded_image": base64_image
            })
        
    print(f"✅ Found {len(image_list)} images.")
    return image_list, collection_name


# Process images: get transcription, drawings, keywords, and paper description per image
def process_images(image_list, collection_name):
    print("🔍 Analyzing images...")
    raw_results = []

    # Send encoded images to gpt-4o for analysis 
    for image in image_list:
        print(f" → Processing: {os.path.basename(image['image_path'])}")
        try: 
            text_transcription = client.responses.create(
                model="gpt-4o",
                input=[
                    {
                        "role": "user",
                        "content": [
                            { "type": "input_text", "text": "Without commentary or additional text, transcribe any handwritten text in this image." },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{image['encoded_image']}",
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
                                "image_url": f"data:image/jpeg;base64,{image['encoded_image']}",
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
                                "image_url": f"data:image/jpeg;base64,{image['encoded_image']}",
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
                                "image_url": f"data:image/jpeg;base64,{image['encoded_image']}",
                                "detail": "high",
                            },
                        ],
                    }
                ],
            ) 
        except Exception as e:
            print(f"Failed to process {image['image_path']}: {e}")
            continue

        # Save results as list of dicts
        raw_results.append({
            'filename': os.path.basename(image['image_path']),
            'transcription': text_transcription.output_text,
            'drawings': drawings.output_text,
            'paper': paper.output_text,
            'keywords': parse_keywords(keywords.output_text),
            'highlight': "0"
        })

    # Write results to json file
    with open(f"/Users/juliamatthews/Documents/CCC/etch-stories/src/data/{collection_name}/analysis.json", 'w') as json_file:
        json.dump(raw_results, json_file, indent=4)

    # Write deduped list of keywords for all images to json file
    unique_keywords = dedupe_keywords(raw_results)
    with open(f"/Users/juliamatthews/Documents/CCC/etch-stories/src/data/{collection_name}/keywords.json", 'w') as json_file:
                json.dump(unique_keywords, json_file, indent=4)

    print("✅ Image analysis complete.")

        

# Generate a common story about the images in a collection
def find_common_story(image_list):
    print("🧠 Writing collection story...")
    prompt = [{
        "type": "input_text", "text": "You are a detective, reviewing these handwritten clues by a people who had an experience together. Without commentary or additional text, create a brief 1-2 sentence story about these people, and the commonalities across the notes they wrote. Keep the tone casual."
    }]
    image_input = []
    for image in image_list:
        image_input.append({
            "type": "input_image", 
            "image_url": f"data:image/jpeg;base64,{image['encoded_image']}",
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


# Process collection for common story, name and aspect ratio
def process_collection(image_list, collection_name, title):
    print("📘 Writing collection metadata...")
    
    with Image.open(image_list[0]['image_path']) as img:
        width, height = img.size
        ratio = get_aspect_ratio(width, height)

    registry_path = "/Users/juliamatthews/Documents/CCC/etch-stories/src/data/collections.json"
    if os.path.exists(registry_path):
        with open(registry_path, 'r') as f:
            collections = json.load(f)
    else:
        collections = []

    # Avoid duplicate entries  
    if not any(c["name"] == collection_name for c in collections):
        collections.append({
            "name": collection_name,
            "title": title,
            "common_story": find_common_story(image_list),
            "aspect_ratio": ratio
        })
        with open(registry_path, 'w') as f:
            json.dump(collections, f, indent=4)
        print("✅ Added to collections.json.")
    else:
        print("⚠️ Collection already in collections.json — skipping update.")



def process(collection_name, title):
    images, collection_name = image_list(collection_name)
    process_images(images, collection_name)
    process_collection(images, collection_name, title)

    print("We recommend reviewing keywords.json and collections.json and further refining the keyword list and story manually.")


def main():
    parser = argparse.ArgumentParser(description="Process an image collection")
    parser.add_argument("collection_name", type=str, help="The name of the collection folder to process")
    parser.add_argument("--title", type=str, required=True, help="The display title for the collection")
    args = parser.parse_args()

    process(args.collection_name, args.title)


if __name__ == "__main__":
    main()