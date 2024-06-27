from os import getenv
from datetime import timedelta


class BaseConfig:
    """
    This class represents the base configuration for the project.

    Configuration settings are defined as class variables. The settings include secret keys, SQLAlchemy settings,
    and JWT token settings.

    :ivar SECRET_KEY: A secret key for the application.
    :type SECRET_KEY: str

    :ivar SQLALCHEMY_TRACK_MODIFICATIONS: A setting that determines if SQLAlchemy should track modifications.
    :type SQLALCHEMY_TRACK_MODIFICATIONS: bool

    :ivar JWT_ACCESS_TOKEN_EXPIRES: The duration before a JWT access token expires.
    :type JWT_ACCESS_TOKEN_EXPIRES: datetime.timedelta

    :ivar JWT_REFRESH_TOKEN_EXPIRES: The duration before a JWT refresh token expires.
    :type JWT_REFRESH_TOKEN_EXPIRES: datetime.timedelta

    :ivar JWT_SECRET_KEY: A secret key for JWT.
    :type JWT_SECRET_KEY: str

    :ivar JWT_ACCESS_TOKEN_LOCATION: The locations where the JWT access token can be found.
    :type JWT_ACCESS_TOKEN_LOCATION: list[str]

    :ivar JWT_REFRESH_TOKEN_LOCATION: The locations where the JWT refresh token can be found.
    :type JWT_REFRESH_TOKEN_LOCATION: list[str]

    :ivar JWT_REFRESH_COOKIE_NAME: The name of the cookie that stores the JWT refresh token.
    :type JWT_REFRESH_COOKIE_NAME: str

    :ivar JWT_COOKIE_CSRF_PROTECT: A setting that determines if CSRF protection should be enabled for the JWT cookie.
    :type JWT_COOKIE_CSRF_PROTECT: bool
    """
    SECRET_KEY = getenv("FLASK_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = getenv("FLASK_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = getenv("FLASK_JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_ACCESS_TOKEN_LOCATION = ["headers"]
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_LOCATION = ["cookies"]
    JWT_REFRESH_COOKIE_NAME = "refresh_token"
    JWT_COOKIE_CSRF_PROTECT = False
