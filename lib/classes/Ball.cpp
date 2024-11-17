#ifndef BL
#define BL

#include <bits/stdc++.h>
#include "Point.cpp"
using namespace std;

class Ball {
public:
    vector<Point*> containedPoints;
    double radius;
    Point* center;

    Ball() {}

    Ball(vector<Point*> pointSet) {
        containedPoints = pointSet;
    }

    Ball(Point* center, double radius) {
        this->center = center;
        this->radius = radius;
    }
};

#endif