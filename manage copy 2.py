#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ANGKORTRANS.settings")

    try:
        from django.core.management import execute_from_command_line

        if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
            host = "localhost"
            port = "52467"

            if len(sys.argv) >= 3 and ":" in sys.argv[2]:
                host, port = sys.argv[2].split(":")

            print("\n" + "=" * 40)
            print("🚀 API SERVER STARTING...")
            print(f"📍 http://{host}:{port}")
            print("=" * 40 + "\n")

        execute_from_command_line(sys.argv)

    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user\n")

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc


if __name__ == "__main__":
    main()