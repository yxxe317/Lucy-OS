import asyncio
from plugins.voice import voice

async def test():
    result = await voice.speak("Hello, I am Lucy")
    print("Result:", result)

asyncio.run(test())