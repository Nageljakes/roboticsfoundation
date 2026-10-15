# Coach voice audio (optional, progressive enhancement)

The game works with **zero audio files** — it falls back to the device's
built-in speech (`af-ZA` for Afrikaans, `en-ZA` for English).

For studio-quality Afrikaans (recommended — most devices have no good `af-ZA`
voice), drop MP3s here:

```
audio/en/<id>.mp3
audio/af/<id>.mp3
audio/manifest.json   # {"en": [...ids], "af": [...ids]}
```

`speakId(id, text)` in `index.html` plays the MP3 when the manifest lists it,
otherwise it uses device TTS. Missing files are fine — that line just falls back.

Generate with the free high-quality voice (no API key):

```bash
pip install edge-tts
python3 tools/make_voice.py --lang af   # af-ZA-AdriNeural
python3 tools/make_voice.py --lang en   # en-ZA-LibbyNeural
python3 tools/make_voice.py --ids mission-0,win-3  # regenerate a few
```

Paid alternatives: Azure `af-ZA-AdriNeural` / `af-ZA-JohanNeural`, Google Cloud
`af-ZA-Chirp3-HD-Aoede`, or ElevenLabs Afrikaans — export 64kbps mono MP3 with
the same filenames. Keep the game single-file + offline: MP3s are sidecars.
