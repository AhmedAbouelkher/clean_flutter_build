import os
from concurrent.futures import ThreadPoolExecutor


def clean_flutter_build(path: str):
    with ThreadPoolExecutor(max_workers=4) as executor:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.__contains__(".flutter-plugins"):
                    _root = root.replace(" ", "\\ ")
                    print(f"[Cleaning] {_root}")
                    # Submit the cleaning task to the thread pool
                    executor.submit(_clean_subfolder, _root)


def _clean_subfolder(root_path):
    command = f"cd {root_path} && flutter clean"
    os.system(command)
    print(f"[DONE Cleaning] {'*' * 60}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean Flutter projects")
    parser.add_argument(
        "apps_dir", nargs="+", help="Paths to directories containing Flutter projects"
    )
    args = parser.parse_args()

    for directory in args.apps_dir:
        clean_flutter_build(directory)
