"""
Class modules for mediaPanel configuration types.
"""
import json


class ConfigSection:
    """
    Base class for all Config objects and subobjects.
    """

    @staticmethod
    def from_v6_values(data: dict) -> dict:
        """
        Convert values from the ColdFusion stored values (which are usually
        all uppercase) to a version more suitable for human readable typing,
        as well as fix up any potential inconsistencies.
        """
        raise NotImplementedError()

    def to_v6_values(self) -> dict:
        """
        Convert values from the ones defined into this class to what the
        v6 code would expect. mediaPanel v6 must use the same code because,
        while the server isn't case-sensitive, the devices are.
        """
        raise NotImplementedError()

    def json(self, iterable: bool = False) -> str:
        """
        Return a JSON string, serialized using ConfigSectionJSONEncoder.
        """
        if iterable:
            return JSON_ENCODER.iterencode(self)
        return JSON_ENCODER.encode(self)


class ConfigSectionJSONEncoder(json.JSONEncoder):
    """
    Encode ConfigSection using the v6 serializable method.
    """

    # pylint: disable=method-hidden,arguments-differ
    def default(self, obj: ConfigSection) -> str:
        if isinstance(obj, ConfigSection):
            return obj.to_v6_values()
        return json.JSONEncoder.default(self, obj)


JSON_ENCODER = ConfigSectionJSONEncoder()


class Config(ConfigSection):
    """
    Base class for all Config objects.
    """

    # pylint: disable=abstract-method

    __slots__ = ("path",)
    file_path = ""

    @classmethod
    def from_v6_file(cls, filename: str):
        """
        Load a mediaPanel v6 JSON file (from the ColdFusion servers) and create
        a GeneralConfig.
        """
        with open(filename) as json_file:
            data = cls.from_v6_values(json.load(json_file))
            # this *does* require a "redundant" keyword arg because of the
            # super().__init__() call.
            # pylint: disable=redundant-keyword-arg
            obj = cls(data, v6_path=filename)
            return obj

    @classmethod
    def from_v6_id(cls, client_id: str, device_id: str,
                   base_path: str = "/var/www/html/mediapanel/device_config/"):
        """
        Load a mediaPanel v6 JSON file when given a client_id and device_id.
        """
        path = f"{base_path}/{client_id}/1/{device_id}/{cls.file_path}"
        return cls.from_v6_file(path)

    def save_v6(self):
        """
        Save the JSON-serialized v6 version to a file.
        """
        with open(self.path, "w") as v6_file:
            for item in self.json(True):
                v6_file.write(item)

    def __init__(self, v6_path: str = None):
        if v6_path is not None:
            self.path = v6_path
