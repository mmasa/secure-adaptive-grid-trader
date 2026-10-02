from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("BITFLYER_API_KEY", "")
    api_secret: str = os.getenv("BITFLYER_API_SECRET", "")
    product_code: str = os.getenv("PRODUCT_CODE", "BTC_JPY")

    dry_run: bool = _bool("DRY_RUN", True)

    grid_step_rate: float = float(os.getenv("GRID_STEP_RATE", "0.001"))
    target_profit_rate: float = float(os.getenv("TARGET_PROFIT_RATE", "0.003"))
    order_size_btc: float = float(os.getenv("ORDER_SIZE_BTC", "0.001"))

    fallback_fee_rate: float = float(os.getenv("FALLBACK_FEE_RATE", "0.0015"))
    slippage_reserve_rate: float = float(os.getenv("SLIPPAGE_RESERVE_RATE", "0.0002"))
    min_net_profit_rate: float = float(os.getenv("MIN_NET_PROFIT_RATE", "0.0005"))
