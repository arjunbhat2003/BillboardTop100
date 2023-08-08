#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 15:05:30 2022

"""
import csv
from operator import itemgetter

# Keywords used to find christmas songs in get_christmas_songs()
CHRISTMAS_WORDS = ['christmas', 'navidad', 'jingle', 'sleigh', 'snow',\
                   'wonderful time', 'santa', 'reindeer']

# Titles of the columns of the csv file. used in print_data()
TITLES = ['Song', 'Artist', 'Rank', 'Last Week', 'Peak Rank', 'Weeks On']

# ranking parameters -- listed here for easy manipulation
A,B,C,D = 1.5, -5, 5, 3

#The options that should be displayed
OPTIONS = "\nOptions:\n\t\
        a - display Christmas songs\n\t\
        b - display songs by peak rank\n\t\
        c - display songs by weeks on the charts\n\t\
        d - display scores by calculated rank\n\t\
        q - terminate the program \n"

#the prompt to ask the user for an option
PROMPT = "Enter one of the listed options: "

def get_option():
    '''
    Prompts the user for a valid option
    Loops until user inputs a valid option
    Returns option as a string 
    '''
    valid_str = 'abcdq'#initializes all valid options as a string
    option_str = input(PROMPT).lower() # prompts for an option and converts to lowercase
    #loops until a valid inout
    while not option_str in valid_str:
        print('Invalid option!\nTry again')
        option_str = input(PROMPT).lower()
    return option_str #retuns option
def open_file():
    '''
    Prompts for a file name
    Loops until a file is correctly opened
    returns file pointer
    '''
    file_name = input('Enter a file name: ')#prompts for file name
    n=0
    #loops until file can be opened
    while n ==0:
        try:
            fp = open(file_name,'r')#tries to ooen file
            return fp#returns filepointer if file can be opened
            n=1#exits loop
        except FileNotFoundError: # except statement for invalid file
            print('\nInvalid file name; please try again.\n')#error message
            file_name = input('Enter a file name: ')#reprompts for file

def read_file(fp):
    '''
    Reads file line by line
    Converts each line to a list and adds the list to master list of lists
    Replaces non int values to -1
    returns master list of lists
    '''
    reader = csv.reader(fp)#uses csv to list each line
    next(reader,None)#skips header
    master_list = []#initializes master list
    #loops through each line, replaces non ints with -1, and appends to master list
    for line in reader:
        list_info = line[0:6]#creates temporary list for song data
        #checks if int values are valid, replaces invalid values to -1
        for i in range(2,6):
            try:
                list_info[i]=int(list_info[i])#tries to change values to int
            except ValueError:
                list_info[i] = -1#changes to -1 if not an integer
        master_list.append(list_info)#adds to list of lists
    return master_list#returns list of lists
def print_data(song_list):
    '''
    This function is provided to you. Do not change it
    It Prints a list of song lists.
    '''
    if not song_list:
        print("\nSong list is empty -- nothing to print.")
        return
    # String that the data will be formatted to. allocates space
    # and alignment of text
    format_string = "{:>3d}. "+"{:<45.40s} {:<20.18s} "+"{:>11d} "*4
    
    # Prints an empty line and the header formatted as the entries will be
    print()
    print(" "*5 + ("{:<45.40s} {:<20.18s} "+"{:>11.9s} "*4+'\n'+'-'*120).format(*TITLES))

    # Prints the formatted contents of every entry
    for i, sublist in enumerate(song_list, 1):
        #print(i,sublist)
        print(format_string.format(i, *sublist).replace('-1', '- '))

def get_christmas_songs(master_list):
    '''
    Selects songs from master list that are christmas theemed and adds them to a new list
    returns christmas song list
    '''
    christmas_list = []#initializes christmas list
    for song in master_list:#loops through each list in master list
        #checks if the christmas words are in song title
        for word in CHRISTMAS_WORDS:
            if word in song[0].lower():
                christmas_list.append(song)#adds song list to christmas list
    return sorted(christmas_list)#returns alphabetically sorted christmas list
        
            
def sort_by_peak(master_list):
    '''
    Sorts master list by peak rank, increasing order
    removes songs with invalid peak ranks(-1)
    returns modified master list
    '''
    master_list.sort(key=itemgetter(4))#sorts master list by peak rank
    #reads throguh each list in master list
    for i in range(0,len(master_list)-1): 
        #removes list if peak rank is -1
        if master_list[i][4] == -1 :
            del master_list[i]
    #removes list if peak rank is -1
    if master_list[0][4] == -1:
        del master_list[0]
    return master_list #returns modified master list

def sort_by_weeks_on_list(master_list):
    '''
    Sorts master list by weeks on top 100, decreasing order
    removes songs with invalid weeks(-1)
    returns modified master list
    '''
    master_list.sort(key=itemgetter(5),reverse=True)#sorts master list by weeks decreasing
    #reads through each list in master list
    for i in range(0,len(master_list)):
        #removes list if weeks are -1
        if master_list[i][5] == -1 :
            del master_list[i]
    return master_list #returns modified master list
        
def song_score(song):
    '''
    Input is song list
    Calculates song score based on ranks 
    returns song score
    '''
    peak_rank = 100 -song[4] #sets peak rank 
    #sets peak rank to -100 if invalid peak
    if song[4] == -1:
        peak_rank = -100
    curr_rank = 100 - song[2]#sets current rank
    #sets current rank to -100 if invalid rank
    if song[2] == -1:
        curr_rank = -100
    rank_delta = song[2] -song[3] # sets rank delta to change in rank from last week to now
    weeks_on_chart = song[5] # sets weeks on chart
    score = A*peak_rank + B*rank_delta + C*weeks_on_chart + D*curr_rank #calculates total socre by adding components
    return score#returns score
def sort_by_score(master_list):
    '''
    Input is master list
    Sorts list based on song score value decreasing
    If there is a tie, reverse alphabetically sort
    returns modified list
    '''
    #adds new componenet to each list for song score
    for song in master_list:
        song.append(song_score(song))#calls song score function to calculate score
    master_list.sort(key=itemgetter(6),reverse=True)#sorts by song score in reverse order
    for i in range(1,len(master_list)):#goes through each componenet in sorted list
        if master_list[i][6] == master_list[i-1][6]:#checks if song score is same as previous song
            if master_list[i][0]>master_list[i-1][0]:#checks if current value is higher alphabetically than last value
                master_list[i],master_list[i-1] = master_list[i-1],master_list[i] # switches positions in list
    #removes the song score from each list
    for song in master_list:
        song.pop()
    return master_list #returns modified list

    
def main():
    '''
    Main driver of program
    All functions called here to put code together
    '''
    
    print("\nBillboard Top 100\n")#openeing statement
    master_list = read_file(open_file())#references open file function to get a file name and sets it to master list using read_file function
    print_data(master_list)#prints original data
    print(OPTIONS)#prints options
    option_str = get_option()#sets option to answer based on get_option function
    #loop that goes until q is input
    while not option_str == 'q':
        if option_str == 'a':#if option is a, christmas list
            print_data(get_christmas_songs(master_list))#prints christmas data from christmas function
            if len(get_christmas_songs(master_list)) != 0:#sets percent to value if it isn't 0
                percent = len(get_christmas_songs(master_list))#sets percent to value if it isn't 0
                if percent == 6:#error checking
                    percent *=10
                print('\n{:d}% of the top 100 songs are Christmas songs.'.format(percent))#prints percent of christmas songs in correct format
            else: 
                print('None of the top 100 songs are Christmas songs.')#prints if percent is 0
        elif option_str == 'b':# if option is b, sort by peak
            print_data(sort_by_peak(master_list))#prints data from sort by peak function
        elif option_str=='c':#if option is c, weeks on list
            print_data(sort_by_weeks_on_list(master_list))#prints data from sort by weeks function
        elif option_str == 'd':#if option is d 
            print_data(sort_by_score(master_list))#prints data from sort by score function
        print(OPTIONS)#reprints options
        option_str = get_option() #reprompts for another option
    print("\nThanks for using this program!\nHave a good day!\n")#closing statement
            
    

# Calls main() if this modules is called by name
if __name__ == "__main__":
    main()           