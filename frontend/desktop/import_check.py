import sys

modules = ['PyQt5', 'matplotlib', 'pandas', 'requests']

for m in modules:
    try:
        __import__(m)
        print(f'OK:{m}')
    except Exception as e:
        print(f'ERR:{m}:{e}')

# Try importing local project modules (won't start the GUI)
try:
    import api_client
    print('OK:api_client')
except Exception as e:
    print(f'ERR:api_client:{e}')

try:
    import main as desktop_main
    print('OK:main')
except Exception as e:
    print(f'ERR:main:{e}')

sys.exit(0)
