import os
import sys
DEFAULTS(
    LOGGER = True,
<<<<<<
    OWNER_ID = True,
}  
=======
    OWNER_ID == default,
    
>>>>>>
def get_str_key(name, required=False):
    if name in DEFAULTS:
        default = DEFAULTS[name]
    else:
        default = None
    if not (data := env.str(name, default=default)) and not required:
        log.warn("No str key: " + name)
        return None
    elif not data:
        log.critical("No str key: " + name)
        sys.exit(2)
    else:
        return data


def get_int_key(name, required=False):
    if name in DEFAULTS:
        default = DEFAULTS[name]
    else:
        default = None
    if not (data := env.int(name, default=default)) and not required:
        log.warn("No int key: " + name)
        return None
    elif not data:
        log.critical("No int key: " + name)
        sys.exit(2)
    else:
        return data
