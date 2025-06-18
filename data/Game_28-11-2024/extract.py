import cv2
import pytesseract
import pandas as pd
import os
from glob import glob
import re

# Preprocess the image for better OCR accuracy
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 31, 2)
    dilated = cv2.dilate(thresh, None, iterations=1)  # Enhance bold text
    return dilated

# Extract text from an image using OCR
def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image, config='--psm 6')
    print(f"Extracted text from {image_path}:")
    print(text)  # Debugging: Print extracted text
    return text

# Parse extracted text to get match details
def parse_match_data(text):
    heroes, villains = [], []
    hero_scores, villain_scores = [], []
    hero_hill_score, villain_hill_score = None, None
    winning_team = None
    
    lines = text.split('\n')
    current_team = None
    
    print("Processing text for match data...")
    for line in lines:
        line = line.strip()
        print(f"Processing line: {line}")  # Debugging: Print each line
        
        # Extract Hill Scores and Winning Team
        score_match = re.search(r'\b(\d{2,4})\s*[:]\s*(\d{2,4})\b', line)
        if score_match:
            hero_hill_score, villain_hill_score = int(score_match.group(1)), int(score_match.group(2))
        if "You Won!" in line:
            winning_team = "Heroes"
        elif "You Lost" in line:
            winning_team = "Villains"
        
        # Identify teams
        elif "Heroes" in line:
            current_team = "heroes"
        elif "Villains" in line:
            current_team = "villains"
        
        # Extract player scores
        else:
            parts = re.findall(r'([A-Za-z0-9_]+)\s+(\d{3,4})', line)
            for match in parts:
                player_name, score = match[0], int(match[1])
                if current_team == "heroes":
                    heroes.append(player_name)
                    hero_scores.append(score)
                elif current_team == "villains":
                    villains.append(player_name)
                    villain_scores.append(score)
    
    # Remove invalid placeholders
    heroes = [name for name in heroes if name not in ['_', '']]  
    villains = [name for name in villains if name not in ['_', '']]  
    hero_scores = [score for score in hero_scores if score > 0]  
    villain_scores = [score for score in villain_scores if score > 0]  
    
    print("Parsed match data:", {
        "Heroes_Team": heroes,
        "Villains_Team": villains,
        "Heroes_Scores": hero_scores,
        "Villains_Scores": villain_scores,
        "Heroes_Hill_Score": hero_hill_score,
        "Villains_Hill_Score": villain_hill_score,
        "Winning_Team": winning_team
    })  # Debugging: Print parsed match data
    
    return {
        "Heroes_Team": ', '.join(heroes),
        "Villains_Team": ', '.join(villains),
        "Heroes_Scores": ', '.join(map(str, hero_scores)),
        "Villains_Scores": ', '.join(map(str, villain_scores)),
        "Heroes_Hill_Score": hero_hill_score,
        "Villains_Hill_Score": villain_hill_score,
        "Winning_Team": winning_team
    }

# Process all images and save results to CSV
def process_images_and_save_to_csv(image_folder, output_csv):
    all_match_data = []
    image_paths = glob(os.path.join(image_folder, '*.jpg'))  # Get all images in the folder
    
    for image_path in image_paths:
        text = extract_text_from_image(image_path)
        match_data = parse_match_data(text)
        if any(match_data.values()):  # Ensure valid match data
            all_match_data.append(match_data)
    
    df = pd.DataFrame(all_match_data)
    df.to_csv(output_csv, index=False)
    print(f"Extracted match data saved to {output_csv}")

# Example usage
image_folder = "path_to_your_images"  # Change this to your image folder path
output_csv = "output_match_results.csv"
process_images_and_save_to_csv(image_folder, output_csv)
