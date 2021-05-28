"""Define a Eufy parameter object."""
from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Union

from .types import ParamType

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Param:
    """Define a param object."""

    def __init__(self, param_info: Union[Dict[str, Any], ParamType]) -> None:
        """Initialise the param."""
        try:
            self._value = None
            if isinstance(param_info, ParamType):
                self.type = param_info
                self.param_info = {}
            else:
                self.type = ParamType(param_info["param_type"])
                self.param_info = param_info.copy()
        except ValueError as err:
            _LOGGER.debug(
                'Unable to process parameter "%s", value "%s"',
                param_info["param_type"],
                param_info["param_value"],
            )
            raise err

    def __eq__(self, other: Any) -> bool:
        """Check whether the other object equals this object."""
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        """Return a hash of the param."""
        try:
            return hash((self.type.value, self.id))
        except KeyError:
            return hash(self.type.value)

    @property
    def id(self) -> int:
        """Return the param id."""
        return self.param_info["param_id"]

    @property
    def status(self) -> bool:
        """Return the param status."""
        return bool(self.param_info["status"])

    @property
    def value(self) -> Any:
        """Return the param value."""
        if not self._value:
            self._value = self.type.loads(self.param_info["param_value"])
        return self._value

    def set_value(self, value: Any) -> None:
        """Set the param value."""
        self.param_info["param_value"] = self.type.dumps(value)
        self._value = value

    @property
    def created(self) -> datetime:
        """Return the param created date time."""
        return datetime.fromtimestamp(self.param_info["create_time"], timezone.utc)

    @property
    def updated(self) -> datetime:
        """Return the param updated date time."""
        return datetime.fromtimestamp(self.param_info["update_time"], timezone.utc)


class Params(list):
    """Define a dictionary of parameters."""

    def __init__(self, param_infos: List[Dict[str, Any]] = []):
        """Initialise params."""
        params = []
        for param_info in param_infos:
            try:
                params.append(Param(param_info))
            except ValueError:
                pass

        super().__init__(params)

    def __contains__(self, item: Any) -> bool:
        """Check a param or param type is contained in this list."""
        if isinstance(item, Param):
            item = item.type
        elif isinstance(item, ParamType):
            pass
        else:
            return False

        for param in self:
            if param.type == item:
                return True

        return False

    def __getitem__(self, key: Any) -> Param:
        """Return the param for the given param type."""
        try:
            param_type = ParamType.lookup(key)
            for param in self:
                if param.type == param_type:
                    return param
        except ValueError:
            pass
        raise KeyError(key)

    def __setitem__(self, param_type: Any, value: Any) -> None:
        """Update or add parameters for the param type."""
        param_type = ParamType.lookup(param_type)
        try:
            param = self[param_type]
        except KeyError:
            param = Param(param_type)
            self.append(param)
        param.set_value(value)

    def items(self) -> Dict[ParamType, Param]:
        """Return a dictionary of params."""
        return {param.type: param for param in self}

    def update(self, data: Dict[str, Any]) -> None:
        """Update the params with the provided dictionary."""
        for param_type, value in data.items():
            self[param_type] = value
