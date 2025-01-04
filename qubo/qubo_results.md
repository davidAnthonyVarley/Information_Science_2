N = 2
Constraints satisfied:  0 / 7
Success ratio:  0.0%
Time elasped for n = 2:
3.1296825408935547 seconds



//////////////////////////////////////////////////////////

N = 3
Printing matrix:
   1 2 3
1 4 5 3
2 4 6 5
3 3 5 5

#########################

m: 15
n: 3
n**2: 9
n**4: 81
----- All Rows = m -----
if ( 12  !=  15 )
if ( 15  !=  15 )
if ( 13  !=  15 )
----
Errors: 2
#############
----- All Columns = m -----
if ( 11  !=  15 )
if ( 16  !=  15 )
if ( 13  !=  15 )
----
Errors: 3
#############
----- Both diagonals = m -----
if ( 15  !=  15 )
if ( 12  !=  15 )
----
diag_errors: 1
#############
----- All different -----
correct_sum: 45
ms_sum: 40
regular_difference: 5

squared_correct_sum: 285
squared_ms_sum: 186
squared_difference: 99
if ( 5  !=  0 )
or
if ( 99  !=  0 )
Not all different
#######################
*************
Constraints satisfied:  2 / 9
Success ratio:  22.22222222222222%
Time elasped for n = 3: 89.62905287742615 seconds