from pathlib import Path
import core.common
import json


class Lang:
    def __init__(
        self,
        path: Path,
    ) -> None:
        parsed_json = json.loads(
            path.read_text(encoding='utf-8')
        )
        for key in self.__annotations__.keys():
            if key in parsed_json:
                val = parsed_json[key]
            else:
                assert langs.en
                val = getattr(langs.en, key)
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
    not_joined_yet: str
    invite_friend_button: str
    clans_invalid_id: str
    clans_already_participate: str
    yes: str
    no: str
    clan_join_request: str
    clan_join_confirmed: str
    clan_join_denied: str


class langs:
    path = core.common.path.langs
    en: Lang = Lang(path / 'en.json')
    ru: Lang = Lang(path / 'ru.json')
    uk: Lang = Lang(path / 'uk.json')


def get_tr(
    lang_code: str,
) -> Lang:
    return langs.__dict__.get(
        lang_code,
        langs.en,
    )

