from pathlib import Path

TOPICS = [
    'analisi_tecnica_tot',
    'strategie',
    'money_management',
    'mindset',
    'volume_profile_tot',
    'smart_money_trading',
    'wyckoff',
    'trading_investing_plan',
    'recessione',
    'investimenti',
    'crypto',
    'price_action',
    'liquidita',
    'backtesting',
    'preparazione',
    'piano_dazione',
    'quant_analysis',
    'opzioni_tot',
]


def test_lesson_files_exist():
    base = Path('learn/trading')
    for t in TOPICS:
        assert (base / f"{t}.md").exists()
