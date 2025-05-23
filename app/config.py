from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str 
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    
    ALGORITHM: str 
    SECRET_KEY: str
    
    GITHUB_CLIENT_ID: str
    GITHUB_AUTH_URL: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_REDIRECT_URI: str
    GITHUB_TOKEN_URL: str 
    GITHUB_USER_URL: str  
    
    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
    )
    

settings = Settings()
