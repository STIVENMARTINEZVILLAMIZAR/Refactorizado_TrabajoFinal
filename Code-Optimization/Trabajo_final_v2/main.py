from infrastructure.config import AppConfig
from infrastructure.factory import build_app


def main() -> None:
    config = AppConfig()
    app = build_app(config)
    app.run()


if __name__ == "__main__":
    main()

