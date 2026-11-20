# 潜在产出 0.1.0：正式发布

2026-11-20（上海），独立产品 `mod_potential_output/` 已发布至 [Steam 创意工坊：潜在产出 / Potential Output (XA)](https://steamcommunity.com/sharedfiles/filedetails/?id=3842767123)。条目 ID 为 `3842767123`；与 MTS、POD 产品分别登记，没有更新其他产品。

- 原生首次创建、四张附加预览图上传并公开、中文标题修正均返回 EResult 1；没有新工坊协议确认请求。
- [说明 BBCode](description.bbcode)和[完整更新日志](change-notes-0.1.0.txt)已上库。公开标题、2953 字符说明、17 行更新日志与仓库按换行规范化后逐字一致。标签为 `Interface`、`Utilities`、`1.21 'Florin'`。
- 四张截图来自最终 R0011 的真实游戏画面，仅裁剪游戏客户区并转换 JPEG；[来源与转换记录](media/provenance.json)保留原图 hash。Steam 图集四张及封面下载字节一致。正文四张图使用固定提交的公开地址；匿名 Chrome 实际加载四张 1800×980 图片，并直接审阅图文穿插结果。
- 首次标题误为 `???? / Potential Output (XA)`。原因是 PowerShell 管道在工具收到参数前破坏了 Python 中文字面量。已用 Unicode 转义更新同一条目，匿名 API 和浏览器均确认 `潜在产出 / Potential Output (XA)`；原创建回执及发布 tag 保留，工作树文本冻结单另记修复。正文与更新日志从 UTF-8 文件读取，未出现同类损坏。

正式 tag 为 `potential-output-v0.1.0-ck3-1.21.0`，指向 `a312484a5c4c5ba852684347a39b86680e5b5a5e`。运行代码与 R0011 的 `58e8727` 完全一致；23 文件，两次构建 ZIP 均为 64056 字节，SHA-256 `955e9ee13b4e2e3db1bd4eb50e122d94aeb7bfff059c5cbf70200ede4eb1d4e5`。创建前的正式清单没有 ID；创建后另存[canonical ID 清单](evidence-0.1.0/release-manifest.json)，文件清单与原件完全一致，没有改写原构建或将新 ID 注入上传内容。

按框架 2026-10-07 缓存规则，实际 SDK callback3406 的 app/item 匹配且 EResult1，下载前目标目录不存在；下载后 23 文件的路径、大小与 SHA-256 全部一致。未用正式 staging 或仓库覆盖缓存。R0012 经公共 GUI-only `workshop_cache` 入口运行，实际日志确认：

```text
Potential Output (XA)|mod/product.mod|Enabled
Mounted Data: C:/SteamLibrary/steamapps/workshop/content/1158310/3842767123
```

游戏到达主菜单后点击「退出到桌面」，原始 Popen 返回 0，无 STOP、超时或 WM_CLOSE。keeper 停止，CAS 释放；最终后台确认 Steam 离线，CK3 进程为 0。没有为缓存验收新开战役或重跑地图业务。

版本范围必须分开：地图与旧存档功能实测使用 CK3 **1.21.0／build26757580**；发布期间发现本机已更新至 **1.21.0.3／build26785313**，EXE SHA `859f0d380098adcb130eb9d453458222749fcdf6d46126ad0ed99d78f9a0aa28`。三份原版 GUI 投影及全部 23 文件的生成字节仍一致，但原构建入口按精确版本合同拒绝重建。故保留原正式构建，仅用当前 EXE 的 GUI-only manifest 完成缓存菜单加载；不追认新版本功能实测。缓存 error.log 为 1005 字节，仅观察到一条 `great_wall_china_gate.txt` Generated Map Objects 读取错误，无产品路径错误；不宣称零日志或本轮新版本原版对照通过。

初次缓存准备辅助脚本因子进程使用系统编码而读总线失败，显式继承 `PYTHONUTF8` 后在分配前重试通过；首次公共文本验证的关键字参数名错误也已按真实函数合同重跑。首次默认 User-Agent 的 CDN 请求 reset，使用普通浏览器请求头后全部字节精确一致。失败均保留，不写成首次全绿。

发布身份的四项真实临时 Git 回归最终通过（1.163 秒），使用测试文件要求的 `--framework` 直接入口。收尾时误用 unittest discovery 曾因该 CLI 的配置全局未初始化而失败；按其显式入口重跑通过，未改运行代码。归档 JSON 在计算归档 hash 前统一为 UTF-8/LF，原工具文件和其嵌入的原件 pins 保持原义。

[结构化发布记录](publication-0.1.0.json)、[公开文本验证](evidence-0.1.0/public-text-verification.json)、[缓存验收](evidence-0.1.0/verify-cache-a01.json)、[公开图文截图一](evidence-0.1.0/public-inline-1.png)、[公开图文截图二](evidence-0.1.0/public-inline-3.png)、[功能实测报告](../../potential-output-report.md)。原始桌面截图、完整启动日志与机器配置留本机忽略的 artifacts；已归档公开页面截图与必要回执，不发布私有桌面画面。

归属：本产品身份、BBCode、图片及实际验收归独立仓库。发布、附加图、文本回读、缓存及受管 GUI 生命周期直接复用框架；乱码发生在框架输入边界之前，本包无需新增通用实现。此前 GUI 上下文和动画刷新经验已按 `c82e82ebe` 富化框架，不将本产品通过结论外推其他 Mod。仅简体中文实机，其余语言仍只做格式与键覆盖校验。
