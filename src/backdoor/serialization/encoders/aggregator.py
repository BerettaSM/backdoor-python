from typing import Any, Sequence
from json import JSONEncoder

from backdoor.serialization.encoders.commands import (
    CommandEncoder,
    CommandResultEncoder,
)
from backdoor.serialization.encoders.encoder import Encoder
from backdoor.serialization.encoders.exceptions import NotEncodableError
from backdoor.serialization.encoders.systemreport import SystemReportEncoder


class EncoderAggregator(JSONEncoder):

    encoders: Sequence[Encoder] = (
        CommandEncoder(),
        CommandResultEncoder(),
        SystemReportEncoder(),
    )

    def default(self, o: Any) -> Any:
        for encoder in self.encoders:
            try:
                return encoder.encode(o)
            except NotEncodableError:
                ...
        return JSONEncoder.default(self, o)
