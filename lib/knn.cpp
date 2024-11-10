// *************************************************************
// TWO STRUCTS have been defined in the comments below, do look at them carefully!!!!!!
// **************************************************************

// // Define a point in N-dimensional space
// struct Point {
//     vector<double> coords;
    
//     Point(int dim) : coords(dim) {} // constructor initializes a Point with dim dimensions, 
//     // creating a vector coords with dim elements, each set to zero

//     double distanceTo(const Point &other) const {   // calculating euclidean distance
//         double dist = 0.0;
//         for (int i = 0; i < coords.size(); ++i) {
//             dist += pow(coords[i] - other.coords[i], 2);
//         }
//         return sqrt(dist);
//     }
// };


// struct BallTreeNode {
//     Point center;   
//     double radius;  
//     vector<Point> points;
//     BallTreeNode *left, *right;

//     BallTreeNode(const Point &c, double r) : center(c), radius(r), left(nullptr), right(nullptr) {}
// };



// helping function to return the nearest neighbours
// input: root of the tree, query point, k (no. of neighbours)
vector<Point> findKNearestNeighbors(BallTreeNode *root, const Point &query, int k) {    
    priority_queue<pair<double, Point>> knearest;   // max heap to store nearest neighbors with distances

    knn(root, query, k, knearest);

    vector<Point> result;   // store the nearest neighbours (without the distance)
    while (!knearest.empty()) {
        result.push_back(knearest.top().second);    // storing
        knearest.pop();                             // poping 
    }

    reverse(result.begin(), result.end());          // reversing the queue
    return result;
}



void knn(BallTreeNode *root, const Point &query, int k, priority_queue<pair<double, Point>>& knearest) {
    // null node
    if (!root) {return;}    

    // if the list is empty and internal node
    // call child closer to query point
    if (knearest.empty() && root->left && root->right) {
        double d1 = query.distanceTo(root->left->center);
        double d2 = query.distanceTo(root->right->center);
        if (d2 < d1) {knn(root->right, query, k, knearest);}
        else {knn(root->left, query, k, knearest);}
    }

    double distTocenter = query.distanceTo(root->center);

    // Checks if list is empty or  
    // if the distance to the boundary of the ball exceeds the greatest distance in the max_queue. 
    // In either case, prune this subtree.
    if (!knearest.empty() && distTocenter - root->radius > knearest.top().first) {return;}


    // leaf node 
    if (!root->left && !root->right) {     // check all the points inside    
        for (const auto& p : root->points) {    
            double dist = query.distanceTo(p);  // calculating distance   

            // if size of queue is less than k, add the element in the queue
            if (knearest.size() < k) {knearest.emplace(dist, p);} 
            
            // else if queue is full && distance is smaller than the largest distance, 
            // pop the top element and place 'dist, p' inside the queue
            else if (dist < knearest.top().first) {
                knearest.pop();
                knearest.emplace(dist, p);
            }        
        }
    }

    // internal node
    else {
        // recursively search the child nodes
        knn(root->left, query, k, knearest);
        knn(root->right, query, k, knearest);
    }
}


