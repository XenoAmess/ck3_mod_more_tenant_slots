# R0011：Absent 是教条名称，撤回空槽归因

2026-10-03，工坊发布前拍照发现连续三个真实信条的草稿仍显示 `Absent is not allowed`。本次使用 R0011 的 CK3 1.20.0.3 现场，产品机制与 R0009/R0010 相同，仅预览图已更新；源码提交 `a0075f2`。本工作包不操作桌面、Steam 或游戏状态，不写进程内存，不调用游戏函数；进程只用 `PROCESS_QUERY_INFORMATION | PROCESS_VM_READ` 读取。具体摘要见 [收据](evidence/live-R0011-blocker-diagnosis.json)。

只读窗口中有 100 个信条槽和 128 个教条条目。连续非空下标 `[0,1,2]` 为 `tenet_communal_identity`、`tenet_sanctity_of_nature`、`tenet_anachoresis`；UI 教条与草稿教条都实际含 `doctrine_monasticism_absent`。数组头及内容双读一致，原始读取保留在 `artifacts/bf-202609141645-5434332d4d--more-tenets-slots--R0011/validation-investigation/`。父任务的原生 GUI 截图记录同一草稿费用 5400、偏离度 20，以及创建阻断。

原版 `localization/english/religion/religion_l_english.yml:1140` 将 `doctrine_monasticism_absent_name` 译作 `Absent`，简中对应为“不存在”。原版 `common/religion/doctrine_types/20_doctrines.txt:2247` 的该定义含：

```text
can_pick = {
    custom_description = {
        text = incompatible_tenet_anachoresis_trigger
        NOT = { tenet:tenet_anachoresis = { is_in_list = selected_doctrines } }
    }
}
```

因此，“Absent 不被允许”对应一个真实教条及其信条冲突。本次通过实际草稿 key、本地化与权威定义闭合了这一解释；独立替换信条的原生创建、付款、保存仍由后续实机验收确认。本轮没有修改产品 GUI、生成器或校验器，也没有增加占位信条。

冻结 EXE SHA-256 为 `94b55397abb687a3dcd436805a5d885e6be90fa6c693feb44a9e3bbeeade02a6`。以下地址均为该构建的 RVA，符号名称来自已注册窗口方法和框架已有研究，不外推其他版本：

| 路径 | 静态证据 | 对本次判断的意义 |
| --- | --- | --- |
| `GetCreationBlockers` `0x14F5780` → `CanCreateRite` `0x14F56D0` | 前者创建输出串后直接调用后者；后者执行最终 validator `0x29A2F60`，并无条件继续名称唯一性 `0x14F8930` | 文本包含真实原生创建限制，不能因显示词看似“空缺”而删除 |
| Rite requirements `0x29C9760` | `0x29C9A30` 起枚举教条，检查 `can_pick`/`is_shown`；`0x29C9A9E` 引用 `RITE_CREATION_VIEW_BLOCKER_CREATION_DOCTRINE` | 该模板使用失败的实际 `DoctrineType.GetName`，不是空槽错误专用消息 |
| 信条选择重建 `0x14F8660` | 展示槽的原生 NULL 对象会进入临时核心信条提案；同一现场确有一个 NULL 和三个真实 key | 这是读取事实，单独不能证明 NULL 导致当前拒绝 |
| 原生创建确认后回调 `0x14F51D0` | `0x14F53C0` 检查 `ObDG` 类型标记，只收集真实对象，随后调用原生命令队列 | 存在原生过滤空对象的执行路径；未经实际创建不能把静态过滤称为保存通过 |

曾考虑精确匹配单一 `Absent` blocker 来启用创建按钮。查明其教条来源后该方案撤回：它会放行真实 `can_pick` 冲突，违背保留原版合法性的产品要求。`CalcPietyMissing` 还是费用减余额的有符号结果，若以后有独立、实证的 UI 修复需求，足额条件应是 `<= 0`；本次不引入该条件或任何按钮旁路。

最短复验路线是保留源码，将第三条换为与当前教条兼容的真实信条，先证明连续三个信条的原生创建、扣费和保存。若继续使用 Anachoresis，应先在原生界面选择兼容的修道制度，并核验其他原生条件。第 100 槽的稀疏选择须单独实测；R0008 选择相同的 Anachoresis 后被拒绝，不能证明中间空洞不合法。R0006/R0009 的两个真实信条加尾部空槽通过事实继续有效。

归属：本产品草稿 key、截图关联、具体来源哈希和验收勘误留独立项目。先追查本地化与数据库定义、再比对原生 key 与校验链的方法，以及将观测和因果判断分开的原则，富化至框架 `docs/external-mod-source-projections.md`。不把游戏二进制、存档或产品定义搬入框架，不把此实例外推为其他 mod 或所有信条组合通过。
