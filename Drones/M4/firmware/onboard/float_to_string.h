/****************************************************************************
* sprintf function
* File: float_to_string.h
* Purpose: Replacement of sprintf to change float format to string
* Project: DroneID
* Author: Martin Skriver <MaSkr@mmmi.sdu.dk> & <MaSkr09@gmail.com>
* Source copied from:
* "http://www.geeksforgeeks.org/convert-floating-point-number-string/"
* ****************************************************************************
* Log:
* Created:  2015-10-26 Martin Skriver,	File created
* Modified:	2015-11-20 Martin Skriver, 	Changed to handle negative numbers
* Modified:	2015-11-21 Martin Skriver, 	Changed change format from .5 to 0.5
* Modified:	2015-11-21 Martin Skriver, 	Changed handle negative numbers
****************************************************************************/
#ifndef FLOAT_TO_STRING_H_
#define FLOAT_TO_STRING_H_

/***************************************************************************/
/* shared functions */
void ftoa(float n, char *res, int afterpoint);

#endif /* FLOAT_TO_STRING_H_ */
