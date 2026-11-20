# 潜在产出（Potential Output XA）

独立子 Mod：`mod_potential_output/`，工坊与仓库版本均为 0.1.1，已在 CK3 1.21.0.3 Florin 自测通过。无需 MTS 或 POD。

## 使用

1. 在启动器中启用 Potential Output (XA)，进入新游戏或旧存档。
2. 点击原生视角栏末尾、“＋”下方带 MOD 角标的绿色圆形按钮，单击进入；悬停显示「潜在产出（XA MOD）」。
3. 点击商品图标开关单项，点击分类名称切换整组；也可全选或清空。
4. 放大地图查看各伯爵领的商品图标和匹配种类数。缩小时保留地图底色。
5. 面板右上角的减号收起为窄标题条，点击标题条左侧圆形图标或右下角圆形入口重新展开；叉号退出并恢复之前的地图模式。

展示的是伯爵领**可以生产**的商品，包含尚未开发的资源。商品清单来自原版潜力接口，不读取当前产量。只列入原版县潜力表中的 35 种商品，不列仅靠加工获得的 9 种商品。

数字 = 该县潜力商品集合与已选商品集合的交集大小。没有匹配为灰色，匹配种类越多绿色越深；单选只有 0/1，多选可能出现 0/1/2 等。数字不是储量、月产量或可建设槽位数。面板默认全选，每次重新进入视角重置为全选；收起面板保留当前筛选。

## 安装与兼容边界

推荐订阅 [Steam 创意工坊：潜在产出 / Potential Output (XA)](https://steamcommunity.com/sharedfiles/filedetails/?id=3842767123)，然后在启动器播放集中启用 Potential Output (XA)。当前发布版本为 0.1.1；[发布记录](workshop/potential-output/publication-0.1.1.md)包含说明、截图及实际下载加载验收。

仓库 0.1.1 的实测截图、兼容边界和本地 ZIP 见 [入口改造验收报告](potential-output-entry-0.1.1-report.md)。新入口独立注册，不改原生视角栏，但原有三份地图/活动 GUI 覆盖仍存在。

手动安装也可使用本地实测 ZIP：

将 ZIP 解压到 CK3 用户目录下的 `mod/`，包中已包含 `mod_potential_output/` 子目录。再在 `mod/` 下新建同级文件 `mod_potential_output.mod`：

```text
name="Potential Output (XA)"
path="mod/mod_potential_output"
supported_version="1.21.*"
```

重新打开启动器，把 Potential Output (XA) 加入播放集并启用。也可以用启动器创建同名本地 Mod，再将本产品目录内容复制到它的 Mod 目录。同一播放集只启用工坊版或本地版其中一个。

该视角使用原版活动规划地图的图标与着色能力，进入时会暂时占用规划界面。请先退出其他活动规划，再打开潜在产出。它禁止实际启动展示用活动，不消耗金钱或推进日期；过滤使用玩家角色上命名空间为 `xapo_hidden_` 的展示变量，退出时清理。若在视角内保存游戏，这些无经济效果的变量可能随存档保留，下次进入会重置。

为提供地图图标，需要覆盖三份原版 GUI：`map_icon_layer.gui`、`window_activity_planner.gui`、`window_activity_list.gui`。修改同一路径的其他 Mod 需要合并补丁。活动规划地图的评分渐变也会使用本 Mod 的灰绿配色，这是共用原版色板的外观影响。

简体中文执行实机验收；另外八种语言仅通过格式与键覆盖校验。MTS、POD、大地图转换 Mod、多人游戏和其他 CK3 版本未做组合实机验收。
