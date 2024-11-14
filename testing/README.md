# Test Results Summary

A test was conducted on **11/12/2024** with **6 participants**.

Transcription Results were saved as .xlsxb files

The transcriptions from two systems were compared:

- **Vosk**
- **Wav2Vec**

Phonetic Similarity Analysis

The results were processed using **Jellyfish**, a python library that calculates the phonetic similarity between the transcriptions and the test word. 

The similarity is represented as a percentage:

- **70% and above**: Results are considered phonetically similar enough to pass.
- **below a 70%**: Results are not phonetically similar enough, therefore fails.
