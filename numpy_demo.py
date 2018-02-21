import numpy as np

def test_run():
    # list to 1D array
    print np.array([2,3,4])

    # list of tuples to 2D array
    print np.array([(2,3,4), (5,6,7)])

    # Empty array
    print np.empty(5)

    # array of 1s
    print np.ones((5, 4))   # 5 rows 4 cols
    

if __name__ == "__main__":
    test_run()