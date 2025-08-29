from nonebot import require

require("nonebot_plugin_alconna")
require("src.nonebot_plugin_activity_tracker")

from nonebot_plugin_alconna import Alconna, Args, Option, on_alconna
from nonebot_plugin_uninfo import Uninfo

from src.nonebot_plugin_activity_tracker import get_all_active_sessions, query_session_active

stats = on_alconna(
    Alconna(
        "stats",
        Option("-s|--scene", Args["scene_type", str]["scene_id", str]),
    ),
    use_cmd_start=True,
)
all = on_alconna("all", use_cmd_start=True)


@stats.handle()
async def _(
        uninfo: Uninfo,
        scene_type: str | None = None,
        scene_id: str | None = None,
):
    adapter = uninfo.adapter.name
    if not scene_type or not scene_id:
        scene_type = uninfo.scene.type.name
        scene_id = uninfo.scene.id

    activity = await query_session_active(adapter, scene_type, scene_id)
    if activity:
        await stats.finish(str(activity))
    else:
        await stats.finish("当前会话不活跃")


@all.handle()
async def _():
    sessions = await get_all_active_sessions()
    if not sessions:
        await all.finish("当前没有活跃会话")
    msg = "\n\n".join(str(session) for session in sessions)
    await all.finish(msg)
