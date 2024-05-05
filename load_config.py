from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings_toml import TomlSettings, TomlConfigSettingsSource, TomlSettingsError


class Project(BaseModel):
    start_url: str


class Defaults(BaseModel):
    region: str = 'us-east-1'


class Profile(BaseModel):
    name: str
    account_id: str
    region: Optional[str] = None
    role: str


class MySettings(TomlSettings):
    project: Project
    defaults: Defaults
    profile: list[Profile]

    model_config = SettingsConfigDict(env_file='config/appconfig.toml', env_file_encoding='utf-8')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    SETTINGS: str
    ENVIRONMENT: str


settings = MySettings()
for profile in settings.profile:
    if "region" not in profile.model_fields_set:
        print("region not set for profile", profile.name)
        profile.region = settings.defaults.region




# main function

print(repr(settings))
from contextlib import AbstractContextManager

class SettingsContextManager(AbstractContextManager):
    def __init__(self):
        pass

    def __enter__(self):
        settings.region = settings.defaults.region

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        settings.region = settings.defaults
        return False


class QuicksightTarget(AbstractContextManager):
    _global_store = {}

    __service_name = 'quicksight'

    def __init__(self, profile_name):
        self.profile_name = profile_name

    def __enter__(self):
        # For demonstration, creating a simple object (dict) using the provided key
        # You can replace this with any object creation logic as required
        self._global_store[self.profile_name] = {"data": f"Info associated with {self.profile_name}"}
        return self._global_store[self.profile_name]

    def __exit__(self, exc_type, exc_value, traceback):
        # Clear the entry from the dictionary upon exiting the context
        del self._global_store[self.profile_name]

# Example usage:
with QuicksightTarget('example_key') as my_obj:
    print(my_obj)
    # Do something with my_obj here. It's accessible as a part of the global store.

# After the context block, the entry is removed from the _global_store
print(QuicksightTarget._global_store)  # Should print an empty dictionary, showing 'example_key' was removed
