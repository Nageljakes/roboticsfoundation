# roboticsfoundation

🤖 **RoboCadet Junior!** — a browser game that introduces young kids (ages ~4–7) to robotics and coding concepts through play.

**▶️ Play it live:** https://nageljakes.github.io/roboticsfoundation/

## What kids learn

- **Robot anatomy** — robots aren't magic: they need inputs (sensors) and outputs (wheels, grippers)
- **Sequential logic** — programs run instructions in exact order, one step at a time
- **Relative direction** — left/right is from the *robot's* perspective, not the child's
- **Debugging** — crashing isn't failing, it's finding a "bug" to fix together

## How to play

1. **Workshop** — Build a robot by choosing a chassis, locomotion, sensors, and tools. The SVG robot updates live as you pick parts.
2. **Coding Arena** — Tap command blocks (⬆️ Forward, ↪️ Turn Left, ↩️ Turn Right) to build a program, then hit **▶️ RUN CODE!** Guide your bot to the battery 🔋 across 5 missions of increasing difficulty.

A built-in coach reads every instruction aloud (tap any speech bubble), and the 👨‍🏫 **Parent Guide** button explains the learning concepts behind the game and how to coach through them.

## Tech notes

- **Zero dependencies** — a single `index.html` of vanilla HTML/CSS/JS, no build step
- Sound effects are synthesized with the Web Audio API; the coach voice uses the browser's Speech Synthesis
- Robot sprites are drawn with inline SVG
- Responsive layout — works on tablets and phones

## Run locally

Just open `index.html` in a browser. No server or tooling needed.
