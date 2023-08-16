# MultiFuseKit: Multi-modal Data Fusion Toolkit
### Florence J Townend
Email: [florence.townend.21@ucl.ac.uk](mailto:florence.townend.21@ucl.ac.uk) \
Twitter: [@FlorenceTownend](https://twitter.com/FlorenceTownend)

## Description

Multi-modal data fusion is the combination of different types of data (or data modalities) in the pursuit of some common goal. For example, using both blood test results and neuroimaging to predict whether somebody will develop a disease.

MultiFuseKit is a library designed to compare different multi-modal data fusion techniques against each other. It supports the following scenarios:

- Regression, binary classification, and multi-class classification
- Combining two types of tabular data or one type of tabular data and one image data (2D or 3D)

The library is built using PyTorch Lightning and PyTorch Geometric. Refer to the methods section to see which fusion methods are included.

Link to documentation: ...

## Installation

Note: To be completed! Include installation instructions for users to set up MultiFuseKit.

## Usage

### Data

Note: To be completed! Specify the required data formats for MultiFuseKit.

### Training

You can use the following training modes:

- K-fold cross-validation or train/test split
- Regression, binary classification, or multiclass classification

### Command Line Arguments

Note: To be completed! Provide details on available command line arguments.

### Logging

MultiFuseKit supports logging with Weights and Biases. (Free for academic use; please verify.)

You can utilize the logging functionality for better experiment tracking.

### Methods

The included methods are based on the review by Cui et al (2022). These methods are categorized as follows:

- Operation-based fusion
- Attention-based fusion
- Tensor-based fusion
- Subspace-based fusion
- Graph-based fusion

![Types of fusion [1]](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/baa42f6b-9fcb-4255-a022-fb45bc6ed197/Screenshot_2023-08-10_at_15.56.15.png)

Note: Add a table of the specific methods included in MultiFuseKit.

### Authors and Acknowledgements

MultiFuseKit is authored by Florence Townend and James H Cole.

This work was funded by the EPSRC (Funding code to be added).

## References

[1] Cui, C., Yang, H., Wang, Y., Zhao, S., Asad, Z., Coburn, L. A., Wilson, K. T., Landman, B. A., & Huo, Y. (2022). Deep Multi-modal Fusion of Image and Non-image Data in Disease Diagnosis and Prognosis: A Review (arXiv:2203.15588). arXiv. [https://doi.org/10.48550/arXiv.2203.15588](https://doi.org/10.48550/arXiv.2203.15588)
