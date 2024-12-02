#include "classes/BallTree.cpp"
#include "../util/mathematicalFunctions.cpp"

// void range_nearestleaf(BallTreeNode* &root, Point* &query, double range, priority_queue<pair<double, Point*>>& knearest);
void range_query(BallTreeNode* &root, Point* &query, double range, priority_queue<pair<double, Point*>>& knearest, int& pointsVisited);

vector<Point*> findrangeNeighbors(BallTreeNode* &root, Point* &query, double range, int& pointsVisited) {    
    priority_queue<pair<double, Point*>> knearest;   // max heap to store nearest neighbors with distances
    pointsVisited = 0; // Initialize the counter

    range_query(root, query, range, knearest, pointsVisited);

    vector<Point*> result;   // store the nearest neighbors (without the distance)
    while (!knearest.empty()) {
        result.push_back(knearest.top().second);    // storing
        knearest.pop();                             // popping 
    }

    reverse(result.begin(), result.end());          // reversing the queue
    return result;
}

void range_query(BallTreeNode* &root, Point* &query, double range, priority_queue<pair<double, Point*>>& knearest, int& pointsVisited) {
    if (!root) return;

    double distanceToCenter = METRIC(query, root->ball->center);

    // if the distance to the boundary of the ball exceeds the range, prune this subtree.
    if (distanceToCenter - root->ball->radius > range) return;

    // leaf node 
    if (!root->left && !root->right) {     
        for (const auto& p : root->ball->containedPoints) {    
            pointsVisited++; // Increment the counter for each visited point
            double dist = METRIC(query, p);  // calculating distance   

            // if the point is within the range, add it to the queue
            if (dist <= range) knearest.emplace(dist, p);    
        }
        return;
    }

    // internal node: recursively search the child nodes
    range_query(root->left, query, range, knearest, pointsVisited);
    range_query(root->right, query, range, knearest, pointsVisited);
}
