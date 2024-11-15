#include "classes/BallTree.cpp"
#include "../util/mathematicalFunctions.cpp"

// void range_nearestleaf(BallTreeNode* &root, Point* &query, double range, priority_queue<pair<double, Point*>>& knearest);
void range_query(BallTreeNode* &root, Point* &query, double range, priority_queue<pair<double, Point*>>& knearest);

vector<Point*> findrangeNeighbors(BallTreeNode* &root, Point* &query, double range) {    
    priority_queue<pair<double, Point*>> knearest;   // max heap to store nearest neighbors with distances

    // range_nearestleaf(root, query, range, knearest);
    range_query(root, query, range, knearest);
    // cout << "knn done" << endl;
    vector<Point*> result;   // store the nearest neighbours (without the distance)
    while (!knearest.empty()) {
        result.push_back(knearest.top().second);    // storing
        knearest.pop();                             // poping 
    }

    reverse(result.begin(), result.end());          // reversing the queue
    return result;
}

// void range_nearestleaf(BallTreeNode* &root, Point* &query, double range, priority_queue<pair<double, Point*>>& knearest) {
//     // null node
//     if (!root) {return;} 
//
//     // leaf node 
//     if (!root->left && !root->right) {     // check all the points inside    
//         for (const auto& p : root->ball->containedPoints) {    
//             double dist = EuclideanDistance(query, p);  // calculating distance   
//
//             // if it lies in the range, push it in the queue 
//             if (dist <= range) {knearest.emplace(dist, p);}      
//         }
//
//         return;
//     }
//    
//     // if the list is empty and internal node
//     // call child closer to query point
//     if (root->left && root->right) {
//         // computing distance to both the child centers from the query point
//         double d1 = EuclideanDistance(query, root->left->ball->center);
//         double d2 = EuclideanDistance(query, root->right->ball->center);
//
//         if (d2 < d1) {range_nearestleaf(root->right, query, range, knearest);}
//         else {range_nearestleaf(root->left, query, range, knearest);}
//     }
// }

void range_query(BallTreeNode* &root, Point* &query, double range, priority_queue<pair<double, Point*>>& knearest) {
    

    double distanceTocenter = EuclideanDistance(query, root->ball->center);
    // cout << "dist done" << endl;
    if(!root) {return;}

    // cout << "querying" << endl;
    // if the distance to the boundary of the ball exceeds the range. 
    // then prune this subtree.
    if (distanceTocenter - root->ball->radius > range) {return;}

    // leaf node 
    if (!root->left && !root->right) {     // check all the points inside    
    // cout << "leaf found" << endl;
        for (const auto& p : root->ball->containedPoints) {    
            double dist = EuclideanDistance(query, p);  // calculating distance   

            // if size of queue is less than k, add the element in the queue
            if (dist <= range) {knearest.emplace(dist, p);}    
        }
        return;
    }

    // internal node
    else {
        // recursively search the child nodes
        range_query(root->left, query, range, knearest);
        range_query(root->right, query, range, knearest);
    }
}
