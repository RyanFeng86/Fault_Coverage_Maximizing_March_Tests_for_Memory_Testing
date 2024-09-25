//Gupta Random Marchtest
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>
#include <iomanip>
#include <thread>
#include <string>
#include <cstring>
#include <cmath>
#include <limits.h>


//STL标准库
#include <iterator>
#include <algorithm>
#include <functional>
#include <deque>
#include <list>
#include <stack>
#include <queue>
#include <set>
#include <map>

#include <numeric>

using namespace std;



//Gupta Random Marchtest

enum rw{
	r0, r1, w0, w1, non
};

enum updown {
	up, down
};

enum symbol {
	emp, com
};
struct block {
	updown up_down;//0 down, 1 up, -1 none
	rw type;//
	symbol emp_com;//0 empty, 1 coma, -1 none
};

class Randommt {
public:
	Randommt(long long int a) :blocksize(a) {};
	~Randommt() {};
	long long int getBlocksize(); //return blocksize
	void clr_mar();//clear marchtest


	string getMarchtest();//return valid final marchtest


	
	void sub_gen_mar(long long int match, long long int line); //generate all marchtest, including wrong one//match=1 com, match=0 other
	long long int gen_mar();


	bool val_mar();// filter wrong marchtest get the right one

	void sort_mar();//sort marchtest into correct format

	

private:
	int blocksize;
	vector<block> marchtest;//store marchtest
	
};

long long int Randommt::getBlocksize(){
	return blocksize;
}

void Randommt::clr_mar() {
	marchtest.clear();
}

void Randommt::sub_gen_mar(long long int match, long long int line) {
	block tmp;
	if (match == 1) {
		if (line == 1) {
			tmp.emp_com = com;	
			tmp.type = non;
		}
		else {
			tmp.emp_com = emp;
			tmp.type = non;
		}			
	}
	else {
		switch (line) {
		case 0:
			tmp.up_down = up;
			tmp.type = r0;
				break;
		case 1:
			tmp.up_down = up;
			tmp.type = r1;
				break;
		case 2:
			tmp.up_down = up;
			tmp.type = w0;
				break;
		case 3:
			tmp.up_down = up;
			tmp.type = w1;
				break;
		case 4:
			tmp.up_down = down;
			tmp.type = r0;
				break;
		case 5:
			tmp.up_down = down;
			tmp.type = r1;
				break;
		case 6:
			tmp.up_down = down;
			tmp.type = w0;
				break;
		case 7:
			tmp.up_down = down;
			tmp.type = w1;
				break;
		}
	}
	marchtest.push_back(tmp);
}


string match_type(rw a) {
	string tmp = {};
	switch (a) {
	case r0:
		tmp = "r0";
		break;
	case r1:
		tmp = "r1";
		break;
	case w1:
		tmp = "w1";
		break;
	case w0:
		tmp = "w0";
		break;
	default:
		exit(-1);
	}
	return tmp;
}

string match_updown(updown a) {
	string tmp = {};
	switch (a) {
	case up:
		tmp = "up";
		break;
	case down:
		tmp = "down";
		break;
	default:
		exit(-1);
	}
	return tmp;
}

string Randommt::getMarchtest() {
	string march_final = {};
	updown previous;
	for (long long int i = 0; i < marchtest.size(); i++) {
		if (i == 0) {
			march_final += match_updown(marchtest[0].up_down);
			march_final = march_final+" "+ match_type(marchtest[0].type);
		}
		else {
			if (marchtest[i].emp_com == com) {
				march_final = march_final + ", " + match_updown(marchtest[i + 1].up_down);
				}
			else {
				march_final = march_final + " " + match_type(marchtest[i].type);
			}
		}
	}
	return march_final;
}


long long int Randommt::gen_mar() {
	static vector<long long int> type1(blocksize-1);
	static vector<long long int> type0(blocksize);
	static long long int counter = 0;
	for (long long int i = 0; i < blocksize * 2 - 1; i++) {
		if (i % 2 == 0) {
			sub_gen_mar(0, type0[i / 2]);
		}
		else {
			sub_gen_mar(1, type1[i / 2]);
		}
	}
	type0[0]++;
	for (long long int n = 0; n < blocksize - 1; n++) {
		if (type0[n] == 8) {
			type1[n]++;
			type0[n] = 0;
		}
		if(type1[n] == 2) {
			type0[n + 1]++;
			type1[n] = 0;
		}
	}
	counter++;
	return counter;
	

}

bool Randommt::val_mar() {
	if(marchtest[0].type==r0 || marchtest[0].type == r1)//第一个不为写,记错
		return false;



	for (long long int i = 1; i < marchtest.size()/2+1; i++) {
		if (marchtest[i*2].type == r0 || marchtest[i*2].type == r1) {//读的最近一次的写不同，记错   //本次为读 
			long long int tmp = i-1;
			for (tmp; tmp >= 0; tmp--) {
				if (marchtest[tmp * 2].type == w0 || marchtest[tmp * 2].type == w1) {//寻找最近的写,找到了
					if ((marchtest[i * 2].type == r0 && marchtest[tmp * 2].type == w0) ||
						(marchtest[i * 2].type == r1 && marchtest[tmp * 2].type == w1))//读写数字相同
						break;
					else
						return false;
				}
			}
		}

		if (marchtest[i * 2].up_down != marchtest[(i - 1) * 2].up_down) {//当前和前一个上下类型不同
			if (marchtest[i * 2 - 1].emp_com != 1)//中间有 “,”则 继续下一个，否则为错
				return false;
		}
	}


	return true;

}

void Randommt::sort_mar() {
	vector<block> tmp;
	for (long long int i = 0; i < marchtest.size(); i++) {//去除空的com格
		if (marchtest[i].type == non && marchtest[i].emp_com == emp)
			continue;
		else
			tmp.push_back(marchtest[i]);
	}
	marchtest.swap(tmp);
}

template <class T>
inline string toString(const T &v) {
	ostringstream os;   //创建字符串输出流
	os << v;        //将变量v的值写入字符串流
	return os.str();    //返回输出流生成的字符串
}

int main() {
	
	long long int a,n=1,m=1;
	cout << "Please input the number of Marchtest Operation:" << endl;
	cin >> a;
	long long int sign = pow(8, a)*pow(2, a - 1);
	cout << sign << endl;
	Randommt creat(a);
	string str1 = "Marchtest_"+toString(a)+".txt";
	ofstream outfile(str1);
	while (creat.gen_mar() <= sign) {
		//n++;
		
		if (creat.val_mar()) {
			string tmp;
			creat.sort_mar();
			tmp=creat.getMarchtest();
			//cout << tmp << endl;
			outfile << tmp << endl;	
			//cout << ".";
			//cout << "Total generated: " << n << "   Total Valid: " << m << endl;
			//m++;
		}
		creat.clr_mar();
	}
	outfile.close();
}

