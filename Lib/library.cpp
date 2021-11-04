#include "library.h"
#include <string>
#include <vector>
#include <iterator>
#include <algorithm>
#include <iostream>
#include <sstream>
#include <set>
#define pb push_back

using namespace std;

double checkResult(const string& st1, const string& st2) {
    vector<string> str1;
    vector<string> str2;
    string t_st1 = st1;
    string t_st2 = st2;
    istringstream is1(t_st1);
    istringstream is2(t_st2);
    copy(istream_iterator<string>(is1), istream_iterator<string>(), back_inserter<vector<string>>(str1));
    copy(istream_iterator<string>(is2), istream_iterator<string>(), back_inserter<vector<string>>(str2));
    vector<vector<string>> vec1;
    vector<vector<string>> vec2;
    vector<vector<string>> str_union;
    vector<vector<string>> str_intersection;
    set<vector<string>> set_str_union;
    set<vector<string>> set_str_intersection;
    int size_str1 = str1.size(), size_str2 = str2.size();

    if (size_str1>=3 && size_str2>=3) {
        vec1.pb(vector<string> {str1[0]});
        vec1.pb(vector<string> {str1[0], str1[1]});
        vec2.pb(vector<string> {str2[0]});
        vec2.pb(vector<string> {str2[0], str2[1]});
        vec1.pb(vector<string> {str1[size_str1-1]});
        vec1.pb(vector<string> {str1[size_str1-1], str1[size_str1-2]});
        vec2.pb(vector<string> {str2[size_str2-1]});
        vec2.pb(vector<string> {str2[size_str2-1], str2[size_str2-2]});

        for (int i = 2; i < max(size_str1, size_str2); i++) {
            if (i<size_str1) {
                vector<string> temp = {str1[i-2], str1[i-1], str1[i]};
                vec1.pb(temp);
            }
            if (i<size_str2) {
                vector<string> temp = {str2[i-2], str2[i-1], str2[i]};
                vec2.pb(temp);
            }
        }
    } else {
        if (size_str1==1) {
            vec1.pb(vector<string> {str1[0]});
        }
        if (size_str1==2) {
            vec1.pb(vector<string> {str1[0]});
            vec1.pb(vector<string> {str1[0], str1[1]});
        }
        if (size_str2==1) {
            vec2.pb(vector<string> {str2[0]});
        }
        if (size_str2==2) {
            vec2.pb(vector<string> {str2[0]});
            vec2.pb(vector<string> {str2[0], str2[1]});
        }
    }
    sort(vec1.begin(), vec1.end());
    sort(vec2.begin(), vec2.end());
    set_union(vec1.begin(), vec1.end(), vec2.begin(), vec2.end(), back_inserter(str_union));
    set_intersection(vec1.begin(), vec1.end(), vec2.begin(), vec2.end(), back_inserter(str_intersection));
    set_str_union.insert(str_union.begin(), str_union.end());
    set_str_intersection.insert(str_intersection.begin(), str_intersection.end());
    return ((double)set_str_intersection.size()/(double)set_str_union.size());

}
