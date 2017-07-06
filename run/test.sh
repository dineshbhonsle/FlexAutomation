#In order to execute a testcase one has to run the shell file 'test.sh' which is in 'run' folder. This shell file
#takes two arguments. One is the absolute path to the testbed file and absolute path of the robot testcase file.
#This testbed path is first set as an environment variable with name "TESTBED" which is then used by the Framework 
#for the rest of the execution.
basePath=
export TESTBED=$1
fname=$(basename $2)
test=$(echo $fname | cut -f 1 -d '.')
robot --timestampoutputs --log ${test}_Log.html --report ${test}_Report.html --loglevel DEBUG --output ${test}_Output.xml --outputdir ../results $2

