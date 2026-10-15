# R17 / R18：native 验收启动与闭场记录（2026-10-15）

本记录仅涉及 `more_tenets_slots_xa_dev` 的真实已发布 v10 基线、CK3 **1.20.0.4**、`simp_chinese`。R17 已失败并完成资源闭场；R18 在本文记录时仍在进行中，使用新的 1800 秒就绪窗口。本文不授予宗教功能、正常退出、native OS0 或发布通过资格，也不将结论外推到 POD 产品。

除明确标为本地时间的 CK3 日志外，下列时间均为 UTC。外置绝对路径是本机证据位置，不是工具或其他机器的固定配置。

## R17：原始 400 秒窗口确实超时

运行 ID 为 `bf-202609141645-5434332d4d--more-tenets-slots--R0017`，使用共享 runtime003、keeper `20261015-mts-a03`、screen task `common-mts-12004-20261015-a03`。原始冻结参数和回执保持原样，没有回写为后续的 1800 秒策略。

| 原始事实 | 结果及证据 |
| --- | --- |
| CaseClient 就绪窗口 | `04:38:22.309222` 开始，预算 400 秒；估算截止 `04:45:02.309222`。见 [readiness-window.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/case-output/readiness-window.json)。 |
| CaseClient 实际结果 | `04:45:02.330956` 返回 `READINESS_TIMEOUT`，elapsed `400.0214743` 秒；当时 host 仍处于 `native-frontend-robert-bootstrap`。见 [readiness-window-result.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/case-output/readiness-window-result.json)。 |
| 单次新游戏后的 host 就绪观察 | `04:49:57.626245` 结束为 `FAILED_AFTER_SINGLE_START_NO_RETRY`；目标身份未证明，未重新提交开始游戏。最后一条观察仍为 `map_ready=false`。见 [native-report.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/native-report.json) 的 `frontend_fixture_business_context` 及 [原始观察日志](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/native-report.frontend-observations.jsonl)。 |
| 业务入口 | public run 实际退出码 2；原始错误为 `Original case readiness budget elapsed`，已提交步骤没有重放。见 [public run 原始完成回执](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/actual-public-run-command.json) 和 [case-error-preserved.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/case-output/case-error-preserved.json)。 |

后续现场确实到达地图；现场汇总的冷启动至地图耗时约 **734 秒**，已超过原始窗口。该近似值描述晚到的地图观察，不是原始就绪验收成功时间，也不是 `debug.log` 中一个独立 duration 字段。

[R17 debug.log](C:/workspace/ck3-common-runtime/cases/mts-v10-baseline-20261015-003/state/profile/logs/debug.log) 分别记录了本地时间 `12:43:09` 的前端启动耗时 `272.750707 seconds`、`12:50:13` 的 `Setup completion (history loaded): 427.214542 seconds`，以及后续地图阶段日志。这些阶段耗时口径不同，不能把其中一个数字当成整个冷启动耗时。[现场地图截图](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/root-evidence/cleanup-map.png) 只证明后来进入地图，不能补算在原截止时间内通过。

## R17：清理完成，正常退出未完成

原始就绪失败后仅续接清理，没有重跑业务。清理过程中曾持有 CK3 进程的同步查询句柄，但最终 GUI 退出未能赶在原 hold 截止前完成。[cleanup-only-resume-result.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/case-output/cleanup-only-resume-result.json) 和 [normal-close-result.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/case-output/normal-close-result.json) 保留 `normal_close_qualified=false`、`native_zero_proof=null`、`business_pass=false`。

原 hold/托管截止于约 `05:05` 停止游戏。终态 [native-report.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/native-report.json) 为 `RED`，原始 host 异常仍在；同时满足：

- `managed_session_done=true`、`managed_session_thread_finished=true`、`cleanup_ok=true`。
- `session.report.exit_reason="stop"`；其 `shutdown.ck3_exit_code=1`。
- native shutdown 的 `tree_gone=true`、`cleanup_proven=true`、最终 job 活跃进程数 0，控制文件和最终进程清单满足清理合同。
- [原始 host Popen wait](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/host-original-process-exit.json) 于 `05:05:01.245568` 返回 1。

CK3 的退出码 1 来源是 native shutdown 回执，**不是**持有句柄的 OS0 证明。较早的 [actual-retained-handle-os-exit.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/case-output/actual-retained-handle-os-exit.json) 仍为 `signaled=false`、`exit_code=null`；该原件没有被改写成最终退出证明。

[keeper 父进程实际 wait 回执](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0017/keeper-actual-parent-exit.json) 返回 0，keeper 线程已结束，`failure=null`、`entry_error=null`。随后 [CAS release 原始回执](../artifacts/bugfix-20261015/native-v10-baseline-003-resource-release.json) 于 `05:08:43.503926` 完成序号 **5984** 的释放，task 为 `done`，资源为空。

因此 R17 的结论为：**失败场次的进程、托管线程和现场资源已闭场；正常 GUI 退出、native OS0、宗教业务和发布验收均未通过。**

## 下一场的资源准入与资格边界

[R17 资源准入复核](../artifacts/bugfix-20261015/native-v10-baseline-003-resource-admission.json) 直接调用框架既有 `closed_session`、`native_cleanup_closed`、`previous_session_closure`、`closed_lease`、当前 screen owner 和进程清单检查，得到既有路线 `previous-shared-managed-session`。原 host、CK3、keeper 身份均已结束，当前现场无占用。

该复核明确记录 `native_report_read=true`、host wait 1、native `stop`、CK3 shutdown exit 1，并保留所有失败资格。这里的 “closed” 仅说明资源可以交给下一场，不表示正常退出或业务通过。它不使用强制声明 `native_report_read=false`、host wait 0 的历史 `lyd.actual-failed-resource-closure.v1` 路线，也无需新增例外；下一次分配使用 R17、a03 和 CAS5984 作为前驱，省略 `--previous-failure-close`。

共享 runtime004 只接入新用户策略的 Python 就绪预算变更，保留 runtime003；生产 DLL 完全复用，SHA-256 为 `2229cdb1fd382460f059c32f1b3f139cf7503aeff42399cc9b7f4bc88c129c19`。

- [runtime004 READY](C:/workspace/ck3-common-runtime/20261015-native-religion-004/READY.actual.json) 的 `live_qualified=false`；[实际 wrapper/profile 静态预检](C:/workspace/ck3-common-runtime/mts-religion-native-20261015-001/full-wrapper-profile-preflight-004-001/RESULT.actual.json) 通过，未执行 engine main。
- [选定源码的预算校验](C:/workspace/ck3-common-runtime/20261015-native-religion-004/READINESS-POLICY.actual.json) 验证 400→1800、1800→1800、2400→2400，host 默认值为 1800；不追溯重分类 R17。
- [两项当前宗教查询离线资格](C:/workspace/ck3-common-runtime/mts-religion-current-native-20261015-001/QUALIFICATION-004.actual.json) 为 `OFFLINE_QUALIFIED_DEFENDER_REGISTRATION_RED`：native 2 case / 41 checks 与官方 SDK whole-wire 测试通过；Defender WMI 登记失败另行保留，没有重试或宣称登记成功。这份 `QUALIFICATION-004` 是离线查询资格回执，不是 R18 实机通过回执。

## R18：1800 秒窗口进行中

运行 ID 为 `bf-202609141645-5434332d4d--more-tenets-slots--R0018`，使用共享 runtime004、keeper `20261015-mts-a04`、screen task `common-mts-12004-20261015-a04`。本节只记录启动时已产生的原件，不预测终态：

- [host-started.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0018/host-started.json) 记录 host 于 `05:25:33.183981` 启动；冻结参数为 `--readiness-timeout 1800`，native session 随后于约 `05:25:38` 开始。
- [readiness-window.json](C:/workspace/ck3-common-runtime/runs/bf-202609141645-5434332d4d--more-tenets-slots--R0018/case-output/readiness-window.json) 记录 `05:25:33.286717` 开始，预算 1800 秒；估算截止为 `05:55:33.286717`，实际判定使用原始 monotonic deadline。
- 本记录时 R18 仍在正常加载与就绪等待中。未在本文记为实机通过、正常退出通过或业务通过；后续结果须引用该场次实际终态回执另行记录。

## 归属与本次文档工作

通用预算策略、native 查询和正常退出源码校验归 `ck3_eternal_recurrence`；本文件记录本产品真实 v10 场次与证据，归独立产品仓库。未为本记录重复启动游戏、提交队列动作或重复运行测试，未修改冻结框架、适配器或既有文档。
