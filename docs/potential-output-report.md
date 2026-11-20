# 潜在产出：实现与验收记录

更新：2026-11-20。独立产品 `mod_potential_output/`，版本 0.1.0。**已完成本地实现、静态验证、简中实机验收及 Workshop 正式发布。** [工坊条目 3842767123](https://steamcommunity.com/sharedfiles/filedetails/?id=3842767123)、[发布回执与范围](workshop/potential-output/publication-0.1.0.md)。使用方式见[玩家说明](potential-output-usage.md)，原版定义见[研究报告](potential-output-definition.md)。

## 最终行为与依据

视角展示伯爵领可以生产的商品，包含尚未开发的资源，数据直接取自原版 `County.GetPotentialTradeGoodTypes`。只提供原版县潜力表中存在的 35 种商品；其余 9 种加工商品不进入筛选。原版潜力表共有 3549 个县，潜力种类数为 2–6；它没有提供储量或月产量。

地图数字和底色共用同一个值：县潜力商品集合与已选商品集合的交集大小。0 为灰色，种类越多绿色越深。单选为 0/1，多选为 0/1/2 等。商品独立开关、整类开关、全选、清空、面板收起与展开均已实现。近距离显示县首府上的商品图标及计数，远距离保留底色。再次进入默认全选；收起面板保留筛选；关闭视角恢复先前地图与相机。

右下角「潜在产出」入口先打开说明，再点击「显示地图」。实现使用原版活动规划地图的全省份定位与评分刷新，不注册不能分配足够图标的自定义地图模式。专用展示活动禁止实际启动与 AI 选择，不收取活动费用，不推进日期。刷新先完成 ScriptedGui 筛选写入，再通过 0.3 秒动画的 on_finish 重新选择原生选项并进入选址，避免读到上一轮筛选。

筛选使用玩家角色上的 35 个 `xapo_hidden_` 展示变量；退出规划器清理，再次进入也会重置。它们不影响经济、资源、建筑、头衔或 AI。若在视角内保存，变量可能随存档保留，因此不再沿用早期“仅 GUI 状态、绝不入存档”的说法。

## 验证与证据

游戏：CK3 1.21.0 Florin，Steam build 26757580；EXE SHA-256 为 `bb3fef106240e95ecdb6f1532982e89e9432c92a99d33db623521572f06e6f79`。运行时使用冻结框架提交 `ef4fd06cd3b9a41030127759e0c63552c70da57b`，公共受管入口负责离线准入、独占、原进程等待与租约释放。当前没有可用的 CK3 MCP 工具，本次按已记录缺口使用官方 GUI 路径；未注入桥接代码。

最终运行代码提交：`58e8727b57187ba5289193ed10d7f68e5663bc56`。23 个交付文件与实测构建逐文件 SHA 完全一致。八项离线测试通过（11.071 秒），覆盖实际按钮表达式的独立切换、空集、多选、整组快照、原版所有县的交集、可逆投影、原生窗口状态层级、独立身份与双构建一致性。九语言的 BOM、结构、非空文本和键集通过；仅简体中文实机验收，不将格式校验称为其他语言体验通过。

| 实机记录 | 结论 |
| --- | --- |
| R0009 / acc4a98 / map-filters | 15 项地图业务与正常退出通过；随后闭场日志发现布局错误，不能称零项目错误 |
| R0010 / 06c3917 / existing-save | 三项独立旧存档业务与正常退出通过；仍有同一布局错误 |
| R0011 / 58e8727 / map-filters | 修正布局后，15 项地图业务再次通过；同一旧存档的加载、潜力图标、过滤也重新直接核对 |

R0011 实际观察：清空时陆地为灰色；谷物单选时各县显示 0/1；加入粟后显示 0/1/2 及对应的深浅；谷物分类整体开启与关闭正确；全选恢复全部潜力图标及各县 3/4/5 等计数。面板收起再展开保留状态，退出后恢复政治地图。原版宴会类型选择和选址正常，专用面板不混入原版规划器。活动列表没有新增正在进行的活动，金钱仍为 50，日期始终为 1066 年 9 月 15 日。

R0011 从冻结正式构建冷启动，没有热改 profile 或诊断控件。通过游戏菜单退出桌面，原始 Popen 返回 0，未触发超时关闭；keeper 与 screen 租约已释放。公共 verify 返回 `process_pass=true`、`closure_pass=true`、`gui_business_pass=true` 和 `case_acceptance_pass=true`。它不授 Workshop 或通用 native 能力资格。

闭场日志经框架两次有界一致读取与完整分组：1005 字节，SHA-256 `034945e50c6a698a903644a16132ec19830d91e34c7a62884baa89657fa0f6c3`，仅 1 条既有原版 Generated Map Objects 读取错误。此前本产品的 `Widget cannot have a position in a layout` 已归零。没有把原版错误删掉或计成零日志。

可审计的运行身份、构建、图片与退出回执 hash 见[证据索引](evidence/potential-output-live-20261120.json)。原始图片、私有存档、机器配置与原生完整文件在忽略的本机 artifacts 中；干净 clone 只包含索引，不保证这些本机原件可用。GUI 实测是代表性县与两种商品组合，不宣称逐个点击过全部 35 个商品或逐县实测。

## 交付与兼容

可用 ZIP：`artifacts/potential-output-20261119/tested-build-a11/mod_potential_output.zip`，64056 字节，SHA-256 `955e9ee13b4e2e3db1bd4eb50e122d94aeb7bfff059c5cbf70200ede4eb1d4e5`。同目录 manifest 绑定上述代码提交，`product=mod_potential_output`、`workshop_item_id=null`，保留为发布前实测记录。正式 tag `potential-output-v0.1.0-ck3-1.21.0` 的两次构建与实测 23 文件完全一致，首次发布后另存[含 canonical ID 的清单](workshop/potential-output/evidence-0.1.0/release-manifest.json)，不改写原 tag、构建或运行文件。

正式发布包含四张真实游戏截图及正文穿插图，公开标题、完整说明和更新日志均回读一致。首次中文标题因 PowerShell 管道将 Python 字面量转为问号，已更新同一条目并在匿名 API 和浏览器中核对修复。R0012 从 Steam 实际下载目录启用并挂载，23 文件精确匹配；正常 GUI 退出、原进程 0、keeper 与 CAS 释放及最终 Steam 离线均通过。其间本机已更新为 1.21.0.3／build26785313，本次缓存验收只证明该版本的菜单加载；上文地图与旧存档功能实测仍属 1.21.0／build26757580，不将缓存加载写成新版本完整功能验收。

需要投影三份原版 GUI：`gui/map_icon_layer.gui`、`gui/window_activity_planner.gui`、`gui/window_activity_list.gui`；依赖原文 hash 改变即拒绝生成。每份投影能逆恢复固定原版全文。其他覆盖同路径的 Mod 需要合并补丁。全图县数据模型复用原版，地图图标只放在县首府；四张透明 DDS 为自行生成的占位资产，没有打包参考截图或复制其他游戏素材。

活动规划器评分共用灰绿配色，普通活动的评分地图也会呈现这套色板。进入视角暂时占用规划器，请先退出其他活动规划。当前活动中或旅行中的角色、多人游戏、MTS/POD 组合、大地图转换 Mod 与其他 CK3 版本未独立实机验收，不作兼容承诺。密集地区全选时图标可能重叠，可进一步放大或筛选商品。

## 开发与归属

```text
<configured-python> -X utf8 dev_tools/potential_output.py generate --framework <framework> --game <game>
<configured-python> -X utf8 dev_tools/potential_output.py validate --framework <framework> --game <game>
<configured-python> -X utf8 dev_tools/potential_output.py build --framework <framework> --game <game> --output <new-output>
```

离线测试使用显式 `XAPO_FRAMEWORK_DIR`、`XAPO_GAME_DIR`，运行 `-m unittest discover -s dev_tools -p test_potential_output.py`。安装识别、解析、可逆投影、日志分组、构建和受管生命周期复用框架；商品清单、筛选与产品证据留本仓库。可复用的 GUI 上下文、布局与刷新时序发现归框架知识文档，不搬运产品源码、私有存档或第三方素材，不外推本产品通过结论。

框架富化已正常提交推送：[c82e82ebe / GUI 经验](https://github.com/XenoAmess/ck3_eternal_recurrence/blob/c82e82ebeac09d32196debb62b2deca1530763ba/docs/grammar/pitfalls.md#gui-上下文地图评分刷新与布局动画2026-11-20ck3-1210)。仅修改知识文档，经差异、编码及证据边界检查；实机原件仍绑定运行时冻结的旧框架提交，后续框架更新不追认其资格。

## 历史失败边界

| 记录 | 保留的失败事实 |
| --- | --- |
| R0001–R0002 | 新地图 key 没有分配全图县图标；原始退出 0，业务未通过 |
| R0003 | 原生规划图层可分配图标，但重复男爵领与初始脚本错误；只作诊断 |
| R0004 | widget 属性、TopScope promote、宾客上限错误；超时触发关闭，未通过 |
| R0005 | 初始化界面不可用；外部作用域警告，业务未通过 |
| R0006 | 全局按钮错误引用窗口上下文，重叠控件挡住入口；清空不能刷新底色 |
| R0007 | 入口修正；仅重新进入选址仍使用旧评分，未通过 |
| R0008 | 诊断证明选项重选及延迟回调可刷新评分；超时且有 profile 热改，未授正式 PASS |

历史原件仍保留于本机 artifacts；旧报告中早期 44 商品、自定义地图 key、只覆盖一份 GUI 和绝不写角色变量等候选描述由本文最终实现取代。Git 历史保留原始失败报告，不追认历史诊断为正式包通过。
