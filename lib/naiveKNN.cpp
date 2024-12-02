#include "classes/BallTree.cpp"
#include "../util/mathematicalFunctions.cpp"

vector<pair<double, Point*>> knn_naive(BallTreeNode* &root, Point* &query, int k) {
    vector<Point*> &dataset = root->ball->containedPoints;
    vector<pair<double, Point*>> distances;
    
    for(auto pt : dataset) {
        distances.push_back({METRIC(pt,query), pt});
    }
    sort(distances.begin(), distances.end());
    return distances;
}