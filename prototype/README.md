# Prototype for TESS

## Install Imports
```bash
pip install numpy sounddevice pillow scipy vosk openpyxl jellyfish
```

## Libraries
1. **numpy**: For numerical operations and array manipulation.
2. **sounddevice**: For audio recording and playback.
3. **pillow (PIL)**: For image processing (replacement for PIL).
4. **scipy**: For scientific computing, including signal processing.
5. **vosk**: Speech recognition model wrapper.
6. **openpyxl**: For reading and writing Excel files.
7. **jellyfish**: For string matching, phonetic algorithms, and distance computations.

## Notes (12/9/2024)
- Post processing of audio has not yet been implemented due to the long processing time.
- UI are simply placeholders.
- Model used is vosk-model-en-us-0.22; https://alphacephei.com/vosk/models
