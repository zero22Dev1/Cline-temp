# Context Window Management Principles

## 1. Context Is A Working Set

コンテキストは保管庫ではなく、現在の判断に使うworking setとして扱う。永続情報は正本となるファイルへ置き、必要時に検索して取得する。

## 2. Relevance Has Multiple Dimensions

情報の優先度は長さではなく次で判断する。

| Dimension | Question |
|---|---|
| Relevance | 現在の判断や変更に直接必要か |
| Authority | ユーザー決定、仕様、ADR、コード、テストのどれが正本か |
| Freshness | 最新の指示・コード・結果と一致するか |
| Evidence | ファイル、シンボル、コマンド、結果へ追跡できるか |
| Risk | 欠落すると安全性、互換性、品質へ影響するか |
| Retrievability | 後から低コストで再取得できるか |

高Riskで再取得困難な情報は保持する。低Riskで再取得容易な詳細はパスだけ残す。

## 3. Compression Must Be Loss-Aware

要約時に保持するもの:

- 最新の依頼と変更履歴
- 完了条件と対象外
- 確定判断、仮定、Unknownの区別
- 重要な失敗と否定された仮説
- 変更ファイルと検証結果
- 根拠の位置

省略できるもの:

- 成功した定型コマンドの全出力
- 再生成可能な一覧
- 重複説明
- 解決済みの探索過程
- 根拠のない思考過程

## 4. Use Event-Based Thresholds

Clineが正確な残量を公開しない場合があるため、固定のトークン比率だけに依存しない。次のイベントをCheckpointの契機にする。

- 計画から実装へ移る
- 実装から検証へ移る
- 変更対象が別モジュールへ移る
- 重要な仕様判断が確定する
- 失敗により仮説を変更する
- ツール出力が長くなった
- 会話内の指示を探し直している
- 再開または引き継ぎを行う

## 5. Prefer Maps And Queries

大量ファイルを先読みする代わりに、索引と検索を整備する。

- ディレクトリマップ
- 用語集
- ADR索引
- 仕様と実装の対応表
- テストコマンド一覧
- 検索語と関連シンボル

これはContext Gapを減らすハーネス改善でもある。

## 6. Separate State From Knowledge

- 現在の作業状態: Context Checkpoint、`activeContext.md`
- 長期的な事実: `memory-bank/`
- 確定した設計判断: ADR
- 現行仕様: `docs/specs/`
- 不明点: `docs/ai/unknowns/`
- 再利用可能な学習候補: `docs/ai/learnings/`
- 生ログ: 一時ファイルまたはCI・計測システム

保存先を混ぜると、古い情報が最新文脈へ再混入する。

## 7. Validate After Context Changes

圧縮、引き継ぎ、再開後は、実装を続ける前に次を照合する。

1. 最新のユーザー依頼
2. Git差分と対象ファイルの現状
3. 完了条件
4. 未解決事項
5. 直近の検証結果

文脈の再構成も変更と同じく検証対象にする。
