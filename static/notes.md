# Notes on static algorithms

## Current pipeline

The pipeline is:
1. Feature engineering: Konstantin's algorithms.
2. Feature transformation:
 * Support transformation: Anastasia's non-linear transforms.
 * Scaling: std, pca, normalization (agnostic to monotonic support transformation).
3. Anomaly detection itself: iso, gmm, svm and lof.

## Possible improvements

### On feature engineering
Long-standing task of doing autoencoders.

### Feature transformations
We may try [robust pca](http://www.princeton.edu/~yc5/ele520_math_data/lectures/robust_PCA.pdf)
-- a promising dimension reduction algorithm.

### Isolation forest anomaly detection
* Introduce priors. This may be done in different ways. This should be conducted in AAD spirit (question-answer-retrain loop).
* Better parallelization.
* Becoming more deterministic.

### GMM
* Don't know what maybe done with it at the moment. It is slow, but not critically.

### Local outlier factor
* Don't see any opportunities at the moment. It is too slow.

### Support Vector Machine
* Original SVM is very-very slow. But there is [linear SVM](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html), [[1]](https://www.csie.ntu.edu.tw/~cjlin/liblinear/)[[2]](https://www.csie.ntu.edu.tw/~cjlin/papers/liblinear.pdf) that promises extreme time performance. One of the starting points is sklearn's [documentation to SVM module](https://scikit-learn.org/stable/modules/svm.html).
