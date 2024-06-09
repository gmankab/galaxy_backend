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
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    stdout_str = stdout.decode().strip()
    stderr_str = stderr.decode().strip()
    success = 'All checks passed!'
    if stdout_str == success:
        return f'ruff: {stdout_str}'
    else:
        raise core.types.NotPassed(stdout_str + stderr_str)

