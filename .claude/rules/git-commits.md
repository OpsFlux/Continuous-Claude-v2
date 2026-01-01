<a id="git-commit-rules"></a>
# Git 提交规则

当用户要求承诺、推动或保存更改为 git 时：

<a id="must-use-commit-skill"></a>
## 必须使用/commit 技能

**不执行**`git commit`直接说 相反：

```
Skill("commit")
```

这个`/commit`技能 :
1. 从承诺中删除 Claude 属性
2. 生成推理。md 捕捉被尝试的东西
3. 清除构建下一个特性的尝试

<a id="why-this-matters"></a>
## 为什么这很重要

- 经常`git commit`添加“ Generated with Claude Code” 和“ 联合认证” 线条
- 这个`/commit`技能删除这些任务， 以显示用户授权
- 理性捕捉为今后届会保留了建设历史

<a id="trigger-words"></a>
## 触发词

在用户提示中看到这些时，请使用承诺技能：
- "承诺","推","拯救"
- "推来推去" "推去改变"
- "承诺和推"

<a id="after-commit"></a>
## 提交后

这个技能会促使你跑：
```bash
bash .claude/scripts/generate-reasoning.sh <hash> "<message>"
```

请按下：
```bash
git push origin <branch>
```
