# 潜在产出：实现与验收记录

2026-11-19；独立产品 `mod_potential_output/`，版本候选 0.1.0。此记录持续更新；初步静态结论不代表地图引擎和实机通过。

## 原版依据与实现

本机只读安装识别：CK3 1.21.0 Florin、Steam public / build 26757580；没有变更 Steam 模式或启动游戏。关键原文的规范化 SHA-256 见 [依赖清单](../dev_tools/potential_output_sources.json)，机器路径仅保存在忽略的本地配置。

原版 `common/trade/county_potential_trade_goods/*.info` 明确按县头衔列出可产商品；`gui/window_county_view.gui:5691` 使用 `County.GetPotentialTradeGoodTypes`。产品直接读取同一运行时列表，包含未投产资源，不估计产量、不改经济。官方开发日志也说明潜力按伯爵领配置：[Silk & Silver Dev Diary #9](https://steamcommunity.com/app/1158310/allnews/)。

独立地图 key `xapo_potential_output` 使用原版县界着色和县首府选择。`ProvinceIcon.GetProvince` 与 `Province.GetCountyCapitalProvince` 的比较把图标限定在伯爵领首府；每个商品图标读取原生 `TradeGoodType.GetSmallIcon`。原版引擎实际分配地图图标的缩放范围仍须实机检查。

界面入口与面板通过 `gui/scripted_widgets` 注册。面板按原版 need category 与 basic 标记分组，共44种商品。商品、分类、全选和清空只修改本机 `GetVariableSystem` 状态；多选按并集展示。不运行事件、on_action、决议、脚本效果或存档迁移；AI与经济状态不变。关闭面板保留当前筛选，关闭视角返回进入前的地图模式；退出游戏后筛选回到默认全选。

筛选的共同键由 `xapo_hidden_` 与原版 `TradeGoodType.GetTextIconNoFormat` 构成，面板通过已核对的 `GetTradeGoodType(native_good_key)` 取同一对象。键不依赖翻译或名称中的 tooltip 格式，只在 GUI 会话存在，不入存档。未知新增商品和全图转换 mod 尚未验收，不宣称兼容。

## 覆盖与升级风险

仅覆盖一份原生 GUI：`gui/map_icon_layer.gui`。生成器在 `province_map_icon` 的原生内容之前增加一个自定义控件，其余内容逐字保留；框架 `project/recover` 验证可逆性。因为 CK3 同路径 GUI 整份覆盖，其他覆盖该文件的 mod 需要专门合并补丁；MTS 两份宗教 GUI 不与它同路径，但组合实机尚未验收。原版变化时 hash 门禁拒绝生成，必须先审查差异。

新增地图定义只追加独立文件，不覆盖原版地图模式。图片仅引用当前游戏的原版图标，参考截图不打包，不包含跨游戏第三方素材。尚无 Workshop ID。

## 离线验证：通过，实机待验

- 框架结构扫描、原生依赖 hash、可逆投影与14文件生成一致性通过。结构扫描不提供 CK3 作用域或数据函数合法性认证。
- 九种语言共12个自定义键：UTF-8 BOM、语言头、结构、非空文本和键集覆盖通过；仅简中安排实机。
- 七项离线测试通过（5.848秒）：实际生成按钮表达式的44商品独立开关、清空后两商品并集、全选恢复、分类批处理快照及组外不变、原版全部县商品交集、投影拒绝原文变化、双构建一致及独立身份。
- 原版 GUI 资产路径检查通过；正式投影仅14个运行文件，ZIP与 manifest 双构建一致，`workshop_item_id=null`，不包含工具或夹具。

状态：`structural-static-pass`；`live-verified=NOT_RUN`；`published=NOT_RUN`。需要检查真实地图模式注册、GUI求值、所有县图标分配、缩放、筛选与恢复，不能以离线测试替代。

## 开发与构建

```text
<configured-python> -B -X utf8 dev_tools/potential_output.py generate --framework <framework> --game <game>
<configured-python> -B -X utf8 dev_tools/potential_output.py validate --framework <framework> --game <game>
<configured-python> -B -X utf8 dev_tools/potential_output.py build --framework <framework> --game <game> --output <new-output>
```

离线测试通过显式环境 `XAPO_FRAMEWORK_DIR`、`XAPO_GAME_DIR` 选择输入，运行 `-m unittest discover -s dev_tools -p test_potential_output.py -v`。公共实机入口按 [验收计划](potential-output-acceptance-plan.md)；本产品不自建第二套 runner。

归属决定：商品规则、生成器、命名空间、兼容边界及具体验收证据只服务本产品，留本仓库；解析、投影、安装识别、日志和确定性封包复用框架。通用地图图标分配与 GUI 接口的富化须等实机查明后再落成可复用知识，当前不把候选写成通用通过。

## R0001：真实加载，业务 RED

公共 GUI-only 生命周期，简中新局、1066.9.15维塔莱·法列罗，独立 profile，仅本产品。新视角与面板确实显示；远景和近景未看到县产物图标，核心需求未通过。日志另发现布局容器内的 `parentanchor` 与无效 `#small` 格式标签。原件与来源见 [R0001 精简证据](evidence/potential-output-R0001.json)。

通过官方调试控制台生成本构建 `script_docs` 和 `dump_data_types`，用来核对数据接口；原件只留隔离 profile，不搬入框架或产品。新发现 `GetTradeGoodType(key)` 全局 getter 和 `TradeGoodType.GetTextIconNoFormat` 确实注册，可据此使用不依赖语言的共同筛选键。数据类型注册仅证明接口存在，不证明地图图标已正确分配。

本轮实际保存12,319,604字节私有存档，原生退出桌面，公共 runner 正常结束；keeper 与 screen 释放已读回。无业务签核，共享 verify 返回非零，保留 RED；进程正常结束不代表功能通过。下一包修复布局、筛选键与地图图标路径后重验。归属：具体失败与产品修复留本仓；可复用的原生 GUI 接口研究在查明并验证后再富化框架。

## R0001 后续修复候选

已移除布局内的文本锚点、改用原生小字号样式，并增加不透明面板背景。共同筛选键改读原生商品 text-icon token。地图候选切换为原版 `economy_buildings` 着色／holding 选择来检查原生省份图标的创建路径；这时底图颜色仍是原生经济底图，不代表商品潜力。商品潜力真值仍仅来自县的潜在商品列表，是否正确绘制须在下一场实际核对。七项离线合同及双构建再次通过（6.450秒），不授实机通过。

## R0002：布局修复通过，地图业务仍 RED

源提交 `d29b192621e9586ef2a8a18148f3c16ea78ac61f` 冷启动后，候选 GUI 无前轮布局／格式警告，但新增地图模式仍未显示县潜力图标，核心业务失败。失败后仅在隔离 profile 热编辑进行图层诊断，备份原文并标记 `formal_business_acceptance_eligible=false`；诊断修改没有回写产品或正式 staging，也不能作为本轮业务通过证据。原生 ProvinceIcon 的无条件测试标记在政治视角出现，在自定义地图模式消失；其他原版图层仍须另行验证。

2026-11-19 01:13:30 UTC 原始 Popen 确认退出码 0；keeper 线程退出、screen CAS 释放读回成功。共享 verify 返回 2／INCOMPLETE，进程与闭环通过，业务和发布均未通过。没有填写通过签核。

用户随后要求先核对“潜在产出”含义，已暂停功能实现。核对结果见 [原版定义报告](potential-output-definition.md)：县级潜力配置涉及 35 种商品，不能把全部 44 种商品作为同等的潜力筛选项。原版概念、县面板数据绑定及资源地产条件均已交叉核对；后续实现须以该报告的集合语义为准。
