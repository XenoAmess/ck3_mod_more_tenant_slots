# 2026-10-15 用户反馈整改记录

**发布里程碑：** [v11已于2026-10-16正式更新](workshop/publication-v11.md)，tag指向`d1c9deee5c0214f9418c8df821a8ac9f3f97d334`。原生上传result1、完整匿名描述／Notes唯一条目1792089226、实际SDK新缓存48文件严格匹配及发布后离线恢复通过。新缓存加载[R24](native-cache-r24-2026-10-16.md)在游戏启动前因共享profile schema拒绝而RED：host1/public2、无native-report、CK3为空、keeper0/CAS6345释放；不授normal/native0。整体`CACHE_LOAD_PENDING/release_complete=false`，后继缓存加载及最终闭场仍待。

执行清单见 [计划](bugfix-plan-2026-10-15.md)。本轮起始公开产品是 [v10](workshop/publication-v10.md)，已于 2026-10-03 发布；源码整改、当前版本实机与下一次正式发布分别记账。

**最新冷载进度：** [R23独立冷载](native-cold-r23-2026-10-16.md)通过：新PID12944恢复R22原binary，首帧精确actor31254/date53145144/Rite150/Faith13/Religion8，当前四核心和Equal/Pluralistic唯一匹配；92.327955秒有限通知窗四原图经Root审阅无顶部重复提示。007原生退出与独立OS/native/host/public/keeper全0、CAS6321释放，公共verify的业务与normal/cold均通过。[索引](evidence/native-cold-r23.json)顶层明确`case_acceptance_pass/normal_close_qualified/independent_cold_load_pass=true`；v11已上传公开，实际新缓存48文件严格匹配；缓存菜单加载与最终闭场仍待。

**新局主场范围：** [R22新局主场](native-main-r22-2026-10-16.md)在机器`bf-202609141645-5434332d4d`通过八项业务事实、一次binary SAVE及离线语义读回、官方GUI正常闭场：两普通候选非空且替换唯一，PeaceOfGod旧核心移除，实际slot99及稀疏四核心创建，默认文化4/6，有限通知收敛。原host唯一failed step为未暂停的只读事件查询被守卫拒绝，原statusRED/实际返回1保持；UTF8公共verify后继实际0、业务及normal pass，原OS/nativeprocess_exit0/fullcleanup/public0/keeper0并CAS6290释放。native fresh Quit因`-continuelastsave`参数未支持而unavailable，不授其动作资格。R23另用007的显式`-loadsave`路径，未升级007或改写前场原件。[R22索引](evidence/native-main-r22.json)保留94个pins与52项嵌套核对。

**R21历史RED保持：** [R21](native-main-r21-2026-10-15.md)原业务窗口超时、第一阶段GAP、没有保存；public wait2、normal-close=false、保留OS0=false。native停止清理、host0、keeper0与CAS6197分别成立，不冒充正常Quit；后继六小时预算没有追改其原期限。

**保留的限定通过：** [R20发布前v10候选旧档回归](native-legacy-r20-2026-10-15.md)四项业务事实与实际保存通过：合法创建分支151→152、普通性别组唯一替换、目标核心旧项移除及79.861秒有限通知收敛；public/host/原OS/native/keeper正常闭场，CAS6110释放。执行机器为`bf-202609141645-5434332d4d`，精确原件见[证据索引](evidence/native-legacy-r20.json)。来源是R8未发布30文件v10候选且有历史标记夹具，不授正式上传46文件v10、新局、直接Edit、独立冷载、100槽/文化或整产品通过。原[R19正式v10旧档](native-legacy-r19-2026-10-15.md)受原版合法性限制的业务RED保持；[R18](native-baseline-r18-2026-10-15.md)等同样保留历史事实。当前工坊已更新v11，R20的限定范围不因此扩大；下文1.20.1及早期未实机文字描述对应历史阶段。

## WP1：信条与文化传统分离

状态：**静态通过；R22默认上限4/6实机通过，完整文化行为及最终缓存加载闭环仍待**。

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

R20已完成发布前候选旧档的代表性创建分支回归；R22进一步完成当前候选新局两个普通教义组、核心旧项移除、实际第100槽及稀疏创建、文化默认4/6、有限通知、保存和正常闭场；R23已将该实际保存经独立新PID冷载，四项恢复事实及正常闭场通过。正式上传v10来源的合法性限制、直接Edit、反向/连续替换、完整文化行为及更多通知路径仍须继续；v11已完成工坊上传、匿名全文／Notes和实际新缓存匹配，缓存菜单加载及最终闭场仍待，不改变v10历史结论。

通知整改已形成 [静态候选](selector-notification-candidate-2026-10-15.md)：创建入口取消对源礼仪的额外写入，编辑保留安全准备；纯内部教义更新不再进入原版通知与宗教领袖effect，真实变化保持原版逻辑。两项投影回归及48文件双构建通过；R20有限窗79.861秒、R22新局创建后87.425699秒、R23独立冷载后92.327955秒均未见顶部信条更新持续重复，R22与R23各四张定时原图有Root直接审阅。有限路径不证明永久循环在所有场景均已关闭。

R20日志保留66条日志头，包括本产品1条重复`on_rite_updated` effect提示、宫廷场景/无效character及活动名错误；没有授日志全净。退出prepare/continue/confirm的原即时`dispatch_unknown_claimed`也保留，正常退出只由后续确认窗和未勾选PNG、原保留句柄OS0、native清理及真实host/keeper wait0成立。详情及归属见[R20报告](native-legacy-r20-2026-10-15.md)。

## 1.20.0.4 原生业务 case 与独立冷载

新增 `native-october-reported-bugs` 与 `native-cold-reload`，通过公共入口的标准 adapter 三接口运行。新局场使用普通1066罗贝尔，按本场native bookmark/角色绑定并由Root核对名称头衔，不硬编码历史运行时ID29829；独立资源夹具仅给予100000虔诚，不预设被测信条、教义、宗教或文化。当前角色/礼仪/信仰/宗教与资源由实际MCP context/snapshot取证；候选及操作按可用typed能力优先，缺口保留后才用官方UI。

第一场八项业务事实以 `save_written` 收尾，记录实际存档pin和原生身份。第二场通过标准saved_campaign产品profile冷启动，要求前场真实normal-close通过、同份保存与正式产品清单、实际不同PID，再核对角色、日期、宗教身份、保存的信条/教义和通知。两个场次不互相冒充，同进程菜单读档不能授第二场通过。

`dev_tools/test_native_acceptance_adapter.py` 首次4项离线回归通过（0.138s）；新增冷载合同后5项通过（0.273s），覆盖真实共享profile准备、mock native run/verify、证据缺失/变更拒绝与新旧PID区分。命令为 `python -B -X utf8 dev_tools/test_native_acceptance_adapter.py --framework-root <framework> --runtime <native-runtime-mapping>`。上述离线包当时未启动CK3，不授业务通过；后续R22实机与其独立记账。

归属：产品adapter、资源fixture、业务事实和冷载关系属于本项目；标准MCP、profile、keeper、正常退出与原生查询能力复用框架。只读确认了可复用的原共享R90闭场；R90自身业务RED保持。Steam当次黑屏经已有正常重启路径恢复，新位移帧人工读到离线；没有据重启ACK推断离线。
