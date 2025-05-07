import os
import shutil
import multiprocessing


def is_flutter_app(directory_path: str) -> bool:
    """
    Smartly detect if a directory is a Flutter app.
    Checks for multiple indicators of a Flutter project.
    """
    indicators = [
        "pubspec.yaml",               # Flutter project manifest
        ".flutter-plugins",           # Flutter plugins config
        ".flutter-plugins-dependencies", # Flutter plugins dependencies
        ".metadata",                  # Flutter metadata file
        "lib/main.dart"               # Common Flutter entry point
    ]
    
    for indicator in indicators:
        if os.path.exists(os.path.join(directory_path, indicator)):
            return True
    
    return False


def _clean_flutter_project(project_path: str):
    """
    Clean a Flutter project and its platform-specific artifacts.
    
    Args:
        project_path: The path to the Flutter project.
    """
    try:
        project_path_escaped = project_path.replace(" ", "\\ ")
        
        # Run flutter clean command
        print(f"Cleaning {project_path}")
        command = f"cd {project_path_escaped} && flutter clean"
        os.system(command)
        
        # Check for iOS directory and clean up iOS-specific artifacts
        ios_dir = os.path.join(project_path, "ios")
        if os.path.exists(ios_dir) and os.path.isdir(ios_dir):
            # Check for Pods directory
            pods_dir = os.path.join(ios_dir, "Pods")
            if os.path.exists(pods_dir) and os.path.isdir(pods_dir):
                try:
                    shutil.rmtree(pods_dir)
                    print(f"Deleted iOS/Pods")
                except Exception:
                    pass
            
            # Check for .symlinks directory
            symlinks_dir = os.path.join(ios_dir, ".symlinks")
            if os.path.exists(symlinks_dir) and os.path.isdir(symlinks_dir):
                try:
                    shutil.rmtree(symlinks_dir)
                    print(f"Deleted iOS/.symlinks")
                except Exception:
                    pass
            
            # Check for Podfile.lock file
            podfile_lock = os.path.join(ios_dir, "Podfile.lock")
            if os.path.exists(podfile_lock) and os.path.isfile(podfile_lock):
                try:
                    os.remove(podfile_lock)
                    print(f"Deleted iOS/Podfile.lock")
                except Exception:
                    pass
        
        # Check for Android directory and .gradle
        android_dir = os.path.join(project_path, "android")
        if os.path.exists(android_dir) and os.path.isdir(android_dir):
            # Check for .gradle directory
            gradle_dir = os.path.join(android_dir, ".gradle")
            if os.path.exists(gradle_dir) and os.path.isdir(gradle_dir):
                try:
                    shutil.rmtree(gradle_dir)
                    print(f"Deleted Android/.gradle")
                except Exception:
                    pass
        
        print(f"Completed cleaning {project_path}")
    except Exception:
        # Ensure any unexpected exception doesn't stop the entire process
        print(f"Failed to fully clean {project_path}")


def clean_flutter_build(path: str):
    """Clean Flutter projects and their iOS/Android build artifacts."""
    # Get CPU count for optimal thread pool size
    cpu_count = multiprocessing.cpu_count()
    
    # Create a thread pool with a number of workers equal to CPU cores
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=cpu_count) as executor:
        for root, dirs, files in os.walk(path):
            # Check if the current directory is a Flutter app
            if is_flutter_app(root):
                print(f"Found Flutter app: {root}")
                
                # Submit the cleaning task to the thread pool
                executor.submit(_clean_flutter_project, root)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Clean Flutter projects and platform-specific build artifacts")
    parser.add_argument(
        "apps_dir", nargs="+", help="Paths to directories containing Flutter projects"
    )
    args = parser.parse_args()

    for directory in args.apps_dir:
        clean_flutter_build(directory)
