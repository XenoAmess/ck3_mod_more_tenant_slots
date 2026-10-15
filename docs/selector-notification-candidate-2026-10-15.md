# 1.20.0.4 选择器与隐藏教义通知整改候选

状态：**静态通过，尚未实机通过或发布**。目标固定为用户指定的 CK3 1.20.0.4 / build25734779 / EXE SHA-256 `98702f88a547cde2eaf29a85f93b85f68ee4cf8148336a4f7afaeb75319dd518`。

## 已查明的生产链

v10 在 FaithWindow 的编辑、新建及傀儡新建三个入口都执行准备effect。每个源礼仪缺少的内部教义都会通过 `change_rite_doctrine` 添加，最多100次。当前原版 `on_rite_updated` 为延迟钩子，会生成 `msg_rite_updated` 并执行宗教领袖更新链。`visible=no` 与空白本地化没有阻断这些副作用；源码中的缺项检查只能防止同一礼仪反复添加，不能消除首次批量通知。

只读原生调查同时确认：`add_rite_doctrine` 与 `change_rite_doctrine` 共用添加与变更处理后端，没有发现前者具备静默通知选项，因此不采用简单改成add的候选。

当前原生 `ShowWindow` 仍以信条槽号读另一组DoctrineItem，不能直接移除所有兼容定义后点击第100槽。普通教义条目的槽号由原向量下标写入，分类只保存指针，先前“隐藏项导致分类重编号”的假设已被静态链否证。空白窗口的实际原因仍需原生草稿、候选与实际UI联合观察。

## 创建与编辑必须分别处理

当前4的编辑分支在 `0x14f6ec5` 直接复制source rite profile；新建分支在 `0x14f6f61` 调用default draft `0x2bdb180` → `0x2bdaaf0`。后者复制已有教义，再遍历所有group，为缺失且 `is_available_on_create` 合法的组追加首个合法definition。该循环没有单独按GUI的visible标记排除内部条目。

因此候选保留100个内部组与definition，但移除**新建和傀儡新建**入口对真实源礼仪的prepare调用，继续原样调用原生创建入口。编辑入口保留幂等准备，因为它没有同样的默认补组路径。能否安全提供100槽必须在实机读到草稿DoctrineItem数量后再操作末端，不能用静态推断替代该检查。

新建工厂的静态原件摘要为 `fa344ddb551d17fe458ad600c6f3a72a96b6f29f3e7dde3a99268783cbf2b962`；当前ShowWindow/窗口布局原件摘要 `4160842b1d6db73b9239783c69308e261d7171d820364d5f9c1fa3d6200ae3b2`。完整字节与反汇编留本轮本地 `artifacts/bugfix-20261015/diagnosis-candidates/`，没有把它们当作真实进程或GUI通过。

## 仅跳过纯内部元数据更新

新增生成的scripted trigger，精确匹配本mod100个内部doctrine key。只有满足以下条件的 `on_rite_updated` 才跳过原版effect：

- added/removed doctrine列表至少一项非空；
- added/removed tenet列表都为空；
- 两个doctrine列表中的每一项均为本mod内部key。

普通教义、真实信条、内部与真实条目混合更新、纯外观更新继续完整走原版effect。没有屏蔽全部宗教通知，也没有仅用短暂flag猜测延迟钩子的执行时机。

正式输出只覆盖 `on_rite_updated` 一个顶层钩子，文件为 `common/on_action/zz_mts_selector_on_action.txt`；其他原版钩子不打包。生成时先对完整原版文件做SHA绑定、最小投影与反向恢复，再提取目标钩子。原版消息与宗教领袖effect主体完整保留在条件内。其他mod若也覆盖同一钩子仍需兼容补丁；本轮不宣称全部宗教mod兼容。

## 验证与下一步

`python -X utf8 dev_tools/test_selector_patch.py --framework <framework> --game <game>`：两项通过，直接检查原生两个创建按钮保持逐字节相同、编辑准备保留，以及原生effect主体完整保留。完整构建检查通过：精确来源、可逆投影、48文件allowlist、九语言格式、确定性双构建。[静态收据](evidence/bugfix-20261015-selector-candidate.json) 保留 `live_verified=false`。

必要实机：未被v10污染的新局source rite；新建draft实际条目数；普通教义候选及替换；第100信条槽；创建后真实旧项/新项；编辑stock与v10礼仪；真实变化通知仍出现而内部变化不刷屏；推进日期后队列收敛；独立冷载。未完成前不授正式发布。

归属：具体内部key、入口投影、钩子兼容与原始报告归本项目；通用宗教草稿查询优先复用并启用框架native runtime，必要的feature生产与MCP登记归框架。可复用的“隐藏不等于无副作用”、创建与编辑生产路径分开验证的方法在实际结果明确后继续富化框架。
