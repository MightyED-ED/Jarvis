def open_app(app_name: str) -> str:
    import subprocess
    try:
        subprocess.Popen(app_name)
        return f"Opened {app_name}"
    except FileNotFoundError:
        return f"Could not find an application called {app_name}"

print(open_app("notepad"))