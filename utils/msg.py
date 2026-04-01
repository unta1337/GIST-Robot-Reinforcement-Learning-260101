import sys

TC_GREEN = '\033[32m'
TC_YELLOW = '\033[93m'
TC_RED = '\033[31m'
TC_RESET = '\033[39;49m'

MSG_INFO = 0
MSG_WARNING = 1
MSG_ERROR = 2
MSG_IGNORE = 3

log_level = MSG_INFO

def msg(s, out=sys.stdout):
    print(s, file=out)

def info(s):
    if log_level <= 0:
        msg(f'{TC_GREEN}[INFO]{TC_RESET} {s}')

def warn(s):
    if log_level <= 1:
        msg(f'{TC_YELLOW}[WARNING]{TC_RESET} {s}')

def err(s):
    if log_level <= 2:
        msg(f'{TC_RED}[ERROR]{TC_RESET} {s}', out=sys.stderr)
