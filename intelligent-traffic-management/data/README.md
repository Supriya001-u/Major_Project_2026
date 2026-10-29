# Data & Traffic Video Feeds

## Directory Structure
```
data/
├── raw/         # Raw unprocessed traffic video clips (git-ignored)
├── sample/      # Small representative sample clips for local testing
└── processed/    # Preprocessed, cropped, or annotated evaluation outputs
```

## Recommended Traffic Datasets
1. **UA-DETRAC Benchmark:**
   - 100 real-world traffic surveillance sequences captured across diverse weather and lighting conditions.
   - Portal: [http://detrac-db.rit.albany.edu/](http://detrac-db.rit.albany.edu/)
2. **BDD100K Driving Video Dataset:**
   - High-diversity automotive video sequences.
   - Portal: [https://www.bdd100k.com/](https://www.bdd100k.com/)
3. **Local Recorded Traffic Video:**
   - Recorded intersection video (e.g., `MAJOR project phase 1 ai video.mp4` located in the project parent directory).

## Git Best Practices
- **Do not commit large video files (`.mp4`, `.avi`, `.mov`) to GitHub.**
- The repository `.gitignore` automatically excludes video containers in `data/raw/` and `data/processed/`.
