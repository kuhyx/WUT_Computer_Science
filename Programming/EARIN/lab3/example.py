#!/usr/bin/env python3
"""Matplotlib scatter demo the lab-3 plotting is modelled on."""

import logging
import sys
import tempfile
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)

# cv2.waitKey returns the ASCII code of the key pressed; 'q' quits.
KEY_Q = ord("q")
# NumPy's legacy np.random.* functions share one global state; Generator is
# the modern API and is what NPY002 asks for.
RNG = np.random.default_rng()


def main() -> None:
    # define number of data points
    """Draw the scatter demo this lab's plotting is based on."""
    point_count = 10

    # define the visualization params
    colors = RNG.random(point_count)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        # iterate over the optimization steps
        for _i in range(10):
            # generate random 2D data - replace it with the results from your algorithm
            x = RNG.random(point_count)
            y = RNG.random(point_count)

            # plot the data
            plt.cla()
            plt.figure()
            plt.scatter(x, y, c=colors, alpha=0.5)
            plt.xlim([0, 1])
            plt.ylim([0, 1])
            plt.savefig(f.name)

            # read image
            image = cv2.imread(f.name)

            # show the image, provide window name first
            cv2.imshow("visualization", image)

            # add wait key. window waits until user presses a key and quits if the key
            # is 'q'
            if cv2.waitKey(0) == KEY_Q:
                # and finally destroy/close all open windows
                cv2.destroyAllWindows()
                sys.exit()

        try:
            f.close()
            Path(f.name).unlink()
        except Exception:
            logger.exception("could not close the preview window")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
