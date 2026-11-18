# CK3 1.21.0 简中实机验收

## 新局 GUI 业务通过；冷载与发布仍待完成

运行 `pc-20260924rtuf-f11af23c08--more-tenets-slots--R0001`，2026-11-18 16:11:52–17:45:48 UTC。游戏1.21.0/build26757580，产品源码 `eb4f0dd74259586056af65cfab2d29c7bbe84d57`，框架 `2fafef1ea76be4087725112760df8605c6816f89`。公共GUI-only入口、隔离userdir、Steam离线、唯一CK3及共享keeper；未注入旧ABI DLL。实机仅简体中文。

| 项目 | 实际结果 |
| --- | --- |
| 普通教义 | 性别三候选正常；男性主导改男女平等，实际保存 `doctrine_gender_equal` |
| 核心信条 | 天主的和平换仁爱；保存的core为 `tenet_apostolic_succession`、`tenet_philanthropia`、`tenet_communion` |
| 第100槽 | 末尾单卡选入事奉圣礼，费用/偏离度变化；取消整个创建再重开后为空，费用恢复 |
| 稀疏创建 | 三个真实core创建阿普利亚天主教礼仪，容量100，余97未填，无假信条 |
| 新版戒律 | 丧葬、加冕、有息贷款、酒精及食物限制保留，界面和存档一致 |
| 文化 | 诺曼界面4/6，符合原版基础5加当前时代1 |
| 通知 | 处理教廷权威及新礼仪两个原生事件；推进1066.9.15至9.26，最终未出现礼仪事件连发 |
| 保存 | 原生UI实际写出ZIP，SHA256 `09527cd7f8813bc3d7831bf6f8ab60e8132e39079c9b521a1c443456f9f2403c` |
| 退出 | 原生退出桌面，原始Popen wait返回0；keeper线程退出无失败，screen释放 |

新版原生条件要求天主教世俗统治者先拥有领地司祭傀儡。本次通过原生互动满足，花费100虔诚，没有修改权限或用夹具设置信条。夹具只在新局提供100000虔诚。创建确认费用5287，创建后余额94762；最终存档绑定玩家36423、礼仪150、信仰14、创始人36423。

历史“两真实信条”计划调整为本轮罗马礼原生三个core加97尾空；两core独立案例本轮 **NOT_RUN**。没有为改变初始数量修改礼仪。尾空结论来自取消/重开界面及保存的core状态，permitted/known/prohibited记录不算core。

共享verify为PASS，process/closure/GUI business均true；native_capability_pass及product_release_pass为false。紧凑证据见 [JSON](evidence/upgrade-20261119-source-live.json)。原图、日志、受管回执和私有存档保留在忽略的 `artifacts/upgrade-20261118/`。

## 日志与归属

error.log为1503字节：原版长城地图对象数量诊断、预期的同名on_rite_updated effect替换警告、原版 `gdp_republic_interactions.txt:3503` 在打开司祭互动时的无效character scope诊断。没有声称零错误或完成原版A/B因果归因。创建、实际保存与正常退出独立验证。

产品源码、场景和具体证据归本项目，私有存档不入库。复用框架已有受管生命周期、坐标映射、Win32扫描码类型和有界无损存档解析器；通用Steam CEF识别修复已提交框架。未扩大为宗教AI研究，GUI及离线保存读回不等于新版native/MCP资格化。
