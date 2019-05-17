/*
Objective: 
            *UI to fill out a form to update PLOs
            *Minimze user error by 2-step verification (user/admin)
            *User can review the data prior to submission to admin
            *Admin can review chanes before pushin to live database
            *Changes to DB are independently saved 
            *Saved changes should be able to be re-integratd on demand
*/


#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <fstream>
#include <sstream>
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
    outs << std::left << setw(3) << setfill(' ') << pd.prog_id
         << std::left << setw(15) << setfill(' ')  << pd.prog_name
         << std::left << setw(50) << setfill(' ') << pd.prog_desc
         << std::left << setw(3) << setfill(' ') << pd.deg_id
         << std::left << setw(3) << setfill(' ') << pd.sp_id;
    return outs;
  }
};

class updatePLOs {

  public:

    // Task Interface
    void MainMenu();

    // Add, Edit, Remove PLOs of a program
    void changePLO();

    // Push Changes to Main Database
    void pushPLO();

    // Save user-created modifications
    // Seperate from Database so data isn't lost when sloscraper is re-executed
    // Should be able to push changes to main DB on demand streamlessly
    void savePLO(string filename);

    // loads file for change
    bool loadPLO(string filename);

    // output PLOs
    string output(vector<programDetails> details);
    
    // Exit - non-commited changes discarded
    void Exit();

  private:
    string filename;
    int option;
    // converts strings to usable datatypees
    programDetails tokenizePLO(string input);
    // holds program details
    vector<programDetails> details;
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
      break;
    }
    case 5: {
     // cout << output(details);
      break;
    }
    case 6: {
      Exit();
      break;
    }
  }
}

void updatePLOs::changePLO() {

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
    return true;
  }
  cout << filename << " was not loaded!";
  return false;
}

string output(vector<programDetails> details) {


  return "";
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
