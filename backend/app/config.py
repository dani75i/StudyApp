from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ExoDéclic"
    database_url: str = "sqlite:///./studysprint.db"
    frontend_origin: str = "http://localhost:5173"
    site_url: str = "http://localhost:5173"
    session_cookie_name: str = "studysprint_session"
    session_days: int = 30
    cookie_secure: bool = False
    admin_email: str = "admin@studysprint.fr"
    admin_password: str = "Admin123!"
    static_dir: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
