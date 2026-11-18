# CK3 最新版测试验收计划

范围仅 `more_tenets_slots_xa_dev/`；上一公开版 v11。实机统一 `simp_chinese`，其余支持语言仅静态校验。每次运行记录机器、时间、游戏版本/build/EXE SHA、产品文件清单、框架/runtime 身份及退出事实。

| 层次 | 必要检查与通过条件 |
| --- | --- |
| 安装 | 官方默认分支实际选中，下载/待更新清空，launcher 与 EXE/build 绑定；选择 ACK 不作下载完成 |
| 来源与投影 | 全部 pinned 原版依赖已审查，生成结果可逆恢复新版原文；原生费用/过滤/同名顶层钩子副作用保留 |
| 产品静态 | 100 核心槽及 ZZ 镜像一致；普通教条候选不被兼容元数据挤出；尾空保持原生空槽；文化上限随原版；所有脚本 BOM/结构/引用正确 |
| 本地化 | 支持语言格式、UTF-8 BOM、结构、重复键及键集覆盖正确；不新增其他语言实机 |
| 构建 | allowlist 排除工具、夹具、报告和内层 Workshop ID，双构建 manifest/ZIP 一致，产品版本与正式 tag/commit 绑定 |
| 新局业务 | 公共受管入口；普通教条候选与替换、核心信条替换、第100槽选择与取消/重开、真实信条加尾空创建、原版文化上限、有限礼仪通知、保存后真实教条语义均符合合同；1.21罗马礼原生三个core，本轮按三core加97尾空执行，历史两core案例另记NOT_RUN |
| 冷载 | 独立新 PID 恢复本轮保存，核心信条/普通教条/空槽一致，原生费用及面板正常；正常退出与资源清理独立记录 |
| 发布 | 同一条目3182367229更新成功，完整 Notes/描述冻结及匿名精确读回，1.21标签来自正式 descriptor 与框架单一 registry，永久 changelog commit/push |
| 缓存 | Steam 实际下载文件 exact match 正式树；CK3 实际 mounted/loaded 此缓存即可，不重复业务；正常退出、Steam离线、资源释放 |

优先复用原产品 adapter 及框架 `tools/ck3_mod_acceptance.py plan/prepare/allocate/preflight/run/verify`。先检查 `open_kaishek` 可覆盖的确定性子集；缺席/不适用如实记录。新版 native/MCP 绑定缺失归环境/能力缺口，不将旧 exact-build DLL pin 改为新 EXE 后强行运行。实机之外独立完成原版差异、源码、单元回归及构建。

初始结果全部 `NOT_RUN`。具体结果随报告追加，静态通过不代表实机或发布通过。归属：产品场景与证据留本仓，通用能力及方法考虑富化框架并记录原因。
