# More Tenets Slots (XA) v11 正式更新：发布闭环完成

**v11已于2026-10-16（Asia/Shanghai）更新公开工坊；整体发布闭环完成，`release_complete=true`。** 原生上传、匿名完整文案和Notes、新缓存48文件严格匹配、R25实际缓存菜单加载／正常退出、最终Steam离线及资源闭场均通过。R22业务和R23独立冷载分别提供产品验收；R24启动前RED及其他历史失败原件保持。

本次更新既有 [Workshop 3182367229](https://steamcommunity.com/sharedfiles/filedetails/?id=3182367229)。精确摘要见 [publication-v11.json](publication-v11.json)，与上一公开版本的差异见 [版本11 changelog](../release-changelogs/more-tenets-slots/11.md)。范围仅为 `more_tenets_slots_xa_dev`，不含独立POD产品。

## 上传身份与上一公开基线

| 项目 | 实际事实 |
| --- | --- |
| 上传源 | `d1c9deee5c0214f9418c8df821a8ac9f3f97d334` |
| tag | annotated `more-tenets-slots-v11-ck3-1.20.0.4` 已推送并指向上述源；manifest原样含该tag |
| descriptor | version `11` / supported_version `1.20.0.4` |
| 验收游戏 | CK3 `1.20.0.4 (Crozier)` / Steam build `25734779` / EXE SHA256 `98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518` |
| 机器与语言 | `bf-202609141645-5434332d4d` / `simp_chinese` |
| 原生更新 | operation `mts-v11-20261016-d1c9dee-001`，`stage=complete/steam_result=1`，无需新法律协议，原Popen实际wait0 |
| 提交时间 | `2026-10-15T18:33:41.694501Z`，即北京时间2026-10-16 02:33:41 |
| 公开内容 | `time_updated=1792089226`，`hcontent_file=6449428825073299086`，`file_size=1015384`，visibility0／banned0 |
| 兼容tag | `Religion`、`1.20 'Crozier'` |

上一公开版本为 [v10](publication-v10.md)，上传源 `da4b579659ebb4de397672b833369e95fdbd03c6`、tag `more-tenets-slots-v10-ck3-1.20.0.3`、version10／1.20.0.3。其46文件manifest SHA256 `d79bd36bcee5c081da05a99fe409421f76b49e890d6b8ec194ad700d8f77ca00`，公开更新时间1790978434。旧源、tag、manifest及历史结论保持，不以本地中间候选代替上一公开版本。

## 正式构建与实际新下载

实际上传目录为 `artifacts/bugfix-20261015/workshop-v11-actual-001/formal-build-001/more_tenets_slots_xa_dev/`。正式48文件与R22/R23受测产品字节精确一致，文档和tag变化在产品内容之外；没有上传夹具、工具、报告或私有保存。构建原报告仍为 `static-ready/live_verified=false`，其边界与实机资格分别保留。

| 产物 | 字节数 | SHA256 |
| --- | ---: | --- |
| [原样正式manifest](release-manifest-v11.json) | 9159 | `2d9c319293b2bce98c2cc041c759b0d6400aa22ce1d9216ba620b8f194823172` |
| `formal-build-001/more_tenets_slots_xa_dev.zip` | 729030 | `235016183f48b6b22ceda152dc78efbcdacb05243a40c45aea0bd72d8f0768fd` |

旧item缓存先精确移入当次artifact，下载开始前实际目标缺席。独立SDK worker得到app1158310／item3182367229的callback3406、result1，原调用进程及worker均实际exit0，耗时8.926秒；安装信息为1015384字节、timestamp1792089226。新缓存**48项路径、size、SHA256严格匹配正式manifest**，没有descriptor规范化或staging复制。下载与清单匹配通过，游戏菜单加载单独待验收。

## 匿名完整文案与保留媒体

最终 `anonymous-publication-readback-final-005.json` 通过标题、正文、metadata及保留媒体身份。正文3981归一化字符，SHA256 `78090be514726d208ae5d1ae24086a7c785e1deb8c62dae2002731afd0156bdd`，与[文本冻结](publication-text-freeze-v11.json)一致。[完整双语Notes](change-notes-v11.txt)在[公开changelog](https://steamcommunity.com/sharedfiles/filedetails/changelog/3182367229?l=english&p=1)的唯一条目 **1792089226** 精确回读：2321归一化字符、21行，SHA256 `06e45811558d8a1f29e6e9a50941c9da9442ff9a7451a3eaa646ed28331ae0e2`。上传ACK没有替代Notes全文证据。

001／002／003的HTTP429、004工具无正文及各原退出码保留。最终005取得匿名HTTP200完整严格UTF8正文后，用框架既有全文比较函数通过。普通请求头、查询参数及冷却时间共同变化，未做A/B，不宣称429单一根因，也未重复上传。

没有上传新媒体。三张附加预览的顺序、URL、文件名／类型，以及thumbnail和正文三图URL均保持v10身份，前后原生列表和匿名metadata核对通过。截图明确标为历史v10素材，封面为宣传概念图；本轮未重新验证CDN字节或像素，不把旧像素资格写成本轮媒体更新。

## 实机范围与边界

[R22新局](../native-main-r22-2026-10-16.md)八事实通过，覆盖两个普通候选及唯一替换、核心旧项移除、实际槽99选择和稀疏创建、文化默认4/6、有限通知、一次保存及离线语义读回。原host唯一failed step为未暂停的只读事件查询被守卫拒绝，原status RED／返回1保留；公共verify后继实际0、业务及正常闭场通过。

[R23独立冷载](../native-cold-r23-2026-10-16.md)以新PID恢复同一原binary，首帧actor31254/date53145144/Rite150/Faith13/Religion8，当前四个真实核心和Equal／Pluralistic各组唯一。四项冷载事实、公共verify和原OS/native/host/public/keeper正常闭场均通过，CAS6321释放。退出未知即时ACK与后验实际退出分别保留。

R22创建后87.425699秒、R23冷载后92.327955秒各四张原图经Root直接审阅，未见顶部礼仪更新反复提示；普通家族toast另记。不外推全部场景永久无循环。R20发布前候选旧档限定通过与R19正式v10来源业务RED保持独立。九语18文件、每语305键仅格式认证，实机只用简中；100槽不保证100个兼容信条。直接Edit、连续／反向替换、全部DLC、完整文化增益、超原版文化上限旧档仍有未覆盖范围，原日志及已知重复effect提示保留。

## R24启动前RED与收尾状态

[R24](../native-cache-r24-2026-10-16.md)使用实际新缓存及runtime007，原host在 `normal_exit_profile.project_profile` 拒绝 `prepared-workshop-cache-v1` 来源，报 `public preparation and selected runtime identities differ`。原host实际1、public实际2，无native-report，Root实查CK3为空。keeper原wait0和CAS6345只证明资源释放，**不授菜单加载、normal0、native0或业务通过**。框架另行处理通用profile整合和新runtime资格，旧007及R24原件不改。

发布后Steam离线恢复已通过：Root直接审阅官方菜单一次切换后的新鲜位移图，实际文字“离线模式”、北京时间2026/10/16 02:47，CK3为空，未重启Steam／ToDesk。图采集于18:47:21Z、Root审阅于18:51:26Z；窗口x40→60并恢复，实际边缘像素变化。原图SHA256 `b31a17df69e318af7d488d220d10e92bcd3f18dfea756c32f968acf7fbded172`。发布keeper原wait0，CAS6341于18:52:41Z释放；该原摘要当时Notes待办，005后续通过另记而不覆盖。

第一永久记录包 `9af59fb5a005ce928e339e8edd98057cf2b7db7b` 当时为 `CACHE_LOAD_PENDING`。下述后继R25补齐实际事实，不追改R24原RED或旧记录。

## R25补齐最终缓存与闭场

[R25](../native-cache-r25-2026-10-16.md)使用runtime008和同一native DLL，实际PID16724／create-time1792092300.8483706；readiness274.486020秒，在原1800秒内进入hold。公共case／GUI合同及 `combined_managed_cache_profile_and_actual_menu_load=true`，公共verify原进程exit0、`case_acceptance_pass/qualified_boundary_pass=true`。

本场证明精确缓存的受管单产品profile与实际稳定主菜单组合；**独立引擎VFS路径为UNKNOWN**，低层实际cache mount和产品业务标志仍false。cache case的 `business_contract_applicable/business_pass/product_release_pass=false` 原样保留，不授其宗教业务通过。整体完成由R22八事实、R23独立冷载、公开回读／下载及R25菜单／正常闭场组合成立。

Root只做一次官方主菜单“退出到桌面”映射点击。退出有延迟；拟用标题栏备用在工具调用前因PID已gone的assert中止，没有第二click、实际fallback或process kill。原保留OS0、native `process_exit/code0` 于19:37:47.920579Z结束且完整清理，host GREEN／原wait0、public／keeper／allocator原wait0，normal_close_qualified=true。菜单用例未调用要求地图actor的typed退出provider，不为本场增加该能力资格。

最终Root审阅游戏关闭后的新鲜Steam位移图，明确“离线模式”、北京时间2026/10/16 03:44、CK3为空；原图SHA256 `942c28522d002b173e34b6e1bb4f36c7d4599b9016eb81ba62fbad7d45de1f73`。CAS6365于19:46:15.043193Z释放，resources为空。该最终回执与此前上传后的离线／CAS6341分别保留。

a12使用R23旧前驱被allocator正确BLOCKED／NOT_RUN，未建立R25或租约。其exit2由Root后记观察原工具及helper输出，记录证据层级，不冒称原进程schema。后继a13采用最新R24及真实prelaunch closure bundle才分配R25。完整pins见[R25索引](../evidence/native-cache-r25.json)。最终永久记录不移动发布tag，不修改manifest或文本冻结。

## 归属与交付

正式清单、版本比较及本产品发布证据归独立仓库，通用原生上传／下载、匿名全文比较、受管profile和闭场复用框架，R24通用schema缺口归框架修复。报告工作未操作Steam、HTTP、GUI或游戏，未改冻结runtime、源码／catalog或历史报告。永久记录提交不移动tag或改写已上传清单。
