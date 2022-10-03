#                                                                      Synchroniser #
The application *Synchroniser.py* creates a copy of the working (*Source*) directory into a *Replica* directory. 
It periodically checks for changes in the *Source* directory and syncronises it in the *Replica* directory.
# How To Run
1. First create the *Source* directory/folder. The directory in which you will be creating all your files and folders.
    1. The *Source* directory can also be a directory that you are already working on.
    2. It can also be an empty directory where you wil be adding all the files.
2. Create a *Replica* directory. The directory where you want all the data to be saved.
    1. The *Replica* directory should be created new and should be empty.
    2. If a pre-exsisting directory is assigned to be a *Replica* directory, its content will be deleted and updated with *Source* directory contents
# Upon Start Up
Upon running the *Synchroniser.py* script several command line input messages pop up. Each described as below:
1. Enter the full path of the *Source* directory
2. Enter the full path of the *Replica* directory
3. Enter the full path of the *Logs.log* file without the exension *Logs.log*
    1. The name of the logging file is set to *Logs.log* by default and cannot be changed at the moment.
    2. Ex: If the full path of *Logs.log* is *C:\Users\neelg\source\repos\python\Synchroniser\Synchroniser\Logs.log* enter *C:\Users\neelg\source\repos\python\Synchroniser\Synchroniser*
4. Enter the frequency of how often you want the syncronisation between *Source* and *Replica* to happen.
    1. The input frequency should be an integer. The units are set to seconds.
    2. Ex: If you enter *20* then syncronisation first starts after *20* seconds and periodically repeats every *20* seconds
 # Dependencies
 All the imports used are internal python libraries, therefore installation of any external library is not required.
 1. It is advisable to use *Python 3.10* for stable operation as the python libraries used are from version: *3.10*
 2. The code should run on both Windows and Linux without any modifications.

