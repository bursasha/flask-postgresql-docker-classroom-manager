from .base_config import BaseConfig


class DevConfig(BaseConfig):
    """
    This class represents the development configuration for the project, which inherits from the base configuration.

    It defines configuration settings specific to a development environment, including the database URI,
    SQLALCHEMY_ECHO and DEBUG settings.

    :ivar SQLALCHEMY_DATABASE_URI: The URI for the development database.
    :type SQLALCHEMY_DATABASE_URI: str

    :ivar SQLALCHEMY_ECHO: A setting that determines if SQLAlchemy should log SQL queries to the console.
    :type SQLALCHEMY_ECHO: bool

    :ivar DEBUG: A setting that determines if the application should run in debug mode.
    :type DEBUG: bool
    """
    DEBUG = True

    SQLALCHEMY_ECHO = True
