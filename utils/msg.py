import sys

TC_GREEN = '\033[32m'
TC_YELLOW = '\033[93m'
TC_RED = '\033[31m'
TC_RESET = '\033[39;49m'

MSG_INFO = 0
MSG_WARN = 1
MSG_ERR = 2
MSG_IGNORE = 3

log_level = MSG_INFO

def msg(s, out=sys.stdout):
    print(s, file=out)

def info(s):
    if log_level <= MSG_INFO:
        msg(f'{TC_GREEN}[INFO]{TC_RESET} {s}')

def warn(s):
    if log_level <= MSG_WARN:
        msg(f'{TC_YELLOW}[WARNING]{TC_RESET} {s}')

def err(s):
    if log_level <= MSG_ERR:
        msg(f'{TC_RED}[ERROR]{TC_RESET} {s}', out=sys.stderr)
