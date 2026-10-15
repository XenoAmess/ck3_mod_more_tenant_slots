# R19：正式 v10 旧档的草稿检查与提交限制

本轮实际加载了 R0013 原存档，普通教义候选列表和草稿替换正常，核心信条草稿替换也正常。**原角色已创建过礼仪且不是礼仪领袖，无法合法提交，业务结果保持 RED。** 没有清除角色限制、修改存档或用草稿结果代替提交后读回。

机器 `bf-202609141645-5434332d4d`，观察日期 2026-10-15；下列时间为 UTC。完整摘要及原件大小/SHA 在 [证据清单](evidence/native-legacy-r19.json)。路径只标识这台机器的原件，不证明其他机器状态。

| 检查 | 实际结果 |
| --- | --- |
| 运行及版本 | `bf-202609141645-5434332d4d--more-tenets-slots--R0019`；CK3 1.20.0.4/build25734779，简体中文；runtime006；候选产品48文件。 |
| 真实旧保存 | R0013 `last_save.ck3`，91,143,003字节，SHA `3a02cfae5d89af71b8229e09e197a1576eaae02977388ac6c043b5e6de6d001f`；原件未改写。 |
| 旧档身份 | 实际角色33339，芒斯特国王穆尔哈德；1066.9.15/date_raw53144328；rite153“松柏礼仪”、faith28 Adamites、religion8。与框架独立保存解析及原生初始读数一致。 |
| 就绪 | 07:40:32.718469进入hold，用时914.3376011秒，在原1800秒窗口内；恢复状态为 `ACTUAL_SAVED_CAMPAIGN_CURRENT_CONTEXT_BOUND`。 |
| 普通候选 | 性别教义弹窗显示男性主导、男女平等、女性主导三项；原生category10、group `doctrine_gender`、cache3。该组未复现空白。 |
| 普通草稿替换 | 官方界面选男性主导后，草稿selected slot10仅为 `doctrine_gender_male_dominated`，旧 `doctrine_gender_equal` 不再占该槽。 |
| 核心草稿替换 | 草稿slot0由 `tenet_communal_identity` 改为原生实际读回的 `tenet_divine_liturgy`，slot1仍为 `tenet_sanctity_of_nature`。这里只记录实际草稿槽，不将父信仰或其他礼仪的核心、已知信条集合视作目标残留。 |
| 提交资格 | 原生 `can_create_rite=false`：角色已经创建/改革过礼仪；`can_edit_rite=false`：角色不是礼仪领袖。另有未填的四项名称。草稿替换后独特性限制已消失，上述身份限制仍存在。 |
| 未覆盖 | 实际提交后的同组唯一性、旧核心移除、修改后的通知收敛、写入保存及独立冷载。没有为这些项目签PASS。 |

退出调用首先通过选定公共队列查询native能力，实际返回 `enabled_mod_gui_or_file_inventory_unsupported`；exact-build、owner、process和source ABI校验均为true，source inventory SHA也与本场准备相同。后续只读定位到冻结C++ verifier仍一律拒绝`.gui`，而Python准备侧已扩展了无关GUI校验规则。这是通用实现不一致，不能由静态准备通过授予native退出能力资格。修复归框架，必须执行真实生产C++校验测试并在后续场次读回确认。

Root随后按官方Escape菜单退出，直接审阅未勾选autosave的原始确认截图，并保存每次坐标映射回执。08:08:05点击“退出到桌面”，原CaseClient持有的OS句柄实际signal/exit0；原生终态为`process_exit/0`、清理完成；原宿主08:08:19实际wait0，`normal_close_qualified=true`。Keeper原父进程实际wait0，08:11:46以CAS6031释放。**正常闭场成立，业务RED不变。** 本地分配包装器在父进程已返回0后解析多段JSON失败，保留该错误及原始两段输出，再从原始完成对象提取keeper回执；没有改写其退出码。

日志保留两条实际E记录：一条为本产品对`on_rite_updated` effect的覆盖，游戏报告使用后加载的候选effect；另一条为07:41:09初始native context查询附近的`character/GetActivityName`类型错误，来源仍待窄范围归因。没有宣称零错误。前一条不能单独证明通知机制有效，后一条也不能在没有来源证据时归为Mod故障或无害。

本轮补记产品报告与证据，未修改已加载候选。下一场必须选用实际有创建/编辑资格的保存或新角色；历史候选与正式公开v10的保存覆盖分别记账。通用退出校验、解析及生命周期工具归`ck3_eternal_recurrence`；具体产品行为、存档和证据归本仓，不向POD产品外推。
