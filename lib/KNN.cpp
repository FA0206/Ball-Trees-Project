#include "classes/BallTree.cpp"
#include "../util/mathematicalFunctions.cpp"

// Modified knn_pruning function to count visited points
void knn_pruning(BallTreeNode* &root, Point* &query, int k, priority_queue<pair<double, Point*>>& knearest, int& pointsVisited);

// Function to find k-nearest neighbors
vector<Point*> findKNearestNeighbors(BallTreeNode* &root, Point* &query, const int k, int& pointsVisited) {    
    priority_queue<pair<double, Point*>> knearest;   // max heap to store nearest neighbors with distances
    Point* temp = NULL;
    knearest.emplace(DBL_MAX, temp);

    pointsVisited = 0; // Initialize the counter
    knn_pruning(root, query, k, knearest, pointsVisited);

    vector<Point*> result;   // Store the nearest neighbors (without the distance)
    while (!knearest.empty()) {
        result.push_back(knearest.top().second);    // Storing
        knearest.pop();                             // Popping
    }

    reverse(result.begin(), result.end());          // Reversing the queue
    return result;
}

// Modified knn_pruning function
void knn_pruning(BallTreeNode* &root, Point* &query, int k, priority_queue<pair<double, Point*>>& knearest, int& pointsVisited) {
    if (!root) return;

    double distanceToCenter = METRIC(query, root->ball->center);

    // Prune subtree if the distance to the boundary of the ball exceeds the greatest distance in the max_queue
    if (distanceToCenter - root->ball->radius > knearest.top().first) return;

    // Leaf node
    if (!root->left && !root->right) {     
        for (const auto& p : root->ball->containedPoints) {    
            pointsVisited++; // Increment the counter for each visited point
            double dist = METRIC(query, p);  // Calculating distance   

            // If size of queue is less than k, add the element in the queue
            if (knearest.size() < k) {
                knearest.emplace(dist, p); 
            } 
            // Else, if queue is full and distance is smaller than the largest distance, replace the top element
            else if (dist < knearest.top().first) {
                knearest.pop();
                knearest.emplace(dist, p);
            }        
        }
        return;
    }

    // Internal node: recursively search the child nodes
    knn_pruning(root->left, query, k, knearest, pointsVisited);
    knn_pruning(root->right, query, k, knearest, pointsVisited);
}
