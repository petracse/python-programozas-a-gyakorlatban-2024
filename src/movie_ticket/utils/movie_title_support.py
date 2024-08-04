def replace_accented_characters(text):
    accented_chars = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ö': 'o', 'ő': 'o', 'ú': 'u', 'ü': 'u', 'ű': 'u'}
    for accented_char, replacement in accented_chars.items():
        text = text.replace(accented_char, replacement)
    return text


def remove_non_alphanumeric(text):
    return ''.join(char for char in text if char.isalnum() or char == ' ')


def convert_to_slug(text):
    text = text.lower()
    text = replace_accented_characters(text)
    text = remove_non_alphanumeric(text)
    text = text.replace(" ", "-")
    while "--" in text:
        text = text.replace("--", "-")
    text = text.strip("-")
    return text
