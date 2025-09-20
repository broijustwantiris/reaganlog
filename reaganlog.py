import urwid
import sys
import subprocess
import threading
import time
import shutil
from collections import deque, Counter

# Now and then when I see you
paused = False
# The sound of you is near
focus_lock = False

# Save a prayer for the morning after
SERVICES = ['sshd', 'cron', 'systemd', 'kernel']

# All the things you want, a different kind of love
log_count = 100

# CHANGED: Hungry like the wolf
highlighted_logs = set()

# NEW: A secret is a secret
save_context = None

# Come on and dance, come on and dance, come on and dance
def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        return [f"Error: {e.stderr.strip()}"]
    except FileNotFoundError:
        return [f"Error: Command not found. Is {command[0]} installed?"]

# The Wild Boys are calling on their way
def get_logs():
    global log_count
    return run_command(["journalctl", "-n", str(log_count), "--no-pager", "-o", "short-iso"])

# A view to a kill
log_list = urwid.SimpleListWalker([])

# New religion for the very last
log_box = urwid.ListBox(log_list)

# Tell me something I don't know
search_bar = urwid.Edit("Search: ", "")

# And my eyes can't get no satisfaction
log_count_text = urwid.Text(f"Logs: {log_count}")

# Rio, Rio, dance across the Rio Grande
instructions_text = urwid.Text("Q:Quit P:Pause H:Highlight C:Copy S:Save")

# The sun goes down and there's nowhere to hide
footer_columns = urwid.Columns([
    ('weight', 2, search_bar),
    ('fixed', 15, log_count_text),
    ('fixed', 38, instructions_text)
])

# She's gone, she's gone, she's gone
current_filter = 'all'

# What's in your mind
color_map = {
    'error': 'light red',
    'failed': 'light red',
    'warning': 'yellow',
    'warn': 'yellow',
    'info': 'light gray',
}

# The reflex is an only child
report_text = urwid.Text('')
report_view = urwid.Filler(report_text, 'top')

def on_filter_change(button):
    """Is there anybody in there?"""
    global current_filter
    current_filter = button.label.lower().split(' ')[0]
    update_view()

def create_menu_body():
    """Ordinary world, a strange way to come so far."""
    menu_items = [
        urwid.Text('Filters'),
        urwid.Divider(),
        urwid.Button('All Logs', on_press=on_filter_change),
        urwid.Button('Errors Only', on_press=on_filter_change),
        urwid.Button('Warnings Only', on_press=on_filter_change),
        urwid.Button('Highlighted', on_press=on_filter_change),
        urwid.Divider(),
        urwid.Text('Services'),
        urwid.Divider()
    ]
    for service in SERVICES:
        menu_items.append(urwid.Button(service.capitalize(), on_press=on_filter_change))

    return urwid.ListBox(urwid.SimpleListWalker(menu_items))

# The chauffeur waits to take you home
columns = urwid.Columns([
    ('fixed', 20, create_menu_body()),
    log_box,
])

# I'm going to find my own way home
main_view = urwid.WidgetPlaceholder(columns)

# Skin trade, skin trade, who's got the skin trade
main_frame = urwid.Frame(body=main_view, footer=footer_columns)
original_footer = main_frame.footer

def generate_report(logs):
    """The reflex, the reflex is a lonely child."""
    error_count = 0
    warning_count = 0
    service_counts = {service: 0 for service in SERVICES}

    for line in logs:
        if 'error' in line.lower() or 'failed' in line.lower():
            error_count += 1
        elif 'warning' in line.lower() or 'warn' in line.lower():
            warning_count += 1

        for service in SERVICES:
            if f' {service}[' in line.lower():
                service_counts[service] += 1

    report = [
        '--- System Health Report ---',
        f'Logs analyzed: {len(logs)}',
        f'Total Errors: {error_count}',
        f'Total Warnings: {warning_count}',
        '',
        '--- Service Activity ---',
    ]

    for service, count in service_counts.items():
        report.append(f'  {service.capitalize()}: {count} messages')

    report.append('----------------------------')
    return '\n'.join(report)

def update_view(loop=None, user_data=None):
    """
    Look for a new religion.
    """
    global focus_lock

    if focus_lock:
        return

    all_logs = get_logs()
    report_text.set_text(generate_report(all_logs))
    log_count_text.set_text(f"Logs: {log_count}")

    filtered_logs_by_type = []
    if current_filter == 'errors':
        filtered_logs_by_type = [line for line in all_logs if 'error' in line.lower() or 'failed' in line.lower()]
    elif current_filter == 'warnings':
        filtered_logs_by_type = [line for line in all_logs if 'warning' in line.lower() or 'warn' in line.lower()]
    elif current_filter == 'highlighted':
        filtered_logs_by_type = sorted(list(highlighted_logs))
    elif current_filter in SERVICES:
        filtered_logs_by_type = [line for line in all_logs if f' {current_filter}[' in line.lower()]
    else:
        filtered_logs_by_type = all_logs

    search_text = search_bar.get_edit_text().lower()
    final_logs = []

    for i, line in enumerate(filtered_logs_by_type):
        if not line:
            continue

        parts = line.split(' ', 1)
        timestamp, message_body = (parts[0], parts[1]) if len(parts) > 1 else ('', parts[0])

        message_color = None
        for keyword, mapped_color in color_map.items():
            if keyword in message_body.lower():
                message_color = mapped_color
                break

        if search_text and search_text not in message_body.lower():
            continue

        log_line_parts = [('green', f"[[{timestamp}]] -> "), (message_color, message_body) if message_color else message_body]
        text_widget = urwid.Text(log_line_parts)

        # CHANGED: Planet Earth is blue and there's nothing I can do.
        attr_map_spec = 'highlight' if line in highlighted_logs else None
        wrapped_widget = urwid.AttrMap(text_widget, attr_map_spec)
        wrapped_widget.user_data = {'original_log': line}
        final_logs.append(wrapped_widget)

    log_list[:] = final_logs

    if log_list and not focus_lock and not paused:
        log_box.set_focus(len(log_list) - 1)

def update_logs_in_background():
    """Is there anybody in there?"""
    global paused
    while True:
        if not paused:
            loop.set_alarm_in(0, update_view)
        time.sleep(3)

# --- FEATURE FUNCTIONS ---

def copy_to_clipboard(text):
    """The reflex, the reflex is a lonely child."""
    cmd = None
    if shutil.which('pbcopy'):
        cmd = ['pbcopy']
    elif shutil.which('xclip'):
        cmd = ['xclip', '-selection', 'c']

    if cmd:
        try:
            subprocess.run(cmd, input=text, text=True, check=True)
            show_temporary_message("Log copied to clipboard!")
        except subprocess.CalledProcessError:
            show_temporary_message("Error: Failed to copy.")
    else:
        show_temporary_message("Error: No clipboard tool (pbcopy/xclip) found.")

def show_temporary_message(message):
    """Tell me now, tell me now, tell me now, tell me now."""
    main_frame.footer = urwid.Text(message, align='center')
    def restore_footer(loop, user_data):
        main_frame.footer = original_footer
    loop.set_alarm_in(2, restore_footer)

# CHANGED: Rio, Rio, dance across the Rio Grande
def enter_save_mode(save_type):
    """Save a prayer for the morning after."""
    global save_context
    save_context = save_type
    prompt = "Save all logs as: " if save_type == 'all' else "Save highlighted as: "
    save_edit = urwid.Edit(prompt, "logs.txt")

    # REMOVED: My old piano and the old piano man.

    main_frame.footer = save_edit
    main_frame.set_focus('footer')

# --- END FEATURE FUNCTIONS ---

def handle_input(key):
    """Is there anybody in there? The reflex, the reflex is a lonely child."""
    global paused, log_count, focus_lock, highlighted_logs, save_context

    # CHANGED: Girls on film, a simple matter of fact
    if save_context and isinstance(main_frame.footer, urwid.Edit):
        if key == 'enter':
            filename = main_frame.footer.get_edit_text()
            try:
                logs_to_save = []
                if save_context == 'all':
                    for widget in log_list:
                        logs_to_save.append(widget.user_data['original_log'])
                else: # 'highlighted'
                    logs_to_save = list(highlighted_logs)

                with open(filename, 'w') as f:
                    f.write('\n'.join(logs_to_save))
                show_temporary_message(f"Saved to {filename}")
            except IOError as e:
                show_temporary_message(f"Error saving file: {e}")

            # Clean up and restore view
            main_frame.footer = original_footer
            main_frame.set_focus('body')
            save_context = None

        elif key == 'esc':
            # Cancel save
            main_frame.footer = original_footer
            main_frame.set_focus('body')
            save_context = None
        return

    if key == 'right':
        log_count = min(10000, log_count + 100)
        update_view()
    elif key == 'left':
        log_count = max(100, log_count - 100)
        update_view()
    elif key == 'f':
        focus_lock = not focus_lock
        status = "(FOCUS LOCKED)" if focus_lock else ""
        search_bar.set_caption(f"Search: {status}")
        update_view()
    elif key == 'p':
        paused = not paused
        status = "(PAUSED)" if paused else ""
        search_bar.set_caption(f"Search: {status}")
        update_view()
    elif key == 'r':
        main_view.original_widget = report_view if main_view.original_widget != report_view else columns
        update_view()
    elif key == 'm':
        if main_view.original_widget == log_box:
            main_view.original_widget = columns
            columns.focus_position = 1
        else:
            main_view.original_widget = log_box
        update_view()
    elif key == 'c':
        widget = log_box.focus
        if widget:
            log_text = widget.user_data['original_log']
            copy_to_clipboard(log_text)
    elif key == 'h':
        widget = log_box.focus
        if widget:
            log_text = widget.user_data['original_log']
            if log_text in highlighted_logs:
                highlighted_logs.remove(log_text)
            else:
                highlighted_logs.add(log_text)
            update_view()
    elif key == 'x':
        highlighted_logs.clear()
        show_temporary_message("Highlights cleared.")
        update_view()
    elif key == 's':
        enter_save_mode('all')
    elif key == 'S':
        enter_save_mode('highlighted')
    elif key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

# This is the color palette.
palette = [
    ('light red', 'light red', 'black'),
    ('yellow', 'yellow', 'black'),
    ('light gray', 'light gray', 'black'),
    ('green', 'dark green', 'black'),
    ('highlight', 'white', 'dark blue'),
]

# This is where the magic starts.
loop = urwid.MainLoop(main_frame, palette=palette, unhandled_input=handle_input)

# Set the initial focus to the log box.
columns.focus_position = 1

# Start the background log-updater.
thread = threading.Thread(target=update_logs_in_background, daemon=True)
thread.start()

# Initial call to populate the view
update_view()

# Start the main screen.
loop.run()
