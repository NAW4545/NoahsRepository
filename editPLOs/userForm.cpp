
#include "userForm.h"
#include "CinReader.h"

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
      MainMenu();
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
    // if the inputted selection matches program(s), call for validation of selection
    std::function<auto(programDetails)->void> f2 = for_each(details.begin(), details.end(), [&selection,this] ( const programDetails& p) {
       if (p.prog_name == selection)  {
         this->detailsHolder.push_back(p);
         }
    });
  cout << std::left << setw(8) << setfill(' ') << "prog_id" 
       << std::left << setw(30) << setfill(' ') << "prog_name"
       << std::left << setw(8) << setfill(' ') << "degreeType\n";
  // output results
  for (unsigned int i = 0; i < detailsHolder.size(); i++) {
     cout << std::left << setw(8) << setfill(' ') << detailsHolder.at(i).prog_id
          << std::left << setw(8) << setfill(' ') << detailsHolder.at(i).prog_name
          << std::right << setw(26) << setfill(' ');
    // disply user-friednly degree types
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
  unsigned int option;
    cout << "Select the prog_id of the program PLO you wish to edit\n"
         << "Submit '0' to return to main menu\n"
         << "Enter prog_id: ";
    cin >> option;
    if (option == 0) {
      detailsHolder.clear();
      cout << endl;
      MainMenu();
    }
    else {
      std::function<auto(programDetails)->void> f2 = for_each(detailsHolder.begin(), detailsHolder.end(), [&option,this] ( const programDetails& h) {
        if (h.prog_id == option)  {
          this->detailsAppender.push_back(h);
        }
      });
      editPLO();
    }
}

void updatePLOs::editPLO() {
  cout << std::left << setw(3) << setfill(' ') << "\n#" << "Options\n"
       << std::left << setw(3) << setfill(' ') << "1" << "Remake PLO\n"
       << std::left << setw(3) << setfill(' ') << "2" << "Add to existing PLO\n"
       << std::left << setw(3) << setfill(' ') << "3" << "Main Menu\n"
       << "Enter Option: ";
    cin >> option;
  if (option == 1) {
    cout << "\nEnter all PLOs to replace existing entries\n";
      CinReader cin;
      PLO = cin.readString(false);
    detailsAppender.at(0).prog_desc = PLO;
    savePLO("userSubmittedChanges.txt");
  }
  if (option == 2) {
    cout << "\nEnter a new PLO to add to existing entries\n";
      cin >> PLO;
    detailsAppender.at(0).prog_desc += PLO;
    savePLO("userSubmittedChanges.txt");
  }
  if (option == 3) {
    detailsAppender.clear();
    detailsHolder.clear();
    MainMenu();
  }
}


void updatePLOs::pushPLO() {

}

void updatePLOs::savePLO(string filename) {
   cout << "\nThe modified program looks like: \n"
       << detailsAppender.at(0) << endl << endl;
    
  cout << std::left << setw(3) << setfill(' ') << "#" << "Options\n"
       << std::left << setw(3) << setfill(' ') << "1" << "Confirm\n"
       << std::left << setw(3) << setfill(' ') << "2" << "Edit\n"
       << std::left << setw(3) << setfill(' ') << "3" << "Main Menu\n"
       << std::left << setw(3) << setfill(' ') << "4" << "Exit\n"
       << "Enter option: ";
  cin >> option;
    switch (option) {
      case 1: {
        cout << "\nOpening" << filename << "for appending..." << endl;
        // Declare our Stream and open all at once
        ofstream fout("userSubmittedChanges.txt", std::ios::app);
          // Output/Append to move.txt
        if (fout.good()) {
          fout << "UPDATE programs" << "\n"
               << "SET prog_desc = " << "'" << detailsAppender.at(0).prog_desc << "'" << "\n"
               << "WHERE prog_name = " << detailsAppender.at(0).prog_name << "\n"
               << "AND deg_id = " << detailsAppender.at(0).deg_id << "\n"
               << "\n";
        // Close out Streams
          fout.close();
            cout << "Successfully added " << detailsAppender.at(0).prog_desc << endl << endl;
            // details.push_back(detailsAppender.at(0)); duplicate entries if filtering agan- fix later
            detailsAppender.clear();
            detailsHolder.clear();
        }
        else {
          cout << "Failed to append\n";
        }
        MainMenu();
        break;
      }
      case 2: {
        detailsAppender.clear();
        savePLO("userSubmittedChanges.txt");
        break;
      }
      case 3: {
        detailsHolder.clear();
        detailsAppender.clear();
        MainMenu();
        break;
      }
      case 4: {
        detailsAppender.clear();
        Exit();
        break;
      }
    }
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
  for (unsigned int i = 0; i < details.size(); i++) {
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
