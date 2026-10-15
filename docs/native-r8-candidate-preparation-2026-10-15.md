# R0008 未发布 v10 候选存档：离线准备记录

2026-10-15，本包仅完成保存来源校验、公共 prepare/plan 和完整 host 静态预检。未分配运行资源、未启动 CK3、未操作屏幕、未修改 `machine.local.json`。实机业务仍为 **NOT_RUN**。

## 来源与适用范围

R0008 原文件为 `artifacts/bf-202609141645-5434332d4d--more-tenets-slots--R0008/userdir/save games/autosave_exit.ck3`，91,083,139 字节，SHA-256 `ecc186cd5ac4623616521db4eb72edd15a8b4dc5c35ec5a27341096687e18e43`。原 SAV0100 文本的版本为 1.20.0.3，body/meta 日期均为 `1066.9.15`，实际 played/current actor 为 33339，Rite 151、Faith 28。原存档保持原字节，不挂新的资源或状态夹具。

其原 session 绑定源码 `b7dc3ef0809a795270bdc3c24769ba6a5c575b95`、声明版本 10、30 个产品文件。这是**发布前候选**；正式上传 v10 的 manifest 有 46 个文件，源码为 `da4b579659ebb4de397672b833369e95fdbd03c6`，并存在共同路径字节差异。不能将本候选的通过外推为正式上传 v10 存档兼容通过。

原 R0008 历史已用控制台清除 `has_created_a_faith`，失败的最后草案没有提交。此历史夹具来源完整保留在 inspection、原粘贴回执和 [R0008 历史报告](evidence/live-R0008.json)；本轮不再次修改标记、人物、关系、政府、资源、教义或信条。没有创建标记只排除一个已知条件，实际创建/编辑、独特性、命名和费用合法性仍须实机查询。

`date_raw=53144328` 来自已闭场 R0019 的同日、精确 1.20.0.4 native 查询锚点。它不是 R0008 的直接 native 时钟读数，也不是离线 parser 解码所得；未来加载必须重新核对实际 snapshot 和 Root 所见日期。

## 产品适配与验证

`legacy_native_acceptance_adapter.py` 保留原 R0013 inspection 路径，新增对真实 `mts-legacy-save-candidate-offline-inspection-v1` 报告的消费，不转换或伪造旧 schema 的 PASS。它先复用框架完整原字节保存读取、player records 和 bounded parser，独立读取实际 actor/Rite/Faith/date；再核验五个 bounded record 的范围、键、SHA 和完整 AST 消费，原 session/source commit、历史夹具、已发布 manifest 及实际 native 日期锚点。准备结果携带全部来源限制，`published_v10_compatibility_credit=false`。

相关离线测试实际运行 11 项：10 项通过，需显式机器参数的完整 host 集成项默认跳过。新增测试覆盖真实双 schema、候选/正式版本范围区分、历史夹具披露、伪造 bounded record 和不匹配日期锚点拒绝。随后独立执行真实 R0008 输入的公共 prepare、公共 plan 和 selected-host `dryrun`，三个原 Python 进程均 exit 0。

当前目标产品是 48 文件候选包；标准准备映射 54 个 profile 输入。runtime006 的实际 wrapper 静态 profile 阶段完成，底层 host main 未执行，`game_started=false`、`normal_exit_qualified=false`、`business_pass=false`。预算为 readiness 1800、hold 7200、case timeout 10800、command timeout 300、poll 0.5，Root normal Quit reserve 900 秒。

机器外置根目录为 `C:/workspace/ck3-common-runtime/cases/mts-r8c6-001/`，输入及结果未复制进版本库：

| 文件（相对外置根） | 字节 | SHA-256 |
| --- | ---: | --- |
| `inputs.json` | 2588 | `7677a2f305bdaa389d45e96b2984429e589865134f825d3a501d93164b705b1d` |
| `prepared/prepared-case.json` | 50873 | `c0cc941b76efde08613a7b6fe6153418e730f412a898ef9a670f35c8aeafce8d` |
| `full-host-static-preflight/RESULT.actual.json` | 1678 | `2e3163a2432e8625149c358f190a7a090b5b97b6213a7241160861d04cdb2f2e` |
| `STATIC-READINESS.actual.json` | 8422 | `b9985201cf032ac9340031018941e4f865916380baf657b9bcedc993cf766ca4` |

汇总内逐项 pin `PREPARE-PROCESS.actual.json`、`PLAN-PROCESS.actual.json`、`FULL-HOST-PROCESS.actual.json`，各自保留实际 argv、cwd、exit 0 和 stdout/stderr pins。原检查报告为 `artifacts/bugfix-20261015/legacy-save-candidates/r0008-inspection-001/inspection.json`，13,059 字节，SHA-256 `dfa2db4f79ca8ba362b98aabff357f59f53a89409062fadc2286227fa3b22c0b`。

## 007 就绪后的重新准备

1. 等 native agent 明确 runtime007 READY，并核对其真实 manifest/READY pins。006 本轮结果只证明其原静态路径，不转换为 007 结果。
2. 以本包 `inputs.json` 为输入数据模板，创建另一全新短目录（例如 `mts-r8c7-001`），只更改外置 `state_dir`。原 save、session、inspection、日期锚点、当前 formal manifest 和四份配置 pins 保持不变。
3. 使用公共 `ck3_mod_acceptance.py prepare`，指定 READY 的 runtime007、`native-legacy-v10-edit`、新输入和新 prepared 输出。不要复用或覆盖 006 的已准备 profile。
4. 对该新 prepared 运行公共 `plan`，将实际 `host_argv` 和新 `state_dir` 写入无分配权的 `ck3-unallocated-profile-static-argv-v1`，再用现有 `ck3_mod_acceptance_host_preflight.py` 跑全新静态输出。此后由 Root 更新机器配置并决定实际 allocate。

原 case 的一个 Root checkpoint 和四个业务事实不变：原档身份、普通教义候选及提交后唯一替换、核心信条提交后旧项移除、通知收敛。草案选择或 ACK 不能证明提交；合法性不足继续保留 RED。

## 本机调度脚本与归属

ignored 的 `artifacts/bugfix-20261015/root_allocate.py` 曾在真实 allocator 父进程 exit 0 后对包含两个 JSON 对象的 stdout 整体 `json.loads`，导致本机包装器尾部解析失败。现只修其最终结果消费：顺序解析所有 JSON 对象，要求恰有一个携带原 keeper 退出结果的闭场对象，拒绝跨 run、重复闭场或尾部垃圾。使用原 R0019 stdout 和三项拒绝场景完成离线验证；没有重跑 allocate，也没有补写原运行的历史收据。

产品候选来源、业务范围和本机调度输入归本项目；通用保存 parser、标准 product profile/startup 证据、运行时及完整 host 静态链继续复用 `ck3_eternal_recurrence`。本包没有复制通用引擎，也没有修改框架合同或 frozen runtime。
