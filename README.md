````markdown
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