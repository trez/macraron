import yaml
import sys
import time
import subprocess

MACRARON_CONF = "macraron.yml"

def travel_dict(cmds, ks):
    if not ks:
        return cmds
    else:
        k, *kks = ks
        return travel_dict(cmds[k], kks)


def flatten_keys(d, prev=None):
    keys = []
    if not prev:
        prev = []
    if isinstance(d, dict):
        for k in d:
            prev_c = prev.copy()
            prev_c.append(k)
            future = flatten_keys(d[k], prev_c)
            keys.extend(future)
    else:
        return [" ".join(prev)]
    return keys


def translate_keypress(k):
    if k == ' ':
        return 'space'
    elif k == '(':
        return 'parenleft'
    elif k == ')':
        return 'parenright'
    elif k == '[':
        return 'bracketleft'
    elif k == ']':
        return 'bracketright'
    elif k == '/':
        return 'slash'
    elif k == '\\':
        return 'backslash'
    elif k == '!':
        return 'exclam'
    elif k == ':':
        return 'colon'
    elif k == '\'':
        return 'apostrophe'
    elif k == '*':
        return 'asterisk'
    elif k == '"':
        return 'quotedbl'
    elif k == ',':
        return 'comma'
    elif k == '.':
        return 'period'
    elif k == '_':
        return 'underscore'
    elif k == '-':
        return 'minus'
    elif k == '+':
        return 'plus'
    elif k == '=':
        return 'equal'
    elif k == '\n':
        return 'Return'
    elif k == '\e':
        return 'Escape'
    elif k.startswith('^'):
        kk = k[1]
        if k.islower():
            return f"ctrl+{kk}"
        else:
            return f"ctrl+shift+{kk}"
    else:
        return k


def emulate_keypress(k):
    new_k = translate_keypress(k)
    subprocess.run(["xdotool", "key", new_k])  # doesn't capture output
    time.sleep(0.05)


def add_to_paste_buffer(paste_str):
    p = subprocess.Popen(['xclip', '-selection', 'c'], stdin=subprocess.PIPE, close_fds=True)
    p.communicate(input=paste_str.encode('utf-8'))


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "-x":
            with open(MACRARON_CONF, "r") as f:
                cmds = yaml.safe_load(f)

            cmd = travel_dict(cmds, sys.argv[2:])

            if isinstance(cmd, str):
                add_to_paste_buffer(cmd)
                emulate_keypress("^V")
            elif isinstance(cmd, list):
                for c in cmd:
                    unescaped_c = bytes(c, 'utf-8').decode('unicode_escape')
                    emulate_keypress(unescaped_c)

        elif sys.argv[1] == "-l":
            with open(MACRARON_CONF, "r") as f:
                cmds = yaml.safe_load(f)
            print("\n".join(flatten_keys(cmds)))
        else:
            print("use -x for eXecute macro or -l for list macros")
    else:
        print("use -x for eXecute macro or -l for list macros")

main()

