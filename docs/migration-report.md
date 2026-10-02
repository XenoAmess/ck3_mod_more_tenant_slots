# CK3 1.20.0.3 兼容迁移记录

目标 `more_tenets_slots_xa_dev/`，旧版本 `9` / CK3 `1.19.0`，迁移版本 `10` / CK3 `1.20.0.3`。当前整体状态为 **`pending-final-live`**：32 文件源码及构建静态通过；空槽创建、存读档、文化扩槽和末端选择已有实机证据；R0009 已通过最终源码加载及两信条创建保存，新存档的独立冷重载仍待 R0010，不称完整兼容或已发布。

本机 launcher 与 EXE 已实际核对，Steam build `25652598`，EXE SHA-256 `94b55397abb687a3dcd436805a5d885e6be90fa6c693feb44a9e3bbeeade02a6`。[精确输入合同](../dev_tools/ck3_1_20_0_3_sources.json) 冻结版本、EXE 和 10 份原版来源。迁移前不兼容，详见 [冻结分析](evidence/compatibility-before.json)；工作范围和门槛见 [迁移计划](migration-plan.md)、[验收计划](acceptance-plan.md)。

## 分析与修复

旧 mod 定义 170 条教义，其中真实核心教义 73 条、空槽 97 条；新版原生 `tenet_types` 共 97 条，旧 `tenet_monasticism`、`tenet_rite` 已不属于新版核心 tenet 类型。旧完整教义副本无法用于新版的 Rite/TenetType 界面，删除其副本和退役的 `doctrine_core_tenets` 组，直接继承新版所有原生 tenet 定义、费用、互斥和 DLC 条件。

新版 `NReligion.FAITH_CORE_TENETS_CAP` 原生上限为 3，迁移改为 100；会议镜像 `pam_faith_core_tenets_cap_value` 同步改为 100。实机曾发现原版 `pam_values.txt` 覆盖较早加载的产品文件，修正为 `zz_mts_core_tenets_cap.txt`，并静态检查定义所有者及加载顺序。保留 `NCulture.DEFAULT_MAX_TRADITIONS = 10000`。这不是个人 tenet 上限扩展；实际可选数量仍受当前游戏定义及互斥/DLC 限制，不能声称有 100 条相互兼容的真实 tenet。

新版原版 `window_faith_creation.gui` 已移除，改用 `window_rite_creation.gui`。生成器在新版创建窗口核心 tenet 网格，以及信仰窗口普通/紧凑两网格加入有界滚动容器；另在玩家所选仪轨的三个原生创建/编辑入口之前增加 ScriptedGui 准备动作。其余原生控件、选择、费用、分歧、流行度、Puppet 条件、信仰/Rite 页签和打开动作保留。反向移除六处投影后分别恢复冻结原版 SHA。生成 GUI 不得手改，原版的空白格式保留。

旧 `on_faith_created` 的角色 root 与字符事件清理不适用于新版的信仰 root。迁移移除旧钩子/清理事件和空槽图标，继承新版原生创建副作用。R0006/R0007 已证明两个真实信条及尾部 98 个原生空槽可创建、保存和冷重载，因此不注册任何占位信条。

R0004 已确认滚动能到达第 100 槽，但点击时原生消费者用信条槽号索引较短的教条数组，发生越界崩溃。后续方案为玩家所选仪轨准备 100 个独立隐藏组及教条：`not_creatable` 分类、`visible=no`、费用和分歧为零，没有参数、修正、特质或特殊机制效果，已有条目不重复添加。这些是持久教条元数据，与信条空槽不同；可能留存在源和新仪轨，不称临时占位信条或自动清理对象。方案和风险见 [候选说明](selector-repair-candidate.md)。

R0008 的第 100 槽选择已通过，但加载日志仍有 300 条缺失本地化和 3 条 scope 声明错误。源码 `3177fd7` 按原版合同增加 `saved_scopes = { mts_rite }`，并生成英文、简中各 300 个空白 BOM 本地化键。R0009 独立新进程加载修正后的最终产品树，最终 `error.log` 为零字节，原生加载修正通过；不覆盖 R0008 的历史 RED。

内层 descriptor 不含 `remote_file_id`，Workshop 身份仍为 `3182367229`；本任务没有发布工坊。作者许可截图保留在源码仓库，正式构建 allowlist 为 32 文件，不包含截图、夹具、报告或机器配置。原有中英文 Shang Confucian 文案保留，新增两份隐藏元数据本地化，不构成完整多语言发布翻译。

## 已有实机结果

| 运行 | 已证明的结果 | 边界 |
| --- | --- | --- |
| [R0006](live-R0006-empty-slots.md) | 100 原生槽，两个真实信条加尾部 98 空槽；替换信条、费用及分歧更新；实际创建、原生保存成功 | 夹具长命令曾产生两条语法错误，不能称整轮日志全绿；当轮未冷重载，也未修复末端选择器 |
| [R0007](live-R0007-cold-reload-culture.md) | 新进程冷载后仍为两个真实信条；文化基础 cap 10000、界面时代加成后 10001；第 10 项 Astute Diplomats 支付 2000 威望并开始建立 | 仅在隔离夹具解除原版传统冷却；未推进 13 年完成建立，未穷举 10000 项；检查时 error.log 为零字节 |
| [R0008](live-R0008-selector.md) | 实际 100 信条槽、128 教条条目；末端原生候选打开并选取 Anachoresis，费用 4837→5587，未重现 R0004 越界 | 实际非空下标 `[0,1,99]`，中间空洞被原生 `Absent is not allowed` 拒绝，未创建/保存该草稿；加载仍 RED，修复另验 |
| [R0009](live-R0009-final-source.md) | 最终产品树加载无错误；100 槽/128 教条，第 100 槽打开及取消通过；两个真实信条加尾部 98 空槽原生创建 `MTS Final Two`，费用 4837，实际保存成功，退出码 0 | 新仪轨 152 含两个真实信条和 100 隐藏/28 原版教条，无占位信条；该存档冷重载及简中界面待 R0010 |

尾部可留空与中间可留空是不同条件。空槽保存通过不能代替末端选择验收，末端选择通过也不能代替创建合法性通过。R0009 已确认修正后的加载、代表性窗口隐藏性及两信条创建/保存结果；新存档的冷重载仍须独立确认，不绕过原生合法性。

### R0009：最终源码创建保存 PASS

冻结源码为 `a64a79aeae126d58a1016de1cb9c7c24d4fbe63c`。英文受管新进程加载 R0008 的退出存档，最终 `error.log` 为零字节。第 100 槽原生候选打开/取消通过；两信条及尾部 98 空槽实际创建成功，界面费用 4837，虔诚 89537→84700。

原生退出存档大小为 91,091,546 字节，SHA-256 为 `ffe56ee19944db8a1e89c30a85e0e9c9be5156b3a9d2a923248a7709f312dee3`。新仪轨 152、来源 151、角色 33339，核心信条为 Communal Identity 和 Sanctity of Nature；100 个隐藏教条及 28 个原版教条持久保存，没有占位信条。退出码 0；详见 [R0009 报告](live-R0009-final-source.md) 与 [收据](evidence/live-R0009.json)。R0010 尚未完成。

### R0010：新结果冷重载待填

当前 `NOT-RUN / pending`。待独立新进程加载最终源码生成的存档，核对真实信条集合、隐藏教条、角色仪轨、费用/分歧和窗口，记录退出码及日志。必要路径闭环后才改为 `live-verified`。

## 复现与验收

需要本项目和 `ck3_eternal_recurrence` checkout，以及完整 CK3 1.20.0.3 安装。命令中的路径使用实际本机路径：

```text
python dev_tools/migrate_to_ck3_1_20.py --framework <framework-root> --game <ck3-installation>
python dev_tools/validate_and_build.py --framework <framework-root> --game <ck3-installation> --output <new-build-directory> --report <report.json>
```

生成器冻结游戏版本、EXE 与原版依赖输入；依赖变更时拒绝生成，须重新审阅。验证器检查生成一致性、可逆正文、上限同步、退役依赖、BOM、结构、本地化和产品allowlist，并复用框架构建原语进行双构建ZIP/manifest对比。花括号检查是结构扫描，不等于完整CK3语法解析。

`open_kaishek` 本机 checkout/JAR 不存在，框架适配器返回 `not-applicable / open_kaishek-root-missing`，原件见 [预验回执](evidence/kaishek-before.json)。这是环境缺口，不是宗教语义通过；实机不得省略。

初次 [静态回执](evidence/static-validation.json) 对应历史 8 文件树，不是当前最终包。修正后的 32 文件静态收据为 `artifacts/selector-load-fix-20261002T173854Z.json`，独立构建在同名目录，双构建通过，ZIP SHA-256 为 `429b0f71f50511635d20d1481795dd69a08a8d0f05420e43a52aebb1b16c668a`；其 `live_verified=false`，manifest 对应当时生成工作树，不代替最终源码提交绑定的构建。原版 tenet 数据库和 on_action 没有产品覆盖。

MCP 路径的本机能力缺口、桌面兜底及只读原生观测按各轮收据记录；没有修改游戏二进制或写入进程内存。

## 系统富化与归属

通用方法与能力已按工作包提交到 `ck3_eternal_recurrence`；产品生成条目、布局、cap 配置、输入 pin、发布 allowlist 和具体存档/截图证据留本独立项目：

| 框架提交 | 富化内容 |
| --- | --- |
| `36a225237` | 通用可逆投影、结构扫描及原版覆盖迁移方法 |
| `1da893e5` | 独立产品的规范实机运行标识 |
| `e42b870a` | GUI 标量/向量反例及受管 owner 租约 CAS 边界 |
| `6a837a1e` | 原生有效值、镜像值和同名定义加载顺序验证 |
| `1a440aa96` | producer/consumer 不同数组索引、末端可达与实际选择分别验收 |
| `27aa5b578` | 编辑框容量及全文读回失败后停止动作、基础与实际文化上限区分 |
| `e273d3cb` | 隐藏元数据加载合同、GUI saved scope、尾部空槽与中间空洞分别验收 |

[框架通用专题](https://github.com/XenoAmess/ck3_eternal_recurrence/blob/master/docs/external-mod-source-projections.md) 回链产品具体证据；不包含产品源码或私有存档，不构成通用宗教 AI 能力或全部 mod 通过。

POD 两产品没有迁移，原版结果不适用于它们。CK3 1.19 扩槽旧存档未取得独立实证，不承诺跨版本迁移；实机仅覆盖记录的本机 DLC 组合，不代表所有组合。文化检查不证明多年后完成或 10000 项穷举；100 核心槽也不保证有 100 个相互兼容的真实信条。本次没有工坊发布或公开缓存复核。
