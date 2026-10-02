# More Tenets Slots v10 工坊发布计划

用户于 2026-10-03 明确授权更新既有工坊条目、审计并入库 BBCode、替换旧 GUI 图片及重做 thumbnail。目标仅为 [3182367229](https://steamcommunity.com/sharedfiles/filedetails/?id=3182367229)，不创建新条目，不更新 POD 产品。

## 发布物料

1. 匿名保存旧描述、标签与预览地址，按 R9/R10 的实际结论翻新英文和中文正文。保存完整 Steam Change Notes，提交前冻结 UTF-8 字符、行数和 SHA-256。
2. 离线启动隔离的 R0011，仅为现有已验收礼仪 GUI 拍摄干净的原生截图。选择创建窗口、信条选择窗口、已创建的两信条礼仪；不把宣传截图当作新玩法验收。
3. 新封面采用新版三列可滚动信条卡片概念，明确为宣传概念图；截图栏使用真实游戏画面。保存生成原图、提示词、缩放参数和真实截图来源；thumbnail 小于 1 MiB，原生附加图片同样小于 1 MiB。
4. 产品专属文案、素材与发布证据留在本仓库。原生附加预览图片的通用 MCP 能力缺口归 `ck3_eternal_recurrence`，由独立工作包实施并验证。
5. 物料完成必要检查后立即提交并推送 master。从冻结提交构建正式 32 文件 staging，保持 version=10、supported_version=1.20.0.3。本次新增产品内容只包括 thumbnail，玩法源码与 R9/R10 已验收内容相同。

## 发布与验收

1. 仅发布阶段将 Steam 上线，使用框架 `steam-native` MCP 更新精确既有 ID。提交前只读冻结旧附加预览，更新封面、描述、兼容标签、完整 Change Notes 和截图。
2. 原生提交成功后匿名回读主描述逐字相等、公开可见性、兼容标签；下载 CDN 封面与附加图片并比较文件哈希和顺序。
3. 独立回读本次 Change Notes entry，HTML 解码、统一换行后精确比较冻结正文。提交成功不能代替公开正文验收。
4. 将旧订阅缓存完整备份，重新下载本条目；按正式 manifest 严格核验 32 文件，仅允许合同规定的 descriptor 换行和 remote_file_id 注入归一化。
5. 发布收尾立即恢复 Steam 离线，记录永久版本 changelog、发布回执、素材来源与缓存验证结果，提交并推送 master。

任何实际失败保留原始回执并说明未完成项；不把本地旧 descriptor version=9 当成匿名证明的上一公开版本，不把图片刷新或构建检查冒充游戏机制回归。

## R0011 发布前发现

新的截图取材中，两信条冷重载页和选择器已拍摄并入库。连续加入第三个真实信条后出现 `Absent is not allowed`；只读检查显示 100 槽 UI 模型非空索引 `[0,1,2]`，但另一组原生提交提案包含一个 Null/Absent singleton 和三条真实信条。这不是已知的中间空洞案例，发布前必须解决并真实验证。该草稿没有确认创建；其原始截图与只读证据保留在 R0011 的 `validation-investigation/`，不用于宣传图。

现有订阅缓存的外层 ACF `timeupdated=1777874459` 与匿名公开 API 相等，manifest 为 `3241202835495521309`，13 文件内层 descriptor 实际是 version=1 / supported_version=1.19.0.4。缓存已完整备份，摘要见 `previous-cache-manifest.json`；发布 changelog 应引用这一具体缓存身份，并保留尚未进行独立新下载验证的边界。
