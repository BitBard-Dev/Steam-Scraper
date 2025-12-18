import re

def clean_languages(raw):
    if not raw:
        return {"full_audio_languages": [], "interface_languages": []}

    audio = set(re.findall(r"<strong>(.*?)</strong>", raw))
    text = re.sub(r"<.*?>", "", raw)
    langs = [l.strip() for l in text.split(",") if l.strip()]

    return {
        "full_audio_languages": sorted(audio),
        "interface_languages": sorted(l for l in langs if l not in audio)
    }