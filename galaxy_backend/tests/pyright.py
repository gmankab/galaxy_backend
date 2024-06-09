import core.common
import core.types
import platform
import asyncio
import sys


async def on_fail(pyright_stderr: str) -> None:
    process = await asyncio.create_subprocess_exec(
        'node',
        '--version',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )
    node_stdout, _ = await process.communicate()
    node_stdout = node_stdout.decode().strip()
    raise core.types.NotPassed(
        f"can't run pyright test: {pyright_stderr}\nnode version: {node_stdout}"
    )


async def on_success(stdout: str):
    success = '0 errors, 0 warnings, 0 information'
    if success in stdout:
        return f'pyright: {stdout}'
    else:
        raise core.types.NotPassed(stdout)


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
    )
    stdout, stderr = await process.communicate()
    if stderr:
        await on_fail(stderr.decode().strip())
    return await on_success(stdout.decode().strip())

