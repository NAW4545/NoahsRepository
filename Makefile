CC=g++
FLAGS = -std=c++11 -Wall -Wextra -Werror -Wfatal-errors -Wpedantic -ggdb3 -Og
# uncomment for Linux/Mac OS X
RM = rm -f

# uncomment for Windows (make sure MinGW/MSYS are installed!)
#RM = del

# compile and
# links: takes seperate object files and links them into a single executable (doughnaughts.exe)
userFormDriver.exe: userForm userFormDriver CinReader
	$(CC) $(FLAGS) userForm.o userFormDriver.o CinReader.o -o userFormDriver.exe

userFormDriver:
	$(CC) $(FLAGS) -c userFormDriver.cpp -o userFormDriver.o

# If these have changed, rebuild
# -c means compile only switch
userForm:
	$(CC) $(FLAGS) -c userForm.cpp -o userForm.o

CinReader:
	$(CC) $(FLAGS) -c CinReader.cpp -o CinReader.o

# Windows cleaning
# clean:
# 	del *.o

# cleanall: clean
# 	del *.exe

# Linux Cleaning
clean:
	$(RM) *.o

cleanall: clean
	$(RM) *.exe
