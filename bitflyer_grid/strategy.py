from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GridCandidate:
    buy_price: int
    sell_price: int
    size_btc: float
    gross_profit_rate: float
    estimated_net_profit_rate: float
    estimated_net_profit_jpy: float
    tradable: bool


class GridStrategy:
    def __init__(
        self,
        *,
        grid_step_rate: float,
        target_profit_rate: float,
        size_btc: float,
        fee_rate: float,
        slippage_reserve_rate: float,
        min_net_profit_rate: float,
    ):
        self.grid_step_rate = grid_step_rate
        self.target_profit_rate = target_profit_rate
        self.size_btc = size_btc
        self.fee_rate = fee_rate
        self.slippage_reserve_rate = slippage_reserve_rate
        self.min_net_profit_rate = min_net_profit_rate

    @staticmethod
    def _jpy_price(value: float) -> int:
        return max(1, int(round(value)))

    def candidate(self, reference_price: float) -> GridCandidate:
        buy_price = self._jpy_price(reference_price * (1.0 - self.grid_step_rate))
        sell_price = self._jpy_price(buy_price * (1.0 + self.target_profit_rate))

        gross_rate = (sell_price / buy_price) - 1.0
        net_rate = (
            gross_rate
            - self.fee_rate
            - self.fee_rate
            - self.slippage_reserve_rate
        )

        gross_profit_jpy = (sell_price - buy_price) * self.size_btc
        estimated_cost_jpy = (
            buy_price * self.size_btc * self.fee_rate
            + sell_price * self.size_btc * self.fee_rate
            + buy_price * self.size_btc * self.slippage_reserve_rate
        )
        net_profit_jpy = gross_profit_jpy - estimated_cost_jpy

        return GridCandidate(
            buy_price=buy_price,
            sell_price=sell_price,
            size_btc=self.size_btc,
            gross_profit_rate=gross_rate,
            estimated_net_profit_rate=net_rate,
            estimated_net_profit_jpy=net_profit_jpy,
            tradable=net_rate >= self.min_net_profit_rate,
        )
