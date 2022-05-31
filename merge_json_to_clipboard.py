import json
import os
import json5
import pyperclip

files = [f for f in os.listdir('.') if os.path.isfile(f)]
result = {}
for f in files:
    with open(f, encoding="utf-8") as f:
        result = result | json5.load(f)

pyperclip.copy(json.dumps(result, ensure_ascii=False, indent=4))
