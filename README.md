Of course. Here is the updated `README.md` for the project, now called **`reaganlog`**.

# `reaganlog`

`reaganlog` is a terminal-based system log viewer. It provides a clean, real-time interface for monitoring system logs and includes powerful features like filtering, searching, and saving logs.

-----

## Features ✨

  * **Real-time Log Streaming**: View `journalctl` logs as they happen, with updates every few seconds.
  * **Color-Coded Output**: Quickly spot important messages with different colors for **errors**, **warnings**, and **standard information**.
  * **Interactive Filtering**: Filter logs by type (errors, warnings) or by specific services like `sshd` and `cron`.
  * **Search Functionality**: Use the built-in search bar to quickly find specific messages.
  * **Highlight and Copy**: Highlight important log lines for later review and copy them directly to your clipboard.
  * **System Health Report**: Generate a quick summary report to see the total number of errors and warnings and the message count for tracked services.
  * **Save Logs**: Save all logs or just your highlighted logs to a file.

-----

## Installation 💻

Before running `reaganlog`, make sure you have the required dependencies installed.

### Prerequisites

  * **Python 3**: The script is written in Python 3.
  * `**urwid**`: The TUI (Text-based User Interface) library.
  * `**journalctl**`: A utility to query and display messages from the `systemd` journal.
  * **Clipboard Utility**: Either `pbcopy` (for macOS) or `xclip` (for Linux) is needed for the copy functionality.

### Install `urwid`

You can install `urwid` using `pip`:

```bash
pip install urwid
```

-----

## Usage ⌨️

To start the log viewer, run the Python script from your terminal:

```bash
python3 reaganlog.py
```

### Keybindings

| Key            | Action                                                                   |
| :------------- | :----------------------------------------------------------------------- |
| `Q` / `q`      | Quit the application.                                                    |
| `P` / `p`      | Pause/Unpause the real-time log stream.                                  |
| `F` / `f`      | Toggle focus lock, preventing the view from scrolling to the bottom.     |
| `M` / `m`      | Show/Hide the filter menu.                                               |
| `R` / `r`      | Toggle the system health report view.                                    |
| `Left Arrow`   | Decrease the number of logs displayed by 100.                            |
| `Right Arrow`  | Increase the number of logs displayed by 100.                            |
| `H` / `h`      | Highlight the currently selected log line.                               |
| `C` / `c`      | Copy the selected log line to the clipboard.                             |
| `S` / `s`      | Save all current logs to a file.                                         |
| `Shift` + `S`  | Save only the highlighted logs to a file.                                |
| `X` / `x`      | Clear all highlighted log lines.                                         |
| `ESC`          | Cancel a pending action, such as saving a file.                          |
