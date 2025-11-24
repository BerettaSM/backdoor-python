from dataclasses import dataclass, field
from typing import Optional

from backdoor.models.client import ClientModel


@dataclass
class ClientRegistry:
    clients: list[ClientModel] = field(default_factory=list[ClientModel])

    def register(self, client: ClientModel) -> None:
        self.clients.append(client)

    @property
    def current_client(self) -> Optional[ClientModel]:
        try:
            return self.clients[0]
        except IndexError:
            return None
