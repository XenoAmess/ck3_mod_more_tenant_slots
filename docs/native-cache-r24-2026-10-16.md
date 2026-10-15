# R0024：工坊新缓存加载在游戏启动前RED

**新缓存逐文件匹配通过，菜单加载／正常退出未通过；资源已释放。** 机器 `bf-202609141645-5434332d4d`，场次 `bf-202609141645-5434332d4d--more-tenets-slots--R0024`，case `workshop_cache`，runtime007，框架checkout `79b1acc475cdf593ad7dd2e66e7de66366e158ea`。原件见 [机器证据](evidence/native-cache-r24.json)。

来源为v11实际独立SDK新下载的item3182367229缓存，48文件严格匹配正式manifest `2d9c319293b2bce98c2cc041c759b0d6400aa22ce1d9216ba620b8f194823172`，没有staging复制或descriptor规范化。[发布里程碑](workshop/publication-v11.md)与本次加载资格分别记录。

原host于2026-10-15T18:57:14Z启动，在 `normal_exit_profile.project_profile` 抛出 `ValueError: public preparation and selected runtime identities differ`。来源为 `ck3-mod-acceptance-prepared-workshop-cache-v1`，startup evidence为旧profile-startup envelope，未被007的normal-exit投影接受。错误在受管CK3/native session启动之前，不是产品菜单或游戏崩溃。

原host实际Popen wait1，public原进程wait2；native-report不存在，Root于18:58:23Z实查CK3 inventory为空。未发生native正常退出动作或保留游戏OS handle的exit0，没有normal/native0信用。

keeper原父进程实际wait0、thread_exited=true、entry_error=null；CAS **6345** 于18:58:47.212581Z释放，resources为空。只证明本次启动前失败的资源闭场，不授菜单、业务或正常退出通过，也不改变R22／R23结论。

本包核对14个原件pin及35项嵌套源pin。R24准备时的框架adapter在闭场后由其owner修复中，其历史SHA在runtime007不可变source中仍精确匹配；索引单列这一源码对应关系，不把当前工作树变化伪报成旧证据变化。

通用cache profile/schema整合归 `ck3_eternal_recurrence`；新008资格及实际后继加载由Root和框架owner继续。本包只记录确定性RED，不改007、原case、源码或catalog，不操作游戏／屏幕／Steam，不重跑验收。
