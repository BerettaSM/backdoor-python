from typing import Any

from backdoor.models.systemreport import SystemReport
from backdoor.serialization.encoders.encoder import Encoder
from backdoor.serialization.encoders.exceptions import NotEncodableError


class SystemReportEncoder(Encoder):

    def encode(self, o: Any) -> Any:
        match o:
            case SystemReport():
                return o.model_dump()
            case _:
                raise NotEncodableError
