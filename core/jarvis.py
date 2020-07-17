import asyncio
import json
from typing import *

import aiohttp
import pyaudio
import core.errors as JarvisErrors


class Jarvis:
    """
    AI Speaker class which is named after `Jarvis`, popular AI personal assistant in Marvel movies.
    """

    kakao_base_url: str = "https://kakaoi-newtone-openapi.kakao.com"
    recognize_api_url: str = "v1/recognize"
    synthesize_api_url: str = "v1/synthesize"

    def __init__(self, prefix: Union[str, List[str]], **attrs):
        """
        Initialize Jarvis instance.
        :param prefix: String value which is used as prefix to call Jarvis and execute commands.
        """
        self.prefix = prefix
        with open(file="../config.json", mode="rt", encoding="utf-8") as config_file:
            self.config = json.load(fp=config_file)

    async def recognize(self, data: bytes):
        headers: Mapping[str, str] = {
            "Transfer-Encoding": "chunked",
            "Content-Type": "application/octet-stream",
            "Authorization": f"KakaoAK {self.config['api-keys']['kakao']}"
        }
        await self._post(url=f"{self.kakao_base_url}/{self.recognize_api_url}", headers=headers, body=data)

    async def synthesize(self, data: str):
        if "<speak>" not in data:
            raise JarvisErrors.api_error.KakaoSynthesizeError(
                msg="음성합성을 시도하고자 하는 데이터는 <speak>~</speak>로 감싸진 xml 형식이어야 합니다!",
                target_xml=data
            )
        headers: Mapping[str, str] = {
            "Content-Type": "application/xml",
            "Authorization": f"KakaoAK {self.config['api-keys']['kakao']}"
        }
        response_bytes: bytes = await self._post(url=f"{self.kakao_base_url}/{self.synthesize_api_url}", headers=headers, body=data)
        with open(file="../sample/result.mp3", mode="wb") as result_audio:
            result_audio.write(response_bytes)

    async def _post(self, url: str, headers: Mapping[str, str], body: Any) -> bytes:
        async with aiohttp.ClientSession(loop=asyncio.get_event_loop()) as session:
            async with session.post(url=url, headers=headers, data=body) as resp:
                print(f"Response Status : {resp.status}")

                return await resp.read()

    async def test(self):
        sample: str = """
        <speak>
        <voice name="MAN_DIALOG_BRIGHT">안녕하세요? 이것은 카카오 음성합성 api의 테스트 코드입니다.</voice>
        <voice name="WOMAN_DIALOG_BRIGHT">카카오에서도 음성 합성 api를 제공하다니, 덕분에 개발하기 편해졌네요!.</voice>
        <voice name="MAN_DIALOG_BRIGHT">그러게요. 카카오 상표를 배치해야한다는 점을 제외하면 좋은것같아요!.</voice>
        </speak>
        """
        await self.synthesize(data=sample)


jarvis_test = Jarvis(prefix="Hey Jarvis")
asyncio.run(main=jarvis_test.test())
