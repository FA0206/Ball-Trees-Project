#include "classes/BallTree.cpp"
#include "../util/mathematicalFunctions.cpp"

// void knn_nearestleaf(BallTreeNode* &root, Point* &query, int k, priority_queue<pair<double, Point*>>& knearest);
void knn_pruning(BallTreeNode* &root, Point* &query, int k, priority_queue<pair<double, Point*>>& knearest);

// helping function to return the nearest neighbours
// input: root of the tree, query point, k (no. of neighbours)
vector<Point*> findKNearestNeighbors(BallTreeNode* &root, Point* &query, const int k) {    
    priority_queue<pair<double, Point*>> knearest;   // max heap to store nearest neighbors with distances
    Point* temp = NULL;
    knearest.emplace(DBL_MAX, temp);

    // knn_nearestleaf(root, query, k, knearest);
    knn_pruning(root, query, k, knearest);
    // cout << "knn done" << endl;
    vector<Point*> result;   // store the nearest neighbours (without the distance)
    while (!knearest.empty()) {
        result.push_back(knearest.top().second);    // storing
        knearest.pop();                             // poping 
    }

    reverse(result.begin(), result.end());          // reversing the queue
    return result;
}


// void knn_nearestleaf(BallTreeNode* &root, Point* &query, int k, priority_queue<pair<double, Point*>>& knearest) {
//     // null node
//     if (!root) {return;} 
    
//     // leaf node 
//     if (!root->left && !root->right) {     // check all the points inside    
//         for (const auto& p : root->ball->containedPoints) {    
//             double dist = EuclideanDistance(query, p);  // calculating distance   

//             // if size of queue is less than k, add the element in the queue
//             if (knearest.size() < k) {knearest.emplace(dist, p);} 
            
//             // else if queue is full && distance is smaller than the largest distance, 
//             // pop the top element and place 'dist, p' inside the queue
//             else if (dist < knearest.top().first) {
//                 knearest.pop();
//                 knearest.emplace(dist, p);
//             }        
//         }

//         return;
//     }
    
//     // if the list is empty and internal node
//     // call child closer to query point
//     if (root->left && root->right) {
//         // computing distance to both the child centers from the query point
//         double d1 = EuclideanDistance(query, root->left->ball->center);
//         double d2 = EuclideanDistance(query, root->right->ball->center);

//         if (d2 < d1) {knn_nearestleaf(root->right, query, k, knearest);}
//         else {knn_nearestleaf(root->left, query, k, knearest);}
//     }
// }


void knn_pruning(BallTreeNode* &root, Point* &query, int k, priority_queue<pair<double, Point*>>& knearest) {
    double distanceTocenter = EuclideanDistance(query, root->ball->center);
    if(!root) {return;}

    // if the distance to the boundary of the ball exceeds the greatest distance in the max_queue. 
    // then prune this subtree.
    // note: we are assuming that the priority queue is NON_EMPTY
    if (distanceTocenter - root->ball->radius > knearest.top().first) {return;}

    // leaf node 
    if (!root->left && !root->right) {     // check all the points inside    
        for (const auto& p : root->ball->containedPoints) {    
            double dist = EuclideanDistance(query, p);  // calculating distance   

            // if size of queue is less than k, add the element in the queue
            if (knearest.size() < k) {knearest.emplace(dist, p);} 
            
            // else if queue is full && distance is smaller than the largest distance, 
            // pop the top element and place 'dist, p' inside the queue
            else if (dist < knearest.top().first) {
                knearest.pop();
                knearest.emplace(dist, p);
            }        
        }

        return;
    }

    // internal node
    else {
        // recursively search the child nodes
        knn_pruning(root->left, query, k, knearest);
        knn_pruning(root->right, query, k, knearest);
    }
}





