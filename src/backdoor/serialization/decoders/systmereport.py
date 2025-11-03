from typing import Any

from pydantic import ValidationError

from backdoor.models.systemreport import SystemReport
from backdoor.serialization.decoders.decoder import Decoder
from backdoor.serialization.decoders.exceptions import NotDecodableError


class SystemReportDecoder(Decoder):

    def decode(self, dct: dict[str, Any]) -> SystemReport:
        try:
            return SystemReport.model_validate(dct)
        except ValidationError as e:
            err, *_ = e.errors()
            loc, *_ = err.get("loc") or ("Unknown location",)
            msg = err.get("msg") or "Something went wrong"
            raise NotDecodableError(f"{msg} ({loc})")
