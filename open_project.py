#!/usr/bin/env python3
import os
import shlex
import shutil
import subprocess
import sys

SEARCH_PATHS = [
    "/opt/homebrew/bin",
    "/usr/local/bin",
    os.path.expanduser("~/.local/bin"),
    "/usr/bin",
]

TERMINAL_ARGS = {
    "kitty": lambda path, cmd: ["--working-directory", path, "sh", "-c", f"{cmd}; exec $SHELL"],
    "wezterm": lambda path, cmd: ["start", "--cwd", path, "--", "sh", "-c", f"{cmd}; exec $SHELL"],
    "alacritty": lambda path, cmd: ["--working-directory", path, "-e", "sh", "-c", f"{cmd}; exec $SHELL"],
}

DEFAULT_TERMINAL_ARGS = lambda path, cmd: [
    "sh", "-c", f"cd {shlex.quote(path)} && {cmd}; exec $SHELL"
]


def find_executable(name: str) -> str:
    if path := shutil.which(name):
        return path
    for directory in SEARCH_PATHS:
        candidate = os.path.join(directory, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    raise FileNotFoundError(f"{name} not found")


def main():
    project_path = sys.argv[1]
    editor = os.getenv("editor_cmd", "zed")
    terminal = os.getenv("terminal_cmd", "kitty")
    cli_tool = os.getenv("cli_tool", "claude")

    try:
        editor_path = find_executable(editor)
        terminal_path = find_executable(terminal)
        cli_path = find_executable(cli_tool)
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return

    subprocess.Popen([editor_path, project_path])

    term_args = TERMINAL_ARGS.get(terminal, DEFAULT_TERMINAL_ARGS)(project_path, cli_path)
    subprocess.Popen([terminal_path, *term_args])


if __name__ == "__main__":
    main()
