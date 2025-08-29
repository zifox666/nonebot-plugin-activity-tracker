<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

## ✨ nonebot-plugin-activity-tracker ✨

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/zifox666/nonebot-plugin-activity-tracker.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-activity-tracker">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-activity-tracker.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/badge/code%20style-ruff-black?style=flat-square&logo=ruff" alt="ruff">
</a>
<a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/badge/package%20manager-uv-black?style=flat-square&logo=uv" alt="uv">
</a>
<a href="https://results.pre-commit.ci/latest/github/zifox666/nonebot-plugin-activity-tracker/master">
    <img src="https://results.pre-commit.ci/badge/github/zifox666/nonebot-plugin-activity-tracker/master.svg" alt="pre-commit" />
</a>
</div>

## 📖 介绍

一个基于 NoneBot2 的会话活跃度追踪插件，用于监测和记录用户与机器人的交互活跃度。该插件可以帮助你：

- 🔍 实时追踪会话活跃状态
- 📊 统计会话交互次数
- ⏰ 记录最后活跃时间
- 💾 支持 Redis 和内存缓存
- 📋 提供完整的数据持久化

适用于需要根据用户活跃度进行消息推送、统计分析等场景。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-activity-tracker --upgrade
使用 **pypi** 源安装

    nb plugin install nonebot-plugin-activity-tracker --upgrade -i "https://pypi.org/simple"
使用**清华源**安装

    nb plugin install nonebot-plugin-activity-tracker --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple"

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details open>
<summary>uv</summary>

    uv add nonebot-plugin-activity-tracker
安装仓库 master 分支

    uv add git+https://github.com/zifox666/nonebot-plugin-activity-tracker@master
</details>

<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-activity-tracker
安装仓库 master 分支

    pdm add git+https://github.com/zifox666/nonebot-plugin-activity-tracker@master
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-activity-tracker
安装仓库 master 分支

    poetry add git+https://github.com/zifox666/nonebot-plugin-activity-tracker@master
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_activity_tracker"]

</details>

<details>
<summary>使用 nbr 安装(使用 uv 管理依赖可用)</summary>

[nbr](https://github.com/fllesser/nbr) 是一个基于 uv 的 nb-cli，可以方便地管理 nonebot2

    nbr plugin install nonebot-plugin-activity-tracker
使用 **pypi** 源安装

    nbr plugin install nonebot-plugin-activity-tracker -i "https://pypi.org/simple"
</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的配置

|         配置项         | 必填 | 默认值 |         说明          |
|:-------------------:| :--: | :----: |:-------------------:|
| DEFAULT_ACTIVE_DAYS |  否  |   7    |     默认活跃天(缓存天数)     |
|     REDIS_HOST      |  否  |   无   | Redis 主机(留空使用内存缓存)  |
|     REDIS_PORT      |  否  | 6379   | Redis 端口(HOST为空时无效) |

### 配置示例

```env
DEFAULT_ACTIVE_DAYS=7
```

## 🎉 使用

### 检查会话活跃状态

```python
from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_activity_tracker import session_active

@matcher.handle()
async def handle(uninfo: Uninfo):
    activity_data = await session_active(uninfo.adapter.name, uninfo.scene.type.name, uninfo.scene.id)
    if activity_data:
        await matcher.send(activity_data)
    else:
        await matcher.send("会话未活跃")
```

### 使用依赖注入获取活跃数据

```python
from nonebot.params import Depends
from nonebot_plugin_activity_tracker import get_session_activity, ActivityData

@matcher.handle()
async def handle(activity_data: ActivityData = Depends(get_session_activity)):
    if activity_data:
        await matcher.send(activity_data)
    else:
        await matcher.send("当前会话无活跃数据")
```


### 获取所有活跃会话

```python
from nonebot_plugin_activity_tracker import get_all_active_sessions

@matcher.handle()
async def handle():
    sessions = await get_all_active_sessions()
    count = len(sessions)
    await matcher.send(f"当前活跃会话数: {count}\n{sessions}")
```


## 🔧 API 参考

### `ActivityData` 模型

| 属性                    | 类型              | 含义              |
| :--------------------: | :---------------: | :---------------: |
| `adapter`              | str               | 适配器名称         |
| `scene_type`           | str               | 场景类型          |
| `scene_id`             | str               | 场景 ID           |
| `count`                | int               | 活跃次数          |
| `last_session_activity`| int               | 最后会话活跃时间   |
| `last_bot_activity`    | datetime \| None  | 最后机器人活跃时间 |

### 主要函数

|             函数名             |     描述     | 参数                    | 返回值                     |
|:---------------------------:|:----------:| :---------------------: | :------------------------: |
|   `query_session_active`    | 检查指定会话活跃状态 | `adapter: str, scene_type: str, scene_id: str`        | `Optional[ActivityData]`   |
|  `get_all_active_sessions`  |  获取所有活跃会话  | 无                      | `List[ActivityData]`       |
|   `get_session_activity`    | 获取当前会话活跃状态 | `uninfo: Uninfo`        | `Optional[ActivityData]`   |
|   `record_active_session`   |   记录用户活跃   | 自动触发                | 无                         |
| `record_bot_active_session` |  记录机器人活跃   | 自动触发                | 无                         |

## 📝 示例

```python
from nonebot import on_command
from nonebot.params import Depends
from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_activity_tracker import (
    session_active, 
    get_last_active_time, 
    get_all_active_sessions,
    ActivityData
)

# 检查当前会话活跃度
check_active = on_command("活跃度", priority=1)

@check_active.handle()
async def handle_check(uninfo: Uninfo):
    activity_data = await session_active(uninfo)
    if activity_data:
        last_time = await get_last_active_time(uninfo)
        await check_active.send(
            f"会话活跃度: {activity_data.count}\n"
            f"最后活跃: {last_time.strftime('%Y-%m-%d %H:%M:%S') if last_time else '未知'}"
        )
    else:
        await check_active.send("当前会话暂无活跃记录")

# 获取所有活跃会话统计
stats = on_command("活跃统计", priority=1)

@stats.handle()
async def handle_stats():
    sessions = await get_all_active_sessions()
    total_count = sum(session.count for session in sessions)
    await stats.send(
        f"活跃会话数: {len(sessions)}\n"
        f"总交互次数: {total_count}"
    )
```
