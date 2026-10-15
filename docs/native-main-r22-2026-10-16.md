# R0022：新局八项业务事实与正常闭场通过

**结论：本场八项业务事实、实际保存及正常闭场通过，独立冷载与正式发布仍待执行。** 原 host 的 **RED／实际返回 1** 保持原样：唯一失败步骤是未暂停时被守卫拒绝的只读事件查询，不是报告写入崩溃。产品 scoped PASS、CK3/native 正常退出与原 host 返回值分别记账。

- `machine_id`：`bf-202609141645-5434332d4d`；场次 `bf-202609141645-5434332d4d--more-tenets-slots--R0022`，公共 case `native-october-reported-bugs`。
- CK3 `1.20.0.4` / build `25734779`，EXE SHA256 `98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518`；PID **17196**，语言 `simp_chinese`。
- runtime007；任务 checkout `3e99036b6a33e8b6278a5b8308316402e1f338da`。实际产品为当前 **48 文件候选**，manifest SHA `133fd81ef2b1c76068a3f5ebe13ed3283aa92f6ab7d933ec42f0db1095f89ca8`，尚未上传工坊；不等同于正式 v10，不外推至 POD。
- 原 public 命令于 `2026-10-15T14:18:02.633523Z` 执行，最终实际 wait 0 为 `17:01:46.368271Z`。readiness 1800、hold 21600、总体 timeout 25200 秒；实际观察 hold 耗时 **872.904582 秒**。本轮没有改 deadline，也没有追改 R21。
- [证据索引](evidence/native-main-r22.json)保存 **94 个原件 pins、52 个嵌套 pin 核对**，无不匹配；包含阶段审阅、native 查询、实际 PNG、保存读回、原 host RED、退出及 CAS 释放，不复制大截图或存档入库。

## 两阶段八项实际事实

第一阶段 Root 四项 true 于 `15:13:00.123476Z` 被 CaseClient 接受；第二阶段四项 true 与实际 `save_origin` 于 `16:39:47.376398Z` 接受。公共 `verify` 的实际 UTF-8 后继进程返回 0，`case_acceptance_pass`、`business_pass`、`case_contract_qualified`、`gui_contract_qualified` 和正常闭场均为 true；`product_release_pass=false` 保持。

| 事实 | 本场结果与界限 |
| --- | --- |
| 普通教义候选 | 实际简中性别与宗教态度弹窗均显示候选，未复现两个被测组的空白。 |
| 普通教义唯一替换 | 男性主导→平等、正义→多元主义；提交后当前 Rite 的两个组分别只有 `doctrine_gender_equal`、`doctrine_pluralism_pluralistic`，各组旧键不在当前选择中。 |
| 核心信条替换与旧项移除 | 草稿 slot0 由 `tenet_peace_of_god` 改为 `tenet_transubstantiation`，完整 100 槽向量仅索引 0 改变；提交后目标当前核心也不含 Peace of God。 |
| 第 100 槽选择 | 内层网格滚到末端，native 观察 `category_materialized=true/current_category_slot=99`；选择后仅 slot99 从 null 改为 `tenet_be_fruitful_and_multiply`。不是只观察到槽数量或凭末行图片猜槽号。 |
| 稀疏礼仪合法创建 | 最终草稿只有 0、1、2、99 四个非空槽，实际创建后当前 Rite **0→150**，Catholic Faith **13**、Religion **8** 保持。 |
| 原版文化限制 | Root 直接查看诺曼文化传统 **4/6**，没有捆绑 10000 上限；未授新增传统、时代增益或超上限旧档行为通过。 |
| 通知收敛 | 两个独立创建事件实例经 native 后置条件各自消退；其后 87.425699 秒有限窗，四张定时原图未见顶部信条变更持续重复。 |
| 实际保存 | 唯一 native Save sequence1 写出原 binary；独立派生文本的 bounded AST 读回角色、日期、当前 Rite、四核心及两个普通组，与暂停 native 状态一致。冷载另验。 |

Root 直接核对本场人物为“狐狸”罗贝尔、51 岁、阿普利亚公爵，native actor **31254**。初始资源夹具仅增加 100000 虔诚，未预设被测信条、教义、宗教关系或文化。原版合法傀儡交互对象为领地司祭 Landulf（53 岁），确认图显示 Accept +5、100 虔诚费用，发送后 banner 留存。

四个中文字段分别为“松柏新局礼仪／松柏新局／松柏信徒／松柏信众”，均有实际控件剪贴板复制读回，四份 `readback_verified=true`；不只凭粘贴输入 ACK。提交前 `can_create_rite=true`，费用 raw451750000/scale100000，即4517.5虔诚且资源足够；分歧40、创建新 Faith 阈值100，原生确认不会创建新 Faith。本次通过创建分支，不授直接 Edit：`can_edit_rite=false` 的非礼仪领袖理由保留。

新目标当前 Rite150 核心恰为 `tenet_transubstantiation`、`tenet_be_fruitful_and_multiply`、`tenet_apostolic_succession`、`tenet_communion`。原 Faith 主 Rite0 保留原核心，知识／允许状态也可能保留旧项；这些与新目标当前核心分开，不构成残留。提交会压紧稀疏列表，最终四项核心的下标不替代提交前实际 slot99 证据。

## 事件、通知与保留的查询问题

`head_of_faith.0100` instance1 通过 native first-shown 选项得到 **1→null**；之后出现的 `faith_creation.1021` instance2 独立得到 **2→null**。这是两次实际实例消退，不把有限创建公告当成永久循环。

四张通知原图分别在 **6.092518、26.062260、51.112792、76.053849 秒**取得，实际日期为9/18、9/27、10/7、10/17。Root 已直接查看并另写 `r22-notifications-root-visual-review.json`；没有回改原 window 的 `root_visual_review=null`。右下普通家族／改信 toast 与用户所述顶部信条更新循环分开。有限窗结论不覆盖所有取消、无修改确认、连续 Edit、DLC组合或冷载。

必须保留两处原始不成功观察：

- `r22-progress-event-context` 的只读查询被拒绝：`event-window queries require a paused CK3 snapshot`。之后独立暂停及新鲜 context 成功，原错误不被覆盖或重放。它是原 host 唯一 failed step，导致其最终 status RED、实际返回1；`native-report.error=null`，原 host stderr 为0字节，不是 report writer crash。
- 观察结束的 pause 原行 `ok=true/accepted=true/status=submitted`，但即时 `after_snapshot.paused=false`，不能据 ACK 宣称暂停。保守断言中止当时保存；随后三条新鲜 native 读取均为 `paused=true/date_raw53145144/noevent/nointeraction`，才进入唯一实际 Save，没有重放 pause。

实际 MCP catalog 首次本地抽取误遍历 envelope 键得到空数组，原件保留；correction 从 `mcp_tools.tools` 读出真实7个宗教只读查询。宗教导航、选择和提交仍无 typed writer，实际操作使用官方 GUI，native负责前后观察；本场不授尚不存在的宗教写入能力。

## 原保存与离线读回

原 `save games/xar_checkpoint.ck3` 为 **70,534,188 字节**，SHA256 `fc72cc80dc16ea5e32b65d6ae33bd85e42e62a3f86552781b1c708a165cdb465`，容器 **SAV0101**。只提交一次 native Save sequence1；原 binary 前后 SHA 相同，没有以转换文本覆盖原件。

原 plaintext reader 实际 exit1，明确仅支持 SAV0100，原 stderr、空 stdout、PROCESS 与 GAP 留档。复用既有 Rakaly0.8.21 melt 实际 exit0，独立生成102,136,243字节文本，SHA `bf4fd28f287bc56b6375f401cf32501aead15d7cd028405e612296cf886409d4`。首个 binary-derived reader process001 又因未匹配 living/31254 实际 exit1；修正原记录缩进匹配的后继 process002 实际 exit0。成功输出文件仍名 `...binary-derived-001.json`，不得将编号误读成首轮通过。

后继为 `OFFLINE_BOUNDED_READBACK_PASS`，精确消费 living/31254、rites/150、faiths/13、rites/0 四条 bounded AST。正文日期 **1066.10.19** / raw53145144、actor31254、Rite150、Faith13、Religion8及当前四核心、平等／多元主义唯一均一致。原父 Rite核心另列；不是用 native 当前值替代保存读取，也不证明游戏新进程已恢复该档。

## 正常闭场、原 host RED 与公共验证

MCP-first 实际 `ck3_query_normal_exit_context_v1` 返回 unavailable，reason `actual_launch_userdir_contract_unsupported`；未消耗任何 claim或退出stage。同一原进程实际 argv 含 `-continuelastsave`，runtime007生产解析器尚未支持它，尚未进入 GUI source inventory 验证。R20已具资格的显式 `-loadsave` 路径保持；不把本场官方 Quit 外推为 fresh native Quit 动作通过。

Root 随后走官方 Escape→Quit→取消退出自动保存→最终桌面 Quit，直接查看未勾选原图，并保留 canonical final mapped click。原 CaseClient 独立得到：

- 原保留 PID17196/create-time1792073898.9873087 的 OS handle signaled、exit0；不是凭进程不存在推断。
- native session 于 `17:01:37.263979Z` 以 `process_exit/code0` 结束；shutdown CK3exit0、完整清理、进程树消失、最终 inventory为空，managed thread完成。
- `normal_close_qualified=true`，host error=null；此子回执自己的 `business_pass=false` 保持正常退出证明的范围。原 host顶层RED／Popen实际1与上述事实同时成立。
- 原 public parent实际0；keeper原父进程wait0、thread_exited=true；任务于 `17:08:09.166884Z` 经 CAS **6290** 释放，resources为空。keeper STOP报告自身的 screen_released=false不替代随后独立CAS释放。

首轮公共 verify 本地调用漏 `-X utf8`，打印结果时 GBK `UnicodeEncodeError`、实际exit1留档；没有改写成成功。显式 UTF-8 的 `public-verify-002` 实际 exit0，消费同一批已经结束的原件确认八事实及 normal pass，没有重启游戏、重放选择或保存。两个失败层次须分开：原hostRED1来自守卫拒绝查询；首轮verify1来自本地stdout编码。

`error.log` 原文件20,748字节已pin，未清理或重写；本包不授日志全净，产品归因及未覆盖场景继续记录。

## 后续与归属

独立新PID冷载、直接Edit、往返／连续替换、反复开关与无修改确认、完整文化行为以及正式发布／缓存核验仍待。R21原超时RED、R19正式v10来源的合法性RED与R20限定旧候选通过保持各自范围。

本包只交付产品报告、证据索引、总计划和整改进度；没有改产品源码、adapter、catalog、冻结 runtime007或原件。具体场景事实归本项目；七查询、正常退出、profile、bounded parser等通用能力继续归框架。`-continuelastsave` 解析缺口另作最小框架包，不为冷载重建DLL或升级选定runtime；冷载仍复用007受支持的显式 `-loadsave` 路径。
