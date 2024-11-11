from aiogram import Router


def setup_message_routers() -> Router:
    from . import (
        admin_panel,
        balance,
        change_city,
        cmd_start,
        delete_post,
        load_post,
        stat_posts,
        stat_subs,
        stat_users,
        unknown_message,
    )

    router = Router()
    router.include_router(balance.router)
    router.include_router(change_city.router)
    router.include_router(cmd_start.router)
    router.include_router(admin_panel.router)
    router.include_router(load_post.router)
    router.include_router(delete_post.router)
    router.include_router(stat_users.router)
    router.include_router(stat_subs.router)
    router.include_router(stat_posts.router)

    router.include_router(unknown_message.router)

    # router.include_router(errors.router)

    return router
