#include <bits/stdc++.h>
#include "constants.cpp"
#include "lib/MedianSplitConstruction.cpp"
#include "lib/rangequeries.cpp"
#include "lib/KNN.cpp"
#include <chrono>
using namespace std;

void codeRunner() {

    /* Dataset Initialization Process. */
    cout << "--> Initialising Dataset." << endl;
    ifstream file(DATASET_IN_USE);

    /*****************************************************************/


    /* File Parsing Process. */
    vector<Point*> universalDataPoints;
    double x, y; int t;

    /* Check if file is opened successfully. */
    if(!file.is_open()) {
        cout << "--> ERROR : File Open Error!" << endl;
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
                cout << "--> ERROR : Value Parse Error." << endl;
                return;
            }
        }

        /* if the dimension of the dataset is different than what is specified. */
        if(values.size() != DIMENSION + 1) {
            cout << "--> ERROR : Inconsistent Dimension Parameter!" << endl;
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
    cout << "--> File Parsed Successfully." << endl;
    cout << "--------------------------------------------------------" << endl;


    /*****************************************************************/


    /* Tree Construction Process. */
    auto start = chrono::high_resolution_clock::now();
    BallTree* tree = NULL;
    tree = constructBallTreeUsingMedianSplit(tree, universalDataPoints);
    tree->setTreeDepths();
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end - start;

    cout << "--> Construction complete." << endl;
    cout << "    --> Construction Time (sec) = " << elapsed.count() << endl;
    cout << "    --> Max Tree Depth = " << tree->maxDepth << endl;
    cout << "    --> Average Tree Depth = " << tree->averageDepth << endl;



    /*****************************************************************/


    /* compute total leaf volume */
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
    cout << "    --> Total Volume of Ball Tree = " << totalVolume << endl;
    cout << "--------------------------------------------------------" << endl;


    /*****************************************************************/


    /* Range Queries */

    Point* query = new Point();
    int a,b;
    double r;
    char choice;
    vector<Point*> rangeNeighbors;

    cout << "\n--> Start Range Querying? (Y/N) : ";
    cin >> choice;
    if(tolower(choice) == 'n') {
        cout << "--------------------------------------------------------" << endl;
        goto knn_search;
    }
    
    while(true) {
        cout << "Enter query coordinates as space separated values (DIMENSION = " << DIMENSION << ") : ";
        double c;
        for(int i = 0; i < DIMENSION; i++) {
            cin >> c;
            query->coordinate[i] = c;
        }
        cout << "Enter Range or 0 to exit : " ;
        cin >> r;
        if(r == 0) {
            break;
        }
        rangeNeighbors = findrangeNeighbors(tree->root, query, r);

        cout << "\nQuery Results : " << endl;
        for(auto i : rangeNeighbors) {
            // cout << "(" << i->coordinate[0] << "," << i->coordinate[1] << ")" << endl;
            cout << "(";
            for(int k = 0; k < DIMENSION; k++) {
                cout << i->coordinate[k];
                if(k != DIMENSION-1) {
                    cout << ",";
                }
            }
            cout << ")" << endl;
        }

        cout << "\nContinue Range Querying? (Y/N) : ";
        cin >> choice;
        if(tolower(choice) == 'n') {
            break;
        }
    }

    delete query;

    cout << "\n--> Completed Range Query Processing." << endl;
    cout << "--------------------------------------------------------" << endl;


    /*****************************************************************/


    /* KNN Search */
knn_search:
    query = new Point();
    int neighborCount;
    vector<Point*> knn_results;

    cout << "\n--> Start KNN Querying? (Y/N) : ";
    cin >> choice;
    if(tolower(choice) == 'n') {
        cout << "--------------------------------------------------------" << endl;
        goto misc;
    }

    while(true) {
        cout << "Enter query coordinates as space separated values (DIMENSION = " << DIMENSION << ") : ";
        double c;
        for(int i = 0; i < DIMENSION; i++) {
            cin >> c;
            query->coordinate[i] = c;
        }
        cout << "Enter No of Neighbours. -1 to exit : " ;
        cin >> neighborCount;
        if(r == -1) {
            break;
        }
        knn_results = findKNearestNeighbors(tree->root, query, neighborCount);

        cout << "\nQuery Results : " << endl;
        
        int j = 0;
        for(auto res : knn_results) {
            if(++j > universalDataPoints.size()) break;
            // cout << "(" << res->coordinate[0] << "," << res->coordinate[1] << ")" << endl;
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

        cout << "\nContinue KNN Querying? (Y/N) : ";
        char choice;
        cin >> choice;
        if(tolower(choice) == 'n') {
            break;
        }
    }

    delete query;

    cout << "\n--> Completed KNN Querying." << endl;
    cout << "--------------------------------------------------------" << endl;


    /*****************************************************************/
misc:
    /* ANY MISCELLANEOUS PROCESSES */


    /*****************************************************************/


    /* Loaded Points Deletion Process. */
    for (Point* p : universalDataPoints) {
        delete p;
    }
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
    cout << "--> Program Termination Successful." << endl;
    auto glb_time_end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = glb_time_end - glb_time_start;
    cout << "--> Total time elapsed : " << elapsed.count() << " seconds."<< endl;
    cout << "--------------------------------------------------------\n" << endl;
}