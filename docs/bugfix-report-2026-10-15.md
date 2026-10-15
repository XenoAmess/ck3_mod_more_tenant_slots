# 2026-10-15 用户反馈整改记录

执行清单见 [计划](bugfix-plan-2026-10-15.md)。本轮起始公开产品是 [v10](workshop/publication-v10.md)，已于 2026-10-03 发布；源码整改、当前版本实机与下一次正式发布分别记账。

**最新实机进度：** [R18 基线](native-baseline-r18-2026-10-15.md)已在1800秒窗口内就绪，并取得当前宗教和普通教义草案的实际读数；性别选择器空白未复现，草案同槽替换有效。原适配器角色ID和900秒操作窗口导致本场仍为RED，无实际创建、冷载、正常退出或产品通过。后继适配器已改为本场动态角色绑定、7200秒操作窗口和900秒退出预留；工坊仍为v10，尚未发布本候选。此前各节的“未实机”描述是对应工作包当时状态。

## WP1：信条与文化传统分离

状态：**静态通过；当前版本实机及发布待执行**。

旧 `common/defines/More tradition slots.txt` 同时包含 `NCulture.DEFAULT_MAX_TRADITIONS=10000` 和 `NReligion.FAITH_CORE_TENETS_CAP=100`，因此仅需信条槽的玩家也被强制修改文化传统上限。现移除整个 `NCulture` 覆盖，文件更名为 `more_tenets_slots.txt`；主产品继承原版文化基础上限及时代等增益，继续保留 100 个信条槽和会议镜像值。本轮不增建新的传统扩展产品，避免把捆绑改成另一项默认依赖；需要额外文化传统的玩家可独立选择传统 mod。

静态回归命令：`python -X utf8 dev_tools/test_caps.py --framework <framework>`，2 项通过。测试消费正式 `validate_caps`，并证明把旧文化覆盖藏到另一文件名也会被拒绝。未以此证明旧存档超过原版文化上限后的所有行为；已选择传统是否保留及是否可继续新增仍待代表性实机。

本机发现当前 CK3 为 `1.20.1`；旧产品精确 `1.20.0.3` 合同静态检查按预期返回 RED，原件摘要见 [基线](evidence/bugfix-20261015-baseline.json)。在更新原版投影及验收输入前，不能声称本轮完整构建或实机通过。

归属：具体文化上限和产品防捆绑检查属于本产品；复用框架 `ck3_text_projection.masked`，没有复制 parser。此包没有新增通用实现；其差异、测试与边界留本报告，后续综合方法再评估框架富化。

## 当前原版投影迁移

状态：**静态通过；仍保留待修复的隐藏教义准备机制，未授业务通过**。

当前安装为 CK3 `1.20.1 (Crozier)`、Steam build `25870654`，EXE `101124216` 字节，SHA-256 `2667e409f586f20d60142873ccb1b4eb345eee54ed996925115a46132260cff7`。新增 [精确输入合同](../dev_tools/ck3_1_20_1_sources.json)，保留原 `1.20.0.3` 合同作为历史输入。

两个 GUI 从当前原版重新生成并可逆恢复。恢复新版的 `TenetPickableForEditedRite` 合法性检查、受限候选提示、自动命名/描述入口、描述长度 define、教义 tooltip block 名及布局修订；没有旁路费用或合法性。`TenetPickableForEditedRite` 来自当前原版 `game/data_binding/pam_data_bindings.txt`，属于编辑主礼仪时的流行度候选限制，不能据此断言它修复了旧条目残留。

开发产品版本提升为 `11`，不表示已经发布。执行 `python -X utf8 dev_tools/validate_and_build.py --framework <framework> --game <game> --report docs/evidence/bugfix-20261015-1201-projection.json`：精确来源、可逆投影、上限/加载顺序、46 文件 allowlist、九语言格式和确定性双构建通过；[收据](evidence/bugfix-20261015-1201-projection.json) 明确保留 `live_verified=false`。

旧 GUI 和当前原版都调用 `ShowWindowSortList(TenetItem.GetSlotIndex)`。当前 EXE 的只读窄链复核仍存在以信条槽号读取另一教义向量的风险，故本包不直接删除 100 个兼容条目。原版 `on_rite_updated` 会对教义变化发送 `msg_rite_updated`；旧准备 effect 连续 `change_rite_doctrine` 100 次构成明确通知生产链，但没有发现本 mod 的周期事件钩子。**百连通知可解释，永久循环尚未实机证实。** 后续继续核对普通教义索引和静默添加原语，不以屏蔽原版通知代替根因修复。

归属：当前版本 GUI、输入 pin、产品版本和具体报告归本项目，复用框架文本投影与构建原语；索引与副作用排查方法待有结果后富化框架。公共 native runtime 仍绑定 `1.20.0.4`，本机暂无可调用 operator/gameplay MCP；实机前将补公共入口的官方 GUI 执行路径，不能注入失配 DLL，也不能沿用旧私有 launcher。

## 公共验收入口接入

本机原公共 runtime 的 native 部分精确绑定 `1.20.0.4`，而当前游戏已为 `1.20.1`；本机也没有 operator/gameplay MCP endpoint。框架新增公共入口的显式 `gui_only` 后备路径，已提交推送 `cf476f656b592190b818a04582434b11667ef87a`，合同在框架 `docs/ck3-mod-acceptance-gui-only.md`。它仍消费统一 manifest、任务总线/keeper、隔离 userdir 和真实游戏 SHA，不注入旧 DLL。离线8项、路由2项和原公共入口22项通过；没有据此授产品实机通过。

本产品提供 [业务 case 数据](../dev_tools/acceptance_products.json)，八个必要证据键覆盖本轮反馈、末槽、创建、文化上限及保存冷载。机器路径、全局 manifest 映射、旧存档与正式 staging pins 留本地配置。本轮公共 `plan` 已消费该产品，结果为 `NOT_RUN/business_pass=false`；不是业务验收。

归属：通用 GUI 后备执行、租约和证据判定属于框架，具体 case、正式产品和源存档属于本仓。没有扩大为通用宗教 AI 研究或把 GUI 通过宣称为 native capability 资格。

## 用户固定 1.20.0.4 后的目标绑定

用户在本轮明确安排本机通过 Steam 回到 `1.20.0.4`，并要求优先复用 native runtime、缺失能力尽可能补入框架。真实 EXE 为 `101040248` 字节，SHA-256 `98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518`，Steam build `25734779`。本任务没有自行切换游戏版本。

新增 [1.20.0.4 精确输入合同](../dev_tools/ck3_1_20_0_4_sources.json)，两个GUI按该原版重新投影，开发descriptor为版本11 / supported_version 1.20.0.4。[本次静态收据](evidence/bugfix-20261015-12004-projection.json)的来源、恢复、九语言格式、46文件清单和双构建均通过，仍为 `live_verified=false`。1.20.1的独立记录保持历史事实，不外推为本目标通过。

首个GUI后备分配号R0014未启动游戏：Steam窗口最大化导致新鲜位移帧未取得，随后版本切换使目标SHA失配。原分配、失败与过期claim的精确CAS释放留本地证据，不重新标为成功。当前没有CK3进程或屏幕占用。本轮重新接入原1.20.0.4公共native manifest；产品只提供业务case/fixture，缺少宗教观察或选择接口时优先补共享provider，不沿用GUI后备作为首选。

## 后续工作

教义空白、替换残留及通知仍在排查。当前未进行新实机、工坊上传或新增发布；不改变 v10 历史结论。

通知整改已形成 [静态候选](selector-notification-candidate-2026-10-15.md)：创建入口取消对源礼仪的额外写入，编辑保留安全准备；纯内部教义更新不再进入原版通知与宗教领袖effect，真实变化保持原版逻辑。两项投影回归及48文件双构建通过，实机仍待执行，不能据此宣称永久循环已经关闭。

## 1.20.0.4 原生业务 case 与独立冷载

新增 `native-october-reported-bugs` 与 `native-cold-reload`，通过公共入口的标准 adapter 三接口运行。原生场使用普通1066罗贝尔29829和独立资源夹具，仅给予100000虔诚，不预设被测信条、教义、宗教或文化。当前角色/礼仪/信仰/宗教与资源由实际MCP context/snapshot取证；候选及操作按可用typed能力优先，缺口保留后才用官方UI。

第一场八项业务事实以 `save_written` 收尾，记录实际存档pin和原生身份。第二场通过标准saved_campaign产品profile冷启动，要求前场真实normal-close通过、同份保存与正式产品清单、实际不同PID，再核对角色、日期、宗教身份、保存的信条/教义和通知。两个场次不互相冒充，同进程菜单读档不能授第二场通过。

`dev_tools/test_native_acceptance_adapter.py` 首次4项离线回归通过（0.138s）；新增冷载合同后5项通过（0.273s），覆盖真实共享profile准备、mock native run/verify、证据缺失/变更拒绝与新旧PID区分。命令为 `python -B -X utf8 dev_tools/test_native_acceptance_adapter.py --framework-root <framework> --runtime <native-runtime-mapping>`。未启动CK3，仍无业务通过。

归属：产品adapter、资源fixture、业务事实和冷载关系属于本项目；标准MCP、profile、keeper、正常退出与原生查询能力复用框架。只读确认了可复用的原共享R90闭场；R90自身业务RED保持。Steam当次黑屏经已有正常重启路径恢复，新位移帧人工读到离线；没有据重启ACK推断离线。
