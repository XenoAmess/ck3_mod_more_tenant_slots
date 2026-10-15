# 正式构建身份

`dev_tools/validate_and_build.py` 的开发构建仍可不带 tag。正式发布使用现有、指向当前源码提交的 `--git-tag`；构建器将 tag 写入 manifest，并拒绝 tag 指向其他提交或产品文件与该 tag 不同的构建。先完成业务验收，再创建正式 tag 和构建，不能事后给历史 manifest 填写发布身份。

Python、框架和游戏目录由显式参数或本机配置提供。静态验证、双构建与正式构建使用同一入口；验收、上传和实际缓存逐文件比对绑定生成的原始 manifest，不修改它补造通过证据。

验证：三个真实临时 Git 仓库测试通过，分别检查 tag/commit 写入、错误 revision 拒绝和产品文件变化拒绝。运行 `dev_tools/test_release_identity.py --framework-root <框架目录>`。构建身份代码归本产品；统一 manifest 格式及工坊缓存验收器归框架。
