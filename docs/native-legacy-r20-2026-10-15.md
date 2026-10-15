# R0020：发布前 v10 候选旧档的分支创建回归

**结论：本用例四项业务事实、实际保存和正常闭场通过；正式发布仍未开始。** 范围为 R0008 发布前 v10 候选存档在当前 48 文件候选产品中的合法分支创建，不授正式上传 v10、新局、直接编辑已有礼仪、独立冷载或整产品通过。

- `machine_id`: `bf-202609141645-5434332d4d`；本报告根据原 public-run、Root 审阅及保存回执绑定该机器，并于 `2026-10-15T11:03:42Z` 用公共 machine 命令核对。
- 完整场次：`bf-202609141645-5434332d4d--more-tenets-slots--R0020`；公共 case：`native-legacy-v10-edit`。
- 执行：`2026-10-15T08:53:15.896529Z` 至原 public parent wait 0 的 `10:50:01.818485Z`。CK3 PID 15228；语言简体中文。
- 目标：CK3 `1.20.0.4` / build `25734779`，EXE SHA-256 `98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518`；runtime007，框架冻结 `82e71018739ba112660d1784867ce5948521fb34`。
- [精简证据与 pins](evidence/native-legacy-r20.json) 保存 33 个原件引用及完整大原件位置；没有复制保存或截图入库。本次记录审计还核对了 34 个原始嵌套 pins，无不匹配。

## 保存来源与操作边界

原 R0008 保存为 91,083,139 字节，SHA-256 `ecc186cd5ac4623616521db4eb72edd15a8b4dc5c35ec5a27341096687e18e43`，日期 `1066.9.15`，actor 33339、Rite 151、Faith 28。其源码为 `b7dc3ef0809a795270bdc3c24769ba6a5c575b95`、版本声明 10、30 个文件；正式上传 v10 是 46 文件且源码、共同路径字节均有区别。[R8 准备说明](native-r8-candidate-preparation-2026-10-15.md)保留此界限。

原 R8 历史已经清除 `has_created_a_faith`，失败的最后草案没有提交。该历史夹具不能被描述为自然未改动的正式 v10 保存。本轮加载原字节，没有再改该标记、资源、人物、关系、政府、教义或信条，也没有挂新的资源夹具。

已保留实际能力缺口 `religion-action-capability-gap.json`：该 provider 有宗教只读查询，没有宗教导航、草稿选择和提交的 typed writer。实际选择和提交使用官方 GUI，native 负责前后当前状态观察、事件操作、保存和正常退出。不把官方 UI 操作外推为尚不存在的 typed 宗教写入能力。

## 四项实际业务事实

| 事实 | 原始观察及结果 |
| --- | --- |
| 原旧档身份加载 | 原生 actor/date/Rite/Faith 与原保存相符；就绪耗时 `893.233162` 秒，在 readiness 1800 秒内。 |
| 普通教义候选与唯一替换 | 性别选择器原始简中图可见男性主导、男女平等、女性主导三项，未复现该组空白。提交后目标当前 Rite 的性别组只有 `doctrine_gender_male_dominated`，旧 `doctrine_gender_equal` 不在该组当前选择中。 |
| 核心信条替换与旧项移除 | 原版分支创建成功，当前 Rite 从 151 变为 152。目标当前核心只有 `tenet_ora_et_labora`、`tenet_communal_identity` 两项，被替换的 `tenet_sanctity_of_nature` 不在新目标核心中。 |
| 通知收敛 | 三个实际创建事件实例经 native 后置条件推进 `3 → 2 → 1 → None`；继续日期后另观察 `79.8610948` 秒，三张定时原图及最终暂停原图均由 Root 审阅，未发现持续重复 `msg_rite_updated`，最终 active event 为 null。 |

这是合法“创建分支”的提交，**没有通过礼仪领袖直接 Edit**。新草稿由 Faith 主 Rite 93 初始化，其起点核心是共同体认同、自然圣洁；不是复制原当前 Rite 151 的苦修主义、自然圣洁。因而提交结果保留共同体认同有明确原生来源。原 Rite 151 作为旧实体继续存在，也不等于旧信条仍附着于新当前 Rite 152。

native 查询和保存分别区分当前 Rite 核心、Faith 主 Rite 核心、个人信条与已知/允许等状态。判定旧项移除使用目标当前核心及目标普通教义组，不把知识状态或父实体的项目当成重复核心。当前只覆盖一个普通教义组和一次 A→B；第二普通组、反向及连续替换仍待验收。

## 原生保存和通知归因

实际 `ck3_save_checkpoint` 完成固定 `save games/xar_checkpoint.ck3`，90,257,883 字节，SHA-256 `fd94f4f30475a5cc214678d6db50b2115b88f52686c6c37fccfc9974808edf0e`。只读 driver 校验 materialization、原文件字节、框架 bounded AST 以及同日暂停 native 查询，读回 `1066.10.9` / raw date `53144904`、actor 33339、Rite 152、Faith 28、Religion 8 和上述两项核心、唯一男性主导教义。它没有修改原档；这证明写入，不证明新 PID 冷载。

通知归因原件为 `artifacts/bugfix-20261015/queued-event-diagnosis/r20-001/report.json`。原 R8 保存已经包含两个到 `1066.9.16` 的 `faith_creation.1021` 队列项，分别对应旧 Rite 150、151；本次创建再产生其实际公告。事件正文使用保存的 `new_rite`，原版 widget 使用 founder 的当前 Rite，可出现正文旧名称与当前 widget 不同的表象。`.1021` 与上方 `msg_rite_updated` 是不同链；源码没有在这些选项内显式重新排程 `.1021`。

处理有限事件队列后，游戏由 `1066.9.16` 推进至 `1066.10.9`；观测时间点为 `10:19:07.945637Z`、`10:19:28.959134Z`、`10:19:53.504961Z`，最终暂停状态没有 active event 或 pending interaction。该有限窗没有复现永久循环；不据此宣称所有开关、取消、无修改确认、新局及冷载场景均已解决。

## 正常闭场与保留的不确定返回

原 native prepare/continue 请求返回 `dispatch_unknown_claimed`，即时回执没有把确认窗、退出或自动保存标为已验证。后续新鲜 native context 观察到实际确认窗；`disable_exit_autosave` 返回 `autosave_disabled`，`should_save=false`，Root 直接查看原 PNG 的未勾选框。

最终 `confirm_desktop` 的原回执仍为 `dispatch_unknown_claimed`，保留其 `orderly_exit_verified=false` 等即时字段；其官方 dispatch 第 2 项确实 invoked/handled。实际退出信用来自后续独立证据，而非该 ACK：

- CaseClient 保留的原 OS handle 对 PID 15228 得到 signaled / exit 0。
- 原 managed session 为 `exit_reason=process_exit`、code 0；原生清理证据完整、进程树消失、最终 inventory 为空、线程完成。
- 原 host PID 16700 的 Popen wait 0；public parent wait 0；`normal_close_qualified=true`。闭场子回执自身的 `business_pass=false` 保持原语义，不抹去产品四事实的 scoped business PASS。
- keeper 实际 wait 0 后，原任务于 `2026-10-15T10:58:04.915976Z` 经 CAS **6110** 释放，resources 为空。这里只描述该次闭场时的事实，不代表后来其他场次的资源状态。

## 日志、未完成项及归属

`error.log` 为 18,314 字节，66 条日志头：1 条本产品 `on_rite_updated` 重复 effect 提示；57 条原版宫廷场景无效 Character-4294967295 trigger；1 条无法找到 culture set；7 条 character 的 `GetActivityName` 错误。原文件已 pin，未清理或重写。重复 effect 的产品影响与其余日志归因仍须后续处理，不能称本场日志全净。

尚未授予：正式上传 v10 保存覆盖、新局主场八事实、直接 Edit、100 末槽/稀疏创建、文化上限实际行为、独立新进程冷载、全面通知回归和正式工坊发布。R19 原正式 v10 保存的合法性 RED 保留，[总计划](bugfix-plan-2026-10-15.md)逐项继续执行。

本包仅提交产品报告、证据索引及计划进度，没有改产品源码、adapter、catalog、框架、冻结工具或原件。通用保存、bounded parser、事件查询与原生正常退出继续归 `ck3_eternal_recurrence`；具体候选来源、UI/保存比对及此范围结论归本项目，不外推给 POD 或其他 mod。
