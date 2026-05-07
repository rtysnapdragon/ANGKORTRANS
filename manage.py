#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from django.conf import settings

def show_startup_message():
    """Show nice startup banner only in the main (reloader) process"""

    allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
    default_host = allowed_hosts[0] if allowed_hosts else "127.0.0.1"
    default_port = getattr(settings, 'SERVER_PORT', 8000)

    # Get the actual addr:port that will be used
    addrport = "127.0.0.1:8000"  # fallback
    if len(sys.argv) > 2:
        addrport = sys.argv[2]
    elif len(sys.argv) == 2:  # only "runserver"
        addrport = f"{default_host}:{default_port}"

    print("\n" + "=" * 60)
    print("🚀 ANGKORTRANS API SERVER STARTING...")
    print(f"📍 http://{default_host}:{addrport}")
    print(f"   Allowed Hosts : {allowed_hosts}")
    print("=" * 60 + "\n")

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ANGKORTRANS.settings')

    import django
    django.setup()  # ✅ IMPORTANT

    from django.conf import settings

    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        default_port = getattr(settings, 'SERVER_PORT', 2222)

        # Only set port if user didn't provide one
        if len(sys.argv) == 2:
            sys.argv.append(str(default_port))

        show_startup_message()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()