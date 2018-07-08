---
title: ROSE Project
tagline: Python Homeworks
description: A pool of Python questions for Homeworks
---

# Variables

## Names

- Create a variable with your name; call it my_name
- Create a variable with your family name; call it my_family_name
- Create a variable called my_full_name which is composed from the 2 variables my_name and my_family_name.
- Create a variable with your city name: call it my_city_name
- Create a variable msg with "My name is XXXX and I from XXXX" using the variables you created to substitute XXXX
- Print the length of msg


# Calculations

## Age in years, days, hours and minutes

Define a parameter : age
Write a program that will compute and print the following messages according to the values in the parameter:
"You are 14 years old , which is 5110 days, or 122640 hours or 7358400 minutes !!"


## ROSE total homeworks times

You are getting each python lesson X questions , each is taking you T minutes in average to complete.

  Write a program that asks you to enter a value for X and T and prints a nice line like:

  "You have to spend 20 minutes this week in doing your ROSE homework ..."


## Money

Let us say that you get 50 shekels every week; You need 6 shekels to buy a meal every day.

Write a formula:
- How much money you have saved after one month (4 weeks)
- You want to go to the football game; and you need to buy a ticket that costs 80 shekels; how many weeks you need to save for the football ticket?
- The meal prices has increased and now it costs 7 shekels; How much you saved after one month?

# Strings

## Letter

write a python code that accepts
   name
   address1
   address2
   date

  and prints :
  ```
                 <date>              For
                                   <name>
                                   <address1>

                 Dear Mr./Mrs. <name>
                 Please visit our office as soon as possible to arrange your payments.
                 We can't wait until its all done ...

                 Sincerely

                 Koogle Inc.
                 <address2>
```

## String methods

Write a program that defines a string including phrase ("xy is not yx")

1) Strips spaces and \n \t from start/end of the string
2) prints how many 'x' are in it
3) replaces xy with wz and prints it
4) prints the string in reverse order

## String slicing

Put the following value into a variable named a_long_str

abcdefghijklmnopqrstuvwxyz

- Print the 3-8 characters (remember that first one is in position 0)
- Print the last character
- Print the length of a_long_str
- Do you need to change your code in b) if the string value is only abcde ? if yes, think of a better solution to b)


# If Statements

## Age : older, younger or same

Define two parameters: my_age, your_age.
Write a program that will print the following messages according to the values in the parameters:
- "You are older than me!!"
- "You are younger than me!!"
- "We are the same age!!"


## Even or odd

Use raw_input to get a number. Print "Even" if the number is even (divided by 2 without reminder) and "Odd" if the number is not even.

Hint:
a = 22
a % 2 == 0   #(Even!!)
True


## Less of Greater 1000

Write a program that accepts a number X from the user and prints:

- if the number is greater than 1000 : "The number is greater than 1000"
- otherwise the program prints: "The number is less than 1000"


## Grade from number to letter
Write a python code that asks for input:
"What grade did you get in the last math exam ?"
Your code should print the grade as a letter, for example:
"95 is a A"
"28 is a F"
The rules are :
- From 90 to 100 :  A
- From 80 to 89 : B
- From 70 to 79: C
- From 60 to 79: D
- From 0 to 59: F


## School hours
Define two parameters: school_hours, school_days.
- Print the total of hours the students learns at school the whole week:
     "You learned this week 400 hours !! " ( Instead of 400, it should be according to the parameters.)
- If the total hours is less than 20 hours, print:  "Less than 20 hours this week, good for you !!"
- If the total hours is less than 30 hours, print:  "Less than 30 hours this week, not bad !!"
- If the total hours is more than 30 hours, print:  "More than 30 hours this week, take some rest !!"


## Vowel or Consonant
- Create a program that reads a letter of the alphabet from the user.
- If the user enters a, e, i, o or u then print 'Vowel'
- If the user enters y then print 'Y : Vowel  and Consonant'
- All other letters: print 'Consonant'


# Data structures


## Favorites

Make a list of your favorites hobbies and give that list the variable name : games
Make a list of your favorites foods and give that list the variable name : foods
Join the two lists and put the result in a variable named favorite
Print the content of the variable favorite


## Secret language

You have invented a secret language in which each letter is replaced with the next letter (i.e. 'a' becomes 'b', 'b' becomes 'c' and 'z' becomes 'a')

You want to write a program that gets a secret string coded by the rule descried above and prints the real string content

Example of a message in a secret language : "ep zpvs ipnfxpsl"

Real message "do your homework"

(Hint: use a dictionary)


## List - less than 5

Define a list :
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 0, 55, 2, 89]
Make a new list that has all the elements less than 5 from the 'a' list in it
Print out this new list.

# For Loop


## Sum of 1 to 10

Create a program that will calculate the sum of the numbers from 1 to 10 using a loop.
It should print the sum of 1+2+3+4+5+6+7+8+9+10


## Loop over list of animals

 Define a list of animals and write a for loop that prints the names one after the other.


## Print numbers with exceptions

Write a Python program that prints all the numbers from 0 to 6 except 3 and 6.

Expected Output : 0 1 2 4 5


## Average of three numbers (this is a warm up for the next question)

Create a program that ask the user to enter 3 numbers and print the average of the numbers.
The program should act like this (the numbers are an example):
- "Please enter number:" 5
- "Please enter number:" 8
- "Please enter number:" 2

"The average is :  5"


## Average of any number of numbers

The user first enter how many numbers he wants to provide.
The program should then ask to enter as many numbers as he asked to.
The program should act like this (the numbers are an example):
- "How many numbers do you want to calculate?" 4
- "Please enter number:" 5
- "Please enter number:" 8
- "Please enter number:" 2
- "Please enter number:" 1

"The average is :  4"

## Multiples of 7 (this is a warm up for the next question))

Write a Python program that prints all the multiples of 7 from 0 to 100.

(reminder: a number is a multiple of 7 when : number%7==0 )


## 7 BOOM

Write a Python program that prints all the numbers from 0 to 100 unless:
- If it is a multiple of 7: print 'BOOM'.
- If the number contains 7: print 'BOOM'.


## Triangle

Using a for loop print the following:

```
####
###
##
#
```


## Square

Write a Python program that asks the user for a number.
Using a for loop print a square according to the number the user entered.

For example:
"Please enter a number: " 4

```
####
####
####
####
```


# While loop


## Password

The secret password is 'cheese'

Write a Python program that asks the user for the password.
As long as the user enters the wrong password, print "Wrong password. Try again.", and ask for it again.

If the user enters the right password, print "Right password. Welcome!" and finish the program

## Print letter

Write a Python program that asks the user for a number using a while loop.
When the user enters '0' the program should exit.
As long as the user enters a number the output should be 'a' times the number

example output:

$ python print_a.py
Enter number: 4
aaaa
Enter number: 1
a
Enter number: 0
$

Hint:
>>> print('a'*3)
aaa

Bonus:
- what happens when you enter a string instead of a number (Enter number: 'a')?

# Functions


## Good Work function


Write a function called good_work that takes in a person's name, and prints out a good work message.

Call it with 3 different names.

For example:
```
good_work("Adriana")
"You are doing good work, Adriana!"
"Thank you very much for your efforts on this project."
```


## Add function

Write a function called add_num that takes in two numbers, and adds them together.

Make your function print out a sentence showing the two numbers, and the result.

For example:
```
add_num(4,7)
"4 + 7 = 11"
```


## Multable function


 Write a function named multable that accepts a number X and prints the multiplication table of X from 1 to 10.

For example:
```
multable(3)
3
6
9
12
15
18
21
24
27
30
```


## Max_num function (2 numbers)

Write a python function named max_num to find the max of two numbers.

For example:
```
max_num(798,2)
"The maximum is 798"
```


## Max_num function (3 numbers)


Write a python function to find the max of three numbers.

For example:
```
max_num(798,2,999)
"The maximum is 999"
```


## Moon weight

Your weight on the moon is 16.5 percents of your weight on earth

Write a function named moonweight that accepts a number of years Y and your weight W and prints for each year your weight on the moon assuming that you gain 1 additional Kilogram each year

for example moonweight(2, 50) should print ;

```
weight for 0 year : 8.25   # 50 * 0.165
weight for 1 year : 8.41   # 51 * 0.165
weight for 2 year : 8.58   # 52 * 0.165
```


# Object Oriented


## Calc


Write a class Calc that have the following functions:
- add(x,y) # adds two numbers
- sub(x,y) # subtracts two numbers
- mul(x,y) # multiplies two numbers
- div(x,y) # divides two numbers


Write few examples that use your calculator


## Giraffe


Suppose you are given the following class:
```
class Giraffe:
    def move(leg,x,y):
       print("Giraffe moves its %s leg to point %s,%s" % (leg, x, y))
```

add a function named dance() that id doing the following

```
move leg 1 to 10,10
move leg 2 to 50,50
move leg 3 to 100,10
move leg 4 to 200,50
```

The function should repeat the above 3 times


## Inheritance


What does the following program do, why ????

```
#!/usr/bin/python

class A:
    def draw(self):
        print("drawing class A")

class B(A):
    def draw(self):
        print("drawing class B")


myobject=A()
mychildobject=B()
myobject.draw()
mychildobject.draw()
```
