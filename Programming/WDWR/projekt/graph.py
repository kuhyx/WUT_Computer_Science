#!/usr/bin/env python3
"""Plot the Pareto front of the WDWR production model: profit against risk.

Each row of ``data/pareto_front.csv`` is one solution of the bi-criteria MILP
-- an average profit, its Gini risk measure, and the production and stock
levels that produced them. The scatter shows the trade-off between the two
criteria.

The data used to be a 20-line CSV embedded in this file as a string literal.
It moved to a sibling file because its header line alone is 342 characters,
and a data record is not something that can be wrapped to fit a line limit.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)

DATA_FILE = Path(__file__).parent / "data" / "pareto_front.csv"

# Everything is sized for a report figure rather than for the screen.
LABEL_FONT_SIZE = 16
MARKER_AREA = 200


def main() -> None:
    """Draw the scatter plot and report the range of each axis."""
    df = pd.read_csv(DATA_FILE, sep=";")

    plt.figure(figsize=(10, 6))
    plt.scatter(df["averageProfit"], df["riskMeasureGini"], alpha=0.7, s=MARKER_AREA)

    plt.xlabel("Przeciętny Zysk", fontsize=LABEL_FONT_SIZE)
    plt.ylabel("Ryzyko", fontsize=LABEL_FONT_SIZE)
    plt.xticks(fontsize=LABEL_FONT_SIZE)
    plt.yticks(fontsize=LABEL_FONT_SIZE)
    plt.grid(visible=True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    logger.info(
        "Average Profit range: %.2f to %.2f",
        df["averageProfit"].min(),
        df["averageProfit"].max(),
    )
    logger.info(
        "Gini Risk range: %.2f to %.2f",
        df["riskMeasureGini"].min(),
        df["riskMeasureGini"].max(),
    )
    logger.info("Number of data points: %d", len(df))


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    main()
