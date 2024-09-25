#include <iostream>
#include <stdio.h>
#include <string.h>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>
#include <iomanip>


#include <cstring>
#include <cmath>
#include <limits.h>
#include <sys/time.h>

//#include <ctime>


#include <iterator>
#include <algorithm>
#include <functional>
#include <deque>
#include <list>
#include <stack>
#include <queue>
#include <set>
#include <map>
#include <thread>
#include <numeric>




using namespace std;



//Gupta Random Insert





string path = "./best/best16_.txt";



template <class T>
inline string toString(const T &v) {

	ostringstream os;

	os << v;

	return os.str();

}



enum rw {

	r0, r1, w0, w1, nonop

};



enum updown {

	up, down, nonarr

};



enum symbol {

	emp, com, noncom

};



struct block {

	rw type;//

	updown up_down;//0 down, 1 up, 2 none

	symbol emp_com;//0 empty, 1 coma, 2 none

};



class Insert {

public:

	Insert() {

		com_ele.emp_com = com;

		com_ele.type = nonop;

		com_ele.up_down = nonarr;

	}

	~Insert() {}

	void readfile();//read from the best file and store the marchtest in the marchtest_init

	void insert_element();

	
	void comma_core(vector<int> &a, vector<int> &b, int l, int m, int M);
	void comma_();

	void gen_file();

	void insert_comma(int times);

	void filter1();

	void add_arrow();

		

	void writefile1(int x);

	int get_element_size(){
		return marchtest_insert_elment.size();
	}
	

	//void reset();

private:

	vector<vector<block> > marchtest_init;

	vector<vector<block> > marchtest_insert_elment;

	vector<vector<block> > marchtest_insert_comma;

	vector<vector<block> > marchtest_insert_arr;

	vector<vector<block> > marchtest_valid;

	vector<string> pre_mar;

	vector<int> comma;

	block element[4];

	block com_ele;

	string filename;

	vector<vector<int> > comma_location;//store all possible insert comma location

};








//read from the best file and store the marchtest in the marchtest_init
void Insert::readfile() {

	ifstream input(path);

	string read_str;

	vector<string> store;

	vector<int> comma_tmp;



	while (getline(input, read_str)) {

		string tmp = {};

		int symbol = 0;



		for (int i = 0; i < read_str.size(); i++) {//store the operations into tmp

			if ((read_str[i] == 'w' && (read_str[i + 1] == '0' || read_str[i + 1] == '1'))

				|| (read_str[i] == 'r' && (read_str[i + 1] == '0' || read_str[i + 1] == '1'))) {

				tmp.push_back(read_str[i]);

				tmp.push_back(read_str[i + 1]);

				i += 1;

			}



		}



		for (int i = 0; i < read_str.size(); i++) {//store the number of comma into comma_tmp

			if (read_str[i] == ',')

				symbol += 1;

		}



		store.push_back(tmp);

		comma_tmp.push_back(symbol);//original comma number

		comma_tmp.push_back(symbol + 1);//there is a chance that one more comma exist



	}

	for (int i = 0; i < store.size(); i++) {//store the distinguish operation sequence into pre_mar

		if (pre_mar.size() == 0)

			pre_mar.push_back(store[i]);

		else {

			for (int j = 0; j < pre_mar.size(); j++) {

				if (j == pre_mar.size() - 1 && store[i] != pre_mar[j])

					pre_mar.push_back(store[i]);

				else if (store[i] == pre_mar[j])

					break;

			}

		}

	}



	for (int i = 0; i < comma_tmp.size(); i++) {//store the distinguish comma number into pre_mar

		if (comma.size() == 0)

			comma.push_back(comma_tmp[i]);

		else {

			for (int j = 0; j < comma.size(); j++) {

				if (j == comma.size() - 1 && comma_tmp[i] != comma[j])

					comma.push_back(comma_tmp[i]);

				else if (comma_tmp[i] == comma[j])

					break;

			}

		}

	}







	for (int i = 0; i < 4; i++) {//initial elements

		element[i].emp_com = noncom;

		element[i].up_down = nonarr;

		element[i].type = static_cast<rw>(i);

	}



	block tmp;

	for (int i = 0; i < pre_mar.size(); i++) {//go through all pre_march	

		vector<block> marchtmp;

		for (int j = 0; j < pre_mar[i].size(); j++) {//use one pre_march generate marchtest, add data structure into it

			tmp.emp_com = noncom;

			tmp.up_down = nonarr;

			if (pre_mar[i][j] == 'w' && pre_mar[i][j + 1] == '0') {

				tmp.type = w0;

			}

			if (pre_mar[i][j] == 'w' && pre_mar[i][j + 1] == '1') {

				tmp.type = w1;

			}

			if (pre_mar[i][j] == 'r' && pre_mar[i][j + 1] == '0') {

				tmp.type = r0;

			}

			if (pre_mar[i][j] == 'r' && pre_mar[i][j + 1] == '1') {

				tmp.type = r1;

			}

			j++;

			marchtmp.push_back(tmp);

		}

		marchtest_init.push_back(marchtmp);

	}



	input.close();



}

//use init insert one element, and retain all valid march bone
void Insert::insert_element() {

	//insert element
	cout<<"Start insert one operation..."<<endl;
	for (int i = 0; i < marchtest_init.size(); i++) {

		for (int j = 0; j < marchtest_init[i].size() + 1; j++) {

			for (int m = 0; m < 4; m++) {

				vector<block> tmp(marchtest_init[i]);

				tmp.insert(tmp.begin() + j, element[m]);

				marchtest_insert_elment.push_back(tmp);



			}

		}

	}

	for(int i=0;i<marchtest_insert_elment.size();i++){
		for(int j=0;j<marchtest_insert_elment[i].size();j++){
			if (marchtest_insert_elment[i][j].type == w0)
				cout << " w0";
			if (marchtest_insert_elment[i][j].type == w1)
				cout << " w1";
			if (marchtest_insert_elment[i][j].type == r0)
				cout << " r0";
			if (marchtest_insert_elment[i][j].type == r1)
				cout << " r1";
		}
		cout<<endl;
	}
	cout<<endl;




	//delete r0 r1, and w0 r1 or w1 r0
	vector<vector<block> > tmp_bone;
	vector<vector<block> > tmp_empty;
	for(int i=0;i<marchtest_insert_elment.size();i++){
		if(marchtest_insert_elment[i][0].type==r0 || marchtest_insert_elment[i][0].type==r1)  //the first element is read
			continue;
		else{
			int sign_break;
			for(int j=0;j<marchtest_insert_elment[i].size();j++){
				sign_break=0;
				if (marchtest_insert_elment[i][j].type == r0 || marchtest_insert_elment[i][j].type == r1) {// current is read option
					for (int find = j - 1; find >= 0; find--) {//find the neareast write option
						if (marchtest_insert_elment[i][find].type == w0 || marchtest_insert_elment[i][find].type == w1) { //find
							if ((marchtest_insert_elment[i][find].type == w0 && marchtest_insert_elment[i][j].type == r0) ||  //does match, break without error
								(marchtest_insert_elment[i][find].type == w1 && marchtest_insert_elment[i][j].type == r1)) {
								sign_break = 0;
								break;
							}
							else {											//doesn't match, break with error
								sign_break = 1;
								break;
							}
						}
					}
					if (sign_break == 1)       //if with error, break j
						break;
				}
			}
			if(sign_break==0)
				tmp_bone.push_back(marchtest_insert_elment[i]);
		}
			
	}	
	marchtest_insert_elment.swap(tmp_empty);
	for(int i=0;i<tmp_bone.size();i++)
		marchtest_insert_elment.push_back(tmp_bone[i]);	
	tmp_bone.swap(tmp_empty);

	for(int i=0;i<marchtest_insert_elment.size();i++){
		for(int j=0;j<marchtest_insert_elment[i].size();j++){
			if (marchtest_insert_elment[i][j].type == w0)
				cout << " w0";
			if (marchtest_insert_elment[i][j].type == w1)
				cout << " w1";
			if (marchtest_insert_elment[i][j].type == r0)
				cout << " r0";
			if (marchtest_insert_elment[i][j].type == r1)
				cout << " r1";
		}
		cout<<endl;
	}
	cout<<endl;






	//delete duplicate bone-operation in element
	vector<vector<block> > identical;
	for (int i = 0; i < marchtest_insert_elment.size(); i++) {
		if(i==0)
			identical.push_back(marchtest_insert_elment[i]);
		else{
			int push=0;			
			for(int j=0;j<identical.size();j++){				
				for(int m=0;m<identical[j].size();m++){
					if(identical[j][m].type!=marchtest_insert_elment[i][m].type){	
						push=1;					
						break;
					}
					else{
						if(m==identical[j].size()-1){
							push=0;
							break;
						}
					}

				}
				if(push==0)
					break;
			}
			if(push==1)
				identical.push_back(marchtest_insert_elment[i]);
		}
	}

	marchtest_insert_elment.erase(marchtest_insert_elment.begin(),marchtest_insert_elment.begin()+marchtest_insert_elment.size());
	for(int i=0;i<identical.size();i++)
		marchtest_insert_elment.push_back(identical[i]);	
	identical.swap(tmp_empty);


	
	for(int i=0;i<marchtest_insert_elment.size();i++){
		for(int j=0;j<marchtest_insert_elment[i].size();j++){
			if (marchtest_insert_elment[i][j].type == w0)
				cout << " w0";
			if (marchtest_insert_elment[i][j].type == w1)
				cout << " w1";
			if (marchtest_insert_elment[i][j].type == r0)
				cout << " r0";
			if (marchtest_insert_elment[i][j].type == r1)
				cout << " r1";
		}
		cout<<endl;
	}
	cout<<endl;
	
	


	cout<<"All identical march_bone has been generated."<<endl;

}


//store all possible comma insert location into comma_location vector
void Insert::comma_core(vector<int> &a, vector<int> &b, int l, int m, int M){//a->n; b store result; left location initial to 0; M-> m; m inital to M  
	int N = a.size();
	vector<int> tmp;
	if (m == 0) {
		for (auto i : b){
			cout << i << ' ';
			tmp.push_back(i);
		}
		cout << endl;
		comma_location.push_back(tmp);
		return;
	}
	for (int i = l; i < N; i++){
		b[M-m] = a[i];
		comma_core(a, b,i+1,m - 1,M);
	}
}

void Insert::comma_(){
	cout<<"start finding comma insert location..."<<endl;
	int element_size=marchtest_insert_elment[0].size();
	vector<int> tmp;//store all location. If there are 3 elements, then location 1,2 can insert comma
	for(int i=1;i<element_size;i++)
		tmp.push_back(i);

	
	for (int i=0;i<comma[i];i++){
		vector<int> tmp_location(comma[i]);
		comma_core(tmp,tmp_location,0,comma[i],comma[i]);
	}
	cout<<"All locations have found"<<endl;
}

void Insert::gen_file(){
	cout<<"Start insert up and down, and write to file"<<endl;
	string name="grow_to_"+toString(marchtest_insert_elment[0].size())+".txt";
	ofstream output(name);
	for(int i=0;i<marchtest_insert_elment.size();i++){//go through all inserted march bone		
		for(int j=0;j<comma_location.size();j++){//go throuth all input comma location
			vector<block> tmp_comma(marchtest_insert_elment[i]);
			for(int k=0;k<comma_location[j].size();k++){//go through each 
				tmp_comma[comma_location[j][k]].emp_com=com; //insert comma
			}

			//insert up and down
			//initial insert up and down needed variables
			vector<int> adder;  //counter function,, determine up or down arrow. 0 up, 1 down
			vector<int> local;  //record the operation location that needs add arrow
			adder.push_back(0);
			adder.push_back(0);//reserve one extra bit to prevent overflow
			local.push_back(0);
			
			for (int l = 0; l < tmp_comma.size(); l++) {
				if (tmp_comma[l].emp_com == com) {
					local.push_back(l);
					adder.push_back(0);
				}
			}

			for (int m = 0; m < pow(2, local.size()-1); m++) {   //if there are 3 arrows need to insert, then 2^3 cases exist 
				vector<block> tmp_updown(tmp_comma);
				for (int n = 0; n < local.size(); n++) {
					if (adder[n] == 0) {
						tmp_updown[local[n]].up_down = up;
					}
					else {
						tmp_updown[local[n]].up_down = down;
					}
				}
				adder[0] ++;
				for (int p = 0; p < adder.size(); p++) {
					if (adder[p] == 2) {
						adder[p] = 0;
						adder[p + 1]++;
					}
				}

				//marchtest_insert_arr.push_back(tmp);
				
				for (int q = 0; q < tmp_updown.size(); q++) {
					if (tmp_updown[q].emp_com == com)
						output << ", ";
					if (tmp_updown[q].up_down == up)
						output << "up";
					if (tmp_updown[q].up_down == down)
						output << "down";					
					if (tmp_updown[q].type == w0)
						output << " w0";
					if (tmp_updown[q].type == w1)
						output << " w1";
					if (tmp_updown[q].type == r0)
						output << " r0";
					if (tmp_updown[q].type == r1)
						output << " r1";
				}
				output << endl;				
			}
		}
	}
	output.close();
	cout<<"File has been write. Done!"<<endl;
}

void Insert::insert_comma(int times){
	cout<<"Insert comma to the "<<times<<"th march_bone..."<<endl;
	int min_com = comma[0], max_com = comma[0];
	for (int i = 0; i < comma.size(); i++) {

		if (comma[i] < min_com)

			min_com = comma[i];

		if (comma[i] > max_com)

			max_com = comma[i];

	}
	vector<int> sign;
	sign.push_back(0);



	for (int k = 0; k < max_com; k++) {

		if (k == 0) {

			

			for (int m = 1; m < marchtest_insert_elment[times].size(); m++) {//insert one comma

				vector<block> tmp(marchtest_insert_elment[times]);

				tmp.insert(tmp.begin() + m, com_ele);

				marchtest_insert_comma.push_back(tmp);

			}

			

			sign.push_back(marchtest_insert_comma.size());

		}

		else {

			for (int j = sign[k - 1]; j < sign[k]; j++) {//insert two comma

				for (int m = 1; m < marchtest_insert_comma[j].size(); m++) {

					vector<block> tmp(marchtest_insert_comma[j]);

					tmp.insert(tmp.begin() + m, com_ele);

					marchtest_insert_comma.push_back(tmp);

				}

			}

			sign.push_back(marchtest_insert_comma.size());

		}

	}

	for (int j = 0; j < sign.size(); j++)
		cout << sign[j] << " ";

	cout<<endl;

	marchtest_insert_comma.erase(marchtest_insert_comma.begin(), marchtest_insert_comma.begin() + sign[min_com - 1]);

	cout<<"Insert comma to the "<<times<<"th march_bone has finished."<<endl;

	
}

void Insert::filter1() {
	cout<<"Start eliminate illegale March Tests..."<<endl;
	int sign = marchtest_insert_comma.size();



	for (int i = 0; i < sign; i++) {

		for (int j = 0; j < marchtest_insert_comma[i].size(); j++) {

			if ((j == 0 && (marchtest_insert_comma[i][j].type == r0 || marchtest_insert_comma[i][j].type == r1)) //#1 first element is read or #2 two consistence comma, then elimilate

				|| (marchtest_insert_comma[i][j].emp_com == com && marchtest_insert_comma[i][j - 1].emp_com == com))

				break;



			int sign_break = 0;

			if (marchtest_insert_comma[i][j].type == r0 || marchtest_insert_comma[i][j].type == r1) {//#3 current is read option

				for (int find = j - 1; find >= 0; find--) {//find the neareast write option

					if (marchtest_insert_comma[i][find].type == w0 || marchtest_insert_comma[i][find].type == w1) { //find

						if ((marchtest_insert_comma[i][find].type == w0 && marchtest_insert_comma[i][j].type == r0) ||  //does match, break without error

							(marchtest_insert_comma[i][find].type == w1 && marchtest_insert_comma[i][j].type == r1)) {

							sign_break = 0;

							break;

						}

						else {												//doesn't match, break with error

							sign_break = 1;

							break;

						}



					}

				}



				if (sign_break == 1)       //if with error, break j

					break;

			}





			if (j == marchtest_insert_comma[i].size() - 1)

				marchtest_insert_comma.push_back(marchtest_insert_comma[i]);



		}

	}

	marchtest_insert_comma.erase(marchtest_insert_comma.begin(), marchtest_insert_comma.begin() + sign);


	cout<<"Illegale March Tests have been eliminated."<<endl;












}

void Insert::add_arrow() {
	cout<<"Start adding up and down..."<<endl;
	for (int i = 0; i < marchtest_insert_comma.size(); i++) {

		vector<int> adder;  //counter function,, determine up or down arrow. 0 up, 1 down

		vector<int> local;  //record the operation location that needs add arrow

		adder.push_back(0);

		adder.push_back(0);//reserve one extra bit to prevent overflow

		local.push_back(0);

		for (int j = 0; j < marchtest_insert_comma[i].size(); j++) {

			if (marchtest_insert_comma[i][j].emp_com == com) {

				local.push_back(j + 1);

				adder.push_back(0);

			}

		}

		for (int m = 0; m < pow(2, local.size()-1); m++) {   //if there are 3 arrows need to insert, then 2^3 cases exist 

			vector<block> tmp(marchtest_insert_comma[i]);

			for (int n = 0; n < local.size(); n++) {

				if (adder[n] == 0) {

					tmp[local[n]].up_down = up;

				}

				else {

					tmp[local[n]].up_down = down;

				}

			}

			marchtest_insert_arr.push_back(tmp);



			adder[0] ++;

			for (int k = 0; k < adder.size(); k++) {

				if (adder[k] == 2) {

					adder[k] = 0;

					adder[k + 1]++;

				}

			}

		}

	}



	vector<vector<block> >tmp;

	marchtest_insert_comma.swap(tmp);
	cout<<"Up and Down have been added."<<endl;
}

void Insert::writefile1(int x) {
	cout<<"Start writting all march test to file..."<<endl;
	ofstream output("tmp.txt");

	for (int i = 0; i < marchtest_insert_arr.size(); i++) {

		for (int j = 0; j < marchtest_insert_arr[i].size(); j++) {

			if (marchtest_insert_arr[i][j].up_down == up)

				output << "up";

			if (marchtest_insert_arr[i][j].up_down == down)

				output << "down";



			if (marchtest_insert_arr[i][j].emp_com == com)

				output << ", ";



			if (marchtest_insert_arr[i][j].type == w0)

				output << " w0";



			if (marchtest_insert_arr[i][j].type == w1)

				output << " w1";



			if (marchtest_insert_arr[i][j].type == r0)

				output << " r0";



			if (marchtest_insert_arr[i][j].type == r1)

				output << " r1";

		}

		output << endl;

	}

	output.close();


	cout<<"Start eliminat duplicate March Test, and replace the file..."<<endl;

	string system_s="cat tmp.txt | sort | uniq > "+toString(x)+".txt";
	char *kkk=(char *)system_s.c_str();
	system(kkk);
	

	vector<vector<block> >tmp;
	marchtest_insert_arr.swap(tmp);

	cout<<"Identical March Test is stored in file."<<endl;

}

int main() {

	

	Insert ak;

	cout << "Start reading seed..." << endl;

	ak.readfile();

	cout << "Seed is read." << endl;

	ak.insert_element();
	ak.comma_();
	ak.gen_file();
	
	return 0;


}









