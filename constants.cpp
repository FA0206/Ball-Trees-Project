/* File containing the core parameters on which the project compiles and executes. */
/* Remember to change the dimension each time the operational dataset is changed. */
/* LEAF_POINT_COUNT_THRESHOLD refers to the max number of points that may lie inside any leaf ball. */
/* METRIC refers to the mathematical parameter on which all distances are computed. Comment out the one not in use*/

#define DIMENSION 10
#define DATASET_IN_USE BLOBS_10D
#define LEAF_POINT_COUNT_THRESHOLD 5
#define METRIC EuclideanDistance
// #define METRIC ManhattanDistance

#define BLOBS_2D "Datasets/csv/2D_Blobs.csv"
#define MOONS_2D "Datasets/csv/2D_Moons.csv"
#define BLOBS_3D "Datasets/csv/3D_Blobs.csv"
#define S_CURVE_3D "Datasets/csv/3D_S_Curve.csv"
#define SWISS_ROLL_3D "Datasets/csv/3D_Swiss_Roll.csv"
#define BLOBS_5D "Datasets/csv/5D_Blobs.csv"
#define BLOBS_10D "Datasets/csv/10D_Blobs.csv"
#define BLOBS_25D "Datasets/csv/25D_Blobs.csv"
#define LATIN_CENTER_DATASET "Datasets/csv/latin_center_data.csv"
#define HIGHLEYMAN_DATASET "Datasets/csv/highleyman_data.csv"
#define LITHUANIAN DATASET "Datasets/csv/lithuanian_data.csv"
#define SOBOL_DATASET "Datasets/csv/sobol_data.csv"
#define BALLS_DATA "lib/cache/ball_center_and_radius.csv"
#define TEST_DATA "Datasets/csv/testdata.csv"