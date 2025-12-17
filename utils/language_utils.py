# utils/language_utils.py

import re

def clean_languages(lang_string):
    """Parses and returns interface and full audio language lists from supported_languages string."""
    if not lang_string:
        return {"full_audio_languages": [], "interface_languages": []}

    full_audio = re.findall(r"<strong>(.*?)</strong>", lang_string)
    cleaned = re.sub(r"<.*?>", "", lang_string)
    all_langs = [l.strip() for l in cleaned.split(",")]
    interface_langs = [l for l in all_langs if l not in full_audio]

    return {
        "full_audio_languages": sorted(set(full_audio)),
        "interface_languages": sorted(set(interface_langs))
    }
