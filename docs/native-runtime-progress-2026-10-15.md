# Native runtime 与实机边界

用户固定目标 CK3 1.20.0.4，Steam build 25734779，EXE SHA-256
`98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518`。

框架已在共享 native runtime 启用既有四项只读接口：宗教改革上下文、草案分组、草案教义候选、草案信条候选。主产品验收声明这四项工具，并保留当前宗教上下文与 snapshot。实际构建只重编七个生产文件，复用 734 个已有对象；原 DLL、冻结源码和历史回执均保留。离线校验涵盖真实原生回包、注册 MCP 传输，以及 100 信条槽、128 教义槽与 128 候选行。框架提交 `0d7ffd1fa`、`6d77d0a3f`；这些是构建和协议资格，尚无本轮实机资格。

独立冷载用例使用新的 CK3 PID，并绑定实际保存来源与上一场正常退出证据，不能用同一进程重开窗口替代。产品 adapter、夹具、具体宗教断言和存档证据归本项目；共享 native 生产工具、协议及通用生命周期能力归框架。本轮不扩展为通用宗教 AI。

当前 native 通用界面动作未覆盖宗教窗口导航、教义选择及信条槽选择。实际测试可在受管会话内经官方 GUI 执行这些缺失动作，再通过 native 读取前后状态；不把鼠标动作写成 native 能力通过。完整 GUI 行为验收与只读 native 接口资格分别记录。

产品用例进一步声明已有的当前礼仪教义与信条两个只读查询，合计七项宗教只读查询及 snapshot。它们用于将实际核心信条与主礼仪/知识状态分开、核对普通教义同组唯一，以及应用与冷载后的状态。五项 adapter 离线测试在后继配置下通过，包含七项只读工具逐项路由至公共 host；最初只允许 context 时留下的旧单工具断言已修正。各接口的实际原生回包、构建资格与实机资格仍分别判定。

首次受管 attempt `bf-202609141645-5434332d4d--more-tenets-slots--R0015` 的原始 host 于 2026-10-15 04:09:13 UTC 退出 1：冻结生成器使用 Windows 默认换行写入 effective host，而记录的 SHA 来自 LF 字符串，命中 `effective host differs from reviewed projection` 校验。游戏未启动，不能记为游戏退出 0 或任何业务结果。已停止原 keeper，并以 CAS 5967 释放屏幕，保留原始 host stderr、实际 Popen wait 和冻结输入。后继包以明确 UTF-8 LF 字节冻结，并离线执行与 wrapper 相同的校验路径至实际 exec 边界，未执行底层 host 或启动游戏。

框架 `c078afe13` 补齐独立产品复用统一工坊缓存用例，以及这一精确启动前失败原因的资源释放准入；29 项离线测试通过。资源释放通道不授予 native 清理、游戏正常退出或业务通过。机器路径和临时二进制保留于配置/外置回执，不写入产品配置。

R0016 后继已通过投影 SHA 检查，但于启动游戏前被原有 normal-exit source inventory 的“所有启用 mod GUI 均不支持”合同拒绝。原始 host 退出 1、公共 entry 在原 400 秒就绪预算后退出 2、keeper 原父进程 wait 0；CAS 5970 已释放，游戏与 native 报告未产生。下一包会补齐与退出菜单无关的宗教 GUI 资格；不删除该守卫，也不把此场算作业务测试。

框架 `4ffaa41e7` 的资源闭场扩展经过八项测试；`3f20da8f3` 在原始 host 已退出且首个报告缺席时保存确切退出收据并及时报告，11 项离线测试通过，R0015/R0016 原档只读核验一致。`d6bbfc40a` 使公共缓存验收兼容当前构建器的 manifest format 2，继续严格核对 tag 与逐文件原始字节，11 项缓存边界测试通过。

下一实机对照使用当时**实际上传的 v10 46 文件**，已逐项匹配正式 manifest `d79bd36bcee5c081da05a99fe409421f76b49e890d6b8ec194ad700d8f77ca00`。它保留原始 supported_version 1.20.0.3 字节；实际执行游戏仍固定 1.20.0.4、简中。之前两场未启动游戏的 1.20.0.4 投影基线不替代用户版本复现。v11 候选 48 文件的当前静态结果见 [回执](evidence/bugfix-20261015-current-static.json)。

R0017 首次真正启动 CK3；共享 runtime 的宗教 GUI source inventory 已通过。原生入口单次选择正确的 1066 bookmark 与罗贝尔模型并提交 Start。原来的 400 秒来自框架现有新用例模板，本项目沿用，未经本机冷启动耗时验证；这是本轮预算设置疏漏。

原公共 client 在 400 秒后记录 `READINESS_TIMEOUT`，host 的开局等待随后也超时。当时原生观察仍为 `map_ready=false/player=null`，没有拿到政体／头衔数据，不应将错误文字解释成实际政体不匹配。`debug.log` 在 04:50:13 UTC 才记录 history setup 完成，04:50:36 才出现真实资源夹具标记；完整冷启动约 734 秒。它说明预算不足，不证明任何宗教业务通过。

Root 保留真实进程句柄并尝试原版菜单退出，已打开退出窗口、取消退出自动保存；最终 Quit 未在原 hold 截止前完成。原运行时于 05:05 触发 managed stop：原 host wait 1，native shutdown 记录 CK3 exit 1、tree gone 和清理完成；Root 旧 retained-handle 收据仍为 signaled false／exit null，不改写为已证明正常退出。keeper 原父进程 wait 0，CAS 5984 已释放。原有资源准入检查真实通过，仅允许下一场继续；正常退出、native0、业务和发布信用均为 false。

用户随后明确要求未来启动／就绪超时最低默认 1800 秒。本产品新局与冷载用例及 adapter 的预算已统一为 1800 秒，五项离线测试通过，包含公共 host 实际 argv 的 1800 秒断言。框架中央下限及 CLI 默认另行提交。R0017 原 400 秒实际记录与原冻结 runtime 保持不变。

## R18 后继：正常退出与产品存档 profile

[R18 实际记录](native-baseline-r18-2026-10-15.md)保留915.936秒就绪、旧角色ID断言失败、普通教义候选和草案替换局部证据，以及900秒hold到期的托管停止。产品后继采用本场动态角色绑定、7200秒hold、10800秒总体上限和900秒退出预留；不重分类R18。

框架 `098854517` 新增原生 `disable_exit_autosave`：读取原版退出确认框实际状态，已经false时不切换，仅true时调用一次原版Toggle并读回false。13个受头文件影响的生产单元真实重编，40项原生检查、45项Python及两种SDK工具入口通过；实际DLL为 `bc1aea14889f29d1df376156d60914de86b936cd0a4a5d52107ec5be82c4579f`。它不证明存档完整性、进程退出或产品通过，仍待本轮实机。Defender WMI登记失败与原构建driver返回1保持RED，独立授权夹具实际wait0另行记录；没有声称已登记成功。

启动前完整预检又发现原normal-exit profile仅接受fixture准备，产品自写旧存档/冷载envelope无法消费。框架 `109e771d1` 提供 `finish_product_profile`，从实际产品文件、选定engine身份和产品inventory生成标准 `ck3-mod-acceptance-prepared-product-v1`，不生成或冒充fixture。两类产品saved_campaign adapter均改为消费该接口。框架13项、主adapter6项、legacy9项离线验证通过；legacy最后一项真实消费48文件候选的公共prepare→完整wrapper静态profile链，在底层game main前停止。旧005 schema RED及首轮诊断路径过长RED保留；短路径后继通过，不放松校验。

具体完整链证据位于本机配置指定的 `cases/mts-lg6-001/full-host-static-preflight/RESULT.actual.json`，SHA-256 `c7ce15bea5c0eb197f12a0baebc6ec832861aaaa01c7f01e98cbce04bd63d059`，54个profile输入。runtime006仅从005窄移植这两个通用准备工具，保留原native、1800秒策略与旧runtime。以上仍为启动前和离线资格，实机与发布尚未完成。
