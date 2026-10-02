# CK3 九语言本地化覆盖与格式认证

日期：2026-10-03。产品：`more_tenets_slots_xa_dev`，版本 `10`，Workshop item `3182367229`。用户明确要求此次发布补齐 CK3 全部支持语言，并指定后续实机只用简体中文；其他语言只做格式认证，不启动游戏测试。规则由主线程记录到根 `AGENTS.md`。

## 实际语言集合

本机冻结输入是 CK3 `1.20.0.3 (Crozier)`，Steam build `25652598`，EXE SHA-256 `94b55397abb687a3dcd436805a5d885e6be90fa6c693feb44a9e3bbeeade02a6`，沿用 [原版输入合同](../dev_tools/ck3_1_20_0_3_sources.json)。

语言集合来自当次安装的 `launcher/settings-layout.json` 中 `name=language`、`provider=lang` 的九个下拉选项，并逐一核对 `game/localization/<language>/` 的实际目录及原版 `.yml` header。该 launcher 文件 SHA-256 为 `649319eebff6212e1993e54bd0dc652c35e2158f77909ed9fb8bd840f2648eb9`。原有隔离 userdir 的 `pdx_settings.txt` 只保存当次选中语言，不能用它单独枚举支持范围。

`game/localization/jomini/` 是引擎内容目录，内部实际 header 是 `l_english` 等，并不是一种语言。Jomini 账户界面附带的其他翻译也不属于本次 CK3 游戏语言下拉选项。因此不添加 `jomini`、繁体中文或其他未被该安装提供的语言。

| CK3 locale | 语言 | 产品文件数 | 真实文案键 | 隐藏空键 | 本工作包认证 |
| --- | --- | ---: | ---: | ---: | --- |
| `english` | 英文 | 2 | 5 | 300 | 格式通过；未新增实机测试 |
| `french` | 法文 | 2 | 5 | 300 | 格式通过；未实机测试 |
| `german` | 德文 | 2 | 5 | 300 | 格式通过；未实机测试 |
| `japanese` | 日文 | 2 | 5 | 300 | 格式通过；未实机测试 |
| `korean` | 韩文 | 2 | 5 | 300 | 格式通过；未实机测试 |
| `polish` | 波兰文 | 2 | 5 | 300 | 格式通过；未实机测试 |
| `russian` | 俄文 | 2 | 5 | 300 | 格式通过；未实机测试 |
| `simp_chinese` | 简体中文 | 2 | 5 | 300 | 格式通过；后续实机由发布线程负责 |
| `spanish` | 西班牙文 | 2 | 5 | 300 | 格式通过；未实机测试 |

合计 18 个本地化文件，每语 305 键，九语共 2745 条键定义。新增七语共 35 条真实译文和 2100 条空文本定义。正式 release allowlist 从 32 文件扩为 46 文件；语言文件之外的 GUI、教条、费用、效果及存档机制没有在本工作包修改。

## 文案与翻译审阅

两种文件族均位于 `localization/<language>/religion/`：

- `MTS_religion_confucianism_l_<language>.yml`：既有 `shangru`、`shangru_adj`、`shangru_adherent`、`shangru_adherent_plural`、`shangru_desc` 五个商儒文案键。中英文原文保持；仅统一单空格缩进和显式 `:0` 版本字段。
- `mts_selector_l_<language>.yml`：100 组隐藏选择器元数据的组名、教条名、描述，共 300 键，所有语言均为真正的空字符串 `""`。这些条目不成为真实信条，也不添加可见文字、费用或机制效果。

迁移后的 GUI 仍引用新版原生 UI 和原生信条数据库。卡片、原生按钮、费用及提示继承游戏本身的各语翻译；不复制或伪造额外 GUI 译文。源码搜索没有发现除商儒五键及隐藏元数据以外的新玩家文案。

按照框架 [国际化翻译合同](../../ck3_eternal_recurrence/docs/localization-workflow.md)，开始前只检查 `MINIMAX_API_KEY` 是否存在，未输出或记录值。复用现有 `tools/translate_localization_minimax.py`，模型 `MiniMax-M3` 仅接收五个已选定 key-value、中英参考、七个目标语言及商周/上帝祭仪的最小语境，返回候选 JSON；未让其设计代码、决定文件或判断验收。

候选经执行者逐条检查后才落盘：修正法文与俄文将仪式名称误写为单个信徒的问题；重写日文偏离“遗忘的约仪”的句子；移除韩文候选混杂汉字与重复短语，改为连贯韩文。上帝统一按商代祭祀语境理解为 Shangdi／上帝／상제，避免补入基督教含义。七语均检查商周年代、龟甲、青铜器、烈火、颅骨供奉和祖先约仪的语义意象与术语一致性。

这属于译文候选审阅及格式认证，不是七语母语者签核。未进行任何其他语言的游戏内布局、截断或运行测试，也不宣称这些语言实机通过。按用户新规则，后续原生实机验收只使用简体中文。

## 校验与构建结果

[选择器生成器](../dev_tools/selector_padding.py) 只将冻结语言集合从两语扩为九语；隐藏组、教条及准备效果生成机制保持一致。[产品校验与构建器](../dev_tools/validate_and_build.py) 复用框架已有严格 CK3 本地化 parser 与 protected-token 校验，无需新增或复制通用解析工具。

2026-10-03 必要校验通过：

- 实际 launcher 支持列表恰好等于冻结九语列表；各原版语言目录存在。
- 18 文件 UTF-8 BOM、精确 `l_<language>:` header、显式 `:0`、合法双引号及转义，严格逐行解析通过。
- 每个文件及跨文件无重复键；各语键集完全一致，恰好 305 键。
- 商儒五键各语均非空，无英文占位；300 个隐藏键各语均保持空字符串。
- CK3 scope、格式、变量、图标及转义 token 与基准一致；本产品这五个真实文案没有动态 token。
- 既有精确原版来源、可逆 GUI 投影、cap、加载顺序及 46 文件 release allowlist 检查通过；临时双构建 manifest 与 ZIP 完全一致。

运行入口（路径由发布者显式提供，不把本机路径当作协议前提）：

```text
<python> dev_tools/validate_and_build.py --framework <framework-root> --game <ck3-install-root> --report <new-report-path>
```

本轮原始收据保留于外置 `artifacts/localization-20261003/static-certification.json`，SHA-256 `5f957d63f64bcf2fa323e6aa8a87a76052b218b767632b958bbe768d7e599004`，使用框架 commit `18dee6291c3e9d2374ac6e8117e208cf1c8319de`，`localization.status=format-certified`、`live_verified=false`。临时双构建 ZIP SHA-256 均为 `2f27143085b94fa6737d31f8dc836b3ed26c8a1ed8fd690f2c137117b613b621`。临时构建用于本工作包必要验证；发布线程会从已提交源码、最终 thumbnail 与正式发布 tag 重新生成实际上传包，不把这个提交前临时 manifest 的 HEAD 当作最终发布绑定。

## 归属决定

商儒译文、隐藏选择器空键、冻结九语清单、产品 allowlist 和本报告只描述本产品，留在独立项目。格式解析、保护 token、MiniMax 最小候选调用器已在 `ck3_eternal_recurrence` 提供，直接复用；不为本包复制同类实现或新建第二个通用工具。已考虑系统富化：跨 mod 可复用方法见框架现有国际化合同，本次没有形成新的通用能力缺口；后续“只简中实机、其他语言格式认证”的用户策略由主线程在相关 AGENTS 规则中落盘。
