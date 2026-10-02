# More Tenets Slots v10 工坊发布计划

用户于 2026-10-03 明确授权更新既有工坊条目、审计并入库 BBCode、替换旧 GUI 图片及重做 thumbnail。目标仅为 [3182367229](https://steamcommunity.com/sharedfiles/filedetails/?id=3182367229)，不创建新条目，不更新 POD 产品。

## 发布物料

1. 匿名保存旧描述、标签与预览地址，按 R9/R10 的实际结论翻新英文和中文正文。保存完整 Steam Change Notes，提交前冻结 UTF-8 字符、行数和 SHA-256。
2. 离线启动隔离的 R0011，仅为现有已验收礼仪 GUI 拍摄干净的原生截图。选择创建窗口、信条选择窗口、已创建的两信条礼仪；不把宣传截图当作新玩法验收。
3. 新封面采用新版三列可滚动信条卡片概念，明确为宣传概念图；截图栏使用真实游戏画面。保存生成原图、提示词、缩放参数和真实截图来源；thumbnail 小于 1 MiB，原生附加图片同样小于 1 MiB。
4. 产品专属文案、素材与发布证据留在本仓库。原生附加预览图片的通用 MCP 能力缺口归 `ck3_eternal_recurrence`，由独立工作包实施并验证。
5. 物料完成必要检查后立即提交并推送 master。从冻结提交构建正式 46 文件 staging，保持 version=10、supported_version=1.20.0.3。新增内容包括 thumbnail 和九语言本地化；信条/教条机制继承 R9/R10，46 文件树由简中 R0012/R0013 补验。

## 发布与验收

1. 仅发布阶段将 Steam 上线，使用框架 `steam-native` MCP 更新精确既有 ID。提交前只读冻结旧附加预览，更新封面、描述、兼容标签、完整 Change Notes 和截图。
2. 原生提交成功后匿名回读主描述逐字相等、公开可见性、兼容标签；下载 CDN 封面与附加图片并比较文件哈希和顺序。
3. 独立回读本次 Change Notes entry，HTML 解码、统一换行后精确比较冻结正文。提交成功不能代替公开正文验收。
4. 将旧订阅缓存完整备份移出，重新下载本条目；按正式 manifest 严格核验 46 文件的路径、size 和 SHA。原生 uploader 不注入 descriptor ID，本次不主动放宽差异。
5. 发布收尾立即恢复 Steam 离线，记录永久版本 changelog、发布回执、素材来源与缓存验证结果，提交并推送 master。

任何实际失败保留原始回执并说明未完成项；不把本地旧 descriptor version=9 当成匿名证明的上一公开版本，不把图片刷新或构建检查冒充游戏机制回归。

## R0011 发布前发现

新的截图取材中，两信条冷重载页和选择器已拍摄并入库。加入 Anachoresis 后出现 Absent is not allowed。R0011 查明 Absent 是 doctrine_monasticism_absent 的名称，与 Anachoresis 冲突，撤销空槽误阻断假说。没有绕过校验或修改 GUI；完整原生诊断见 ../live-R0011-native-blocker-diagnosis.md。其原始草稿保留，不用于宣传图。后续使用简体中文和兼容信条复验实际创建。

追加九语言后正式构建为46文件；本地化格式认证见 ../localization-coverage.md。AGENTS.md 已记录后续实机只用简体中文。

发布前订阅缓存的外层 ACF `timeupdated=1777874459` 与匿名公开 API 相等，manifest 为 `3241202835495521309`，13 文件内层 descriptor 实际是 version=1 / supported_version=1.19.0.4。旧缓存已完整备份，摘要见 `previous-cache-manifest.json`；该旧版本未独立重新下载，不能把本地迁移 version=9 当成上一公开版本。发布后的新版缓存另行完成从空目标开始的新下载和 46 文件严格验证。

## R0012 / R0013 补验及最终素材

R0012 简中创建第 1、2、3、100 槽四个兼容真实信条、中间 96 空槽，费用 5775，保存退出 0、error.log 0；R0013 独立冷载并原生重存保持四 core/100 hidden/28 vanilla/78925 及中文名称。两个真实信条与 98 尾空由 R9/R10 独立证明。

截图顺序为简中创建窗口、原生选择器、已保存两信条礼仪；素材 commit 为 `5be332f4bf9c4da6652b3977cbc973919861e513`。正文三张图使用该 commit 的 raw URL，封面单独使用新版礼仪卡片概念图。BBCode 和 Notes 冻结指标见 `publication-text-freeze-v10.json`，最终审计见 `bbcode-audit.md`。

本次还富化通用 `workshop_native_download` MCP，以独立进程等待精确 `DownloadItemResult_t` callback 3406，再核验实际缓存；工具不移动/删除缓存，操作方负责精确备份移出旧目标。通用实现归框架，具体发布回执归产品。

## 2026-10-03 完成记录

已从 `da4b579659ebb4de397672b833369e95fdbd03c6` 的 46 文件冻结 staging 更新既有条目，原生结果 `1`；匿名标题/BBCode 及完整 Change Notes entry `1790978434` 精确回读，新封面和三张追加预览 CDN bytes/像素匹配，全新下载 46 文件按正式 manifest 严格 PASS。annotated tag `more-tenets-slots-v10-ck3-1.20.0.3` 已推送指向该源，构建时 manifest 的 `git_tag=null` 不改写。

Steam 已经恢复离线，新鲜画面于 `2026-10-02T22:29:12.069423+00:00` 审阅，窗口位移证明实时像素变化，CK3=0。发布闭环 complete；永久事实、摘要及证据边界见 [publication-v10.md](publication-v10.md)、[publication-v10.json](publication-v10.json)、[release-manifest-v10.json](release-manifest-v10.json) 和 [版本 changelog](../release-changelogs/more-tenets-slots/10.md)。此记录完成当前计划，不改变旧运行的输入或历史 RED。
