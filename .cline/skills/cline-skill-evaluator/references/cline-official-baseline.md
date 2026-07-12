# Cline Official Skill Baseline

評価時は公式ドキュメントを正本として再確認する。このファイルは評価項目の入口であり、公式仕様より優先しない。

## Official Sources

- Skills: https://docs.cline.bot/customization/skills
- Commands and Custom Workflows: https://docs.cline.bot/core-workflows/using-commands
- Rules: https://docs.cline.bot/customization/cline-rules
- Configuration: https://docs.cline.bot/getting-started/config

## Baseline Checks

- Workspace Skillは`.cline/skills/<skill-name>/SKILL.md`に配置
- YAML frontmatterに`name`と`description`が必要
- `name`はdirectory名と完全一致
- `name`はlowercase kebab-case
- `description`は最大1024文字
- descriptionがSkillの内容と使用条件を具体的に示す
- Skill本文は5k tokens未満を目安にする
- 詳細資料とscriptは必要時に段階的に読む
- SkillがClineで有効になっている
- 同名Global Skillがある場合はGlobalが優先される
- Custom Workflowは`.clinerules/workflows/<name>.md`へ配置し、`/<name>.md`で実行

## Runtime Evidence

静的構造だけで発見・発火を合格にしない。新しいClineタスクで次を確認する。

- Workspace Skillとして検出される
- Skillが有効
- 同名Global Skillに置き換わっていない
- 固定Trigger fixtureで`use_skill`が実行される
- 固定Non-trigger fixtureで誤発火しない

実行環境で確認できない項目は`NOT RUN`とし、推測でPASSにしない。
