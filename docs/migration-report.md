# CK3 1.20.0.3 兼容迁移记录

目标 `more_tenets_slots_xa_dev/`，旧版本 `9` / CK3 `1.19.0`，迁移版本 `10` / CK3 `1.20.0.3`。本机 launcher 与 EXE 已实际核对，Steam build `25652598`，EXE SHA-256 `94b55397abb687a3dcd436805a5d885e6be90fa6c693feb44a9e3bbeeade02a6`。输入哈希见 [精确输入合同](../dev_tools/ck3_1_20_0_3_sources.json)。迁移前不兼容，详见 [冻结分析](evidence/compatibility-before.json)。当前状态 `static-ready`，实机尚未验收。

## 分析与修复

旧 mod 定义 170 条教义，其中真实核心教义 73 条、空槽 97 条；新版原生 `tenet_types` 共 97 条，旧 `tenet_monasticism`、`tenet_rite` 已不属于新版核心 tenet 类型。旧完整教义副本无法用于新版的 Rite/TenetType 界面，删除其副本和退役的 `doctrine_core_tenets` 组，直接继承新版所有原生 tenet 定义、费用、互斥和 DLC 条件。

新版 `NReligion.FAITH_CORE_TENETS_CAP` 原生上限为 3，迁移改为 100；`pam_faith_core_tenets_cap_value` 是会议逻辑使用的镜像值，原版注明必须与 define 同步，因此同时改为 100。保留 `NCulture.DEFAULT_MAX_TRADITIONS = 10000`。这不是个人 tenet 上限扩展；实际可选数量仍受当前游戏定义及互斥/DLC 限制，不能声称有 100 条相互兼容的真实 tenet。

新版原版 `window_faith_creation.gui` 已移除，改用 `window_rite_creation.gui`。生成器只对新版创建窗口的核心 tenet 网格，以及新版信仰窗口普通/紧凑两网格加入有界滚动容器；保留原生选择、费用、分歧、流行度、信仰/Rite 页签与其他操作。反向移除三处投影后逐字恢复冻结原版。生成 GUI 不得手改；原版的空白格式保留，GUI 的 diff whitespace 检查允许原版 trailing whitespace。

旧 `on_faith_created` 的角色 root 与字符事件清理不适用于新版的信仰 root。迁移移除整个旧钩子/清理事件和空槽图标，直接继承全部新版原生创建副作用；不注册空槽 tenet，不运行旧清理。新版是否允许未填满所有上限槽创建，以及100上限的原生渲染/创建行为，须由实机进一步验证。

内层 descriptor 不再携带 `remote_file_id`，正式 Workshop 身份仍为 `3182367229`；本任务没有发布工坊。作者许可截图保留在源码仓库，正式构建仅允许8文件，不包含截图、夹具或报告。原有中英文 Shang Confucian 文案保留，未新增多语言发布翻译。

## 复现与验收

需要本项目和 `ck3_eternal_recurrence` checkout，以及完整 CK3 1.20.0.3 安装。命令中的路径使用实际本机路径：

```text
python dev_tools/migrate_to_ck3_1_20.py --framework <framework-root> --game <ck3-installation>
python dev_tools/validate_and_build.py --framework <framework-root> --game <ck3-installation> --output <new-build-directory> --report <report.json>
```

生成器冻结游戏版本、EXE 与原版依赖输入；依赖变更时拒绝生成，须重新审阅。验证器检查生成一致性、可逆正文、上限同步、退役依赖、BOM、结构、本地化和产品allowlist，并复用框架构建原语进行双构建ZIP/manifest对比。花括号检查是结构扫描，不等于完整CK3语法解析。

`open_kaishek` 本机 checkout/JAR 不存在，框架适配器返回 `not-applicable / open_kaishek-root-missing`，原件见 [预验回执](evidence/kaishek-before.json)。这是环境缺口，不是宗教语义通过；实机不得省略。

[静态验收回执](evidence/static-validation.json)：9类检查全部通过；3处 GUI 投影反向恢复原版 SHA 通过，正式8文件的两次 manifest 与 ZIP 完全相同。原版 tenet 数据库和 on_action 没有产品覆盖。生成GUI使用保留原版空白的diff检查，其余文件标准diff检查均通过。本机安装完整，当前无CK3进程；下一步为隔离实机。初次构建的commit记录指向生成时已有的计划提交，后续验收构建将绑定实际迁移源码提交。

## 系统富化与归属

已将通用可逆投影、结构扫描和覆盖迁移方法提交到框架 `36a225237`（7项生产路径测试通过）：[框架方法合同](https://github.com/XenoAmess/ck3_eternal_recurrence/blob/36a225237/docs/external-mod-source-projections.md)。工具没有mod ID、宗教机制或固定机器路径。产品投影布局、cap配置、输入pin、构建allowlist和具体验收证据仅留本独立仓库。当前无需新增通用宗教AI/策略或原生研究矩阵。

POD 两产品源码没有迁移，原版结果不适用于它们。跨CK3 1.19→1.20旧存档不能保证兼容；没有取得旧扩槽存档实证前不作存档迁移承诺。
