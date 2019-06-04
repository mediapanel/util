# pylint: disable-all

from distutils.core import setup

setup(
    name="mediapanel",
    version="0.1.0",
    packages=["mediapanel", "mediapanel.config", "mediapanel.db"],
    install_requires=["sqlalchemy"]
)
