from pathlib import Path

from src.config import Config


def main() -> None:
    config = Config.load(Path.cwd())
    config.validate()
    print("Config OK (Fish Audio)")


if __name__ == "__main__":
    main()
