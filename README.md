# Game Screenshot OCR Analyzer

This project leverages EasyOCR and OpenCV to extract structured player performance data from game screenshots for analysis.

## Project Structure

```
.
├── data/                     # Input screenshots (from ZIP)
├── results/                  # Output JSON data
│   └── game_summary_all.json
├── easy_ocr.ipynb            # OCR test notebook
├── ocr_json_example.ipynb    # Single-image test
├── ocr_json.py               # Full pipeline to process all images
```

## Requirements

This project was developed using **Python 3.10** in a **Anaconda environment**.

###  Environment Setup

```bash
conda create -n ocr-env python=3.10
conda activate ocr-env
conda install -c conda-forge jupyterlab opencv tqdm matplotlib numpy
pip instlal easyocr
```

## How to Run

### Batch Process All Screenshots

Run the full OCR + parser pipeline across all `.png` and `.jpg` images in `./data`:

```bash
python3 ocr_json.py
```

This will:
- Load and preprocess all images
- Use EasyOCR to extract player names and scores
- Structure the output into a single JSON file at:
  ```
  results/game_summary_all.json
  ```

## Other Notebooks

- `easy_ocr.ipynb`: an early-stage test to verify the parsing logic
- `ocr_json_example.ipynb`: run the algorithm on a single image

## Sample Output

The result JSON looks like:

```json
{
  "image": "data/match1.png",
  "result": "You Lost",
  "score": "21 : 45",
  "teams": {
    "Red": [
      {
        "Name": "Alex",
        "Score": 12,
        "Objective Score": 5,
        "Offense Score": 4,
        "Support Score": 1
      },
      ...
    ]
  }
}
```

## Notes

- The OCR model is CPU-based by default. If you have a GPU, change `gpu=False` to `gpu=True` in `easyocr.Reader(...)`.
- Accuracy can be improved by adjusting the confidence threshold or using stronger image preprocessing.

## Author

Created by Laura as part of a game OCR pipeline project. Contributions and feedback welcome.
