# R0025：实际工坊新缓存菜单加载与正常闭场通过

**结论：本场缓存菜单加载、公共验证、正常退出和最终离线／资源闭场通过。** 本场是菜单加载用例，`business_contract_applicable=false/business_pass=false/product_release_pass=false`原样保留；v11整体发布完成由R22业务、R23独立冷载、公开发布和本场共同组成，不能把菜单用例改成宗教业务通过。

- 机器 `bf-202609141645-5434332d4d`，场次 `bf-202609141645-5434332d4d--more-tenets-slots--R0025`，case `workshop_cache`。
- CK3 `1.20.0.4`，EXE SHA256 `98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518`，简体中文；runtime008与007使用同一native DLL，修复限于通用Python整合。
- 框架checkout `38a0616157aba4ffdfa3975409bd959c449b6f34`，实际游戏PID **16724**、create-time **1792092300.8483706**。
- [证据索引](evidence/native-cache-r25.json)含28个原件pins及15项嵌套核对，均无差异；本报告未启动游戏、发送查询、操作屏幕或改写运行证据。

## 实际新缓存与菜单资格

本场使用[v11正式发布](workshop/publication-v11.md)的实际SDK新下载缓存，item3182367229／app1158310。其48文件已严格匹配正式manifest `2d9c319293b2bce98c2cc041c759b0d6400aa22ce1d9216ba620b8f194823172`，没有staging复制或descriptor规范化。

公共profile只启用该缓存产品；实际原命令使用本场userdir，`continue_last_save=false/load_save_name=null`，没有宗教夹具或进入campaign。原host于2026-10-15T19:24:50.702675Z启动，readiness实际274.486020秒，在原1800秒内观察hold，未重开计时或重放启动。原生只读route为 `main_menu`，tree为可用的 `mainmenu_panel_bottom`；原图由Root直接审阅。

`workshop-cache-case-result.json`的 `case_contract_qualified/gui_contract_qualified/combined_managed_cache_profile_and_actual_menu_load` 为true。这一资格是**精确缓存的受管单产品profile与实际稳定主菜单的组合证明**。原低层 `product_acceptance_proven=false/actual_cache_mount_proven=false` 和 `independent_engine_vfs_path_readback=UNKNOWN/actual_cache_mount_proven_by_independent_vfs=false` 保持，不能称为独立引擎VFS路径读回，也没有重做R22八事实。

公共verify原进程实际exit0，`case_acceptance_pass/qualified_boundary_pass`为true，两个case／GUI合同也为true；其business与product_release仍false。case原件中的“pending original normal0”是写入时的边界，后续独立 `normal-close-result.json`另行授予正常退出，不改写原case文件。

## 一次官方退出与独立正常闭场

菜单用例允许六个只读MCP工具；现有typed正常退出provider要求地图／actor，故未越过case工具集调用地图退出查询。Root通过官方主菜单“退出到桌面”做了**一次**规范映射左击，保留 `r25-menu-quit-once.mapping.json`和原图。

点击后退出有延迟。之后拟用标题栏备用操作，在任何工具调用前因PID已消失的assert中止；**没有第二次点击、实际备用派发或process kill**。不能将延迟写成菜单无效或备用退出成功。

独立后验为：

- 原保留PID16724的OS handle signaled，实际exit0。
- native session于 **19:37:47.920579Z** 以 `process_exit/code0`结束；shutdown CK3exit0、进程树消失、完整清理、inventory为空、watchdog及control文件消失。
- `normal_close_qualified=true/cleanup_ok=true/managed_thread_finished=true/host_error=null`；正常闭场子回执business仍false。
- 原host **GREEN／wait0**、无failed step；原public PID17860实际wait0，keeper原父进程实际wait0，原allocator实际wait0。不是用新进程轮询或报告文件存在代替原wait。

## 最终离线与资源释放

Root在游戏关闭后直接审阅新鲜Steam移动原图，画面为“离线模式”、北京时间 **2026/10/16 03:44**，窗口移动及边缘像素变化有独立回执；图SHA256 `942c28522d002b173e34b6e1bb4f36c7d4599b9016eb81ba62fbad7d45de1f73`。Root回执同时记录CK3为空、正常零退出已读回、实际GUI退出动作1次及备用派发false。

最终CAS **6365** 于 **19:46:15.043193Z** 释放，resources为空。旧keeper报告中的screen_released=false保持原字段，由这份后续CAS单独证明释放。

## 前驱、保留失败与归属

[R24](native-cache-r24-2026-10-16.md)原host1/public2、启动前schema拒绝、无native-report和normal/native0信用不变。a12错误使用R23旧前驱，被中央allocator正确拒绝为BLOCKED／NOT_RUN，没有建立本场或租约；Root后记观察记录原工具exit2及原helper stdout，明确不是伪造原进程schema。a13使用真正最新R24和真实prelaunch closure bundle后，才分配本R25。

R22原host RED／返回1、早先匿名Notes回读429及全部历史原件保留。v11最终完成范围见[永久记录](workshop/publication-v11.md)，仍有直接Edit、全部DLC／信条组合、超文化上限旧档及更多通知路径等未覆盖风险，不因发布扩大为全场景通过。

本场产品缓存、具体UI和发布事实归独立产品；通用cache profile与allocator前驱整合归框架。本包只更新八份产品永久文档／证据，不改manifest、文本freeze、源码、catalog、runtime或框架。
