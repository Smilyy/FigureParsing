import easyocr
import cv2
import json
import os
import numpy as np
from pathlib import Path
from tqdm import tqdm


# In[ ]:


def extract_game_data(image_path):
    # Initialize OCR reader
    reader = easyocr.Reader(['en'], gpu=False)
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
    # Initialize easy_ocr, and only record information with a confidence > 60% accuracy.
    results = reader.readtext(image_rgb)
    texts = [text for (_, text, prob) in results if prob > 0.6]
    
    # Extract match result and score
    try:
        result_index = texts.index("You Lost")
        result = "You Lost"
        score = f"{texts[result_index + 1]} : {texts[result_index + 2]}"
    except:
        result = "Unknown"
        score = "?"
    
    # Group words into rows: [name, score1, score2, score3, score4]
    structured_rows = []
    temp_row = []

    for item in texts:
        if item.lower() in ["total", "score", "objective", "support", "offense", ]:
            continue
        if item.replace('_', '').isalnum() and not item.isdigit():
            if temp_row:
                structured_rows.append(temp_row)
                temp_row = []
            temp_row = [item]
        elif item.isdigit():
            temp_row.append(int(item))
            if len(temp_row) == 5:
                structured_rows.append(temp_row)
                temp_row = []

    # assign teams
    teams = {}
    current_team = None

    for row in structured_rows:
        if len(row) == 1 and isinstance(row[0], str):
            current_team = row[0]
            teams[current_team] = []
        elif len(row) == 5 and current_team:
            player_data = {
                "Name": row[0],
                "Score": row[1],
                "Objective Score": row[2],
                "Offense Score": row[3],
                "Support Score": row[4],
            }
            teams[current_team].append(player_data)

    # make the results into JSON
    return {
        "result": result,
        "score": score,
        "teams": teams
    }


# In[18]:


def process_all_game_images(base_dir='./data', output_json='./results/game_summary_all.json'):
    image_paths = list(Path(base_dir).rglob("*.png")) + list(Path(base_dir).rglob("*.jpg"))
    print(f"Found {len(image_paths)} images")
    all_data = []
    for image_path in tqdm(image_paths):
        try:
            game_data = extract_game_data(str(image_path))
            all_data.append(game_data)
        except Exception as e:
            print(f"Failed to process {image_path}: {e}")

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"All data saved to {output_json}")


# In[19]:


# Run batch processor
if __name__ == "__main__":
    process_all_game_images()


# In[ ]:




