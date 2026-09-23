#!/usr/bin/env python3
"""Generate a component-encoded GitHub-to-Workspace bridge resource URI."""
import argparse
from urllib.parse import quote


def main():
    parser = argparse.ArgumentParser(description="Generate a bridge:// GitHub-to-Workspace resource URI")
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--ref", default="main")
    parser.add_argument("--repo-path", default="")
    parser.add_argument("--drive-folder-id", required=True)
    parser.add_argument("--drive-path", required=True)
    args = parser.parse_args()

    owner = quote(args.owner, safe="")
    repo = quote(args.repo, safe="")
    ref = quote(args.ref, safe="")
    repo_path = "/".join(quote(part, safe="") for part in args.repo_path.split("/") if part)
    folder_id = quote(args.drive_folder_id, safe="")
    drive_path = quote(args.drive_path, safe="")
    uri = f"bridge://github-workspace/repos/{owner}/{repo}/tree/{ref}"
    if repo_path:
        uri += f"/{repo_path}"
    uri += f"?drive_folder_id={folder_id}&drive_path={drive_path}"
    print(uri)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
