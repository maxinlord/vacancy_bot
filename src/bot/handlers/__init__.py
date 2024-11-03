from aiogram import Router


def setup_message_routers() -> Router:
    from . import cmd_start

    router = Router()
    router.include_router(cmd_start.router)

    # router.include_router(errors.router)

    return router
