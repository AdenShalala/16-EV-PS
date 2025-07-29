from nicegui import ui, app
def bold(text):
    return ''.join(
        chr(ord(c) + 0x1D400 - ord('A')) if 'A' <= c <= 'Z' else
        chr(ord(c) + 0x1D41A - ord('a')) if 'a' <= c <= 'z' else
        c for c in text
    )

def on_tree_select(e):
    label_to_path = {
        'User Information': '/userInformation',
        'Session History': '/sessionHistory',
    }

    selected_label = e.value
    if selected_label in label_to_path:
        ui.navigate.to(label_to_path[selected_label])