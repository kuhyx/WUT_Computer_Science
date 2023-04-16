import tempfile
import os

import cv2
import numpy as np
import matplotlib.pyplot as plt


def main():
    # define number of data points
    N = 10

    # define the visualization params
    colors = np.random.rand(N)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        # iterate over the optimization steps
        for i in range(10):
            # generate random 2D data - replace it with the results from your algorithm
            x = np.random.rand(N)
            y = np.random.rand(N)

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
            cv2.imshow('visualization', image)

            # add wait key. window waits until user presses a key and quits if the key is 'q'
            if cv2.waitKey(0) == 113:
                # and finally destroy/close all open windows
                cv2.destroyAllWindows()
                exit()

        try:
            f.close()
            os.unlink(f.name)
        except:
            pass

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
