from dotenv import dotenv_values


def build_db_uri(env_path: str) -> str:
    config_dict = dotenv_values(env_path)

    protocol = "postgresql+psycopg://"
    user = config_dict.get("DB_USER")
    password = config_dict.get("DB_PASSWORD")
    host = config_dict.get("DB_HOST")
    instance = config_dict.get("DB_INSTANCE")

    return f"{protocol}{user}:{password}@{host}/{instance}"


def build_api_url(env_path: str) -> str:
    config_dict = dotenv_values(env_path)

    host = config_dict.get("API_HOST", "localhost")
    port = config_dict.get("API_PORT", 5000)

    return f"http://{host}:{port}"
