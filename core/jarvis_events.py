from typing import NoReturn

from chronous import BaseEvent
from chronous.events import EventContext


class InitEvent(BaseEvent):
    """
    Jarvis Initialization event
    """
    def __init__(self) -> None:
        super(InitEvent, self).__init__(name="init")

    @staticmethod
    def listener(ec: EventContext) -> NoReturn:
        """
        Base listener structure
        :param ec: EventContext containing event information.
        :raise: Error occurred during executing listener.
        """


