import core.common
import core.types
import platform
import asyncio
import sys


async def pyright() -> str:
    pyrightconfig = core.common.path.pyproject
    python_version = platform.python_version()
    cmd = [
        sys.executable,
        '-m',
        'pyright',
        str(core.common.path.app),
        f'--project={pyrightconfig}',
        f'--pythonpath={sys.executable}',
        f'--pythonversion={python_version}',
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
    success = '0 errors, 0 warnings, 0 information'
    if success in stdout_str:
        return f'pyright: {stdout_str}'
    else:
        raise core.types.NotPassed(stdout_str + stderr_str)

