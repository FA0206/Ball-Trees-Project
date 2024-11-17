#include <bits/stdc++.h>
#include "classes/BallTree.cpp"
#include "../util/mathematicalFunctions.cpp"
using namespace std;

// creates a ball tree from a root containing all points
void medianSplitAlgorithm(BallTreeNode* &root, const vector<Point*> &univSet) {

    // return if set size falls below threshold
    if(univSet.size() <= LEAF_POINT_COUNT_THRESHOLD) {
        return;
    }

    //compute median
    Point* median = computeMedian(univSet);

    //find farthest point from median say p1
    Point* P1 = findFarthestPoint(univSet, median).first;

    //find farthest point from p1, say p2
    Point* P2 = findFarthestPoint(univSet, P1).first;

    // delete median, no longer required
    delete median;

    //create ball around p1 and p2
    BallTreeNode* leftChild = root->left = new BallTreeNode();
    leftChild->parent = root;
    BallTreeNode* rightChild =  root->right = new BallTreeNode();
    rightChild->parent = root;

    //assign points
    for(int i = 0; i < univSet.size(); i++) {
        if(METRIC(univSet[i], P1) <= METRIC(univSet[i], P2)) {
            leftChild->ball->containedPoints.push_back(univSet[i]);
        }
        else {
            rightChild->ball->containedPoints.push_back(univSet[i]);
        }
    }
    
    //resize leftChild ball
    Point* leftChildBallMedian = computeMedian(leftChild->ball->containedPoints);
    leftChild->ball->center = leftChildBallMedian;
    leftChild->ball->radius = findFarthestPoint(leftChild->ball->containedPoints, leftChildBallMedian).second;
    
    //resize rightChild ball
    Point* rightChildBallMedian = computeMedian(rightChild->ball->containedPoints);
    rightChild->ball->center = rightChildBallMedian;
    rightChild->ball->radius = findFarthestPoint(rightChild->ball->containedPoints, rightChildBallMedian).second;

    // write the ball centers and radius to cache file
    FILE* fp = fopen(BALLS_DATA, "a");
    
    // write data for left child
    for (int i = 0; i < DIMENSION; i++) {
        fprintf(fp, "%lf,", leftChild->ball->center->coordinate[i]);
    }
    fprintf(fp, "%lf\n", leftChild->ball->radius);

    // write data for right child
    for (int i = 0; i < DIMENSION; i++)
    {
        fprintf(fp, "%lf,", rightChild->ball->center->coordinate[i]);
    }
    fprintf(fp, "%lf\n", rightChild->ball->radius);

    // close the file
    fclose(fp);

    // recursively continue the process until threshold is met
    medianSplitAlgorithm(leftChild, leftChild->ball->containedPoints);
    medianSplitAlgorithm(rightChild, rightChild->ball->containedPoints);
}

/* Construct a Ball Tree from a NULL root using the given dataset. */
BallTree* constructBallTreeUsingMedianSplit(BallTree* &ballTree, vector<Point*>& completePointSet) {
    ballTree = new BallTree();
    ballTree->root = new BallTreeNode(completePointSet);
    Point* root_center = computeMedian(completePointSet);
    ballTree->root->ball->center = root_center;
    double r = findFarthestPoint(completePointSet, root_center).second;
    ballTree->root->ball->radius = r;
    
    // open the cache file to store data
    FILE* fp = fopen("lib/cache/ball_center_and_radius.csv", "w");
    
    // place the labels
    for(int i = 0; i < DIMENSION; i++) {
        fprintf(fp, "Center%d,", i+1);
    }
    fprintf(fp, "Radius\n");

    // place the root's coordinates
    for(int i = 0; i < DIMENSION; i++) {
        fprintf(fp, "%lf,", root_center->coordinate[i]);
    }
    fprintf(fp, "%lf\n", r);

    // close the file
    fclose(fp);
    delete root_center;

    // call the median split algorithm
    medianSplitAlgorithm(ballTree->root, completePointSet);

    // rename the file to a csv
    rename("lib\\cache\\ball_center_and_radius.txt", "lib\\cache\\ball_center_and_radius.csv");

    return ballTree;
}