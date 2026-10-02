# R0005：新版创建窗口接口核对

本轮是兼容故障调查，不是产品实机验收。输入为 `43765b0ffa53ea84e398e02e64086915be387624`，使用独立 userdir，原生主菜单执行 `dump_data_types` 后正常 Exit to Desktop，进程退出码 0。游戏内实际导出文件的 SHA-256 见 [收据](evidence/live-R0005.json)；外置目录为 `artifacts/bf-202609141645-5434332d4d--more-tenets-slots--R0005/`。

`DoctrineCategoryWindow` 导出 `ShowWindow`、`ShowWindowSortList`、两个候选数据模型以及槽号 getter；没有导出独立的教义窗口打开函数或槽号 setter。`RiteCreationWindow.SelectTenet` 接收 `TenetItem`。冻结 1.20.0.3 EXE 的只读反汇编显示，该动作从条目读取槽号，并检查它在实际教义槽数组范围内。R0004 的崩溃则发生在打开窗口时：同一个槽号被用于教条数组，并且读取前没有相应范围检查。这解释了“100 个槽已生成”和“点击第 100 槽崩溃”为何同时成立。

没有修改游戏二进制、进程内存、产品或存档。导出清单不能证明所有内部方法不存在；尚未验证任何兼容方案，产品仍为实机 RED。

用户新增优先级：先验证两个真实信条及其他空槽也可创建、保存和重载。隐藏中性教条方案只记录为备选，尚未实施。空槽保存与末端点击分别验收，不能相互代替。

归属：本轮具体 GUI 方法和产品故障证据留在本项目；datamodel 数量与消费者可用索引必须分别验证的通用反例，考虑富化 `ck3_eternal_recurrence`。
