import os


def clean_flutter_build(path: str):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.__contains__(".flutter-plugins"):
                _root = root.replace(" ", "\\ ")
                print("[Cleaning] " + _root)
                command = "cd " + _root + " && flutter clean"
                os.system(command)
                print("[DONE Cleaning]", '*' * 60)


if __name__ == '__main__':
    apps_dir = "/Users/ahmedmahmoud/AndroidStudioProjects/test_clean_utility/"
    clean_flutter_build(apps_dir)
