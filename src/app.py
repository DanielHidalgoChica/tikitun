from src.ui.main_window import run_app
from src.ui.login_window import show_login
import tkinter as tk


if __name__ == "__main__":
    # show login modal first; only start main window if authenticated
    try:
        authenticated, username = show_login()
        if authenticated:
            run_app(username=username)
    except Exception as e:
        import traceback
        print(f"[ERROR] Exception in app: {e}")
        traceback.print_exc()
