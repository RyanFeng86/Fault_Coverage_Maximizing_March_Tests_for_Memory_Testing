#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <sstream>

using namespace std;
string path1="grow_to_16.txt";
string path2="tmp.txt";
string path3="best16_.txt";


inline int fromString(const string &str){
    istringstream is(str);
    int v;
    is>>v;
    return v;
}


int main(){
    vector<int> line_name;
    ifstream input1(path2);
    string tmp={};
    while(getline(input1,tmp)){
        line_name.push_back(fromString(tmp));
    }        
    input1.close();


    ofstream output(path3);
    ifstream input2(path1);
    int n=0;
    for(int i=0;i<line_name.size();i++){
        
        
        string k={};
        while(getline(input2,k)){
            n++; 
            if(n==line_name[i]){
                output<<k<<endl;
                break;
            }
                       
        }
    }

    input2.close();
    output.close();
    return 0;

}
