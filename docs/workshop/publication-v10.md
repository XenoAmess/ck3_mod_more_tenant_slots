# More Tenets Slots (XA) v10 正式工坊更新

2026-10-03（Asia/Shanghai）已更新并公开 [Workshop 3182367229](https://steamcommunity.com/sharedfiles/filedetails/?id=3182367229)，标题为 **More Tenets Slots (XA) - CK3 1.20**。内容上传、匿名完整文案回读、新媒体 CDN、全新订阅缓存验收及 Steam 离线恢复均 PASS，正式发布闭环完成。

永久机器摘要见 [publication-v10.json](publication-v10.json)，相对上一公开版本的变更见 [版本 10 changelog](../release-changelogs/more-tenets-slots/10.md)。本页记录本产品，不扩展至独立 POD 产品。

## 已发布身份与上一公开基线

| 项目 | 当次事实 |
| --- | --- |
| 上传冻结源 | `da4b579659ebb4de397672b833369e95fdbd03c6` |
| 当前 descriptor | version `10` / supported_version `1.20.0.3` |
| 本机验证目标 | CK3 `1.20.0.3 (Crozier)`，Steam build `25652598`，EXE SHA-256 `94b55397abb687a3dcd436805a5d885e6be90fa6c693feb44a9e3bbeeade02a6` |
| 原生提交 | operation `update`，item `3182367229`，`steam_result=1`，`stage=complete`，无需新法律协议 |
| 提交时间 | `2026-10-02T22:00:32.325876+00:00`，即北京时间 2026-10-03 06:00:32 |
| 公开上传时间 | `time_updated=1790978434`，2026-10-02 22:00:34 UTC |
| 公开内容身份 | `hcontent_file=2486335635832374929`，1,008,047 字节，visibility `0`、banned `0` |
| 兼容标签 | `1.20 'Crozier'` 与 `Religion` |
| 版本 tag | annotated tag `more-tenets-slots-v10-ck3-1.20.0.3` 已推送，指向上传冻结源 |

上一公开基线来自保留的 [13 文件订阅缓存摘要](previous-cache-manifest.json)：内层 descriptor 实际为 version `1` / supported_version `1.19.0.4`，ACF manifest `3241202835495521309`，ACF `timeupdated=1777874459` 与发布前匿名 API 相等。旧源 commit/tag 未知，且未独立重新下载旧内容；这一匹配缓存是本次可核验的前一公开内容身份。本地迁移起点 version `9` / CK3 `1.19.0` 单列，不能替代公开基线。

## 构建与下载验收

实际上传目录为 `artifacts/workshop-v10/final-build-frozen/more_tenets_slots_xa_dev/`，正式 46 文件；没有上传报告、夹具、源码工具或素材原图。最终构建回执仍为 `static-ready`、`live_verified=false`，其边界保留；实机证据独立链接下方。

| 产物 | 大小 | SHA-256 |
| --- | ---: | --- |
| [原样正式 manifest](release-manifest-v10.json) | 8,775 字节 | `d79bd36bcee5c081da05a99fe409421f76b49e890d6b8ec194ad700d8f77ca00` |
| `artifacts/workshop-v10/final-build-frozen/more_tenets_slots_xa_dev.zip` | 727,367 字节 | `2f27143085b94fa6737d31f8dc836b3ed26c8a1ed8fd690f2c137117b613b621` |

manifest 的 `git_sha` 精确绑定上传源，`git_tag` 当时为 **null**。之后建立 tag 不修改这份已上传构建 manifest，也不重签其摘要。

旧 item 缓存完整移到当次 artifact 备份，新下载开始前精确目标路径不存在。框架 `workshop_native_download` 独立 worker 等到 app `1158310` / item `3182367229` 的 `DownloadItemResult_t` callback `3406`、result `1`，退出码 `0`。随后 **46 文件路径、size、SHA-256 严格逐项匹配正式 manifest**；未做 descriptor ID 或换行规范化，本次原生 uploader 未注入内层 ID。下载成功回调与清单匹配分别有原件，不能互相替代。

## 公开文案与媒体

匿名 public verifier 确认标题及 [BBCode 全文](description.bbcode) 精确相等：4044 文件 UTF-8 字节、3241 归一化字符、45 行，正文 SHA-256 `96e7059b85c42b5ab9503d0d3e443a6dc8078ce3b83018253523423088c0299f`。平衡标签、Holger 致谢、来源链接、三张固定提交 raw 图片及 byte limit 已在 [审计](bbcode-audit.md) 独立核对。

[完整双语 Steam Change Notes](change-notes-v10.txt) 在 [公开 changelog](https://steamcommunity.com/sharedfiles/filedetails/changelog/3182367229?l=english&p=1) 的唯一条目 **1790978434** 精确回读：2013 归一化字符、23 行，SHA-256 `009a95736c0a87d7fd4db4e9bfb592594a6d4e0b60b5556cec25ea01aa837754`，与 [提交前冻结文本](publication-text-freeze-v10.json) 一致。原生提交 ACK 没有被当成 Notes 正文证明。

新 thumbnail 使用新版礼仪卡片的宣传概念图，640×640、673,309 字节；CDN 原文件与本地 bytes/解码像素均相等，SHA-256 `53fa59a29aa04d18a7ac623dc19223f7d213938ac5a8a692531d5616e2ba0690`。其宣传性质在正文明确区分。附加预览精确顺序为：

1. `01-rite-creation.jpg`：简中原生礼仪创建窗口与空卡片，458,079 字节。
2. `02-tenet-selector.jpg`：原生信条选择器，510,841 字节。
3. `03-two-tenet-rite.jpg`：已保存的两信条礼仪，529,406 字节。

三图均为 1920×1080 JPEG，Steam CDN HTTP 200，公开 bytes 与解码像素逐一匹配来源。原旧附加预览 index 0 已更新，另两张追加；不是把图片存在仓库便算已发布。来源、处理参数和原图见 [素材账本](media/provenance.json)，精确 CDN URL、图片摘要与回读结果保存在永久 JSON；完整 HTTP 头和桌面截图保留当次 artifact，不入库匿名 cookie。

## 实机覆盖与边界

[R0009/R0010](../live-R0010-cold-reload.md) 证明两个真实信条加尾部 98 空槽可创建、保存及简中独立冷载。[R0012](../live-R0012-sparse-create.md) 在 46 文件树简中实际以非空下标 `[0,1,2,99]`、96 中间空槽创建“松柏礼仪”，支付 5775 虔诚。[R0013](../live-R0013-cold-reload.md) 原生冷载并重存，离线文本结构确认角色 33339 当前 rite `153`，四 core、28 vanilla/100 hidden doctrines、虔诚 `78925`；不是直接离线 melt R0012 二进制。隐藏条目为持久且无费用/效果的教条元数据，核心信条没有占位条目。

[九语言本地化格式认证](../localization-coverage.md) 覆盖 18 文件、每语 305 键；后续实机只用简体中文，其他语言不宣称实机或母语者签核。保留历史英文验收和截图。原生信条/教条互斥、费用及 DLC 条件仍生效；不承诺 100 个兼容信条、全部 DLC 组合、1.19 旧存档迁移或 POD。文化第十项已支付并开始建立，未推进多年完成或穷举 10000 项。R0010 的历史场景日志错误仍在迁移报告记录。

## 收尾与系统富化

**Steam 离线恢复：PASS。最终闭环：complete。** 主任务于 `2026-10-02T22:29:12.069423+00:00` 捕获并人工审阅当次画面：明确“离线模式”，桌面日期/时钟为 2026/10/3 06:29，CK3 进程数为 0。1920×1080 原图 `artifacts/workshop-v10/steam-offline-verified.png` SHA-256 为 `ae469ee6cfa4529bd6dabc46462ced4e1681b479a0be4c51a2e559117b2c264a`；窗口 x=40→80 的位移引起实际像素变化，不能用旧图或文件时间代替新鲜画面。

本次正常 Steam 退出曾等待 CK3 关闭；实际 CK3 为 0，但有七个父进程已结束的旧 Crash Reporter。主任务通过各原生 Cancel 按钮关闭，七份回执均确认进程退出及原有 crash 文件逐个 SHA 不变，没有上传报告；以 `-cef-disable-gpu` 重新启动客户端并进入官方离线模式后，8 秒后的 UI 真正显示离线。其有效恢复路径是该组合，未做 A/B，不能宣称单一根因。回执 `steam-offline-verification.json` 与 `orphan-crash-reporters-closed.json` 的本地路径/摘要保存在永久 JSON，不入库可能包含私密上传参数的其他原始材料。本报告线程没有操作桌面、启动游戏或改变远端会话。

客户端重启时曾显示 CK3 下载进度；主任务只读复核本机 EXE 为 101,039,736 字节，SHA-256 仍为本报告的精确 1.20.0.3 pin，没有据进度画面推断游戏已换版，也没有新增游戏启动或测试。

永久文档、清单及 changelog 作为同一主线工作包提交推送；其交付 commit 由 Git 历史记录，不改写上传冻结源或 manifest。

通用原生附加图片更新、独立下载 callback 等待、首轮真实验收及离线组合恢复经验归框架，已推送：`26c9943e1e60cf377d25ed6b30327986b4c35ffa`、`fcc29d14da759493a547f6419af87ca286212906`、`90f2a7a596653d57da3910885a4ef22c99c1d95c`、`5a2c0a8b77aaa98efcbd71973c9133d6a0f62167`。产品源码、BBCode、素材、当次清单和报告归本独立仓库；不将本产品成功外推为全部 mod 通过。
