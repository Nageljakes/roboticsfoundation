# roboticsfoundation

🤖 **RoboCadet Junior!** — a bilingual (English/Afrikaans) browser game suite that introduces young kids (ages ~4–7) to robotics and coding concepts through play. Chloé picks a game on the start screen; language, voice, and her workshop robot are shared across the suite.

**▶️ Play it live:** https://nageljakes.github.io/roboticsfoundation/

## The games

1. **RoboCadet** (8 missions) — guide your robot with step-by-step code.
2. **Repeat Racers** (4 races, Loop Lagoon) — lazy-smart coding: build a short unit once, then repeat it ×N to reach the battery.

## What kids learn

- **Robot anatomy** — robots aren't magic: they need inputs (sensors) and outputs (wheels, grippers)
- **Sequential logic** — programs run instructions in exact order, one step at a time
- **Relative direction** — left/right is from the *robot's* perspective, not the child's
- **Loops** — build it once, repeat it: the laziest (smartest) way to code
- **Debugging** — crashing isn't failing, it's finding a "bug" to fix together

## How to play

1. **Pick a game + language** — 🇬🇧 English or 🇿🇦 Afrikaans on the start screen. GUI and voice follow the choice.
2. **Workshop** — Build a robot by choosing a chassis, locomotion, sensors, and tools. The SVG robot updates live as you pick parts.
3. **Coding Arena** — Tap command blocks (⬆️ Forward, ↪️ Turn Left, ↩️ Turn Right) to build a program, then hit **▶️ RUN CODE!** Guide your bot to the battery 🔋. In Repeat Racers, also set the **🔁 repeat picker** (×1–×4): shortest tape wins the most stars.

A built-in coach reads every instruction aloud (tap any speech bubble), and the 👨‍🏫 **Parent Guide** button explains the learning concepts behind the game and how to coach through them.

## Voice

The coach prefers studio MP3s in `audio/<lang>/<id>.mp3` (see `audio/manifest.json`) and falls back to device speech (`af-ZA`/`en-ZA`). Afrikaans lines are generated with `af-ZA-AdriNeural`:

```bash
pip install edge-tts
python3 tools/make_voice.py --lang af
```

Note: Chloé is pronounced "Chloe" — the voice scripts use the phonetic alias `Kloei` for Afrikaans audio while the screen keeps the spelling `Chloé`.

## Tech notes

- **Zero dependencies** — a single `index.html` of vanilla HTML/CSS/JS, no build step
- Sound effects are synthesized with the Web Audio API; the coach voice uses the browser's Speech Synthesis
- Robot sprites are drawn with inline SVG
- Responsive layout — works on tablets and phones

## Run locally

Just open `index.html` in a browser. No server or tooling needed.
