# More Tenets Slots(XA)

`more_tenets_slots_xa_dev/` 的迁移目标为 CK3 **1.20.0.3**，产品版本 10。当前状态为 **`pending-final-live`**：已有多项实机通过，最终源码的冷启动和存读档回归仍待完成，本任务尚未发布 Steam 创意工坊。

核心信条上限为 100，会议使用的镜像上限同步为 100；新版仪轨创建及信仰详情窗口支持纵向滚动。文化传统基础上限保留为 10000，界面有效上限还包含时代等原版加成。原版信条、个人信条、候选过滤、费用、互斥、DLC 条件和创建钩子继续使用游戏自身定义。

两个真实信条和尾部 98 个空槽已通过原生创建、保存及冷重载，无需填满 100 槽，也没有占位信条。为修复新版末端选择器的另一个索引问题，创建入口会为玩家所选仪轨准备 100 个隐藏、费用零、分歧零、无机制效果的教条；这些教条与核心信条不同，可能持久留在源和新仪轨。正式构建 allowlist 为 32 文件。

第 100 槽的原生候选、实际选择和费用更新已通过。原生合法性拒绝中间留空、末端另选信条的草稿；增加真实信条时应按槽位顺序选择，尾部仍可留空。文化第 10 个传统也已通过原生选取、支付 2000 威望和开始建立；没有穷举 10000 个传统，也不保证存在 100 个可同时兼容的真实信条。

迁移与验收详情：[迁移计划](docs/migration-plan.md)、[验收计划](docs/acceptance-plan.md)、[迁移报告](docs/migration-report.md)。旧 CK3 1.19 存档尚未验证，POD 产品须独立迁移和验收。

本项目修改自原作者 Holger 的模组，感谢其贡献。[源码仓库](https://github.com/XenoAmess/ck3_mod_more_tenant_slots)、[原模组](https://steamcommunity.com/sharedfiles/filedetails/?id=2904268802)、[本产品创意工坊页](https://steamcommunity.com/sharedfiles/filedetails/?id=3182367229)。工坊页链接用于产品身份，不能代替本次迁移的发布证明。

###  **pod_mts_xa_patch_xa_dev** folder:

It is the MTS patch for Princes of Darkness mod.

It is modified from modified original mod, and standalone(don't need any other MTS mod with it)

source codes: https://github.com/XenoAmess/ck3_mod_more_tenant_slots

original mod: https://steamcommunity.com/sharedfiles/filedetails/?id=2890708074

this mod: https://steamcommunity.com/sharedfiles/filedetails/?id=3182385109

POD mod: https://steamcommunity.com/sharedfiles/filedetails/?id=2216659254

### order

![mods_order](mods_order.png)
