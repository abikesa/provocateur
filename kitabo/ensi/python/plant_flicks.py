#!/usr/bin/env python3
"""
plant_flicks.py 🌱

Performs the flick ritual:
- Walks the Git-rooted directory tree starting from shill.
- Appends symbolic graffiti to existing dotfiles or creates new ones.
- Commits each flick individually with a unique message.
- Supports flicking a random subset of folders (--percent).
"""

import os
import random
import string
from datetime import datetime
import subprocess
import argparse

# Dynamically resolve Git root from script location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

def random_tag():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))

def random_filename():
    return f".{''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 8)))}"

def generate_graffiti():
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    tag = random_tag()
    return f"# flick {timestamp}-{tag}\n"

def find_git_root(start_path):
    current = os.path.abspath(start_path)
    while current != "/":
        if os.path.isdir(os.path.join(current, ".git")):
            return current
        current = os.path.dirname(current)
    raise RuntimeError("❌ Git root not found.")

def get_or_create_flick_path(folder):
    existing = [f for f in os.listdir(folder) if f.startswith('.') and not f.startswith('..')]
    flicks = [f for f in existing if os.path.isfile(os.path.join(folder, f))]
    if flicks:
        return os.path.join(folder, random.choice(flicks))  # Append to existing
    else:
        return os.path.join(folder, random_filename())      # Create new

def git_commit(file_path, message, repo_root):
    try:
        subprocess.run(["git", "add", file_path], cwd=repo_root, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=repo_root, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Git commit failed for {file_path}: {e}")

def plant_flicks(base_dir, percent=100):
    repo_root = find_git_root(base_dir)
    all_folders = [root for root, _, _ in os.walk(base_dir)]
    sample_size = int(len(all_folders) * percent / 100)
    chosen_folders = random.sample(all_folders, sample_size) if percent < 100 else all_folders

    flicked = 0
    for root in chosen_folders:
        try:
            flick_path = get_or_create_flick_path(root)
            with open(flick_path, 'a') as f:
                graffiti = generate_graffiti()
                f.write(graffiti)
            rel_path = os.path.relpath(flick_path, start=repo_root)
            commit_msg = f" {rel_path}"
            git_commit(flick_path, commit_msg, repo_root)
            print(f"✅ {commit_msg}")
            flicked += 1
        except Exception as e:
            print(f"❌ Failed in {root}: {e}")

    print(f"\n🌿 Ritual complete: {flicked} of {len(all_folders)} folders received their entropy.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🌱 Plant flicks in a random % of folders.")
    parser.add_argument("--percent", type=int, default=100,
                        help="Percentage of folders to flick (default: 100)")
    args = parser.parse_args()

    plant_flicks(BASE_DIR, percent=args.percent)
