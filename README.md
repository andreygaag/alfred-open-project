# Open Project -- Alfred Workflow

Open any project in your editor and terminal with a CLI tool in one action.

Default setup: **Zed** + **Kitty** + **Claude Code**. Fully configurable.

## Installation

1. Download `OpenProject.alfredworkflow` from [Releases](https://github.com/andreygaag/alfred-open-project/releases)
2. Double-click to install in Alfred
3. Configure via Alfred Preferences -> Workflows -> Open Project -> Configure

Requires: Python 3.10+, [Alfred Powerpack](https://www.alfredapp.com/powerpack/).

## Usage

| Input | Result |
|---|---|
| `proj` | List all projects from configured directories |
| `proj api` | Filter projects by name |
| `proj ~/Desktop` | Browse arbitrary directory |
| `proj ~/Desktop/my-app/` | Autocomplete into subdirectories |

Select a project and press Enter -- opens editor and terminal with CLI tool.

Tab on any item to autocomplete and drill deeper.

## Configuration

Open Alfred Preferences -> Workflows -> Open Project -> Configure Workflow:

| Setting | Default | Description |
|---|---|---|
| Keyword | `proj` | Keyword to trigger the workflow in Alfred |
| Project Directories | `~/Projects` | Comma-separated list of directories to scan |
| Editor | `zed` | Editor command (`zed`, `code`, `cursor`) |
| Terminal | `kitty` | Terminal command (`kitty`, `wezterm`, `alacritty`) |
| CLI Tool | `claude` | CLI tool launched inside terminal (`claude`, `aider`, `bash`) |
| Skip Directories | `node_modules, dist, ...` | Comma-separated directory names to skip when scanning |

## How it works

- **Script Filter** scans configured directories (2 levels deep), skipping directories from the Skip Directories list
- Paths starting with `~` or `/` switch to filesystem browsing mode with autocomplete
- **Run Script** launches the editor and terminal as separate processes
- Executables are resolved via `$PATH` and common install locations (`/opt/homebrew/bin`, `/usr/local/bin`, `~/.local/bin`)

## Supported terminals

Built-in support for kitty, wezterm, alacritty. Other terminals work via a generic fallback (`sh -c "cd <path> && <cli_tool>"`).

## Building from source

```
git clone https://github.com/andreygaag/alfred-open-project.git
cd alfred-open-project
./build.sh
```

Double-click `OpenProject.alfredworkflow` to install.

## Development

To develop with live changes, symlink the repo into Alfred's workflow directory:

```
ln -s /path/to/alfred-open-project ~/Library/Application\ Support/Alfred/Alfred.alfredpreferences/workflows/user.workflow.open-project
```

## License

MIT
