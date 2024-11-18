#ifndef PNT
#define PNT

#include <bits/stdc++.h>
#include "../../constants.cpp"
using namespace std;

class Point {
    // create an n-dimensional point in space
public:
    vector<double> coordinate;

    Point() {
        /* Plus one to accomodate for the target value. */
        coordinate.resize(DIMENSION+1);
    }

    bool operator<(const Point& other) const {
        return coordinate < other.coordinate;  // Uses lexicographical comparison
    }
};

#endif