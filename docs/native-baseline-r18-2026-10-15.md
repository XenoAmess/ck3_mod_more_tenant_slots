# R18：v10 原生基线观察与实际失败（2026-10-15）

本场取得了1800秒窗口内的真实就绪、当前宗教与草案的原生读数，以及一个普通教义选择器的画面与草案替换证据。**公共用例仍为 RED，未完成提交、冷载、正常退出或产品业务验收。** 本记录只适用于 `more_tenets_slots_xa_dev` 的本场 v10 基线，不外推到整改候选或两个 POD 产品。

所有时间为 UTC；原游戏日志为本机 UTC+8。精确文件大小、SHA-256、查询步骤与汇总见 [小型证据清单](evidence/native-baseline-r18.json)。该清单只保存摘要和原件引用，不复制截图、大型通信日志、原生完整结果或存档。外置绝对路径仅为本机证据位置。

## 场次、实际输入与就绪

运行 ID：`bf-202609141645-5434332d4d--more-tenets-slots--R0018`；原 CK3 PID **6168**，connection generation **1**。使用简体中文、CK3 **1.20.0.4**（Steam build25734779），EXE SHA-256 `98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518`。

公共入口选定 runtime004，其 manifest SHA-256 为 `6e36f884a95986cca671411700eac94cfd2409630e71b81ee194c8df4ff28e98`；生产 DLL 为 `2229cdb1fd382460f059c32f1b3f139cf7503aeff42399cc9b7f4bc88c129c19`。正式输入来自 [v10 frozen manifest](../artifacts/workshop-v10/final-build-frozen/more_tenets_slots_xa_dev.manifest.json)，具体绑定以本场 prepared/frozen 原件为准。

| 原始事实 | 实际结果 |
| --- | --- |
| 冻结预算 | readiness **1800**、hold **900**、business timeout **2100**、command **300**、poll **0.5** 秒。 |
| 就绪开始 | `05:25:33.286717`，原 monotonic deadline `498177.2077232`，估算 UTC 截止 `05:55:33.286717`。 |
| 实际就绪 | `05:40:49.223110`，`READINESS_HOLD_OBSERVED`，用时 **915.9363791秒**，在原1800秒窗口内。 |
| 单次 Start | `05:30:20.802745` ACK；没有重试开始游戏。 |
| 玩家与场景 | 原生 actor **31254**、date_raw **53144328**、封建制、公国层级、primary_title_id **2230**。 |

启动期间资源标记恰好出现一次，失败标记为零；最后进入实际上下文前，host 等待两个相同业务身份、且 owner `pump_epoch` 严格推进的帧。早先 `WAITING_FOR_PAUSED_EVENT_FREE_OWNER_FRAMES` 不能解释为政府、层级或角色不符：当时尚未发起 campaign-root 查询，随后该门槛实际通过。

原适配器接着因 `initial_actor_id=29829` 抛出 `ValueError: Ordinary 1066 Robert initial actor not observed`，写入 [原错误收据](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0018/case-output/case-error-preserved.json)。[原角色截图](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0018/root-evidence/baseline-character-open.png) 显示阿普利亚公爵罗贝尔“狐狸”；本场原生ID为31254。不能仅因旧硬编码不等就认定选错人物，也不能删除这次适配器 RED。后续应核验实际书签、角色身份及本次原生ID绑定，而非直接沿用旧数字。

## 同一 PID 中已实际观察到的范围

适配器失败后，Root 使用同一受管进程与公共队列保留诊断，没有重放原用例。以下是局部观察，不能补签原八项业务合同。

| 证据 | 实际覆盖与边界 |
| --- | --- |
| `baseline-current-01` 三次查询 | 宗教 context、current tenets、current doctrines 均 `ok=true/available=true`，绑定 actor31254、日期53144328、`native:3`/public revision4/native revision3；实际 Catholic、rite0、faith13、religion8。 |
| 当前核心信条 | `current_rite.core_tenets` 为 `tenet_peace_of_god`、`tenet_apostolic_succession`、`tenet_communion`。另外的 effective 状态不是额外核心槽，不能把其存在当作“旧核心信条未删除”。本场没有实际替换核心信条。 |
| 草案 groups | 普通候选弹窗打开前未物化 category（slot=-1/cache=0）；性别选择器打开后 slot10、`doctrine_gender`、cache3。草案 selected slots 共130项，该数字不是文化传统容量。 |
| 普通教义候选 | 原生 full doctrine choices 返回130个草案slot；性别组男性主导、男女平等、女性主导均 `passed_shown=true`。前两项可选，女性主导因未掌握且无Prophet不可选。 |
| 普通 picker 画面 | [原图](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0018/root-evidence/baseline-gender-popup.png) 实际显示上述三项，故**本场这一性别选择器没有复现空白**。不能据此宣布全部普通教义或用户旧存档的问题消失。 |
| 草案同槽替换 | 官方GUI点击男女平等后，[原图](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0018/root-evidence/baseline-gender-equal-after.png) 与 `baseline-after-gender-0` 一致：slot10 selected由 `doctrine_gender_male_dominated` 改为 `doctrine_gender_equal`，旧项 `currently_selected=false`、新项为true。这里只证明草案选择替换。 |
| reform 原生读取 | `baseline-after-gender-1` 成功读到已打开草案、成本与最终门槛；`can_create_rite=false/can_edit_rite=false`，名称、形容词及信徒单复数为空等原生原因仍在。没有实际提交，也没有提交后的 current-rite 读回。 |

实际宗教工具清单是只读查询，没有打开宗教窗口、选择草案或提交礼仪的专用写操作；Root 留存 [实际能力缺口](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0018/root-evidence/religion-action-capability-gap.json)，再经官方GUI操作并用原生读回。`ck3_open_character_window_v1` 本场实际报不支持，原失败也保留。

v10 [文化 defines 原件](<../artifacts/workshop-v10/final-build-frozen/more_tenets_slots_xa_dev/common/defines/More tradition slots.txt>) 仍含 `DEFAULT_MAX_TRADITIONS = 10000`。这是该基线的**静态事实**，本场未验证文化UI上限，也没有证明整改候选已正确分离信条与传统容量。

本场未覆盖：核心信条替换、末槽选择、稀疏礼仪实际创建或编辑提交、旧教义提交后删除、持续通知收敛、写存档与新PID冷载。没有原业务检查点签核，不授这些项目或产品发布 PASS。

### 创建资格的实际拦截

同一 reform 原生回包还明确返回 `not_is_puppet_action_valid_first` 对应的缺少可创建礼仪之傀儡理由。实际费用4500、虔诚100150、`has_enough_piety=true`，宗教 context 的 `player_piety_devotion_profile.effective_level=5`；因此不是资源或奉献等级不足。当前安装 `00_religious_triggers.txt:3154` 的 `can_create_rite_trigger` 对符合神权制、世俗角色及神职傀儡类型条件者，要求有效 `puppet_trigger_can_create_rite`。正常路径是通过领地司祭的 `make_clerical_puppet_interaction` 并获得实际接受；填写四项名称仅消除名称错误，不能替代这个条件。候选不修改该原版合法性，也不在测试夹具中直接设置傀儡或被测教义。

已只读核对该文件的Steam内容来源：当前ACF对应depot1158311/manifest5078208590259867811，其本机缓存manifest所列 `game/common/scripted_triggers/00_religious_triggers.txt` 为88549字节、SHA1 `6aca0fabfb7b96649d4e64cb20d9a8a6bf2d4cd5`，与当前文件一致；缓存manifest SHA-256 `948e302219df401ec40d6f49b1f14b51ffcdeac38f39980aa85cb6ae01b6929d`。文件中 `empire_faith_gate` 字样不构成机器注入证据。本次未在线验证整个安装，未修改游戏文件。

## 实际退出与资源闭场

原 hold 截止为 **`05:55:47.096181`**（epoch `1792043747.0961807`）。适配器失败后，原 CaseClient 已持有 PID6168 的同步查询句柄并进入 normal/manual Quit 等待。最终没有 `normal-quit-root-result.json`；尝试的 `exit-context-01` 被公共队列以 `Original host normal Quit reserve reached` 拒绝，未 dispatch 原生退出查询或确认，不能称为 native 正常退出尝试成功。

| 终态原件 | 实际结果 |
| --- | --- |
| public run 原完成回执 | 退出码 **2**，`05:55:47.217739` 完成，产品维持 `RED_OR_INCOMPLETE`。 |
| 原 normal-close 结果 | `normal_close_qualified=false`、`native_zero_proof=null`、Root review=null；截止当时保留句柄尚未signal、exit_code=null、OS0=false。这份较早收据不改写为稍后的退出结果。 |
| 原生最终报告 | `status=RED`，`exit_reason=stop`，shutdown CK3 exit **1**；`managed_session_done/managed_session_thread_finished/cleanup_ok=true`，最终进程清单为空。 |
| 原 host retained wait | `05:55:53.090593` 实际返回 **1**。 |
| keeper 原父进程 wait | `keeper-process.json` 中原 PID18240实际返回 **0**；thread已结束、failure/entry_error=null。操作者终端session编号不充当OS PID。 |
| CAS释放 | **6002**，`06:01:30.024169`，task=done、resources=[]。 |

因此本场证明失败资源已闭合，**没有正常GUI Quit、retained OS0、native0或业务PASS信用**。原900秒hold到期的 managed stop 与角色硬编码失败均保留，不以稍后成功清理改判。

## 后续范围与归属

下一轮计划使用 readiness **1800**、hold **7200**、business timeout **10800** 秒，为已观察到的操作时长留出空间；这只是后续准备计划，不修改 R18 的900/2100秒原预算或失败。继续复用本场已证明适用的读取能力，补实际身份绑定后执行必要产品路径，并提前完成原生/官方GUI正常退出。单独的 cold-reload case 仍需真实保存来源和新PID，不能由本场草案替换代替。

公共 readiness、查询与生命周期机制归 `ck3_eternal_recurrence`；本报告、v10局部观察和具体证据清单归独立产品。本次仅只读核对原件并新增这两份报告文件，没有重新测试、启动游戏、操作屏幕、提交队列或修改适配器/框架。
