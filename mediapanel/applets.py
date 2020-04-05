"""
Applet utility functions and classes
"""
import json
from os import makedirs, rename
from os.path import dirname, exists, join
from tempfile import NamedTemporaryFile


class StorageManager:
    """
    Create a StorageManager, either tied to or detached from a specific
    client_id. If a client_id is not passed, it will need to be assigned or
    passed to the method as the last argument.
    """
    __slots__ = ["applet_directory", "applet_name", "context", "client_id"]

    def __init__(self, applet_name: str, context: str, client_id: int = None,
                 applet_directory: str = "/applets"):
        self.applet_directory = applet_directory
        self.applet_name = applet_name
        self.context = context
        self.client_id = client_id

    def _assert_client_id(self, client_id: int = None) -> bool:
        if client_id is None and self.client_id is None:
            raise ValueError("both client_id and self.client_id are None")
        else:
            return client_id or self.client_id

    def _get_filename(self, client_id: int = None) -> str:
        client_id = self._assert_client_id(client_id)

        return join(self.applet_directory, str(client_id), self.applet_name,
                    self.context + ".json")

    def save(self, content: dict, client_id: int = None):
        # this isn't strictly necessary but it makes sense to check it
        # before the actual temporary file is written, just in case
        client_id = self._assert_client_id(client_id)

        # create temporary file with new content
        temp_file = NamedTemporaryFile(mode="w", delete=False)
        with temp_file:
            json.dump(content, temp_file)
            temp_filename = temp_file.name

        # rename old file
        filename = self._get_filename(client_id)
        if not exists(dirname(filename)):
            # directory doesn't exist, make it
            makedirs(dirname(filename), exist_ok=True)
        rename(temp_filename, filename)

    def load(self, client_id: int = None) -> dict:
        filename = self._get_filename(client_id)
        with open(filename) as f:
            return json.load(f)
