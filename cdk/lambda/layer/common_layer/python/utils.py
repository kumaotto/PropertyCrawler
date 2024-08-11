import re


def extract_property_id(message_text: str) -> str | None:
    """
    URLをメッセージから抽出する
    """
    match = re.search(r'\*URL:\* <(https://suumo\.jp/chintai/jnc_\d+/\?bc=\d+)>', message_text)
    if match:
        return match.group(1)

    return None
