# 潜在产出：实现与验收记录

2026-11-19；独立产品 `mod_potential_output/`，版本候选 0.1.0。此记录持续更新；初步静态结论不代表地图引擎和实机通过。

## 原版依据与实现

本机只读安装识别：CK3 1.21.0 Florin、Steam public / build 26757580；没有变更 Steam 模式或启动游戏。关键原文的规范化 SHA-256 见 [依赖清单](../dev_tools/potential_output_sources.json)，机器路径仅保存在忽略的本地配置。

原版 `common/trade/county_potential_trade_goods/*.info` 明确按县头衔列出可产商品；`gui/window_county_view.gui:5691` 使用 `County.GetPotentialTradeGoodTypes`。产品直接读取同一运行时列表，包含未投产资源，不估计产量、不改经济。官方开发日志也说明潜力按伯爵领配置：[Silk & Silver Dev Diary #9](https://steamcommunity.com/app/1158310/allnews/)。

独立地图 key `xapo_potential_output` 使用原版县界着色和县首府选择。`ProvinceIcon.GetProvince` 与 `Province.GetCountyCapitalProvince` 的比较把图标限定在伯爵领首府；每个商品图标读取原生 `TradeGoodType.GetSmallIcon`。原版引擎实际分配地图图标的缩放范围仍须实机检查。

界面入口与面板通过 `gui/scripted_widgets` 注册。面板按原版 need category 与 basic 标记分组，共44种商品。商品、分类、全选和清空只修改本机 `GetVariableSystem` 状态；多选按并集展示。不运行事件、on_action、决议、脚本效果或存档迁移；AI与经济状态不变。关闭面板保留当前筛选，关闭视角返回进入前的地图模式；退出游戏后筛选回到默认全选。

筛选的共同键由 `xapo_hidden_` 与原版商品名称构成，面板用 `Localize(native_good_key)`、地图用 `TradeGoodType.GetName`。这些键只在当前语言的 GUI 会话存在，不入存档。未知新增商品、同名商品和全图转换 mod 尚未验收，不宣称兼容。

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
