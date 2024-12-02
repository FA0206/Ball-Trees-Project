#include <bits/stdc++.h>
#include "constants.cpp"
#include "lib/MedianSplitConstruction.cpp"
#include "lib/rangequeries.cpp"
#include "lib/KNN.cpp"
#include "lib/naiveKNN.cpp"
#include <chrono>
using namespace std;

inline void FileParsingProcess(const char* filename, vector<Point*>& universalDataPoints) {
    ifstream file(DATASET_IN_USE);
    double x, y; int t;

    /* Check if file is opened successfully. */
    if(!file.is_open()) {
        cout << "\033[31:40m--> ERROR : File Open Error!\033[0m" << endl;
        return;
    }

    string line;
    getline(file, line); // skip the label line
    
    /* Parsing the stream. */
    while(getline(file, line)) {
        stringstream ss(line);
        string value;
        vector<double> values;

        /* Splitting the csv using , as delimiter. */
        while(getline(ss, value, ',')) {
            try {
                values.push_back(stod(value));
            }
            catch (exception e) {
                /* Exception that arises when file contains other than double data. */
                cout << "\033[31:40m--> ERROR : Value Parse Error.\033[0m" << endl;
                return;
            }
        }

        /* if the dimension of the dataset is different than what is specified. */
        if(values.size() != DIMENSION + 1) {
            cout << "\033[31:40m--> ERROR : Inconsistent Dimension Parameter!\033[0m" << endl;
            return;
        }

        /* Create new datapoint. */
        Point* newPoint = new Point();

        /* Assign values to the datapoint. */
        for(int i = 0; i < DIMENSION+1; i++) {
            newPoint->coordinate[i] = values[i];
        }
        /* Add it to the pointset. */
        universalDataPoints.push_back(newPoint);
    }

    file.close();
    cout << "\033[32:40m--> Dataset Parsed Successfully.\033[0m" << endl;
    cout << "--------------------------------------------------------" << endl;
}

inline void TreeConstructionProcess(BallTree* &tree, vector<Point*>& universalDataPoints) {
    auto start = chrono::high_resolution_clock::now();
    tree = constructBallTreeUsingMedianSplit(tree, universalDataPoints);
    tree->setTreeDepths();
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    cout << "\033[32:40m--> BallTree Construction complete.\033[0m" << endl;
    cout << "    \033[34:40m--> Construction Time (sec) = " << elapsed.count() << "." << endl;
    cout << "    --> Max Tree Depth = " << tree->maxDepth << "." << endl;
    cout << "    --> Average Tree Depth = " << tree->averageDepth << ".\033[0m" << endl;
}

inline void VolumeComputationProcess(BallTree* &tree) {
    FILE* fptr2 = fopen("lib/cache/volumedata.txt", "w");
    computeBallVolumesAndSaveToFile(fptr2, tree->root);
    fclose(fptr2);

    fptr2 = fopen("lib/cache/volumedata.txt", "r");
    double totalVolume = 0.0f;
    double v;
    while(fscanf(fptr2, "%lf", &v) == 1) {
        totalVolume += v;
    }
    fclose(fptr2);
    cout << "    \033[34:40m--> Total Volume of Ball Tree = " << totalVolume << ".\033[0m" << endl;
    cout << "--------------------------------------------------------" << endl;
}

inline void RangeQueryProcess(BallTree* &tree) {
    Point* query = new Point();
    double r;
    char choice;
    vector<Point*> rangeNeighbors;

    cout << "\n\033[32:40m--> Start Range Querying? (Y/N) : \033[0m";
    cin >> choice;
    if(tolower(choice) == 'n') {
        cout << "--------------------------------------------------------" << endl;
        return;
    }
    
    while(true) {
        // input query coordinates
        cout << "Enter query coordinates as space separated values (DIMENSION = " << DIMENSION << ") : ";
        double c;
        for(int i = 0; i < DIMENSION; i++) {
            cin >> c;
            query->coordinate[i] = c;
        }

        // input query range
        cout << "Enter Range or 0 to exit : " ;
        cin >> r;
        if(r <= 0) {
            break;
        }

        // find the range query neighbors
        int pointsVisited = 0;
        auto range_start = chrono::high_resolution_clock::now();
        rangeNeighbors = findrangeNeighbors(tree->root, query, r, pointsVisited);
        auto range_end = chrono::high_resolution_clock::now();

        // print the query results
        cout << "\n\033[32:40mQuery Results : \033[0m" << endl;
        for(auto i : rangeNeighbors) {
            cout << "(";
            for(int k = 0; k < DIMENSION; k++) {
                cout << i->coordinate[k];
                if(k != DIMENSION-1) {
                    cout << ",";
                }
            }
            cout << ")" << endl;
        }
        cout << "\n\033[32:40m--> Query Successful.\033[0m" << endl;

        chrono::duration<double> elapsed = range_end - range_start;

        // display metrics
        cout << "\033[34:40m    --> Total Points Traversed = " << pointsVisited << "." << endl;
        cout << "    --> Relevent Points Found = " << rangeNeighbors.size() << "." << endl;
        cout << "    --> Query Time = " << elapsed.count() << " seconds.\033[0m" << endl;

        cout << "\n\033[32:40m--> Continue Range Querying? (Y/N) : \033[0m";
        cin >> choice;
        if(tolower(choice) == 'n') {
            break;
        }
    }

    delete query;

    cout << "\n\033[32:40m--> Completed Range Query Processing.\033[0m" << endl;
    cout << "--------------------------------------------------------" << endl;

}

inline void NaiveKNNProcess(BallTree* &tree) {
    Point* query = new Point();
    int neighborCount;
    char choice;

    cout << "\n\033[32:40m--> Start Naive KNN Querying? (Y/N) : \033[0m";
    cin >> choice;
    if(tolower(choice) == 'n') {
        cout << "--------------------------------------------------------" << endl;
        return;
    }

    while(true) {
        // input query coordinates
        cout << "Enter query coordinates as space separated values (DIMENSION = " << DIMENSION << ") : ";
        double c;
        for(int i = 0; i < DIMENSION; i++) {
            cin >> c;
            query->coordinate[i] = c;
        }

        // input neighbor count
        cout << "Enter No of Neighbours, -1 to exit : " ;
        cin >> neighborCount;
        if(neighborCount <= -1) {
            break;
        }

        // query knn
        int pointsVisited = tree->root->ball->containedPoints.size();
        auto nknn_time = chrono::high_resolution_clock::now();
        vector<pair<double, Point*>> results = knn_naive(tree->root, query, neighborCount);
        auto nknn_end = chrono::high_resolution_clock::now();


        for(int i = 0; i < neighborCount; i++) {
            cout << "(";
            for(int j = 0; j < DIMENSION; j++) {
                cout << results[i].second->coordinate[j] << ",";
            }
            cout << ")" << endl;
        }

        cout << "\n\033[32:40m--> Query Successful.\033[0m" << endl;
        chrono::duration<double> elapsed = nknn_end - nknn_time;

        // display metrics
        cout << "\033[34:40m    --> Total Points Traversed = " << pointsVisited << "." << endl;
        cout << "    --> Relevent Points Found = " << min(neighborCount, (int)results.size()) << "." << endl;
        cout << "    --> Query Time = " << elapsed.count() << " seconds.\033[0m" << endl;

        cout << "\n\033[32:40m--> Continue Naive KNN Querying? (Y/N) : \033[0m";
        char choice;
        cin >> choice;
        if(tolower(choice) == 'n') {
            break;
        }
    }

    delete query;
    

    cout << "\n\033[32:40m--> Completed Naive KNN Querying.\033[0m" << endl;
    cout << "--------------------------------------------------------" << endl;

}

inline void KNNProcess(BallTree* &tree, vector<Point*>& universalDataPoints) {
    char choice;
    int neighborCount;
    Point* query = new Point();
    vector<Point*> knn_results;

    cout << "\n\033[32:40m--> Start KNN Querying? (Y/N) : \033[0m";
    cin >> choice;
    if(tolower(choice) == 'n') {
        cout << "--------------------------------------------------------" << endl;
        return;
    }

    while(true) {
        // input query coordinates
        cout << "Enter query coordinates as space separated values (DIMENSION = " << DIMENSION << ") : ";
        double c;
        for(int i = 0; i < DIMENSION; i++) {
            cin >> c;
            query->coordinate[i] = c;
        }

        // input neighbor count
        cout << "Enter No of Neighbours, -1 to exit : " ;
        cin >> neighborCount;
        if(neighborCount <= -1) {
            break;
        }

        // query knn
        int pointsVisited = 0;
        auto knn_start = chrono::high_resolution_clock::now();
        knn_results = findKNearestNeighbors(tree->root, query, neighborCount, pointsVisited);
        auto knn_end = chrono::high_resolution_clock::now();

        // print query results
        cout << "\n\033[32:40mQuery Results : \033[0m" << endl;
        int j = 0;
        for(auto res : knn_results) {
            if(++j > universalDataPoints.size()) break;
            cout << "(";
            for (int k = 0; k < DIMENSION; k++)
            {
                cout << res->coordinate[k];
                if (k != DIMENSION - 1)
                {
                    cout << ",";
                }
            }
            cout << ")" << endl;
        }
        cout << "\n\033[32:40m--> Query Successful.\033[0m" << endl;
        chrono::duration<double> elapsed = knn_end - knn_start;
        

        // display metrics
        cout << "\033[34:40m    --> Total Points Traversed = " << pointsVisited << "." << endl;
        cout << "    --> Relevent Points Found = " << knn_results.size() << "." << endl;
        cout << "    --> Query Time = " << elapsed.count() << " seconds.\033[0m" << endl;

        cout << "\n\033[32:40m--> Continue KNN Querying? (Y/N) : \033[0m";
        char choice;
        cin >> choice;
        if(tolower(choice) == 'n') {
            break;
        }
    }

    delete query;

    cout << "\n\033[32:40m--> Completed KNN Querying.\033[0m" << endl;
    cout << "--------------------------------------------------------" << endl;
}

void deleteTree(BallTreeNode* root) {
    if (!root) return;

    // Delete left and right subtrees
    deleteTree(root->left);
    deleteTree(root->right);

    // Delete the current node
    delete root;
}

inline void TreeDeletionProcess(BallTree* &tree, vector<Point*>& universalDataPoints) {
    deleteTree(tree->root);
    delete tree;

    for (Point* p : universalDataPoints) {
        delete p;
    }
}

void codeRunner() {

    /* Dataset Initialization Process. */

    cout << "\033[32:40m--> Initialising Dataset.\033[0m" << endl;
    vector<Point*> universalDataPoints;
    FileParsingProcess(DATASET_IN_USE, universalDataPoints);

    /*****************************************************************/

    /* Tree Construction Process. */
    BallTree* tree = NULL;
    TreeConstructionProcess(tree, universalDataPoints);

    /*****************************************************************/

    /* compute total leaf volume */
    VolumeComputationProcess(tree);

    /*****************************************************************/

    /* Range Queries */
    RangeQueryProcess(tree);
    
    /*****************************************************************/

    /* Naive KNN Search */
    NaiveKNNProcess(tree);
    
    /*****************************************************************/

    /* KNN Search */
    KNNProcess(tree, universalDataPoints);
    
    /*****************************************************************/

    /* ANY MISCELLANEOUS PROCESSES */
    
    /*****************************************************************/

    /* Free all allocated memory. */
    TreeDeletionProcess(tree, universalDataPoints);
}

int main()
{
    auto glb_time_start = chrono::high_resolution_clock::now();
#ifdef _WIN32
    system("cls");
#elif __linux__
    system("clear");
#elif __APPLE__
    system("cls");
#endif
    cout << "A PROJECT ON BALL TREES AND KNN." << endl;
    cout << "By Faheem Arif, Aryan Bodhe, Ravirala Aditya, Tanmay Banjari." << endl;
    cout << "--------------------------------------------------------" << endl;
    
    codeRunner();
    cout << "\033[32:40m--> Program Termination Successful.\033[0m" << endl;
    auto glb_time_end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = glb_time_end - glb_time_start;
    cout << "\033[34:40m    --> Total time elapsed : " << elapsed.count() << " seconds.\033[0m"<< endl;
    cout << "--------------------------------------------------------\n" << endl;
}