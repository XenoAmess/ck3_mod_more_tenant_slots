# CK3 1.20.0.3 兼容迁移记录

目标 `more_tenets_slots_xa_dev/`，旧版本 `9` / CK3 `1.19.0`，迁移版本 `10` / CK3 `1.20.0.3`。核心迁移及本机记录安装/DLC 组合的代表性关键路径已完成，整体状态为 **`live-verified`**：迁移阶段 32 文件静态/构建、两个真实信条加尾部 98 空槽的原生创建保存、最终产品树简中冷重载、文化扩槽及第 100 槽操作均有证据。后续九语言将发行树扩为 46 文件，并在 R0012/R0013 完成简中四信条和中间空槽补验。迁移阶段没有 Workshop 发布，正式发布单独登记；R0010 有 58 条原版场景路径日志错误，保留历史事实。

本机 launcher 与 EXE 已实际核对，Steam build `25652598`，EXE SHA-256 `94b55397abb687a3dcd436805a5d885e6be90fa6c693feb44a9e3bbeeade02a6`。[精确输入合同](../dev_tools/ck3_1_20_0_3_sources.json) 冻结版本、EXE 和 10 份原版来源。迁移前不兼容，详见 [冻结分析](evidence/compatibility-before.json)；工作范围和门槛见 [迁移计划](migration-plan.md)、[验收计划](acceptance-plan.md)。

## 分析与修复

旧 mod 定义 170 条教义，其中真实核心教义 73 条、空槽 97 条；新版原生 `tenet_types` 共 97 条，旧 `tenet_monasticism`、`tenet_rite` 已不属于新版核心 tenet 类型。旧完整教义副本无法用于新版的 Rite/TenetType 界面，删除其副本和退役的 `doctrine_core_tenets` 组，直接继承新版所有原生 tenet 定义、费用、互斥和 DLC 条件。

新版 `NReligion.FAITH_CORE_TENETS_CAP` 原生上限为 3，迁移改为 100；会议镜像 `pam_faith_core_tenets_cap_value` 同步改为 100。实机曾发现原版 `pam_values.txt` 覆盖较早加载的产品文件，修正为 `zz_mts_core_tenets_cap.txt`，并静态检查定义所有者及加载顺序。保留 `NCulture.DEFAULT_MAX_TRADITIONS = 10000`。这不是个人 tenet 上限扩展；实际可选数量仍受当前游戏定义及互斥/DLC 限制，不能声称有 100 条相互兼容的真实 tenet。

新版原版 `window_faith_creation.gui` 已移除，改用 `window_rite_creation.gui`。生成器在新版创建窗口核心 tenet 网格，以及信仰窗口普通/紧凑两网格加入有界滚动容器；另在玩家所选仪轨的三个原生创建/编辑入口之前增加 ScriptedGui 准备动作。其余原生控件、选择、费用、分歧、流行度、Puppet 条件、信仰/Rite 页签和打开动作保留。反向移除六处投影后分别恢复冻结原版 SHA。生成 GUI 不得手改，原版的空白格式保留。

旧 `on_faith_created` 的角色 root 与字符事件清理不适用于新版的信仰 root。迁移移除旧钩子/清理事件和空槽图标，继承新版原生创建副作用。R0006/R0007 已证明两个真实信条及尾部 98 个原生空槽可创建、保存和冷重载，因此不注册任何占位信条。

R0004 已确认滚动能到达第 100 槽，但点击时原生消费者用信条槽号索引较短的教条数组，发生越界崩溃。后续方案为玩家所选仪轨准备 100 个独立隐藏组及教条：`not_creatable` 分类、`visible=no`、费用和分歧为零，没有参数、修正、特质或特殊机制效果，已有条目不重复添加。这些是持久教条元数据，与信条空槽不同；可能留存在源和新仪轨，不称临时占位信条或自动清理对象。方案和风险见 [候选说明](selector-repair-candidate.md)。

R0008 的第 100 槽选择已通过，但加载日志仍有 300 条缺失本地化和 3 条 scope 声明错误。源码 `3177fd7` 按原版合同增加 `saved_scopes = { mts_rite }`，并生成英文、简中各 300 个空白 BOM 本地化键。R0009 独立新进程加载修正后的最终产品树，最终 `error.log` 为零字节，原生加载修正通过；不覆盖 R0008 的历史 RED。

内层 descriptor 不含 `remote_file_id`，Workshop 身份仍为 `3182367229`；迁移阶段没有发布工坊，后续正式发布见 [发布报告](workshop/publication-v10.md)。作者许可截图保留在源码仓库；迁移阶段 allowlist 为 32 文件，不包含截图、夹具、报告或机器配置。该阶段保留中英文 Shang Confucian 文案并新增两份隐藏元数据本地化；后续九语言将正式发布树扩为 46 文件，见增补记录。

## 已有实机结果

| 运行 | 已证明的结果 | 边界 |
| --- | --- | --- |
| [R0003](evidence/live-R0003.json) / [R0004](evidence/live-R0004.json) | R0003 连续四个真实信条创建/5775 费用支付及原生保存；R0004 简中冷载保留四信条，并验证第 4、5、6 项选取、费用变化、重复排除与原生条件 | 使用此前源码；两轮整体 RED 分别为镜像覆盖和末端崩溃，保留失败事实，不称最终 32 文件树另建四信条并冷载通过 |
| [R0006](live-R0006-empty-slots.md) | 100 原生槽，两个真实信条加尾部 98 空槽；替换信条、费用及分歧更新；实际创建、原生保存成功 | 夹具长命令曾产生两条语法错误，不能称整轮日志全绿；当轮未冷重载，也未修复末端选择器 |
| [R0007](live-R0007-cold-reload-culture.md) | 新进程冷载后仍为两个真实信条；文化基础 cap 10000、界面时代加成后 10001；第 10 项 Astute Diplomats 支付 2000 威望并开始建立 | 仅在隔离夹具解除原版传统冷却；未推进 13 年完成建立，未穷举 10000 项；检查时 error.log 为零字节 |
| [R0008](live-R0008-selector.md) | 实际 100 信条槽、128 教条条目；末端原生候选打开并选取 Anachoresis，费用 4837→5587，未重现 R0004 越界 | 实际非空下标 `[0,1,99]`，草稿被原生 `Absent is not allowed` 拒绝，未创建/保存该草稿；加载仍 RED，修复另验 |
| [R0009](live-R0009-final-source.md) | 最终产品树加载无错误；100 槽/128 教条，第 100 槽打开及取消通过；两个真实信条加尾部 98 空槽原生创建 `MTS Final Two`，费用 4837，实际保存成功，退出码 0 | 新仪轨 152 含两个真实信条和 100 隐藏/28 原版教条，无占位信条；该轮只验证创建保存，独立冷重载见 R0010 |
| [R0010](live-R0010-cold-reload.md) | 最终 32 文件树简中独立冷载 R0009 存档，来源 SHA 严格一致；角色仪轨、两个真实信条、100 隐藏/28 原版教条、虔诚 84700 和偏离度 0%保持；再次保存/退出码 0 | 没有产品加载错误，但有 58 条原版宫廷场景路径错误；未做独立 vanilla A/B，不称整轮日志全绿 |

尾部可留空与中间可留空是不同条件。空槽保存通过不能代替末端选择验收，末端选择通过也不能代替创建合法性通过。R0009/R0010 已分别确认最终产品树的创建保存和独立冷重载；100 隐藏教条持久保留，核心信条没有占位条目，R0011 已纠正 Absent 为真实修道制度教条名称，不能用该拒绝证明空洞限制；原生信条与教条兼容条件仍须满足。

### R0009：最终源码创建保存 PASS

冻结源码为 `a64a79aeae126d58a1016de1cb9c7c24d4fbe63c`。英文受管新进程加载 R0008 的退出存档，最终 `error.log` 为零字节。第 100 槽原生候选打开/取消通过；两信条及尾部 98 空槽实际创建成功，界面费用 4837，虔诚 89537→84700。

原生退出存档大小为 91,091,546 字节，SHA-256 为 `ffe56ee19944db8a1e89c30a85e0e9c9be5156b3a9d2a923248a7709f312dee3`。新仪轨 152、来源 151、角色 33339，核心信条为 Communal Identity 和 Sanctity of Nature；100 个隐藏教条及 28 个原版教条持久保存，没有占位信条。退出码 0；详见 [R0009 报告](live-R0009-final-source.md) 与 [收据](evidence/live-R0009.json)。

### R0010：最终产品简中冷重载 PASS

新进程严格按 R0009 的存档 SHA 冷载。原生简中详情仍显示 `MTS Final Two`、团体身份、圣洁自然、0%偏离度和虔诚 84700，角色 33339 仍为仪轨 152。再次原生保存保持两个真实信条及 128 教条，占位信条为零，退出码 0。R0009/R0010 的产品 32 文件和最终 staging 逐文件摘要一致；详见 [R0010 报告](live-R0010-cold-reload.md)、[收据](evidence/live-R0010.json) 及 [综合验收](evidence/migration-final.json)。

R0010 的 `error.log` 为 17,415 字节、58 条 `[E]`：57 条原版 `gfx/court_scene/scene_cultures/00_default_cultures.txt` 对无效角色 4294967295 的 trigger 错误及 1 条 `court_scene_manager` 错误，均在同一冷载时刻。该文件无产品覆盖，无产品命名空间/本地化/GUI 解析错误，未观察到验收仪轨或角色界面影响。没有独立 vanilla A/B，不能断言因果基线或完整排除产品相关性；错误如实单列，本次不扩修原版宫廷场景，也不将整轮称为零错误。

## 复现与验收

需要本项目和 `ck3_eternal_recurrence` checkout，以及完整 CK3 1.20.0.3 安装。命令中的路径使用实际本机路径：

```text
python dev_tools/migrate_to_ck3_1_20.py --framework <framework-root> --game <ck3-installation>
python dev_tools/validate_and_build.py --framework <framework-root> --game <ck3-installation> --output <new-build-directory> --report <report.json>
```

生成器冻结游戏版本、EXE 与原版依赖输入；依赖变更时拒绝生成，须重新审阅。验证器检查生成一致性、可逆正文、上限同步、退役依赖、BOM、结构、本地化和产品allowlist，并复用框架构建原语进行双构建ZIP/manifest对比。花括号检查是结构扫描，不等于完整CK3语法解析。

`open_kaishek` 本机 checkout/JAR 不存在，框架适配器返回 `not-applicable / open_kaishek-root-missing`，原件见 [预验回执](evidence/kaishek-before.json)。这是环境缺口，不是宗教语义通过；实机不得省略。

最终 [静态回执](evidence/static-final.json) 检查 32 文件、六处可逆投影和双构建通过；它是静态工具结果，仍保留 `status=static-ready`、`live_verified=false`。实机完成结论由独立 [综合收据](evidence/migration-final.json) 记录，不修改工具能力边界。初次 [8 文件静态回执](evidence/static-validation.json) 和候选构建仍作为历史证据保留。原版 tenet 数据库和 on_action 没有产品覆盖。

迁移阶段历史 32 文件包为 `artifacts/release-v10-ck3-1.20.0.3/more_tenets_slots_xa_dev.zip`，669,682 字节，SHA-256 `429b0f71f50511635d20d1481795dd69a08a8d0f05420e43a52aebb1b16c668a`。manifest 绑定 `a90b16ca9957cb6ebe5607744519c1cb37ea8d07`，SHA-256 为 `c544384c02f7a14134980f2e7431bab7183cdfe4a5e8aef441c4f1b1193bd9b4`；该历史树与 R0009/R0010 逐文件相同，构建交付本身不等于上传。实际工坊发布使用后续九语言/新版封面的 46 文件包，详见 [正式 manifest](workshop/release-manifest-v10.json) 和 [发布报告](workshop/publication-v10.md)。

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

POD 两产品没有迁移，原版结果不适用于它们。CK3 1.19 扩槽旧存档未取得独立实证，不承诺跨版本迁移；实机仅覆盖记录的本机 DLC 组合，不代表所有组合。文化检查不证明多年后完成或 10000 项穷举；100 核心槽也不保证有 100 个相互兼容的真实信条。迁移阶段不含发布验收，2026-10-03 的正式工坊发布及公开缓存复核另见 [永久发布记录](workshop/publication-v10.md)。

2026-10-03 勘误：原生提示 Absent 指 doctrine_monasticism_absent（无修道制度），该教条与 Anachoresis 冲突。R0008 的失败不是中间空洞的因果证据；详情见 live-R0011-native-blocker-diagnosis.md。新增九语言静态认证与简中发布复验独立记录，不覆盖历史运行。

## 2026-10-03 发布前增补

九种 CK3 语言已补齐，每种 305 个键（5 个有效 Shang Confucian 文案和 300 个刻意空白的隐藏元数据键），正式 allowlist 扩为 46 文件。九语言格式认证见 [覆盖报告](localization-coverage.md)，后续实机按 AGENTS.md 仅使用简体中文；此前 32 文件证据保留为对应旧输入的历史事实。

[R0012](live-R0012-sparse-create.md) 在九语言及新版 thumbnail 的 46 文件树上，简中创建第 1、2、3、100 槽放入四个兼容真实信条、96 中间空槽留空的礼仪，原生扣款 5775，退出 0，error.log 0 字节。[R0013](live-R0013-cold-reload.md) 独立加载其原生二进制存档并重新保存，角色仪轨 153、四信条、100 隐藏/28 原版教条、虔诚 78925 和中文名称保持。

新的封面为礼仪卡片概念宣传图；三张原生截图、来源与处理参数见 [素材账本](workshop/media/provenance.json)。发布及公开验收独立按 [发布计划](workshop/publication-plan-v10.md) 执行，入库物料本身不证明已经上传。

## 2026-10-03 正式发布完成

既有工坊 `3182367229` 已更新为 version `10` / CK3 `1.20.0.3`，上传冻结源 `da4b579659ebb4de397672b833369e95fdbd03c6`，annotated tag `more-tenets-slots-v10-ck3-1.20.0.3` 指向该源并已推送。原生提交、匿名 BBCode 和完整 Notes entry `1790978434`、新版封面与三图 CDN、全新 46 文件下载清单均 PASS；Steam 在当次新鲜离线画面审阅后恢复离线，发布闭环 complete。

最终 manifest 的构建时 `git_tag=null` 原样保留，ZIP 727,367 字节/SHA-256 `2f27143085b94fa6737d31f8dc836b3ed26c8a1ed8fd690f2c137117b613b621`。精确信息见 [发布报告](workshop/publication-v10.md)、[紧凑回执](workshop/publication-v10.json)、[永久 manifest](workshop/release-manifest-v10.json) 与 [相对上一公开版本的 changelog](release-changelogs/more-tenets-slots/10.md)。上一公开匹配缓存是 version `1` / CK3 `1.19.0.4`，源 commit/tag 未知；本地迁移 v9 不作为上一公开版本。

发布通用原生附加预览、独立 DownloadItem callback 验收、首轮实证及离线组合恢复经验已富化框架：`26c9943e1e60cf377d25ed6b30327986b4c35ffa`、`fcc29d14da759493a547f6419af87ca286212906`、`90f2a7a596653d57da3910885a4ef22c99c1d95c`、`5a2c0a8b77aaa98efcbd71973c9133d6a0f62167`。具体产品文案、素材、冻结清单及回执仍归本独立项目。
