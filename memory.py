# -*- coding: utf-8 -*-
import json
import os

MEMORY_FILE = 'memory_store.json'

def _load_memory():
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            f.write('{}')
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_memory(key, value):
    memory = _load_memory()
    memory[key] = value
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def load_memory(key):
    memory = _load_memory()
    return memory.get(key, None)





