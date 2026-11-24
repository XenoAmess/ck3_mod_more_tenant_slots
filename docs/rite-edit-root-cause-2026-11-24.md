# 礼仪领袖修改礼仪闪退：排查结果与候选修复

截至 2026-11-24：**已取得原生崩溃，并确认首次打开编辑器时的列表准备时序缺陷；候选修复静态检查及无 DLC 场首次打开、末槽选择的有限实机回归通过。确认修改与完整矩阵仍待完成，未发布工坊修复版。**

范围仅为 More Tenets Slots(XA)，CK3 **1.21.0.3 / Steam build26785313**。实机均为简体中文、Steam 离线、隔离 userdir，使用框架受管进程和排他租约。本报告不覆盖 POD，也不宣称所有政体均已通过。

## 1. 已确认的故障机制

原来的“修改礼仪”按钮在同一次点击中依次执行：

1. `mts_prepare_selector_gui.Execute(...)`，请求向选中礼仪补入 100 项不可见兼容教义。
2. `OpenGameViewData('rite_creation', ...)`，立即打开原生编辑器。

脚本准备命令尚未生效时，原生编辑器已经复制了旧礼仪。**随后源礼仪补齐元数据，已打开的草稿仍保留旧列表。** 原生核心信条选择器把信条槽索引用于读取这份教义列表，没有对高槽位做长度检查。

因此，画面显示 100 个信条槽，并不代表原生选择器的消费列表有 100 项。第一次打开时可能只有 32 项，点击第 100 槽会传入索引 99；是否立即闪退取决于越界地址当时的内容。只测试“这次点了没有崩溃”，不足以证明安全。

取消后重开会复制已完成准备的礼仪，列表变为 132 项。这解释了部分旧存档和重复打开操作看起来正常的现象。故障路径没有按政体分支，但政体的完整验收仍需分别执行。

## 2. 崩溃与独立对照证据

| 场次 | 操作与结果 | 证据边界 |
| --- | --- | --- |
| R0007 / `no-dlc-a04` | 仅 MTS，禁用全部 31 个已安装 DLC 描述文件；封建角色成为自创礼仪领袖，首次打开修改界面，点击第 100 空槽后 `C0000005`，原始进程退出 1 | 此场此前超时收到过 WM_CLOSE，取消退出后继续；保留此混杂条件，不记为验收通过 |
| R0008 / `short-a05` | 独立新开局，仅 MTS、相同 DLC 排除条件；合法封建罗贝尔创建并转入礼仪、刷新领袖；首次打开草稿为 **32 项 / 0 项兼容元数据**，高槽选择未立即崩溃 | 没有收到 WM_CLOSE；证明越界前置缺陷可独立存在，不能写成第二次 CTD |
| 同一 R0008，取消并重开同一礼仪 151 | 草稿变为 **132 项 / 100 项兼容元数据** | 同一进程、同一角色、同一礼仪、同一源码，直接区分首次与重开 |

R0007 转储中的原生故障地址为 EXE RVA `0x16B6737`，选择器入口 `0x16B66B0`。槽索引 `r10=99`，owner+`0x798` 数组数量 **32**、容量 **42**，元素步长 **72 字节**。原生代码按索引取出指针后再解引用而访问冲突。转储没有包含数组全部元素内容，未臆测其教义键。

R0008 在界面暂停时，按框架当前精确构建的 owner 链和布局作有界外部只读诊断，逐项核对教义类型及内部键；两次完整采样一致。首次草稿数量 32、容量 141、兼容键 0；重开后数量 132、容量 141、兼容键 100。首次点击没有闪退仍是逻辑越界，较大的分配容量不能使索引 99 成为数量 32 的合法元素。

此诊断仅使用 `ReadProcessMemory`，没有写内存、注入 DLL、调用原生函数或改变游戏文件；**它不具备主线程执行凭证，属于定位证据，不冒充合格 observer 或业务验收。** R0008 从 2026-11-23 18:02:09 UTC 至 18:55:19 UTC，通过原生菜单退出，原始 Popen 退出 0，`window_close_requested=false`、keeper 无失败、租约已释放。业务验收仍未签署。

## 3. 另一个已确认的编辑异常

100 槽下确认修改会出现 `rite_edit` 的 `Failed to read key reference: : , near line: 1`。替换已有核心后，实际存档曾保留旧核心并加入新核心。

R0006 使用同一输入存档，加上明确标记的诊断 fixture，将原生上限和议会镜像同时设为 3：替换后实际存档保持三个核心，旧核心移除，且没有该解析错误。**这是三槽对照，不是产品通过，也不将缩减容量作为修复。** 此异常须单独继续处理，尚未证明与本次选择器访问冲突具有同一根因。

早期 R0004/R0005 的普通教义修改、费用扣除及有限正常退出仅作为历史观察；不能据此否认崩溃或宣称全部功能通过。详细记录见[连续调查记录](rite-edit-investigation-2026-11-23.md)。

## 4. 已实施的候选修复

- “修改礼仪”点击只提交准备请求并设置本地待开标记。
- 新增只读就绪检查，要求选中礼仪**全部 100 项**兼容教义都已存在。
- 原生 GUI state 在就绪且原生编辑权限仍成立时，清除标记并打开编辑器。
- 关闭信仰窗口会清理待开标记，避免遗留请求。
- 保留原生 100 槽、真实空槽、选择器、费用及权限；创建礼仪入口保持原生行为。

生成源为 `dev_tools/migrate_to_ck3_1_20.py` 和 `dev_tools/selector_padding.py`，生成文件位于正式产品目录。候选产品版本为 **13**，仍未发布。

输入合同已复核到 1.21.0.3：10 项原生输入中 9 项未变；`00_defines.txt` 内容变化，但当前原生 `NReligion.FAITH_CORE_TENETS_CAP` 仍为 3。产品只覆盖该上限，不分发原版 defines 文件。精确 EXE SHA256 为 `859f0d380098adcb130eb9d453458222749fcdf6d46126ad0ed99d78f9a0aa28`。

## 5. 候选修复后的有限实机回归

提交 `286b708bc89a124602e0af7e0dd70ae1c4103a72` 已在 R0009 / `wait-fix-a06` 实测：独立新开局，仅 MTS、无 fixture、同样禁用 31 个 DLC 描述文件、封建罗贝尔、自创礼仪 150。点击修改之前通过原生菜单保存，存档确认兼容元数据为 **0**（11676264 字节，SHA256 `7d82108a21969a748c4710591d0e4e93c180b5eac0d621bf54c0b03386dc97b2`）。

首次只点击一次“修改礼仪”，编辑器直接取得 **132 项教义、100 项兼容键**；外部诊断的选择槽仍为 -1，尚未点选任何槽。随后点击第 100 槽，实际选择索引 99，列表仍为 132 项；选入苦修信条，原生报价显示 375。普通性别教义选择器仍提供男性主导、男女平等和女性主导三项；选平等后合计报价 825。取消并重开后，草稿恢复原信条、男性主导、报价 0，兼容列表仍完整。

此无 DLC 前置场原生“你的神职领袖可以创建或修改礼仪”条件不满足，确认按钮按原生规则禁用，**没有确认修改或扣费，不把报价显示当成实际支付**。因此它验证首次准备时序、末槽及普通教义选择和取消重开，不能替代完整编辑验收或证明 rite_edit 解析错误已经修复。

R0009 于 2026-11-24 01:45:51 UTC 由原生菜单正常退出，原始进程退出 0，`window_close_requested=false`、keeper 无失败、CAS 已释放。该场仍为 `business_pass=false`，没有签署完整 rite-edit case。简明机器可读原件索引及有限结论见[证据记录](evidence/rite-edit-selector-20261124.json)。

## 6. 验证状态与下一步

| 检查 | 当前结果 |
| --- | --- |
| 编辑打开必须等待完整元数据、关闭清理、创建入口保持原生、on_action 原生效果完整保留 | 4 项回归检查通过 |
| 精确原生输入、可逆 GUI 投影、BOM/结构、上限与议会镜像、48 文件发布白名单 | 静态通过 |
| 九语言格式、编码、结构及每语言 305 键覆盖 | 静态通过；其他语言未启动游戏 |
| 两次构建清单与 ZIP 可重复性 | 通过 |
| 候选修复首次打开时草稿长度、末槽和普通教义选择、取消重开 | **R0009 无 DLC 场有限通过**；未确认修改 |
| 确认修改、费用、旧核心移除、解析错误消失、保存及冷载 | **待完成** |
| 不同政体的代表性礼仪领袖 | **未完成矩阵，不宣称全部通过** |
| 创意工坊修复版 | **未发布** |

后续按[修复与验收计划](rite-edit-crash-plan-2026-11-23.md)继续。发布前须如实保留上述独立编辑异常与未完成项，不用静态通过替代实机通过。

## 7. 原件索引与归属

私有存档、机器配置、截图和转储保留在本地 `artifacts/rite-crash-20261123/`，不提交 Git。

| 原件 | 大小 / SHA256 |
| --- | --- |
| R0007 `crashes/ck3_20261124_002634/minidump.dmp` | 54295089 字节 / `a31a5ae5a650d5f833335d259e83d4e74f6a3c3c0d4a44f393899d14b2e48be4` |
| R0008 `review/selector-184723885898.json`，首次草稿 | 1728 字节 / `beb8e31852e89aa5c20a774482551c7be05ce457302baad9ea0fb2930c1cdedd` |
| R0008 `review/selector-184945925867.json`，重开草稿 | 5129 字节 / `4f25152f6647d65fcc36f701550b86cceb6aa55ebbeb2df6a44009c9dc60e769` |
| `static-candidate-13.json` | SHA256 `6bf28589324e83e48ca6cacb9f8c6246331cbae1ea680b575947a8ee153ff31e` |

R0008 运行目录 ID 为 `pc-20260924rtuf-f11af23c08--more-tenets-slots--R0008`。其保存的罗贝尔礼仪 150 已补齐 100 项元数据，存档 SHA256 `c838628a8092bcdd53c9fa2249dcda54180b503300a6f2e36b928b6b490114d6`；它与随后礼仪 151 的两次草稿读取是不同观察，不混为同一存档证明。

归属决定：具体时序修复、产品回归和本报告归 MTS 项目。通用的显式 DLC 排除受管准备能力已富化到框架提交 `7aa155ad7`（41 项离线 GUI 测试及生产模块类型检查通过）。本次方法补充框架已有 ScriptedGui 排队刷新知识：使用可观察的完整就绪条件，不把固定等待时间或“未闪退”作为事务屏障。本次外部诊断脚本仍为精确构建的定位实验，暂不上收为正式 observer，因为缺少主线程资格；没有新增可用于业务判定的通用读取能力。产品源码、第三方素材、私有存档和转储不搬入框架。

通用方法已另行提交并推送框架 `6a610ebc472e75b637753c3daa62191b0dac2546`，补充[语法与引擎坑](https://github.com/XenoAmess/ck3_eternal_recurrence/blob/6a610ebc472e75b637753c3daa62191b0dac2546/docs/grammar/pitfalls.md)，并记录当日与当周进度；该文档包未新增游戏运行或运行时资格。R0009 公共 `verify` 实际退出 2 / `INCOMPLETE`，进程与闭场为 true，完整业务、发布及 Native 资格为 false；此结果保持原样。

## 8. Follow-up: cancel pending edit when selecting another rite

The readiness check uses the currently selected rite. Previously a pending
request could therefore open a different rite if the user changed selection
before the GUI state consumed the request and the new rite was already ready.
All five native rite-selection buttons in the projected faith GUI now clear the
local flag before changing the selection. A preparation command already queued
for the original rite can still finish on that rite.

The exact-build reversible projection, five selector checks, nine-language
validation and 48-file release allowlist passed. This product-specific change
belongs in MTS. The selection-switch path has static coverage. Live confirmation,
piety deduction, old-tenet removal, the rite_edit parse error, and save/cold-load
remain open. The native removal effect takes an explicit tenet, so an automatic
cleanup would require evidence identifying the intended old key even when the
native edit delta is incomplete. The existing R0009 receipt remains limited to
opening, choosing and cancelling. No candidate was published.
