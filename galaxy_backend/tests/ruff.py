import core.common
import core.types
import asyncio
import sys


async def ruff() -> str:
    cmd = [
        sys.executable,
        '-m',
        'ruff',
        'check',
        str(core.common.path.app),
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )
    response = await process.communicate()
    stdout = response[0]
    stdout_str = stdout.decode().strip()
    success = 'All checks passed!'
    if stdout_str == success:
        return f'ruff: {stdout_str}'
    else:
        raise core.types.NotPassed(stdout_str)

