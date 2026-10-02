from bitflyer_grid.strategy import GridStrategy


def test_old_style_03pct_target_with_015pct_fee_is_blocked():
    strategy = GridStrategy(
        grid_step_rate=0.001,
        target_profit_rate=0.003,
        size_btc=0.001,
        fee_rate=0.0015,
        slippage_reserve_rate=0.0002,
        min_net_profit_rate=0.0005,
    )
    candidate = strategy.candidate(10_000_000)
    assert candidate.tradable is False


def test_zero_fee_case_can_pass():
    strategy = GridStrategy(
        grid_step_rate=0.001,
        target_profit_rate=0.003,
        size_btc=0.001,
        fee_rate=0.0,
        slippage_reserve_rate=0.0002,
        min_net_profit_rate=0.0005,
    )
    candidate = strategy.candidate(10_000_000)
    assert candidate.tradable is True
