# 2026-10-15 用户反馈整改记录

执行清单见 [计划](bugfix-plan-2026-10-15.md)。本轮起始公开产品是 [v10](workshop/publication-v10.md)，已于 2026-10-03 发布；源码整改、当前版本实机与下一次正式发布分别记账。

## WP1：信条与文化传统分离

状态：**静态通过；当前版本实机及发布待执行**。

旧 `common/defines/More tradition slots.txt` 同时包含 `NCulture.DEFAULT_MAX_TRADITIONS=10000` 和 `NReligion.FAITH_CORE_TENETS_CAP=100`，因此仅需信条槽的玩家也被强制修改文化传统上限。现移除整个 `NCulture` 覆盖，文件更名为 `more_tenets_slots.txt`；主产品继承原版文化基础上限及时代等增益，继续保留 100 个信条槽和会议镜像值。本轮不增建新的传统扩展产品，避免把捆绑改成另一项默认依赖；需要额外文化传统的玩家可独立选择传统 mod。

静态回归命令：`python -X utf8 dev_tools/test_caps.py --framework <framework>`，2 项通过。测试消费正式 `validate_caps`，并证明把旧文化覆盖藏到另一文件名也会被拒绝。未以此证明旧存档超过原版文化上限后的所有行为；已选择传统是否保留及是否可继续新增仍待代表性实机。

本机发现当前 CK3 为 `1.20.1`；旧产品精确 `1.20.0.3` 合同静态检查按预期返回 RED，原件摘要见 [基线](evidence/bugfix-20261015-baseline.json)。在更新原版投影及验收输入前，不能声称本轮完整构建或实机通过。

归属：具体文化上限和产品防捆绑检查属于本产品；复用框架 `ck3_text_projection.masked`，没有复制 parser。此包没有新增通用实现；其差异、测试与边界留本报告，后续综合方法再评估框架富化。

## 当前原版投影迁移

状态：**静态通过；仍保留待修复的隐藏教义准备机制，未授业务通过**。

当前安装为 CK3 `1.20.1 (Crozier)`、Steam build `25870654`，EXE `101124216` 字节，SHA-256 `2667e409f586f20d60142873ccb1b4eb345eee54ed996925115a46132260cff7`。新增 [精确输入合同](../dev_tools/ck3_1_20_1_sources.json)，保留原 `1.20.0.3` 合同作为历史输入。

两个 GUI 从当前原版重新生成并可逆恢复。恢复新版的 `TenetPickableForEditedRite` 合法性检查、受限候选提示、自动命名/描述入口、描述长度 define、教义 tooltip block 名及布局修订；没有旁路费用或合法性。`TenetPickableForEditedRite` 来自当前原版 `game/data_binding/pam_data_bindings.txt`，属于编辑主礼仪时的流行度候选限制，不能据此断言它修复了旧条目残留。

开发产品版本提升为 `11`，不表示已经发布。执行 `python -X utf8 dev_tools/validate_and_build.py --framework <framework> --game <game> --report docs/evidence/bugfix-20261015-1201-projection.json`：精确来源、可逆投影、上限/加载顺序、46 文件 allowlist、九语言格式和确定性双构建通过；[收据](evidence/bugfix-20261015-1201-projection.json) 明确保留 `live_verified=false`。

旧 GUI 和当前原版都调用 `ShowWindowSortList(TenetItem.GetSlotIndex)`。当前 EXE 的只读窄链复核仍存在以信条槽号读取另一教义向量的风险，故本包不直接删除 100 个兼容条目。原版 `on_rite_updated` 会对教义变化发送 `msg_rite_updated`；旧准备 effect 连续 `change_rite_doctrine` 100 次构成明确通知生产链，但没有发现本 mod 的周期事件钩子。**百连通知可解释，永久循环尚未实机证实。** 后续继续核对普通教义索引和静默添加原语，不以屏蔽原版通知代替根因修复。

归属：当前版本 GUI、输入 pin、产品版本和具体报告归本项目，复用框架文本投影与构建原语；索引与副作用排查方法待有结果后富化框架。公共 native runtime 仍绑定 `1.20.0.4`，本机暂无可调用 operator/gameplay MCP；实机前将补公共入口的官方 GUI 执行路径，不能注入失配 DLL，也不能沿用旧私有 launcher。

## 公共验收入口接入

本机原公共 runtime 的 native 部分精确绑定 `1.20.0.4`，而当前游戏已为 `1.20.1`；本机也没有 operator/gameplay MCP endpoint。框架新增公共入口的显式 `gui_only` 后备路径，已提交推送 `cf476f656b592190b818a04582434b11667ef87a`，合同在框架 `docs/ck3-mod-acceptance-gui-only.md`。它仍消费统一 manifest、任务总线/keeper、隔离 userdir 和真实游戏 SHA，不注入旧 DLL。离线8项、路由2项和原公共入口22项通过；没有据此授产品实机通过。

本产品提供 [业务 case 数据](../dev_tools/acceptance_products.json)，八个必要证据键覆盖本轮反馈、末槽、创建、文化上限及保存冷载。机器路径、全局 manifest 映射、旧存档与正式 staging pins 留本地配置。本轮公共 `plan` 已消费该产品，结果为 `NOT_RUN/business_pass=false`；不是业务验收。

归属：通用 GUI 后备执行、租约和证据判定属于框架，具体 case、正式产品和源存档属于本仓。没有扩大为通用宗教 AI 研究或把 GUI 通过宣称为 native capability 资格。

## 后续工作

教义空白、替换残留及通知仍在排查。当前未进行新实机、工坊上传或新增发布；不改变 v10 历史结论。
