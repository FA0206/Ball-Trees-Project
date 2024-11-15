# Ball Trees Project

This project explores the construction and usage of Ball Trees, a spatial data structure used for efficient nearest neighbor (k-NN) and range queries. The project includes two methods of Ball Tree construction:

1. **Median Split Method** (Implemented in C++)  
2. **PCA-Based Method** (Ball* Tree, Implemented in Python)

## Features

### Ball Tree Construction
- **Median Split Method (C++)**: Constructs a Ball Tree using the median split approach for partitioning data points.  
- **PCA-Based Method (Python)**: Constructs a Ball* Tree using Principal Component Analysis (PCA) to find optimal partitions.  
  - This method **preserves a target column** (if one exists), which is an attribute of the `BallTree` class.

### Querying
- **k-NN Queries**: Efficiently retrieve the k-nearest neighbors of a point.  
- **Range Queries**: Retrieve all points within a specified range.

### Visualization
- **2D Dataset Visualization**:  
  - Currently supports visualization of Ball* Tree outputs, showing the hierarchical partitioning of the 2D space.  
  - Future plans include adding visualization support for the **Median Split Method** as well.

### Dataset Support
- **Wide variety of datasets**: Includes datasets with and without class labels.

## Future Plans
Our roadmap for further development includes:
1. **Comparative Analysis**:  
   Conducting an in-depth analysis to compare the two Ball Tree construction methods using the following metrics:  
   - Average and maximum tree depth.  
   - Construction time (requires converting C++ implementation to Python for fair comparison).  
   - Average number of nodes traversed during queries.  

   This analysis will be performed across multiple datasets with varying characteristics.

2. **Welzl's Algorithm**:  
   Understanding, implementing, and incorporating **Welzl's Algorithm**, which computes the smallest enclosing ball for a set of points in n-dimensional space.

3. **Enhanced Visualization**:  
   Expanding the visualization capabilities to include outputs from the **Median Split Method**.

## References
Our implementation and studies were inspired by several key research papers and articles:
[this paper] (https://arxiv.org/pdf/1511.00628) and [this paper] (https://steveomohundro.com/wp-content/uploads/2009/03/omohundro89_five_balltree_construction_algorithms.pdf) and [this paper] (https://dl.acm.org/doi/pdf/10.5555/1248547.1248588).


