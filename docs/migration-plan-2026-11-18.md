# CK3 最新版迁移与 Workshop 更新计划

本轮用户授权更新本机 CK3、适配 `more_tenets_slots_xa_dev/` 并更新现有 Workshop **3182367229**。不包含两个 POD 产品。计划先于产品修改落盘；上一公开基线为 v11 / CK3 1.20.0.4。

1. 同步两个仓库 `master`，阅读框架安装识别、Steam 版本技能、任务总线、存储、受管验收与发布合同。登记本机任务并核现场占用。机器身份由 `ck3_live_run_id.py machine` 读取；本轮为 `pc-20260924rtuf-f11af23c08`，不沿用其他机器状态。
2. 使用框架 `skills/steam-ck3-versions` 识别本机安装与 Steam 官方版本目录。目标为最新稳定默认分支 `public`；官方公告当前为 1.21 Florin，最终以下载完成后 launcher、Steam build 与 EXE SHA 为准。必要上线仅用于更新/发布/缓存下载，结束即恢复离线。不能关闭用户游戏或接管其他任务。
3. 冻结旧依赖摘要，审查新版 faith/rite GUI、核心与普通 doctrine 数据、defines、原版 on_action、触发器及本地化。保留 100 核心槽、尾部原生空槽、原版文化上限、选择器保护及原版费用/合法性；仅按新版实际差异修改投影生成器和产品实现。不得只改 supported_version。
4. 按 [验收计划](acceptance-plan-2026-11-18.md) 完成静态与可重复构建，复用框架解析、投影、日志和唯一公共受管入口。新版 ABI 未资格化时不得重签旧 DLL；独立离线工作继续。
5. 简中实机验证关键业务与独立冷载。正式构建的产品字节须与受测树一致；每包必要验证后立即英文 commit / 普通 push master。
6. 从正式 tag 构建 allowlist staging；冻结完整双语 Change Notes 和描述，更新同一 Workshop ID，匿名读回全文和兼容标签。由 Steam 实际下载并逐文件匹配，再仅验缓存实际加载、正常退出、离线与资源释放，永久 changelog 入库后才称发布完成。

归属：本产品源码、依赖配置、夹具与具体证据留本仓。通用 Steam/解析/投影/受管/发布问题优先复用框架；若有实际可复用修复或知识，按框架主线单独验证提交，并回链本轮报告。机器路径与私有存档不搬入框架。产品命令使用显式 Python 与 framework/game/userdir 参数，本机参数存忽略的外置工作目录。

状态分别记录 `static-ready`、`live-verified`、`published` 与完整发布闭环；历史通过只适用于原记录版本。外部条件不足时保留失败与未完成项，不写通过。
