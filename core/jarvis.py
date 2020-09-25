from typing import NoReturn, Any, Dict
from aiofile import AIOFile
import json
from chronous import BaseArchitecture, BaseEvent


class Jarvis(BaseArchitecture):
    """

    """
    config: Dict[str, Any] = {}

    def __init__(self, config_dir: str) -> None:
        """
        Intialize Jarvis
        :param config_dir: String value of configuration file path.
        """
        super(Jarvis, self).__init__(name="Jarvis")
        self.config_dir: str = config_dir

    async def process(self) -> NoReturn:
        """
        Jarvis process loop.
        :return:
        """
        # Initialize Jarvis
        await self.init()
        # Run main process
        await self.main()
        # Close process
        await self.close()

    async def init(self) -> NoReturn:
        """

        ::raise: Errors occured during process
        """
        async with AIOFile(self.config_dir, "rt") as afp:
            self.config: Dict[str, Any] = json.loads(afp.read())
        await self.dispatch("init")

    async def main(self) -> NoReturn:
        """

        :raise: Errors occured during process
        """
        while True:
            """
            Main Process Loop
            """

    async def close(self) -> NoReturn:
        """

        :raise: Errors occured during process
        """


jarvis_instance: Jarvis = Jarvis(config_dir="./config.dir")
