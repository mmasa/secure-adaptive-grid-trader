# Secure Adaptive Grid Trader

bitFlyer Lightning 現物 BTC/JPY を対象にした、手数料考慮型のグリッドトレード実験プロジェクトです。

## Phase 1

この段階では実注文を出しません。Public API から価格を取得し、Private API を設定した場合は自分の口座の取引手数料率を取得して、旧システムと同じ思想の 0.1% グリッド / 0.3% 利確候補を計算します。

- bitFlyer Public API から BTC/JPY の ticker を取得
- Private API を設定した場合、実際の取引手数料率を取得
- 0.1% グリッド / 0.3% 利確候補を計算
- 買い・売り手数料とスリッページ余裕を差し引いたネット利益率を計算
- `DRY_RUN=true` が初期値
- API キーは `.env` に置き、Git には入れない

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Private API も確認する場合のみ `.env` に bitFlyer API Key / Secret を設定します。

```env
BITFLYER_API_KEY=...
BITFLYER_API_SECRET=...
```

最初は参照系の権限だけを推奨します。

## Default strategy

- Product: `BTC_JPY`
- Grid step: 0.1%
- Target gross profit: 0.3%
- Order size: 0.001 BTC
- Minimum net profit: 0.05%
- Slippage reserve: 0.02%

ネット利益率は概ね次で判定します。

```text
gross_profit
- buy_fee
- sell_fee
- slippage_reserve
```

## Safety

Phase 1 の `main.py` は実注文を送信しません。実発注は、注文状態管理・二重発注防止・最大損失制御・再起動復元を実装してから有効化します。

## Roadmap

1. API 接続・価格取得・手数料考慮
2. ペーパートレード
3. 複数グリッド状態管理
4. 約定検知と利確注文
5. SQLite による状態保存と再起動復元
6. bitFlyer Realtime API 対応
7. 実売買の安全制御
8. FOMC / CPI / NFP などイベント戦略の追加
