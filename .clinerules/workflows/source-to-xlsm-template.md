# Source To XLSM Template Workflow

## Teams Notification Option

開始時に`Teams通知: 有効 / 無効`を選択する。未指定は`無効`とし、今回の実行だけに適用する。`有効`の場合でもXLSM生成、実テンプレート検証、品質ゲートがPASSした時だけ通知する。

既存ソースからHTMLモック画面を生成し、`<section>`ごとに文字またはHTMLレンダリング画像をマクロ付きExcelテンプレートへ出力する。

## Step 1: Confirm Inputs

Skill `source-to-xlsm-template`を読み込む。ワークフォルダー内から入力、`.xlsm`テンプレート、JSONマッピングを確認し、出力先を`outputs/excel/`に決める。

実際に使用するHTML、`.xlsm`テンプレート、mapping、画像対象セクションを開始前に確定する。テンプレートが未配置、破損、またはWindows版Excelでの互換性確認が必要なのに実施できない場合は`Blocked`とし、完成扱いにしない。

## Step 2: Normalize Source

既存ソースをSkill `legacy-source-spec-writer`で調査し、画面仕様とUnknownを分離する。その仕様を基にSkill `implementation-loop`で確認用HTMLモックを生成する。HTMLは画面・機能のまとまりごとに`<section id="一意なID">`で構造化する。

## Step 3: Generate

HTMLの各`<section>`に一意な`id`を付け、`text / image / image-and-text`を決める。画像対象だけをブラウザでキャプチャし、selector、表示形式、画像パス、出典をmanifestへ記録する。

各画像対象について、ブラウザで対象selectorが1要素だけに一致すること、キャプチャが空白でないこと、期待状態が表示されていることを確認する。取得できない画像をダミー画像で代替しない。

テンプレートのファイルハッシュとVBAハッシュを記録し、再利用スクリプトで説明とモック画面画像をコピー先だけへ書き込む。元テンプレートを上書きしない。

## Step 4: Verify

- 出力拡張子が`.xlsm`
- 原本テンプレートのハッシュが不変
- `vbaProject.bin`が存在し、原本と同一
- 対象シートと出力件数が正しい
- セクション、本文、出典が対応する
- HTMLセクションとExcel上のHTMLレンダリング画像が対応する
- 文字のみのセクションに不要な画像がなく、画像対象のセクションに欠落がない
- 既存数式と書式に意図しない変更がない
- 名前定義、結合セル、外部リンクなどテンプレート固有要素に意図しない変更がない
- 実際のHTML、manifest、`.xlsm`テンプレートを使ったEnd-to-End検証がPASS

`source-to-xlsm-template/scripts/verify_xlsm.py`を実行し、結果JSONを検証証拠として保存する。

必要に応じて`/artifact-quality-gate.md`で帳票内容を検証する。マクロ動作が完了条件の場合は、信頼済みWindows版Excelで確認する。

synthetic fixtureの単体テストだけでは実テンプレートの合格根拠にしない。実テンプレート検証を実行できない場合は`NOT RUN`とし、最終判定は最大`NEEDS_REVISION`とする。

実テンプレート検証後に`/artifact-quality-gate.md`とSkill `loop-verifier`を実行する。`Teams通知: 有効`かつQuality Gateが`PASS`、Skill `loop-verifier`が`APPROVE`の場合だけ、`/teams-completion-notification.md`を`workflow`モードで実行する。

## Step 5: Report

- 入力ファイル
- 使用テンプレートとマッピング
- 出力`.xlsm`
- セクション件数
- VBA保持検証
- Excelでのマクロ動作確認状況
- Unknownと未検証事項
