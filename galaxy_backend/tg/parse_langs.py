from pathlib import Path
import json
import core.common
from typing import Optional

class Lang:
    def __init__(self, path: Path, default_lang: Optional['Lang'] = None) -> None:
        parsed_json = json.loads(path.read_text(encoding='utf-8'))
        for key in self.__annotations__.keys():
            val = parsed_json.get(key, getattr(default_lang, key) if default_lang else None)
            setattr(self, key, val)

    start_game: str
    bonuses: str
    back: str
    join: str
    check: str
    join_our_channel: str
    hello: str
    coins_for_tasks: str
    click_to_join: str
    thanks_for_joining: str
    invite_friend_button: str
    clans_invalid_id: str
    clans_already_participate: str
    yes: str
    no: str
    clan_join_request: str
    clan_join_confirmed: str
    clan_join_denied: str
    not_subscribed: str
    clan_already_owned: str


def load_langs(path: Path) -> dict:
    langs = {}
    langs['en'] = Lang(path / 'en.json')
    langs['ru'] = Lang(path / 'ru.json', default_lang=langs['en'])
    langs['uk'] = Lang(path / 'uk.json', default_lang=langs['en'])
    langs['be'] = Lang(path / 'be.json', default_lang=langs['en'])
    return langs

langs = load_langs(core.common.path.langs)

def get_tr(lang_code: str) -> Lang:
    return langs.get(lang_code, langs['en'])
