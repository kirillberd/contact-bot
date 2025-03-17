from abc import abstractmethod, ABC
from domain.contact import Contact
from typing import List, Optional

class IContactRepository(ABC):

    @abstractmethod
    def add(self, contact: Contact) -> None: ...

    @abstractmethod
    def get(self, tags: Optional[List[str]] = None, region: Optional[str] = None) -> List[Contact]: ...

    @abstractmethod
    def update(self, contact: Contact, id: int) -> None: ...

    @abstractmethod
    def delete(self, id: int) -> None: ...

    