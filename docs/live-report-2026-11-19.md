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


## 独立冷载通过

R0002 / PID18452，独立隔离userdir，仅正式产品；精确复制R0001的存档。载入1066.9.26，罗贝尔/阿普利亚天主教、三个core与男女平等教义保留，原生面板正常，实际超过75秒未出现礼仪事件连发。资源夹具未挂载，载入列表的缺少mod提示对应此夹具。正常退出桌面，原始Popen返回0，keeper和screen释放通过。共享verify为PASS；新版native/MCP资格化及正式发布仍不由此推定。日志1183字节，保留长城原版诊断及同名effect警告。见[冷载证据](evidence/upgrade-20261119-cold-live.json)。


## 发布闭环完成

v12已更新既有3182367229，完整描述/双语Notes/1.21标签匿名精确回读，原预览保留。Steam重新下载48文件逐字节匹配正式tag树；R0003实际从缓存目录mounted/Enabled并到达主菜单，未开新局、未重复业务，正常GUI退出原始进程0。最终Steam后台探针为offline，keeper及screen均释放。首次缓存准备RED保留；通用GUI缓存磁盘身份修复d5dfb281f归框架，33项检查及新模块严格mypy通过，不授新native ABI资格。见[完整发布记录](workshop/publication-v12.md)。
