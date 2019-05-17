/*

Objective: 
            *UI to fill out a form to update PLOs
            *Minimize user error by 2-step verification (user/admin)
            *User can review the data prior to submission to admin
            *Admin can review chanes before pushin to live database
            *Changes to DB are independently saved as an SQL statement
            *Saved changes should be able to be re-integratd on demand
*/
#include "userForm.h"

int main(int argc, char* argv[]) {
  if (argc == 2) {
    cout << "Attempting to process " << argv[1] << "..." << endl;
    for (int i = 0; i < argc; i++) {
      cout << i << " : " << argv[i] << endl;
    }
      
    updatePLOs pd;
    pd.loadPLO("programs.csv");
    pd.MainMenu();
    
  } 
  else {
    cout << "Usage: "  << argv[0] << " FILENAME" << endl
         << "Make sure the file is exported from current Database.\n"
         << "See User_Guide on accessing database instructions.\n";
  }

}
