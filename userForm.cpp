/*
Objective: 
            *UI to fill out a form to update PLOs
            *Minimze user error by 2-step verification (user/admin)
            *User can review the data prior to submission to admin
            *Admin can review chanes before pushin to live database
            *Changes to DB are independently saved 
            *Saved changes should be able to be re-integratd on demand
*/

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <iterator>
#include <functional>
using std::vector;
using std::cout;
using std::cin;
using std::endl;
using std::string;
using std::setw;
using std::setfill;
using std::ifstream;
using std::ofstream;
using std::getline;
using std::istringstream;
using std::stringstream;
using std::ostringstream;
using std::stringstream;
using std::ostream;
using std::for_each;

struct programDetails {
  unsigned int prog_id;
  string prog_name;
  string prog_desc;
  unsigned int deg_id;
  unsigned int sp_id;

  programDetails() {
    prog_id = 0;
    prog_name = "Example Program";
    prog_desc = "Program Description";
    deg_id = 2;
    sp_id = 737;
  }

  // Overlod operator <<
  // Allows convinient stream output of program details
  friend ostream& operator<< (ostream& outs, const programDetails& pd) {
    outs << std::left << setw(8) << setfill(' ') << pd.prog_id
         << std::left << setw(40) << setfill(' ')  << pd.prog_name
         << std::left << setw(20) << setfill(' ') << pd.prog_desc
         << std::left << setw(8) << setfill(' ') << pd.deg_id
         << std::left << setw(8) << setfill(' ') << pd.sp_id;
    return outs;
  }
};

class updatePLOs {

  public:

    // Task Interface
    void MainMenu();

    // Add, Edit, Remove PLOs of a program
    void changePLO();
    
    // Review PLO before adding
    void validateSelection();
    
    // Push Changes to Main Database
    void pushPLO();

    // Save user-created modifications
    // Seperate from Database so data isn't lost when sloscraper is re-executed
    // Should be able to push changes to main DB on demand streamlessly
    void savePLO(string filename);

    // loads file for change
    bool loadPLO(string filename);

    // output PLOs
    string output();
    
    // Exit - non-commited changes discarded
    void Exit();

  private:
    string filename;
    int option;
    string filter;
    // converts strings to usable datatypees
    programDetails tokenizePLO(string input);
    // holds program details
    vector<programDetails> details;
    vector<programDetails> detailsHolder;

};

int main() {
  updatePLOs pd;
  pd.loadPLO("programs.csv");
  pd.MainMenu();
}


void updatePLOs::MainMenu() {
  cout << "Welcome to our PLO editor\n\n";
  cout << std::left << setw(3) << setfill(' ') << "#" << "Main Menu" << endl
       << std::left << setw(3) << setfill(' ') << "1" << "Edit PLO" << endl
       << std::left << setw(3) << setfill(' ') << "2" << "Add program" << endl
       << std::left << setw(3) << setfill(' ') << "3" << "Delete program" << endl
       << std::left << setw(3) << setfill(' ') << "4" << "Load new file" << endl
       << std::left << setw(3) << setfill(' ') << "5" << "Output current file" << endl
       << std::left << setw(3) << setfill(' ') << "6" << "Exit" << endl
       << "Enter Option: ";
  cin >> option;
    switch (option) {
    case 1: {
      changePLO();
      break;
    }
    case 2: {
      // add PLO
      break;
    }
    case 3: {
      // delete PLO
      break;
    }
    case 4: {
      // load new DB file
      cout << "Enter filename: ";
        cin >> filename;
      loadPLO(filename);
      MainMenu();
      break;
    }
    case 5: {
      cout << output();
      break;
    }
    case 6: {
      Exit();
      break;
    }
  }
}

void updatePLOs::changePLO() {
  string selection;
  cout << "\nEnter the exact name of the program you wish to edit\n"
       << "Program: ";
    cin >> selection;
    cout << endl;
    // If inputed name matches an item in vending machine, call for validation of selection
    std::function<auto(programDetails)->void> f2 = for_each(details.begin(), details.end(), [&selection,this] ( const programDetails& p) {
       if (p.prog_name == selection)  {
         this->detailsHolder.push_back(p);
         }
    });
  cout << std::left << setw(8) << setfill(' ') << "prog_id" 
       << std::left << setw(30) << setfill(' ') << "prog_name"
       << std::left << setw(8) << setfill(' ') << "degreeType\n";
  for (auto i = 0; i < detailsHolder.size(); i++) {
     cout << std::left << setw(8) << setfill(' ') << detailsHolder.at(i).prog_id
          << std::left << setw(8) << setfill(' ') << detailsHolder.at(i).prog_name
          << std::right << setw(26) << setfill(' ');
    if (detailsHolder.at(i).deg_id == 3) 
      cout << "AA\n";
    else if (detailsHolder.at(i).deg_id == 41)
      cout << "AA-T\n";
    else if (detailsHolder.at(i).deg_id == 4)
      cout << "AS\n";
    else if (detailsHolder.at(i).deg_id == 6)
      cout << "AS-T\n";
  }
  validateSelection();
}

void updatePLOs::validateSelection() {
  
}


void updatePLOs::pushPLO() {

}

void updatePLOs::savePLO(string filename) {

}

bool updatePLOs::loadPLO(string filename) {
  // open file
  ifstream inputFile;
  inputFile.open(filename);
  // if open
  if(inputFile.is_open()) {
    string fileLine;
    unsigned int i = 0;
    // load fileline data into vector
    while (getline(inputFile, fileLine)) {
      // ignore comment lines with # in file
      if ( fileLine[0] != '#') {
        details.push_back(tokenizePLO(fileLine));
        i++;
      }
    } 
    inputFile.close();
    cout << filename << " was loaded\n\n";
  }
    return true;
  
  cout << filename << " was not loaded!";
  return false;
}

string updatePLOs::output() {
  // header
  cout  << std::left << setw(15) << setfill(' ') << "prog_id"
        << std::left << setw(37) << setfill(' ')  << "prog_name"
        << std::left << setw(15) << setfill(' ') << "prog_desc"
        << std::left << setw(8) << setfill(' ') << "deg_id"
        << std::left << setw(4) << setfill(' ') << "sp_id"
        << endl;
  // output
  ostringstream outs;
  for (auto i = 0; i < details.size(); i++) {
   // outs << *i << endl;
   cout << std::left << setw(8) << setfill(' ') << details.at(i).prog_id
        << std::left << setw(40) << setfill(' ')  << details.at(i).prog_name
        << std::left << setw(20) << setfill(' ') << details.at(i).prog_desc.substr(0,17) 
        << std::left << setw(8) << setfill(' ') << details.at(i).deg_id
        << std::left << setw(8) << setfill(' ') << details.at(i).sp_id
        << endl;
  }
  return outs.str(); 
}

void updatePLOs::Exit() {
  cout << "\nSuccesfully Exited Program\n";
}

programDetails updatePLOs::tokenizePLO(string input) {
  programDetails pd;  
  string convertProg_id, convertDeg_id, convertSp_id;
  istringstream ss(input);
  // convert to #
  getline(ss, convertProg_id, ';');
    stringstream ssCRN(convertProg_id); 
    ssCRN >> pd.prog_id;
    // clear string + buffer so it can be used again
    ssCRN.str("");
    ssCRN.clear();   
  getline(ss, pd.prog_name, ';');
  // convert segment into integer
  getline(ss, pd.prog_desc, ';');
  getline(ss, convertDeg_id, ';');
    ssCRN << " " << convertDeg_id;
      ssCRN >> pd.deg_id;
      ssCRN.str("");
      ssCRN.clear();
  getline(ss, convertSp_id, ';');
    ssCRN << " " << convertSp_id;
      ssCRN >> pd.sp_id;
      ssCRN.str("");
      ssCRN.clear();
  return pd;
}
