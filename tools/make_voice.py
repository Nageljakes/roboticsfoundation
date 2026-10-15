#!/usr/bin/env python3
"""Generate high-quality coach-voice MP3s for RoboCadet (English + Afrikaans).

Why this exists: browser speechSynthesis has no good af-ZA voice on most
devices, so Afrikaans read by an English voice sounds weird. These MP3s play
instead of the robot voice whenever present (see speakId() in index.html),
with device TTS as automatic fallback. The game stays fully offline.

Best free option (no API key): Microsoft Edge TTS via the `edge-tts` package,
voice af-ZA-AdriNeural (natural female) / en-ZA-LibbyNeural.
    pip install edge-tts
    python3 tools/make_voice.py --lang af
    python3 tools/make_voice.py --lang en

Paid alternatives with even higher quality (edit VOICES below):
  - Azure Speech: af-ZA-AdriNeural / af-ZA-JohanNeural
  - Google Cloud TTS: af-ZA-Chirp3-HD-Aoede or af-ZA-Wavenet-A
  - ElevenLabs: any Afrikaans voice, export as mp3 64kbps mono

Output: audio/<lang>/<id>.mp3 + audio/manifest.json
Keep MP3s small (64kbps mono is plenty for a kids game).
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"

VOICES = {"af": "af-ZA-AdriNeural", "en": "en-ZA-LibbyNeural"}

# (id, en_text, af_text) — must match speakId() ids in index.html
LINES = [
    ("map-new", "Pick mission one to start, Cadet Chloe!", "Kies missie een om te begin, Kadet Chloé!"),
    ("map-back", "Welcome back, Cadet Chloe! Pick a mission.", "Welkom terug, Kadet Chloé! Kies 'n missie."),
    ("locked", "Finish the last mission first!", "Voltooi eers die vorige missie!"),
    ("mem-full", "My memory is full! Let's test these steps first.", "My geheue is vol! Kom ons toets eers hierdie stappe."),
    ("bonk", "Bonk! You found a bug. Debug time! Tap the red step, or press Help.", "Bons! Jy het 'n foutjie gevind. Ontluis-tyd! Tik op die rooi stap, of druk Hulp."),
    ("almost", "Almost! Your robot stopped before the battery. Add more steps!", "Byna! Jou robot het voor die battery gestop. Voeg nog stappe by!"),
    ("hint-crash", None, None),  # dynamic (step number) — TTS fallback is fine
    ("hint-ready", "That already reaches the battery! Press RUN!", "Dit bereik alreeds die battery! Druk LAAT LOOP!"),
    ("hint-reset", "Hmm, let's press Reset and try again.", "Hmm, kom ons druk Begin oor en probeer weer."),
    ("hint-f", "Try Go Forward next!", "Probeer Ry Vooruit volgende!"),
    ("hint-l", "Try Turn Left next!", "Probeer Draai Links volgende!"),
    ("hint-r", "Try Turn Right next!", "Probeer Draai Regs volgende!"),
    ("win-last", "Congratulations Cadet Chloe! You are an official Robot Cadet! You graduated from Robot Academy!", "Baie geluk Kadet Chloé! Jy is 'n amptelike Robot-kadet! Jy het by die Robot-akademie gegradueer!"),
    ("win-3", "Mission complete! Three stars! You are a brilliant engineer!", "Missie voltooi! Drie sterre! Jy is 'n briljante ingenieur!"),
    ("win-other", "Mission complete! Well done, Cadet Chloe!", "Missie voltooi! Goed gedoen, Kadet Chloé!"),
    ("ws-step-0", "Hello Cadet Chloe! First, choose a body for your robot.", "Hallo Kadet Chloé! Kies eers 'n lyf vir jou robot."),
    ("ws-step-1", "Now choose how your robot will move!", "Kies nou hoe jou robot gaan beweeg!"),
    ("ws-step-2", "Next, choose eyes and sensors so your robot can see and hear.", "Kies volgende oë en sensors sodat jou robot kan sien en hoor."),
    ("ws-step-3", "Now choose hands so your robot can pick things up.", "Kies nou hande sodat jou robot dinge kan optel."),
    ("ws-step-4", "Last step! Paint your robot your favourite color.", "Laaste stap! Verf jou robot jou gunstelingkleur."),
    ("mission-0", "Mission 1! Tell your robot to go forward to reach the battery.", "Missie 1! Sê vir jou robot om vorentoe te ry tot by die battery."),
    ("mission-1", "Mission 2! Rocks are in the way. Go around them to the battery.", "Missie 2! Rotse is in die pad. Gaan om hulle tot by die battery."),
    ("mission-2", "Mission 3! A tall wall of rocks. Climb up the side, then turn.", "Missie 3! 'n Hoë muur van rotse. Klim teen die kant op, draai dan."),
    ("mission-3", "Welcome to the Crystal Caves! Think about your robot's left and right hand.", "Welkom by die Kristalgrotte! Dink aan jou robot se linker- en regterhand."),
    ("mission-4", "The bridge is blocked! Find a safe way around the crystals.", "Die brug is geblok! Vind 'n veilige pad om die kristalle."),
    ("mission-5", "Your robot starts facing the crystal! Turn first, then zig zag to the battery.", "Jou robot kyk na die kristal! Draai eers, dan sig-sag tot by die battery."),
    ("mission-6", "Star Station! Follow the twisty path to the battery.", "Sterstasie! Volg die kronkelpad tot by die battery."),
    ("mission-7", "The final mission! Two big walls. Find the gaps to reach the battery.", "Die laaste missie! Twee groot mure. Vind die gapings tot by die battery."),
    ("part-chassis-round", "A round bubble body! Smooth and speedy.", "'n Ronde borrellyf! Glad en vinnig."),
    ("part-chassis-square", "An armored box! A strong metal frame protects the computer chips inside.", "'n Pantserboks! 'n Sterk metaalraam beskerm die rekenaarsjirpies binne."),
    ("part-chassis-capsule", "A cyber pod! Perfect for squeezing through tight spaces.", "'n Kuberpeul! Perfek om deur nou plekkies te glip."),
    ("part-locomotion-wheels", "Twin wheels! Motors spin the wheels so your robot can zoom along flat floors.", "Tweelingwiele! Motors draai die wiele sodat jou robot vinnig oor plat vloere kan ry."),
    ("part-locomotion-treads", "Tank treads! They are great for climbing over bumpy ground.", "Tenkwiels! Hulle is oulik om oor stampperige grond te klim."),
    ("part-locomotion-legs", "Walker legs! Your robot can step over things, just like you do.", "Stapbene! Jou robot kan oor dinge stap, net soos jy."),
    ("part-sensors-visor", "Camera eyes! Cameras are a robot input. They help it see colors and shapes.", "Kamera-oë! Kameras is 'n robot-inset. Hulle help hom om kleure en vorms te sien."),
    ("part-sensors-dual", "Sonar antennas! They listen for echoes, like a bat does.", "Sonar-antennas! Hulle luister vir eggo's, soos 'n vlermuis."),
    ("part-sensors-radar", "A laser dome! It spins around to map everything nearby.", "'n Laserkoepel! Dit draai rond om alles naby te karteer."),
    ("part-tools-claws", "Pincer claws! They can grab things, like a crab.", "Knyptange! Hulle kan dinge gryp, soos 'n krap."),
    ("part-tools-hands", "Bionic hands! Fingers can push buttons and pull levers.", "Bioniese hande! Vingers kan knoppies druk en hefbome trek."),
    ("part-tools-magnet", "An electro-magnet! It pulls metal things closer.", "'n Elektromagneet! Dit trek metaaldinge nader."),
    ("color-0", "sky blue! What a great color.", "hemelblou! Wat 'n mooi kleur."),
    ("color-1", "hot pink! What a great color.", "pienk! Wat 'n mooi kleur."),
    ("color-2", "lime green! What a great color.", "lemmetjiegroen! Wat 'n mooi kleur."),
    ("color-3", "sunny yellow! What a great color.", "sonniggeel! Wat 'n mooi kleur."),
    ("color-4", "purple! What a great color.", "pers! Wat 'n mooi kleur."),
    ("color-5", "orange! What a great color.", "oranje! Wat 'n mooi kleur."),
]


async def gen_edge(lang: str, ids: set | None):
    import edge_tts  # pip install edge-tts

    voice = VOICES[lang]
    outdir = AUDIO / lang
    outdir.mkdir(parents=True, exist_ok=True)
    done = []
    for vid, en, af in LINES:
        if ids and vid not in ids:
            continue
        text = af if lang == "af" else en
        if not text:
            continue
        out = outdir / f"{vid}.mp3"
        if out.exists():
            done.append(vid)
            continue
        await edge_tts.Communicate(text, voice).save(str(out))
        print(f"  {lang}/{vid}.mp3")
        done.append(vid)
    return done


def write_manifest():
    man = {}
    for lang in ("en", "af"):
        d = AUDIO / lang
        man[lang] = sorted(p.stem for p in d.glob("*.mp3")) if d.exists() else []
    (AUDIO / "manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    print(f"manifest: en={len(man['en'])} af={len(man['af'])}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["en", "af", "both"], default="both")
    ap.add_argument("--ids", help="comma-separated voice ids to (re)generate")
    ap.add_argument("--manifest-only", action="store_true")
    args = ap.parse_args()
    if args.manifest_only:
        write_manifest()
        return
    ids = set(args.ids.split(",")) if args.ids else None
    langs = ["en", "af"] if args.lang == "both" else [args.lang]
    for lang in langs:
        try:
            asyncio.run(gen_edge(lang, ids))
        except ImportError:
            sys.exit("edge-tts not installed: pip install edge-tts")
    write_manifest()


if __name__ == "__main__":
    main()
