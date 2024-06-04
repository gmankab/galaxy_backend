import uvicorn
import core.main
import core.config
import tests.run
import asyncio


def main():
    if core.config.env.tests:
        asyncio.run(tests.run.main())
    else:
        app = core.main.app
        uvicorn.run(
            app=app
        )


if __name__ == '__main__':
    main()

