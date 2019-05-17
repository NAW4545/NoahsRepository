#pragma once

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

    // Select program PLO to change
    void changePLO();
    
    // Edit PLO of selected program
    void editPLO();
    
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
    unsigned int option;
    string filter, PLO;
    // converts strings to usable datatypees
    programDetails tokenizePLO(string input);
    // holds program details
    vector<programDetails> details;
    vector<programDetails> detailsHolder;
    vector<programDetails> detailsAppender;

};