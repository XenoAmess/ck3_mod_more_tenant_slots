# R0023：独立新进程冷载与正常闭场通过

**结论：本场独立冷载四项事实、公共验证及正常闭场通过；正式发布与工坊缓存验证仍待执行。** 范围为当前48文件候选加载R22实际写出的同一份保存，不外推正式v10、全部存档、POD或未测试的编辑／替换路径。

- `machine_id`：`bf-202609141645-5434332d4d`；场次 `bf-202609141645-5434332d4d--more-tenets-slots--R0023`，公共 case `native-cold-reload`。
- CK3 `1.20.0.4` / EXE SHA256 `98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518`，语言 `simp_chinese`；runtime007未改。任务checkout为 `781efbf42b57d20460b11271767656002f323739`，不等于将该提交的新parser部署进旧DLL。
- 原public从 `2026-10-15T17:40:05.406997Z` 执行，实际wait0为 `18:15:30.036777Z`。readiness实际 **744.976863秒**，在原1800秒内观察hold；hold21600、总体25200秒及原退出预留未延长。
- [证据索引](evidence/native-cold-r23.json)包含56个原件pins、27项嵌套核对，均无差异。顶层 `case_acceptance_pass`、`normal_close_qualified`、`independent_cold_load_pass` 均为true，`product_release_pass=false`。

## 保存来源与新进程

本场消费[R22](native-main-r22-2026-10-16.md)的实际binary保存：**70,534,188字节**，SHA256 `fc72cc80dc16ea5e32b65d6ae33bd85e42e62a3f86552781b1c708a165cdb465`。其原生写入和独立离线读回来源、前场normal-close及正式候选清单在prepare时绑定；本场没有新资源夹具、宗教setter或再次Save来制造匹配。

R22原保留PID **17196**；R23新保留PID **12944**、create-time **1792086024.3112938**，PID及创建时间均不同。公共 `saved_campaign` 使用受支持的显式 `-loadsave` 路径，实际restore为 `ACTUAL_SAVED_CAMPAIGN_CURRENT_CONTEXT_BOUND`。不是同进程重开面板或回到菜单读档，也没有为了冷载采用新DLL。

## 四项实际冷载事实

Root的四项true已由CaseClient消费；实际公共verify原进程exit0，`case_acceptance_pass/business_pass/case_contract_qualified/gui_contract_qualified`均为true。

| 事实 | 本场读回 |
| --- | --- |
| 保存人物与宗教身份 | 首帧精确actor **31254**、date raw **53145144**（1066.10.19）、Rite **150**、Faith **13**、Religion **8**，与R22实际保存一致。Root直接查看原人物图，核对阿普利亚公爵罗贝尔“狐狸”、51岁及保存后的礼仪标识。 |
| 保存核心信条 | 当前Rite150恰有 `tenet_transubstantiation`、`tenet_be_fruitful_and_multiply`、`tenet_apostolic_succession`、`tenet_communion` 四核心；旧 `tenet_peace_of_god` 不在当前核心。 |
| 保存普通教义 | 当前有效性别组唯一为 `doctrine_gender_equal`；宗教态度组唯一为 `doctrine_pluralism_pluralistic`。各组旧项不在当前选择中。 |
| 冷载后通知 | speed1推进后四张原图经Root直接查看，无顶部宗教／信条变更反复提示；最后一帧普通家族关系toast另记。新鲜最终snapshot暂停、无事件与交互。 |

信条判定使用 `current_rite.core_tenets`，普通教义使用目标当前Rite的有效组行，不把Faith主Rite、个人信条或知识／允许状态混入。R22原本0/1/2/99的稀疏草稿提交后已压紧；本场证明那次选择的内容持久化，不以压紧后的列表下标再次证明草稿槽99。

## 有限通知观察

原观察记录elapsed **92.327955秒**，包含本轮采集／控制开销。文件名5/25/50/75是计划标记，四帧实际elapsed分别为 **9.657842、28.331539、51.068967、77.484682秒**；直接看到的日期为 **1066.10.19、10.20、10.29、11.9**。不能把计划文件名当成精确采样时刻。

Root另写 `r23-root-visual-review.json`，保留原window中“review pending”的历史note，没有覆盖原件。最终新鲜snapshot为 `paused=true/date_raw53145696/active_event=null/pending_character_interaction=null`。该窗支持此保存冷载后的收敛，不保证所有DLC组合、取消、无修改确认或连续Edit均无循环。

## 原生正常退出与独立后验

本场runtime007初始native退出context实际观察 `stock_files_verified/loaded_source_binding_verified/frame_verified=true`，与R22 fresh路线不支持 `-continuelastsave` 的事实分开。本场无需部署已在框架修正、但不在007内的新parser。

`prepare_confirmation` 与 `continue_preparation` 的原始返回均为 `dispatch_unknown_claimed`，claim已消费、retry未授权。prepare还保留 `expected_exit_context_signature requires 64 lowercase hexadecimal characters` 的原reason；不把它改为成功或据此重发。后继新鲜context1读到prepare stage已消费，context2观察确认窗可见。

`disable_exit_autosave` 实际仅提交一次，返回 `autosave_disabled`，原版状态由true读回false；随后两次新鲜context仍为false，Root直接查看未勾选PNG。原回执 `autosave_verified=false` 保持其范围，本次只证明退出勾选状态，不凭它推断新存档。

最终 `confirm_desktop` 仍返回unknown，但原dispatch第2项确实 `claim_latched/dispatch_invoked/native_handled=true`、`native_submission_count=1`；即时post-read／postcondition未验证，未重试。退出通过来自后续独立原件：

- 原保留PID12944的OS handle signaled、实际exit0。
- native session于 `18:15:25.755745Z` 以 `process_exit/code0` 结束；shutdown CK3exit0、完整清理、进程树消失、最终inventory为空，managed thread完成。
- 原host **GREEN／实际wait0**、error=null；原public wait0。CaseClient的 `normal_close_qualified=true`，闭场子回执自己的 `business_pass=false` 不变；产品四项通过由业务回执授予。
- keeper原父进程实际wait0；随后于 `18:16:05.308093Z` 经CAS **6321** 释放，resources为空。未以旧keeper的screen_released字段替代独立CAS结果。

R22原host RED／返回1继续保留，不因R23全零闭场追改。R23原host没有failed step；本场unknown ACK与后验过程也没有被抹去。

## 日志、剩余范围与归属

本场原 `error.log` **203,716字节**已pin，未清理或重写。可见一条直接引用本产品的 `on_rite_updated` 重复effect提示；文件还包含原版Mandala unset-scope等错误，不授日志全净。它们不被通知图中没有顶部循环的有限结论遮盖。

当前候选已取得R22新局八事实与R23独立冷载的组合通过，正式工坊上传、匿名回读和实际Steam缓存逐文件核验仍未完成。直接Edit、反向／连续替换、完整文化增益／超上限旧档及更多通知路径保持未覆盖范围；不将代表性用例扩写成全部场景完成。

本包仅更新产品报告、证据、计划和整改记录，没有改产品源码、adapter、catalog或框架。具体保存／UI与用例结论归本项目；通用profile、七查询、原生退出和任务总线继续复用框架既有能力，不为本场重复全矩阵构建。
