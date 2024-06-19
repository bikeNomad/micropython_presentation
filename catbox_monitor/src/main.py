import os

# allow for filesystem /main.py to override this one
print("frozen main.py")
root_files = os.listdir()
if 'main.py' in root_files:
    print("main.py found; running")
    import main

else:
    print("main.py not found; running app_main")
    import app_main