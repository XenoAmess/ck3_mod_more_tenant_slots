# R0021：新局主场超时，业务与正常闭场 RED

**结论：本场未完成主场验收，没有保存，也没有正常 Quit 资格。** 部分初始观察保留；不得据 native 顶层 `GREEN`、清理成功或宿主返回 0 改写成业务通过。[R20 的限定旧候选存档通过](native-legacy-r20-2026-10-15.md)保持原范围。

- `machine_id`：`bf-202609141645-5434332d4d`；场次 `bf-202609141645-5434332d4d--more-tenets-slots--R0021`。
- 公共 case：`native-october-reported-bugs`；本场任务 checkout `3e99036b6a33e8b6278a5b8308316402e1f338da`；实际 provider 仍为不可变 runtime007，加载源以其原始 source-index 为准，不把任务 checkout 的后续知识库变化冒充已加载能力。语言为 `simp_chinese`。
- CK3 `1.20.0.4` / Steam build `25734779`；EXE SHA256 `98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518`。CK3 PID 17256。
- 原 public parent 从 `2026-10-15T11:30:28.183511Z` 执行，最终在 `13:43:49.713250Z` 实际 wait **2**。原预算为 readiness 1800、hold 7200、总体 timeout 10800 秒。
- [证据索引](evidence/native-main-r21.json)记录原始命令、155 个原件 pins、原 native 查询、PNG/映射回执、超时、清理及资源释放；未复制大截图或存档入 Git。

## 已取得的有限事实

| 观察 | 原件支持与界限 |
| --- | --- |
| 实际新局身份 | 本场 native 选择／启动和角色图绑定罗贝尔，实际 actor 为 31254，日期 raw 53144328，当前 Rite 0、Faith 13、Religion 8。不是把历史运行时 ID 29829 换成新的硬编码常量；主场八项事实仍未完成。 |
| 文化上限显示 | 原始简中 `r21-culture-cap-tooltip.png` 显示诺曼文化传统 **4/6**，Root 与报告复核者直接查看。未进行新增传统、时代增益或旧档超上限保留测试，不授完整文化行为通过。 |
| 原版合法傀儡交互 | 原界面向领地司祭发送合法交互，确认窗显示接受及 100 虔诚费用；原生独立 snapshot 从 100150 降至 100050，差额为 100。初始资源夹具只增加 100000 虔诚，未预设被测信条、教义或宗教关系。本次实际交互通过官方 GUI 执行。 |
| 创建草案已打开 | 新鲜 native `current_creation_window` 可见且取得草案；`can_create_rite=false` 的理由只有名称、形容词、信徒单数、复数四项为空，未再出现缺傀儡理由。`can_edit_rite=false` 另有非礼仪领袖理由，不授直接 Edit 资格。 |
| 初始草案内容 | native 观察 100 个信条槽，前三项为 `tenet_peace_of_god`、`tenet_apostolic_succession`、`tenet_communion`；余槽为空。草案费用 4275 虔诚且资源足够，没有实际支付创建费用或提交。观察到槽向量不等于已选择末槽。 |

虔诚的三个独立观察点保存在 MCP wire 原件中：`11:41:25.336257Z` 为 150；资源夹具后 `11:43:37.750971Z` 为 100150；原版交互后 `13:02:52.548512Z` 为 100050。上述差额和 UI 交互只支持有限前置条件进展，不替代礼仪创建、教义或信条替换的后置条件。

## 未完成项

Root 的第一业务阶段仍为 **GAP**。名称尚未填写，没有新的礼仪创建提交；普通教义候选／唯一替换、核心信条替换及旧项移除、实际末槽选择、稀疏布局创建和通知回归均未完成。native 普通教义查询与初始草案读取不是这些操作的通过证据。

没有 `save_written` 或有效 R21 checkpoint；检查该隔离 profile 时 `save games` 目录不存在。因此不能从本场构造“已保存续行”或独立冷载通过。历史 `r21-main-saved-continuation-plan-001.json` 是设计稿，其 `WAIT_FOR_R21_SAVE_NORMAL_CLOSE_AND_RELEASE` 条件没有满足，保留原文，不冒充实施结果。

## 原超时与退出事实

原 hold deadline 为 `13:43:49.550518Z`，其 900 秒正常退出预留从 `13:28:49.550518Z` 开始。原 `case-error-preserved.json` 保存：

```text
TimeoutError: Original normal Quit reserve reached; pending Root phase remains GAP
```

Root 未执行本轮实际正常 GUI Quit。`manual-quit-awaiting.json` 和 `normal-quit-awaiting.json` 是等待／授权记录，不是已执行的退出动作；没有最终 Root Quit 回执。原 `normal-close-result.json` 为 `normal_close_qualified=false`，原保留 OS handle 为 `signaled=false / exit_code=null / actual_retained_os0=false`。

后续清理须分别记账：

- native session 于 `13:43:52.339914Z` 结束，`exit_reason=stop`、session `process_exit_code=null`；shutdown 记 `ck3_exit_code=1`、`cleanup_proven=true`、进程树消失且 final inventory 为空。原 native 顶层 `GREEN` 是其宿主／清理结果，不授正常 CK3 退出或产品通过。
- 原 host Popen 于 `13:43:53.831487Z` 实际 wait 0，`normal_ck3_exit_inferred=false`；与 public wait 2、保留 OS0=false 同时成立。
- keeper 原 parent wait 0；其报告时间为 `14:09:51.676324Z`。原 task 于 `14:10:05.533074Z` 经 CAS **6197** 释放，resources 为空。
- 后补的新鲜进程盘点原件实际时间为 **`14:12:20.271366Z`**，`ck3_processes=[]`。这是当时资源观察，不倒签到 Root 未持久化的 14:09 观察，也不授 normal-close/business PASS。

## 下一轮与归属

未来 MAIN/COLD 改为 hold 21600、timeout 25200 秒，详见[预算策略](native-main-cold-budget-policy-2026-10-15.md)；readiness 1800 和独立退出预留继续执行。该政策只约束未来新场，不延长 R21 原 deadline，不使原失败变为成功。R22 在本报告时为后继新场准备，尚无本报告授予的业务或正常退出信用。

下一主场仍需实际完成全部必要事实并写入保存，再满足正常闭场与独立新 PID 冷载前置条件。R20 的发布前 v10 候选旧档分支创建、唯一性、有限通知及保存／正常退出通过不被本场 RED 撤销，也不能填补本场缺口；正式工坊版本仍为 v10，本候选未发布。

本包只更新报告、证据与整改计划；没有修改产品／框架代码、GUI、冻结运行时、原存档或原回执，没有启动游戏。具体 UI、来源与验收事实归本产品；通用 runtime、正常退出及任务总线能力继续复用框架。
