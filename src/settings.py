from pydantic import BaseSettings


class Settings(BaseSettings):

    TG_BOT_TOKEN: str

    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_CLUSTER: str

    DB_NAME: str = "sampleDB"
    COLLECTION_NAME: str = "sample_collection"

    class Config:
        env_file = ".env"

    @property
    def mongodb_url(self) -> str:
        return f"mongodb+srv://{self.MONGO_USER}:" \
               f"{self.MONGO_PASSWORD}@{self.MONGO_CLUSTER}." \
               f"mongodb.net/?retryWrites=true&w=majority"


settings = Settings()
