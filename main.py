from bitflyer_grid.client import BitFlyerClient
from bitflyer_grid.config import Settings
from bitflyer_grid.strategy import GridStrategy


def pct(value: float) -> str:
    return f"{value * 100:.4f}%"


def main():
    settings = Settings()
    client = BitFlyerClient(settings.api_key, settings.api_secret)

    ticker = client.ticker(settings.product_code)
    ltp = float(ticker["ltp"])

    fee_rate = settings.fallback_fee_rate
    fee_source = "fallback"

    if settings.api_key and settings.api_secret:
        try:
            fee_rate = client.trading_commission(settings.product_code)
            fee_source = "bitFlyer account API"
        except Exception as exc:
            print(f"[WARN] commission API failed; using fallback: {exc}")

    strategy = GridStrategy(
        grid_step_rate=settings.grid_step_rate,
        target_profit_rate=settings.target_profit_rate,
        size_btc=settings.order_size_btc,
        fee_rate=fee_rate,
        slippage_reserve_rate=settings.slippage_reserve_rate,
        min_net_profit_rate=settings.min_net_profit_rate,
    )

    candidate = strategy.candidate(ltp)

    print("=== Secure Adaptive Grid Trader / Phase 1 ===")
    print(f"product               : {settings.product_code}")
    print(f"LTP                   : {ltp:,.0f} JPY")
    print(f"best bid / ask        : {ticker.get('best_bid'):,.0f} / {ticker.get('best_ask'):,.0f}")
    print(f"fee rate ({fee_source}) : {pct(fee_rate)} each side")
    print(f"grid step             : {pct(settings.grid_step_rate)}")
    print(f"target gross profit   : {pct(settings.target_profit_rate)}")
    print(f"slippage reserve      : {pct(settings.slippage_reserve_rate)}")
    print()
    print(f"candidate BUY         : {candidate.buy_price:,} JPY")
    print(f"candidate SELL        : {candidate.sell_price:,} JPY")
    print(f"size                  : {candidate.size_btc:.8f} BTC")
    print(f"gross profit rate     : {pct(candidate.gross_profit_rate)}")
    print(f"estimated net rate    : {pct(candidate.estimated_net_profit_rate)}")
    print(f"estimated net profit  : {candidate.estimated_net_profit_jpy:,.2f} JPY")
    print(f"profit filter         : {'PASS' if candidate.tradable else 'BLOCK'}")
    print()
    print("DRY_RUN               :", settings.dry_run)
    print("No real order is submitted in Phase 1.")


if __name__ == "__main__":
    main()
