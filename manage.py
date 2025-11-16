#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodmarket.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Developer convenience: when running the development server, open
    # the main site and the kitchen login in the default browser.
    # Only do this for local development when the command is `runserver`.
    if 'runserver' in sys.argv:
        try:
            import threading, webbrowser, time

            def _open_dev_urls():
                # Small delay to let the server start
                time.sleep(1.0)
                try:
                    webbrowser.open('http://127.0.0.1:8000/')
                except Exception:
                    pass
                try:
                    webbrowser.open('http://127.0.0.1:8000/kitchen/login/')
                except Exception:
                    pass

            threading.Thread(target=_open_dev_urls, daemon=True).start()
        except Exception:
            # If anything goes wrong, don't block the server start.
            pass

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
