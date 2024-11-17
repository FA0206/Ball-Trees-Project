#ifndef BLT
#define BLT

#include <bits/stdc++.h>
#include "BallTreeNode.cpp"
using namespace std;

class BallTree {
public:
    BallTreeNode* root;
    int maxDepth;
    double averageDepth;

    BallTree() {
        root = NULL;
        maxDepth = 0;
        averageDepth = 0.0f;
    }

    void setTreeDepths() {
        int i = 0;
        setDepth(this->root, this->maxDepth);
        setAverageDepth(root, 0, i);
    }

private:
    void setAverageDepth(BallTreeNode* &root, int dep, int& i) {
        if(root == NULL) {
            averageDepth = ((averageDepth * i) + dep-1) / ++i;
            return;
        }

        setAverageDepth(root->left, dep+1, i);
        setAverageDepth(root->right, dep+1, i);
    }

    void setDepth(BallTreeNode* &root, int dep) {
        if(root == NULL) {
            if(dep > this->maxDepth) {
                this->maxDepth = dep-1;
            }
            return;
        }
        setDepth(root->left, dep+1);
        setDepth(root->right, dep+1);
    }
};

#endif