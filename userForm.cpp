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
  friend ostream& operator<< (ostream& outs, const litskiDetails& pd) {
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
    string output(vector<programDetails> formula);

  private:
    // converts strings to usable datatypees
    programDetails tokenizePLO(string input);
    // holds program details
    vector<programDetails> details;
}

int main() {
  updatePLOs pd;
  pd.loadPLO("userSubmittedChanges.txt");
  pd.MainMenu();
}


void updatePLOs::MainMenu() {
  cout << "Welcome to our PLO editor";

}

void updatePLOs::changePLO() {

}

void updatePLOs::pushPLO() {

}

void updatePLOs::savePLO(string filename) {

}

bool updatePLOs::loadPLO(string filename) {

  return false;
}

string output(vector<programDetails> formula) {


  return "";
}

programDetails updatePLOs::tokenizePLO(string input) {
  programDetails pd;

  return pd;
}
