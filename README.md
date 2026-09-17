````markdown
# Cline Migration Rules

## 目的

このRepositoryにおけるClineの役割は、

**旧VB.NETシステムと既存.NET移行先プロジェクトを解析し、機能単位のMigration Planを作成し、移行漏れを敵対的に検証すること**

である。

このフェーズでは実装を行わない。

Clineが行うのは以下のみ。

```text
Read
Search
Analyze
Compare
Map
Document
Audit
```

以下は行わない。

```text
Production Code変更
Test Code変更
SQL変更
Config変更
自動Refactoring
Git Commit
Git Merge
Migration実装
```

---

# 1. Migration基本原則

必ず以下を守ること。

1. 一度に1Featureのみ処理する
2. Legacy SourceはREAD ONLY
3. Target SourceもREAD ONLY
4. 実装は行わない
5. Function NameだけでMappingしない
6. Targetだけを見てMigration済みと判断しない
7. LegacyをCoverageの基準とする
8. 推測でMappingしない
9. 不明な項目は `UNRESOLVED` とする
10. Migration PlannerとAdversarial Auditorの役割を分離する
11. Plannerの判断をAuditorは信用しない
12. 移行漏れが存在する状態でPASSにしない

---

# 2. Feature単位で処理する

MigrationはFeature単位で管理する。

例:

```text
FUNC-001
FUNC-002
FUNC-003
```

1Featureにつき1つのMarkdownを作成する。

```text
.migration/
└─ features/
   ├─ FUNC-001.md
   ├─ FUNC-002.md
   └─ FUNC-003.md
```

このMarkdownをFeature MigrationのSingle Source of Truthとする。

一度に複数FeatureをMigration対象として扱ってはいけない。

---

# 3. Feature Scope

処理開始時に必ずFeature IDを特定する。

例:

```text
Current Feature:
FUNC-012
```

最初に以下を確認する。

```text
.migration/features/FUNC-xxx.md
.migration/features/feature-index.md
.migration/inventory/
.migration/mapping/
```

存在する情報を優先してScopeを決定する。

---

## 3.1 Scope Expansion

解析中に新しい依存Functionを発見しても、
即座にMigration Scopeへ追加してはいけない。

以下を確認する。

```text
Dependency Candidate

Caller

Callee

Reason

Evidence

Current Featureとの関連
```

現在Featureの挙動に必要な依存である場合のみScopeへ追加する。

---

## 3.2 Out of Scope

対象Featureとの直接・間接依存が確認できないものは、

```text
OUT_OF_SCOPE
```

とする。

別Featureを勝手に解析対象へ広げない。

---

# 4. READ ONLY

Migration PlanningおよびAudit中は、
Legacy / Targetの両方をREAD ONLYとする。

禁止:

```text
Create
Edit
Delete
Rename
Format
Refactor
```

Legacy Sourceを変更してはいけない。

Target Sourceも変更してはいけない。

必要なTarget変更を発見した場合は、

```text
Target Modification Requirement
```

としてFeature Markdownへ記録する。

---

# 5. Target変更は実装しない

Target側に不足している処理を発見しても、
コードを変更してはいけない。

代わりに以下を記録する。

```text
Target File

Target Class

Target Function

Required Change

Migration Reason

Legacy Evidence

Expected Behavior

Risk
```

悪い例:

```text
OrderServiceを修正する
```

良い例:

```text
OrderService.RegisterOrderの
Repository呼び出し前に
CustomerCode必須Validationを追加する必要がある。

LegacyではCustomerCodeが空の場合、
ERR_CUST_001を返しDB更新を行わないため。
```

---

# 6. Target Architectureを優先する

Legacy ArchitectureをTargetへそのままコピーしてはいけない。

例:

Legacy:

```text
Form
 ↓
Logic
 ↓
DAO
```

Target:

```text
Presentation
 ↓
Application
 ↓
Domain
 ↓
Infrastructure
```

この場合、Target ArchitectureをMigration先の基準とする。

Legacy Functionに複数責務が存在する場合は、
Target Architectureに合わせて責務を分割する。

その場合:

```text
Migration Type = SPLIT
```

とする。

---

# 7. Existing Target Componentを優先する

新しいClass / Functionを提案する前に、
Target側の既存Componentを確認する。

確認対象:

```text
Application Service
Domain Service
Repository
Validator
Mapper
Utility
Error Handler
Configuration
Transaction Component
```

既存Componentで責務を満たせる場合は、
新規作成を提案しない。

---

# 8. Framework変更の扱い

共通Frameworkや共通基盤の変更が必要と思われる場合は、

```text
FRAMEWORK_CHANGE_REQUIRED
```

として通常Feature変更と分離する。

Feature Migrationの一部として
共通Frameworkを勝手に変更しない。

---

# 9. Search基本方針

検索は目的ではない。

**必要なEvidenceへ到達するための手段**

として使用する。

無計画なRepository全体検索は禁止する。

---

# 10. Search順序

必ず以下の順番で調査する。

```text
1. Feature Markdown
2. Feature Index
3. Legacy / Target Inventory
4. Relation Mapping
5. Known File
6. Known Symbol
7. Limited Search
8. Broad Search
```

最初からRepository全体をGREPしてはいけない。

---

# 11. Broad Search制限

Repository全体へのBroad Searchは、
1Featureにつき原則最大3回までとする。

Broad Search前に以下を明確にする。

```text
Search Purpose

Expected Result

Why Existing Index Is Insufficient
```

目的のない、

```text
grep
rg
findstr
```

を実行してはいけない。

---

# 12. Search対象除外

原則以下を検索対象から除外する。

```text
.git/
bin/
obj/
packages/
node_modules/
generated/
build/
dist/
logs/
```

生成物・キャッシュ・Build Outputを
Migration Mappingの根拠として扱わない。

---

# 13. 対象ファイル発見後

対象File / Symbolを特定した後は、
同じ目的でRepository全体検索を続けてはいけない。

以降は対象Fileを直接読む。

禁止例:

```text
rg "Order"
rg "OrderId"
rg "RegisterOrder"
rg "InsertOrder"
rg "OrderRepository"
```

のように、
同じ目的の検索を表現を変えて繰り返すこと。

---

# 14. Search History

Broad Searchを実施した場合、
Feature Markdownへ記録する。

```markdown
### Search History

| No | Purpose | Query | Result |
|---|---|---|---|
| 1 | Order登録処理検索 | RegisterOrder | OrderService.vb確認 |
```

---

# 15. Mapping基本原則

Legacy FunctionとTarget Functionを
Function NameだけでMappingしてはいけない。

以下を比較する。

```text
Responsibility

Input

Output

Validation

Business Rule

Called Functions

Database Side Effect

Oracle Dependency

Transaction

Rollback

Exception

Error Code

Configuration

File I/O

External Interface

UI Side Effect
```

---

# 16. Mapping Evidence

すべてのMappingにはEvidenceを付ける。

Legacy Evidence:

```text
File
Symbol
Behavior
Dependency
```

Target Evidence:

```text
File
Symbol
Current Behavior
Architecture Role
```

EvidenceなしでMappingを確定してはいけない。

---

# 17. Mapping Type

以下のみ使用する。

```text
EXACT
ADAPT
SPLIT
MERGE
CREATE
REMOVE
UNRESOLVED
```

---

## 17.1 EXACT

最も厳しく判定する。

以下が実質的に同等であること。

```text
Responsibility
Input
Output
Business Rule
Validation
Database Effect
Transaction
Error Behavior
Side Effect
```

重要な差分が1つでも存在する場合、
EXACTにしてはいけない。

---

## 17.2 ADAPT

Target側に対応するFunctionが存在するが、
Legacy Behaviorの一部が不足している場合。

例:

```text
Legacy:
CustomerCode空ならエラー

Target:
Validationなし
```

↓

```text
ADAPT
```

とする。

---

## 17.3 SPLIT

Legacy 1Functionに複数責務があり、
Target Architecture上で複数Functionへ分割する場合。

---

## 17.4 MERGE

Legacy複数Functionを、
Target側の1責務に統合する場合。

---

## 17.5 CREATE

Target側に対応責務が存在しない場合。

ただし新規実装は行わない。

以下のみ記録する。

```text
ADD_FUNCTION_REQUIRED
ADD_CLASS_REQUIRED
```

---

## 17.6 REMOVE

Targetに存在しないことだけを理由に
REMOVEとしてはいけない。

以下のようなEvidenceが必要。

```text
Approved Specification
Requirement Change
Decommission Decision
Migration Decision
```

Evidenceがない場合は、

```text
UNRESOLVED
```

とする。

---

## 17.7 UNRESOLVED

Mapping根拠が不足している場合は、
無理にMappingせずUNRESOLVEDとする。

100% Coverageにするために推測してはいけない。

---

# 18. Legacy FunctionだけでCoverageを判断しない

Migration Coverage対象は以下。

```text
Function
Event Handler
Business Rule
Validation
SQL
Table
View
Oracle Package
Oracle Procedure
Oracle Function
Sequence
Trigger Dependency
Transaction
Rollback
Exception
Error Code
Configuration
File I/O
External Interface
UI Side Effect
```

Functionだけ100%でもMigration Completeとはしない。

---

# 19. Event Mapping

LegacyのEvent Handlerを必ず独立して確認する。

例:

```text
Form_Load
Button_Click
TextChanged
Leave
SelectedIndexChanged
KeyDown
Closing
```

Event処理がTarget側でFunctionへ統合されている場合でも、
Mapping表に明示する。

Eventが消えている場合はMigration Gap候補とする。

---

# 20. Business Rule / Validation Mapping

以下をFunctionとは別に確認する。

```text
Required
Length
Range
Format
Cross Field Validation
Existence Check
Duplicate Check
Status Check
Date Rule
Amount Rule
Rounding Rule
```

Legacy RuleのTarget到達先が存在しない場合:

```text
VALIDATION_MISSING
```

または

```text
BUSINESS_RULE_MISSING
```

とする。

---

# 21. Database Mapping

以下を個別に確認する。

```text
SELECT
INSERT
UPDATE
DELETE
MERGE
```

確認対象:

```text
Table
Column
WHERE条件
JOIN
ORDER BY
GROUP BY
NULL条件
件数条件
Lock
```

SQLが存在するだけで同等と判断しない。

---

# 22. Oracle Mapping

Oracle固有処理を必ず確認する。

```text
Package
Procedure
Function
Sequence
Trigger
View
PL/SQL
Cursor
Exception
```

Legacyに存在するOracle依存について
Target Mappingがない場合:

```text
ORACLE_MAPPING_MISSING
```

とする。

---

# 23. Transaction Mapping

必ずTransaction境界を比較する。

確認:

```text
Begin
Commit
Rollback
Transaction Scope
Repository呼び出し順序
Exception時挙動
```

LegacyとTargetで境界が異なる場合:

```text
TRANSACTION_DIFFERENCE
```

とする。

Transactionが確認できない場合は推測せず、

```text
UNKNOWN
```

または

```text
UNRESOLVED
```

とする。

---

# 24. Exception / Error Mapping

以下を比較する。

```text
Business Error
Validation Error
DB Error
Oracle Error
Timeout
Duplicate
Unexpected Exception
Error Code
Error Message
Return Code
```

ErrorがTarget側に存在しない場合:

```text
ERROR_MAPPING_MISSING
```

とする。

---

# 25. Config Mapping

以下を確認する。

```text
Connection Settings
Timeout
Feature Flags
Limits
Paths
Encoding
Environment Settings
```

Legacy ConfigがTarget側に存在しない場合は
移行要否を記録する。

---

# 26. File / External Interface Mapping

以下を確認する。

```text
CSV
Fixed Length
XML
JSON
File Encoding
Directory
HTTP
SOAP
TCP
External Command
Other System Interface
```

FormatやEncodingの差異もBehavior Gapとして扱う。

---

# 27. NULL / Nothing / Empty

以下は必ず確認する。

```text
Nothing
DBNull
NULL
Empty String
Whitespace
0
Zero Rows
```

LegacyとTargetで扱いが異なる場合は、
Behavior Differenceとして記録する。

---

# 28. Boundary確認

最低限以下を意識して比較する。

```text
0
1
Maximum
Minimum
Empty
NULL
Date Boundary
Month End
Leap Year
Decimal
Rounding
Duplicate
Large Data
```

実際にテストを実装する必要はないが、
移行確認ポイントとして記録する。

---

# 29. Migration Method

各Featureについて必ず、

**どう移行するのか**

を文章で説明する。

以下を含める。

```text
Legacy Architecture

Target Architecture

Legacy Responsibility

Target Responsibility

Responsibility Redistribution

Existing Target Component Reuse

Required Target Changes

Database / Oracle Migration

Transaction Migration

Error Handling Migration

Known Behavior Gaps
```

第三者が、

```text
なぜこのLegacy Functionを
このTargetへ移行するのか
```

を理解できる説明にする。

---

# 30. Target Modification Requirement

Target側で必要な変更を一覧化する。

例:

```markdown
| ID | Target | Required Change | Reason | Legacy Evidence | Risk |
|---|---|---|---|---|---|
| CHANGE-001 | OrderService.RegisterOrder | ADD_VALIDATION | CustomerCodeチェック不足 | RULE-001 | HIGH |
```

実装はしない。

---

# 31. Migration PlannerとAuditorを分離する

Planner:

```text
Legacy解析
↓
Target解析
↓
Mapping
↓
Migration Method作成
```

Auditor:

```text
Mappingを信用しない
↓
Legacyを独立再解析
↓
Legacy → Target Compare
↓
Target → Legacy Reverse Compare
↓
Migration漏れ探索
```

同じ思考で自己レビューしてはいけない。

---

# 32. Adversarial Audit基本原則

Audit時は、

```text
Migration Planには
漏れ・誤り・誤Mappingが存在する
```

という前提で確認する。

Plannerの以下を信用しない。

```text
EXACT
Target Candidate
Coverage
Migration Method
Migration Ready
```

Legacy Sourceを起点として再確認する。

---

# 33. Independent Legacy Inventory

Audit開始時、
対象Featureについて独自に以下を列挙する。

```text
Functions
Events
Business Rules
Validation
SQL
Oracle Objects
Transactions
Rollback Paths
Errors
Exceptions
Config
File I/O
External IF
UI Side Effects
```

PlannerのLegacy Scopeと比較する。

Planner側に存在しないLegacy要素を発見した場合:

```text
PLANNING_MISSING
```

とする。

---

# 34. Forward Compare

Legacy → Targetを確認する。

```text
Legacy Function
      ↓
Target Function?

Legacy Event
      ↓
Target Use Case?

Legacy Validation
      ↓
Target Validation?

Legacy SQL
      ↓
Target Repository?

Legacy Oracle
      ↓
Target Caller?

Legacy Transaction
      ↓
Target Transaction?

Legacy Error
      ↓
Target Error?
```

Target到達先がない場合:

```text
MIGRATION_MISSING
```

とする。

---

# 35. Reverse Compare

Target → Legacyも確認する。

```text
Target Behavior
      ↓
Legacy Evidence?
```

Legacy根拠が存在しない処理は、

```text
TARGET_ONLY_BEHAVIOR
```

として記録する。

目的:

```text
勝手な仕様追加
Migration対象外処理
過剰な変更
Legacyに存在しないBehavior
```

の発見。

---

# 36. EXACT Challenge

PlannerがEXACTとした項目は
優先的に敵対検証する。

以下を確認する。

```text
Input
Output
Validation
Business Rules
DB Effects
Transaction
Errors
Side Effects
```

重要な差異が存在する場合:

```text
FALSE_EXACT
```

とする。

---

# 37. Audit Finding Classification

以下を使用する。

```text
PLANNING_MISSING

MIGRATION_MISSING

FALSE_EXACT

WRONG_TARGET

BEHAVIOR_DIFFERENCE

TARGET_ONLY_BEHAVIOR

UNSUPPORTED_REMOVE

TRANSACTION_DIFFERENCE

ERROR_MAPPING_MISSING

ORACLE_MAPPING_MISSING

VALIDATION_MISSING

BUSINESS_RULE_MISSING

UNRESOLVED
```

---

# 38. Severity

以下を使用する。

```text
BLOCKER
HIGH
MEDIUM
LOW
```

BLOCKER例:

```text
主要業務処理漏れ

主要DB更新漏れ

Transaction破壊

Migration不可能な重大Gap
```

HIGH例:

```text
Validation漏れ

Oracle処理漏れ

Error処理漏れ

重要Event漏れ

主要Business Rule差異
```

MEDIUM例:

```text
Config差異

UI副作用差異

軽微なBusiness Behavior差異
```

LOW例:

```text
Documentation不足

Evidence不足

軽微なMapping説明不足
```

---

# 39. Audit Agentは修正しない

敵対的検証中に問題を発見しても、
Productionコードを修正してはいけない。

Planning部分も勝手に修正しない。

Findingとして記録する。

例:

```markdown
### AUDIT-001

Severity:

HIGH

Classification:

MIGRATION_MISSING

Legacy:

OrderForm.txtCustomerCode_Leave

Finding:

LegacyではCustomerCode変更時に
Customer情報を再取得している。

Target:

対応処理を確認できない。

Impact:

Customer変更後に旧Customer情報が
残る可能性がある。

Required Planning Correction:

Event MappingおよびMigration Methodの
再検討が必要。
```

---

# 40. UNRESOLVED Policy

不明な項目を無理に解決してはいけない。

UNRESOLVEDには以下を記録する。

```text
Legacy Symbol

Problem

Target Candidates

Why It Cannot Be Determined

Additional Evidence Required
```

例:

```text
Legacy:
CalculateSpecialPrice

Candidates:
PricingService.Calculate
SpecialPricingService.Calculate

Required Evidence:
Caller
SQL
Specification
Runtime Behavior
```

---

# 41. Planning CompleteとMigration Readyを分離する

UNRESOLVEDが存在しても、

```text
Planning Complete = YES
```

とすることはできる。

しかし、

```text
Migration Ready = YES
```

とはしてはいけない。

以下を混同しない。

```text
Documentation Complete
Migration Ready
```

---

# 42. Coverageの分母

Coverageの分母はTarget側ではない。

必ずLegacy Inventoryを使用する。

例:

```text
Legacy Functions:
27

Mapped:
27

Coverage:
27 / 27 = 100%
```

Target Function数でCoverageを計算してはいけない。

---

# 43. Category Coverage

以下を個別に算出する。

```text
Function Coverage

Event Coverage

Business Rule Coverage

Validation Coverage

Database Coverage

Oracle Coverage

Transaction Coverage

Error Coverage

Config Coverage

External Interface Coverage
```

単一の総合Coverageだけでは不十分。

---

# 44. Completion Gate

以下をすべて満たした場合のみ、

```text
Migration Ready = YES
```

とする。

```text
Function Coverage = 100%

Event Coverage = 100%

Business Rule Coverage = 100%

Database Coverage = 100%

Oracle Coverage = 100%

Validation Coverage = 100%

Transaction Coverage = 100%

Error Coverage = 100%

UNRESOLVED = 0

Adversarial BLOCKER = 0

Adversarial HIGH = 0
```

---

# 45. Self-Declaration禁止

ClineはEvidenceなしに以下を書いてはいけない。

```text
問題ありません

移行漏れはありません

完全です

Migration完了です
```

必ずCoverage・Evidence・Findingsを提示する。

---

# 46. Feature Markdown構造

各Feature Markdownは以下の構成を使用する。

```markdown
# FUNC-xxx Feature Name Migration

## 1. Summary

## 2. Legacy Scope

## 3. Target Scope

## 4. Legacy Processing Flow

## 5. Function Mapping

## 6. Event Mapping

## 7. Business Rule / Validation Mapping

## 8. Database / Oracle Mapping

## 9. Transaction Mapping

## 10. Exception / Error Mapping

## 11. Config / External Interface Mapping

## 12. Migration Method

## 13. Target Modification Requirements

## 14. Unresolved

## 15. Adversarial Verification

## 16. Coverage

## 17. Final Result
```

Plannerは原則、

```text
1〜14
```

を作成する。

Auditorは、

```text
15〜17
```

を作成する。

---

# 47. Final Result Format

Feature Markdownの最後に必ず以下を記載する。

```markdown
## 17. Final Result

### Planning

Status:

MAPPED / BLOCKED

### Adversarial Verification

Status:

PASS / FAIL

### Coverage

- Functions: XX%
- Events: XX%
- Business Rules: XX%
- Validation: XX%
- Database: XX%
- Oracle: XX%
- Transaction: XX%
- Errors: XX%

### Findings

- BLOCKER: X
- HIGH: X
- MEDIUM: X
- LOW: X

### Unresolved

X

### Migration Ready

YES / NO
```

---

# 48. Final Rule

このHarnessの目的は、

```text
ClineにコードをMigrationさせること
```

ではない。

目的は、

```text
Legacy
  ↓
Legacy Behaviorの完全な把握
  ↓
Targetとの対応関係
  ↓
Behavior Gap
  ↓
Migration Method
  ↓
Target Modification Requirement
  ↓
Adversarial Compare
  ↓
Migration漏れの検出
```

を機能単位で説明可能にすることである。

最終的に第三者がFeature Markdownを読むだけで、

```text
旧機能は何をしているか

どこへ移行するのか

なぜそこへ移行するのか

何を変更する必要があるのか

何が未解決なのか

移行漏れがないか

敵対的検証で何を確認したのか

Migration Readyなのか
```

を判断できる状態にすること。
---------------
skills

---
name: legacy-system-inventory
description: >
  Legacy VB.NETシステム全体をREAD ONLYで解析し、
  Feature Migrationで使用するSource InventoryとFeature候補を作成する。
  Productionコードの変更・移行・実装は行わない。
---

# Legacy System Inventory

## Purpose

Feature単位のMigration Planningを開始する前に、
Legacyシステム全体の構造を一度だけ棚卸しする。

このSkillの目的は、

```text
Legacy Repository
        ↓
System Inventory
        ↓
Feature Index
        ↓
Feature Migration Planning
```

の土台を作ることである。

Productionコードは変更しない。

---

# 1. Inputs

解析対象:

```text
Legacy VB.NET Project
Target .NET Project
```

確認対象:

```text
*.sln
*.vbproj
*.vb
*.config
*.json
SQL
PL/SQL
Resources
Reports
Batch
External Interfaces
```

除外:

```text
bin/
obj/
.git/
packages/
generated/
build outputs/
```

---

# 2. Legacy Project Metadata

Legacy `.vbproj` を読み、

以下を記録する。

```text
Project Name
Target Framework
Root Namespace
Project References
Package References
External Dependencies
```

推測してはいけない。

---

# 3. Target Project Metadata

Target `.vbproj` も解析する。

記録:

```text
Project Name
Target Framework
Architecture
Project References
Data Access Pattern
Transaction Pattern
Error Handling Pattern
Configuration Pattern
```

TargetはMigration先Architectureの基準として使用する。

---

# 4. Inventory対象

最低限以下を棚卸しする。

```text
Feature / Screen
Form
Class
Module
Function
Sub
Property
Event Handler

SQL
Table
View
Sequence

Oracle Package
Procedure
Function

Validation
Business Rule
Transaction

Exception
Error Code

Configuration

File I/O
CSV
XML
JSON

External Interface

Batch
Report
```

---

# 5. Stable IDs

各要素にはStable IDを設定する。

例:

```text
LEGACY-FUNC-0001
LEGACY-EVENT-0001
LEGACY-SQL-0001
LEGACY-ORA-0001
LEGACY-VALID-0001
```

IDは後続のFeature Markdownで使用する。

---

# 6. Function Inventory

例:

```markdown
| ID | File | Type | Function | Role |
|---|---|---|---|---|
| LEGACY-FUNC-0001 | OrderForm.vb | OrderForm | btnRegister_Click | Entry Point |
| LEGACY-FUNC-0002 | OrderLogic.vb | OrderLogic | CalculateTotal | Business Logic |
| LEGACY-FUNC-0003 | OrderDao.vb | OrderDao | InsertOrder | Data Access |
```

---

# 7. Dependency Discovery

Functionごとに以下を記録する。

```text
Caller
Callee
SQL
Oracle Object
Config
File
External IF
```

目的は、

```text
Function
    ↓
Dependencies
    ↓
Feature Boundary
```

を把握すること。

---

# 8. Feature Candidate Discovery

Entry Pointを中心としてFeature候補を抽出する。

例:

```text
OrderForm.btnRegister_Click
    ↓
OrderLogic.CalculateTotal
    ↓
OrderDao.InsertOrder
```

↓

```text
Candidate Feature:
FUNC-012 受注登録
```

Feature IDが既に存在する場合は既存IDを優先する。

---

# 9. Outputs

以下を作成する。

```text
.migration/
├─ inventory/
│  ├─ legacy-inventory.md
│  ├─ target-inventory.md
│  └─ dependency-index.md
│
└─ features/
   └─ feature-index.md
```

---

# 10. Feature Index

例:

```markdown
# Feature Index

| Feature ID | Feature Name | Entry Point | Main Dependencies | Status |
|---|---|---|---|---|
| FUNC-001 | 顧客検索 | CustomerForm.Search | CustomerDao | NOT_ANALYZED |
| FUNC-012 | 受注登録 | OrderForm.btnRegister_Click | OrderLogic / OrderDao | NOT_ANALYZED |
```

---

# 11. Completion

Inventory完了条件:

```text
Legacy Project Metadata確認済み
Target Project Metadata確認済み
Entry Point抽出済み
Function Inventory作成済み
Event Inventory作成済み
Database依存抽出済み
Oracle依存抽出済み
Feature候補作成済み
```

このSkillでは、

```text
Migration Mapping
Migration Ready判定
Target Modification設計
```

は実施しない。

それらはFeature Migration Plannerへ渡す。
````


---
name: feature-migration-planner
description: >
  Legacy VB.NETと既存.NET Target Projectを1Feature単位でREAD ONLY解析し、
  Legacy要素からTarget要素への対応関係、Behavior Gap、
  Target側に必要な変更、Migration方法を1つのFeature Markdownへまとめる。
  実装・コード変更・Git操作は行わない。
---
# Feature Migration Planner
## Purpose
1 Featureにつき1つのMarkdownを作成し、
```text
Legacyで何をしているか
↓
Targetのどこへ移行するか
↓
何が不足しているか
↓
どのように移行するべきか
↓
Targetの何を変更する必要があるか
```
を第三者が説明可能な状態にする。
Productionコードは変更しない。
---
# 1. Core Principle
このSkillは、
```text
Migration Implementation
```
ではなく、
```text
Migration Design / Mapping
```
を行う。
禁止:
```text
Production Code変更
Test Code変更
SQL変更
Config変更
Git Commit
Git Merge
Refactoring
```
---
# 2. Inputs
必須:
```text
Feature ID
Legacy Project
Target Project
```
優先して読む:
```text
.migration/inventory/
.migration/features/feature-index.md
既存のFUNC-xxx.md
```
---
# 3. One Feature Only
一度に1Featureのみ扱う。
例:
```text
Current Feature:
FUNC-012
```
他FeatureはMigration対象へ含めない。
共通依存を発見した場合は、
```text
DEPENDENCY
```
として記録する。
---
# 4. Output
出力は原則1ファイル。
```text
.migration/features/FUNC-012.md
```
補助ファイルを乱立させない。
Feature Migrationに関するSingle Source of Truthとする。
---
# 5. Required Markdown Structure
必ず以下の構成で作成する。
```markdown
# FUNC-xxx Feature Name Migration
## 1. Summary
## 2. Legacy Scope
## 3. Target Scope
## 4. Legacy Processing Flow
## 5. Function Mapping
## 6. Event Mapping
## 7. Business Rule / Validation Mapping
## 8. Database / Oracle Mapping
## 9. Transaction Mapping
## 10. Exception / Error Mapping
## 11. Config / External Interface Mapping
## 12. Migration Method
## 13. Target Modification Requirements
## 14. Unresolved
## 15. Adversarial Verification
## 16. Coverage
## 17. Final Result
```
Planning担当はSection 1〜14まで作成する。
Section 15以降はAudit Skillが更新する。
---
# 6. Legacy Scope
Featureに関連するLegacy要素を列挙する。
```markdown
| ID | Type | File | Symbol | Role |
|---|---|---|---|---|
| LEGACY-FUNC-001 | Function | OrderForm.vb | btnRegister_Click | Entry Point |
| LEGACY-FUNC-002 | Function | OrderLogic.vb | CalculateTotal | Business Logic |
| LEGACY-SQL-001 | SQL | OrderDao.vb | INSERT ORDER | Data Access |
```
ここがCoverageの分母になる。
---
# 7. Legacy Processing Flow
正常系だけでなく異常系も記述する。
```text
btnRegister_Click
    ↓
ValidateCustomer
    ├─ NG → ERR_CUST_001 → END
    ↓
CalculateTotal
    ↓
Begin Transaction
    ↓
InsertOrder
    ↓
InsertOrderDetail
    ↓
Commit
```
Rollback経路も確認する。
---
# 8. Legacy Contract
各重要Functionについて以下を確認する。
```text
Responsibility
Inputs
Outputs
Validation
Calls
Database
Transaction
Exception
Error Code
UI Side Effect
Configuration
File I/O
External IF
```
コード行数ではなくBehaviorをマッピングする。
---
# 9. Target Candidate Discovery
対応Targetは以下の順序で探す。
```text
1. Explicit Specification / Trace ID
2. Business Responsibility
3. Input / Output
4. DB Side Effect
5. Caller / Callee Relationship
6. Transaction
7. Error Behavior
8. Target Architecture
9. Signature
10. Name
```
名前一致だけでMappingしてはいけない。
---
# 10. Mapping Types
使用可能:
```text
EXACT
ADAPT
SPLIT
MERGE
CREATE
REMOVE
UNRESOLVED
```
## EXACT
Targetに実質同等Behaviorが存在。
## ADAPT
Targetは存在するが一部変更が必要。
## SPLIT
Legacy 1責務群をTarget複数要素へ分離。
## MERGE
Legacy複数要素をTarget 1責務へ統合。
## CREATE
Targetに適切な責務が存在しない。
## REMOVE
承認済み要件によりLegacy Behaviorを廃止。
## UNRESOLVED
証拠不足。
推測してはいけない。
---
# 11. Function Mapping
必ずLegacy起点で全Functionを記録する。
```markdown
| ID | Legacy | Target | Type | Gap | Migration Method | Status |
|---|---|---|---|---|---|---|
| FMAP-001 | OrderForm.btnRegister_Click | OrderService.RegisterOrder | SPLIT | UI責務混在 | Application等へ責務分離 | MAPPED |
| FMAP-002 | OrderLogic.CalculateTotal | OrderCalculator.Calculate | ADAPT | 丸め条件不足 | Legacy丸め条件をTargetへ追加 | MAPPED |
```
---
# 12. Event Mapping
EventをFunction Mappingだけに埋め込まず独立管理する。
```markdown
| Legacy Event | Trigger | Target | Migration Method | Status |
|---|---|---|---|---|
| Form_Load | Form Open | LoadOrderMaster | 初期化UseCaseへ移行 | MAPPED |
| txtCustomer_Leave | Focus Lost | CustomerValidator | Validationへ再配置 | MAPPED |
```
Event漏れを防ぐため必須。
---
# 13. Business Rule / Validation Mapping
```markdown
| ID | Legacy Rule | Target | Gap | Required Change |
|---|---|---|---|---|
| RULE-001 | CustomerCode必須 | OrderService | Missing | ADD_VALIDATION |
| RULE-002 | Quantity > 0 | OrderValidator | None | NO_CHANGE |
```
Business RuleはFunctionとは別に数える。
---
# 14. Database / Oracle Mapping
以下を個別に確認する。
```text
SELECT
INSERT
UPDATE
DELETE
MERGE
Table
View
Sequence
Trigger
Package
Procedure
Function
PL/SQL
```
例:
```markdown
| ID | Legacy | Target | Type | Status |
|---|---|---|---|---|
| DB-001 | ORDER INSERT | OrderRepository.Insert | SQL | MAPPED |
| ORA-001 | PKG_ORDER.REGISTER | OrderRepository.Register | Package | MAPPED |
```
---
# 15. Transaction Mapping
必ず境界を比較する。
Legacy:
```text
Begin
 ↓
Insert Order
 ↓
Insert Detail
 ↓
Commit
```
Target:
```text
Application Transaction
 ↓
OrderRepository
 ↓
OrderDetailRepository
 ↓
Commit
```
以下を記録する。
```text
Equivalent: YES / NO / UNKNOWN
```
UNKNOWNはUNRESOLVEDへ追加する。
---
# 16. Error Mapping
確認:
```text
Business Error
Validation Error
Oracle Error
Timeout
Duplicate
Unexpected Exception
```
例:
```markdown
| Legacy Error | Target | Status |
|---|---|---|
| ERR_CUST_001 | CustomerRequiredError | MAPPED |
| ORA-00001 | DuplicateOrderException | MAPPED |
| Timeout | - | MISSING |
```
---
# 17. Behavior Gap
LegacyとTargetの差分は明示する。
例:
```markdown
### GAP-001
Legacy:
CustomerCodeが空文字の場合、
ERR_CUST_001を返しDB処理を行わない。
Target:
CustomerCodeのValidationが存在せず、
Repositoryが呼び出される。
Impact:
LegacyとTargetで登録結果が異なる。
Required Migration:
Repository呼び出し前にLegacy相当Validationが必要。
```
---
# 18. Target Modification Requirement
コードは変更しない。
必要になるTarget変更だけを設計する。
```markdown
| ID | Target | Required Change | Reason | Legacy Evidence | Risk |
|---|---|---|---|---|---|
| CHANGE-001 | OrderService.RegisterOrder | ADD_VALIDATION | LegacyとのBehavior Gap | RULE-001 | HIGH |
| CHANGE-002 | OrderCalculator.Calculate | MODIFY_RULE | 丸め条件差異 | LEGACY-FUNC-002 | MEDIUM |
```
説明は具体的にする。
悪い:
```text
OrderServiceを修正する
```
良い:
```text
OrderService.RegisterOrderのRepository呼出前に
CustomerCode必須Validationを追加する必要がある。
CustomerCodeが空の場合は
ERR_CUST_001相当を返し、
DB更新を実行しない。
```
---
# 19. Migration Method
Feature全体の移行方法を文章で説明する。
説明には必ず以下を含める。
```text
Legacy Architecture
Target Architecture
責務の再配置方法
既存Target Componentの再利用
新規追加が必要な責務
Behavior Gap
Oracle / Transaction方針
```
第三者が、
```text
なぜこの移行方法なのか
```
を理解できる内容にする。
---
# 20. Unresolved
不明事項は隠さない。
```markdown
| ID | Legacy | Problem | Candidates | Required Evidence |
|---|---|---|---|---|
| UNR-001 | CalculateSpecialPrice | Target責務不明 | PricingService / SpecialPricingService | Caller / SQL / Specification |
```
UNRESOLVEDが存在してもPlanningは完了可能。
ただし、
```text
Migration Ready = NO
```
とする。
---
# 21. Search Policy
検索順序:
```text
Feature Markdown
↓
Inventory
↓
Known File
↓
Known Symbol
↓
Limited Search
↓
Broad Search
```
Broad Searchは原則3回まで。
対象ファイル発見後は直接読む。
検索量ではなくEvidenceの質を重視する。
---
# 22. Planning Completion
Planning完了条件:
```text
Legacy Scope確定
Target Scope確認
Legacy Processing Flow作成
Function Mapping作成
Event Mapping作成
Business Rule Mapping作成
Database / Oracle Mapping作成
Transaction Mapping作成
Error Mapping作成
Migration Method記載
Target Modification Requirements作成
Unresolved記載
```
Planning完了後:
```text
Status = MAPPED
```
とする。
Planning担当は、
```text
Migration Ready = YES
```
を判定してはいけない。
最終判定はAdversarial Auditが行う。

````markdown
---
name: feature-migration-auditor
description: >
  Feature Migration Plannerが作成したFUNC-xxx.mdを信用せず、
  Legacy SourceとTarget SourceをREAD ONLYで独立再解析する。
  Legacy→TargetおよびTarget→Legacyの双方向Compareにより、
  移行漏れ、誤Mapping、Target側の余計な処理、Behavior Gapを検出する。
  ProductionコードやMigration Planを勝手に修正しない。
---

# Feature Migration Adversarial Auditor

## Purpose

Migration Planが正しいことを確認するのではない。

```text
Migration Planには
漏れ・誤り・誤Mappingが存在する
```

という前提で検証する。

目的:

```text
移行元に存在する重要Behaviorが
移行先で行方不明になっていないか
```

を独立して検証する。

---

# 1. Independence

Audit担当はPlanning担当の結論を信用しない。

信用してはいけないもの:

```text
EXACT判定
Target Candidate
Coverage
Migration Method
Migration Ready
```

LegacyとTargetを自分で確認する。

---

# 2. Inputs

```text
Feature ID

.migration/features/FUNC-xxx.md

Legacy Source

Target Source

System Inventory
```

すべてREAD ONLY。

---

# 3. Audit Order

必ず以下の順序で実施する。

```text
Legacy Inventory
↓
Legacy Source
↓
独立したLegacy要素一覧
↓
Target Source Compare
↓
既存FUNC-xxx.mdとCompare
↓
Findings
↓
Coverage
↓
Final Result
```

最初からFUNC-xxx.mdのMapping表を答えとして使わない。

---

# 4. Independent Legacy Inventory

対象Featureについて独自に以下を列挙する。

```text
Functions
Events
Business Rules
Validation
SQL
Tables
Views
Sequences
Oracle Packages
Procedures
Functions
Transactions
Rollback Paths
Errors
Exceptions
Config
File I/O
External IF
UI Side Effects
```

この一覧とPlannerのLegacy Scopeを比較する。

Plannerに存在しないものを、

```text
PLANNING_MISSING
```

とする。

---

# 5. Forward Compare

Legacy → Targetを1件ずつ追跡する。

```text
Legacy Element
       ↓
Target Destination
       ↓
Equivalent Behavior?
```

確認:

```text
Function → Function
Event → Event / Use Case
Rule → Rule
Validation → Validation
SQL → Repository
Package → Target Caller
Transaction → Transaction
Error → Error
Config → Config
External IF → Client
```

Targetへの到達先がない場合:

```text
MIGRATION_MISSING
```

---

# 6. Behavioral Compare

「存在する」だけではPASSにしない。

比較する。

```text
Input
Output
Condition
Validation
DB Side Effect
Transaction Boundary
Rollback
Error
Exception
UI Side Effect
External Side Effect
```

差異が存在する場合:

```text
BEHAVIOR_DIFFERENCE
```

とする。

---

# 7. EXACT Challenge

Plannerが `EXACT` としたものは重点監査する。

以下すべてを確認する。

```text
Responsibility
Input
Output
Business Rules
Validation
Database Effect
Transaction
Error Behavior
```

重要差異が1つでもあれば、

```text
FALSE_EXACT
```

Findingを作成する。

---

# 8. Reverse Compare

Target → Legacyも確認する。

Target Feature Scopeに存在する処理について、

```text
Target Behavior
      ↓
Legacy Evidence?
```

を調査する。

Legacy根拠が存在しない場合:

```text
TARGET_ONLY_BEHAVIOR
```

とする。

目的:

```text
勝手な仕様追加
過剰Migration
不要なBehavior変更
```

の検出。

---

# 9. Required Adversarial Checks

最低限以下を確認する。

```text
[ ] Functions
[ ] Event Handlers
[ ] Business Rules
[ ] Validation
[ ] SELECT
[ ] INSERT
[ ] UPDATE
[ ] DELETE
[ ] MERGE
[ ] Oracle Package
[ ] Oracle Procedure
[ ] Oracle Function
[ ] Sequence
[ ] Trigger Dependency
[ ] Transaction
[ ] Rollback
[ ] Exceptions
[ ] Error Codes
[ ] Configuration
[ ] File I/O
[ ] External Interfaces
[ ] UI Side Effects
[ ] NULL / Nothing
[ ] Empty String
[ ] Zero Rows
[ ] Boundary Conditions
[ ] Date Conditions
[ ] Decimal / Rounding
```

---

# 10. Finding Format

問題発見時:

```markdown
### AUDIT-001

Severity:

HIGH

Classification:

MIGRATION_MISSING

Legacy Evidence:

- File: OrderForm.vb
- Symbol: txtCustomerCode_Leave

Legacy Behavior:

CustomerCode変更時にCustomer情報を再取得する。

Target Evidence:

対応する処理を確認できない。

Impact:

CustomerCode変更後に旧Customer情報が残る可能性がある。

Planner Status:

Feature MarkdownにMappingなし。

Required Planning Correction:

Event Mappingへ追加し、
Migration MethodとTarget Modification Requirementを再検討する。
```

---

# 11. Finding Classification

使用する。

```text
PLANNING_MISSING
MIGRATION_MISSING
FALSE_EXACT
WRONG_TARGET
BEHAVIOR_DIFFERENCE
TARGET_ONLY_BEHAVIOR
UNSUPPORTED_REMOVE
TRANSACTION_DIFFERENCE
ERROR_MAPPING_MISSING
ORACLE_MAPPING_MISSING
VALIDATION_MISSING
UNRESOLVED
```

---

# 12. Severity

```text
BLOCKER
HIGH
MEDIUM
LOW
```

BLOCKER例:

```text
主要DB更新漏れ
主要業務処理漏れ
Transaction破壊
```

HIGH例:

```text
Validation漏れ
Oracle処理漏れ
Error処理漏れ
重要Event漏れ
```

MEDIUM例:

```text
Config差異
UI副作用差異
```

LOW例:

```text
Mapping根拠不足
Documentation不足
```

---

# 13. Coverage

Coverageの分母はTargetではなくLegacy。

例:

```markdown
## 16. Coverage

| Category | Legacy | Mapped | Coverage |
|---|---:|---:|---:|
| Functions | 25 | 25 | 100% |
| Events | 8 | 8 | 100% |
| Business Rules | 17 | 17 | 100% |
| SQL | 12 | 12 | 100% |
| Oracle Objects | 5 | 5 | 100% |
| Validation | 14 | 14 | 100% |
| Errors | 6 | 6 | 100% |
```

総合CoverageだけでなくCategory別に表示する。

---

# 14. Migration Ready Gate

以下をすべて満たす場合のみYES。

```text
Function Coverage = 100%
Event Coverage = 100%
Business Rule Coverage = 100%
Database Coverage = 100%
Oracle Coverage = 100%
Validation Coverage = 100%
Transaction Coverage = 100%
Error Coverage = 100%

UNRESOLVED = 0

BLOCKER = 0
HIGH = 0
```

---

# 15. Update Feature Markdown

Audit結果は既存の

```text
.migration/features/FUNC-xxx.md
```

の以下のSectionだけに追記する。

```text
## 15. Adversarial Verification
## 16. Coverage
## 17. Final Result
```

Planning部分を無断で書き換えない。

問題がある場合はFindingとして指摘する。

---

# 16. Final Result Format

```markdown
## 17. Final Result

### Planning

Status:

MAPPED

### Adversarial Verification

Status:

PASS / FAIL

### Coverage

- Functions: 100%
- Events: 100%
- Business Rules: 100%
- Database: 100%
- Oracle: 100%
- Validation: 100%
- Transaction: 100%
- Errors: 100%

### Findings

- BLOCKER: 0
- HIGH: 0
- MEDIUM: 0
- LOW: 0

### Unresolved

0

### Migration Ready

YES / NO
```

---

# 17. Critical Rule

Auditの目的は、

```text
Plannerの成果物を承認すること
```

ではない。

目的は、

```text
Plannerが見落としたLegacy Behaviorを探す
```

ことである。

「問題を発見できなかった」と

「問題が存在しない」は同義ではない。

PASSとは、

```text
定義されたLegacy Scopeと検証カテゴリについて
Targetへの対応を確認し、
BLOCKER / HIGH / UNRESOLVEDが残っていない
```

ことを意味する。
````