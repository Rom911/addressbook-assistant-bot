import difflib

def guess_command(user_input, commands, aliases):
    user_input = user_input.lower()
    possible = list(commands.keys()) + list(aliases.keys())

    prefix_matches = [cmd for cmd in possible if cmd.startswith(user_input)]
    
    if len(prefix_matches) == 1:
        return prefix_matches[0]
    elif len(prefix_matches) > 1:
        return prefix_matches[0]

    matches = difflib.get_close_matches(user_input, possible, n=1, cutoff=0.8)
    if matches:
        return matches[0]
    return None

def smart_guess(user_input, commands, aliases):
    text = user_input.lower()
    
    if text in aliases:
        return aliases[text]
    
    if text in commands:
        return text
    
    for cmd in commands:
        if cmd in text:
            return cmd

    return guess_command(text, commands, aliases)
