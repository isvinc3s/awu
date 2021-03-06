#!/usr/bin/env python3

import sys
import argparse
import requests
import json
from colored import fg, bg, attr
from os import system, name as osname, environ

version = "1.3.1"
clear_prompt = 'cls' if osname == 'nt' else 'clear'
boards = [ 'a', 'burg', 'cyb', 'd', 'lain', 'mu', 'new', 'tech', 'test', 'u', 'v', 'all' ]
reset = 'reset'

# Initial colors
class colors:
    main   = 'blue'
    second = 'red'
    sticky = 'yellow'
    title  = 'purple_1b'

'''
"""     Check wether python encoding is UTF-8
'''


try:
    if ( environ["PYTHONIOENCODING"] == "UTF-8" ):
        pass
    else:
        raise KeyError
except KeyError:
    print('\n[ %sWARNING%s ]' % (fg('red'), attr('reset')), "Enviroment variable $PYTHONIOENCODING is not set to UTF-8, unicode characters will not be displayed.")



'''
"""     arg check
'''

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--version', 
        help='Display current version',
        action="store_true")

parser.add_argument('-n', '--nocolor', 
        help='Disable the color scheme',
        action="store_true")

parser.add_argument('--colors',  
        type=str,
        nargs=4,
        help='Set a custom color scheme (hex codes). Use quotes.')

args = parser.parse_args()

if args.version:
    print('v1.1')
    sys.exit()

if args.nocolor:
    def fg(a):
        return ""
    def attr(a):
        return ""

if args.colors:
    colors.main   = args.colors[0]
    colors.second = args.colors[1]
    colors.sticky = args.colors[2]
    colors.title  = args.colors[3]


'''
"""     functions
'''

def board( boardname ):
    while True:
        # Prompt change after you select a board
        userin = input('\n%s/%s' % ( fg(colors.second), fg(colors.main) ) + str(boardname) + 
                '%s/%s >> %s' % ( fg(colors.second), fg(colors.main), attr('reset') )).lower()

        if "thread" in userin:
            if " list" in userin: 
                # Thread counter
                tc = 0
                
                # Get front page threads from the API
                t = json.loads( requests.get("https://dangeru.us/api/v2/board/" + boardname + "?page=0").text )

                # If the thread counter exceeds 18 (max posts on a page), stop the counter and print the boards
                while tc < 20:
                    #if boardname == "all":
                    #    is_all = '%s/%s' % (fg(colors.second), fg(colors.main)) + str(t[tc]['board']) + '%s/' % (fg(colors.second)),
                    #else:
                    #    is_all = ""

                    if ( t[tc]['is_locked'] == True ):
                        if ( t[tc]['sticky'] == True ):
                            th_color = colors.sticky
                        else:
                            th_color = "red"

                    elif ( t[tc]['sticky'] == True):
                        th_color = colors.sticky

                    else:
                        th_color = colors.main

                    # Please don't look at this I'm fucking retarded.
                    print('%s' % (fg(colors.second)),   str( t[tc]['post_id'] ) , 
                            '%s' % (fg(th_color)),      str( t[tc]['title'].encode('utf-8') )[2:][:-1] ,
                            #is_all ,
                            '%s' % (fg(colors.second)), str( t[tc]['number_of_replies'] ) , 
                            '%s' % (attr('reset')) )

                    tc += 1

            elif " start" in userin:
                try:
                    th_subject = input('%sSubject >> %s' % ( fg(colors.main), fg(colors.second) ))
                    print('%sEnter your reply, terminating with a single \".\"%s' % ( fg(colors.main), fg(colors.second) ))
                    reply = []
                    while True:
                        user_input = input('%sContent >> %s' % ( fg(colors.main), attr('reset') ))
                        if user_input == ".": break
                        reply.append(user_input)
                    th_content = "\n".join(reply);
                    th_confirm = input('%sConfirm (%sy%s/%sN%s) >> %s' % ( 
                        fg(colors.main), fg(colors.second),
                        fg(colors.main), fg(colors.second), 
                        fg(colors.main), fg(colors.second) ))

                    if th_confirm == "y" or th_confirm == "Y":
                        requests.post('https://dangeru.us/post', data = {'board': boardname, 'title': th_subject, 'comment': th_content})
                        print('> Thread created.')

                except KeyboardInterrupt:
                    pass

            elif len(userin) > 7: 
                while True:
                    # Thread numbers
                    threadno = userin.split(' ')[1:][0] # The normal thread number
                    threadnoC = '%s' % (fg(colors.second)) + userin.split(' ')[1:][0] # This is the colored thread number, don't use this outside of strings

                    # Prompt changes once again when you enter a thread
                    th_userin = input('\n' + threadnoC + '%s >> %s' % ( fg(colors.main), attr('reset') )).lower()

                    if th_userin == "show":
                        # Thread meta from API
                        meta = json.loads(
                                requests.get("https://dangeru.us/api/v2/thread/" + threadno + "/metadata").text )

                        # Thread title
                        print( '\n%s[%s'      % (fg(colors.main),fg(colors.title)), 
                                meta['title'] , 
                                '%s]%s'       % (fg(colors.main),attr('reset')) )
                        
                        # Reply counter
                        rc = 0

                        # Get thread replies from the API
                        reps = json.loads( requests.get("https://dangeru.us/api/v2/thread/" + threadno + "/replies").text )

                        try:
                            while True:
                                try:
                                    cap = reps[rc]['capcode']
                                    is_capcode = '%s' % (fg(colors.second)) + str(cap)

                                except KeyError:
                                    is_capcode = '%sAnonymous' % (fg(colors.main))

                                # Please don't look at this either I'm fucking retarded
                                try:
                                    print(  '\n' + str(is_capcode),
                                        '%s(%s'       % (fg(colors.main), fg(colors.second))    + str(reps[rc]['hash']) +
                                        '%s)  No. %s' % (fg(colors.main), fg(colors.second))    + str(reps[rc]['post_id']) +
                                        '\n%s| %s'    % (fg(colors.main), attr('reset'))        + str(reps[rc]['comment']) )
                                except UnicodeEncodeError:
                                    print(  '\n' + str(is_capcode),
                                            '%s(%s'       % (fg(colors.main), fg(colors.second))    + str(reps[rc]['hash']) +
                                            '%s)  No. %s' % (fg(colors.main), fg(colors.second))    + str(reps[rc]['post_id']) +
                                            '\n%s| %s'    % (fg(colors.main), attr('reset'))        + str(reps[rc]['comment'].encode("utf-8") )[2:][:-1] )

                                rc += 1

                        except IndexError:
                            pass

                        except json.decoder.JSONDecodeError:
                            pass

                    elif th_userin == 'post':
                        try:
                            print("%sType your reply lines here, enter a single \".\" to end%s" % ( fg(colors.main), attr('reset') ))
                            reply = []
                            while True:
                                user_input = input('%sContent >> %s' % ( fg(colors.main), attr('reset') ));
                                if user_input == ".": break
                                reply.append(user_input)
                            post_content = "\n".join(reply)
                            post_confirm = input('%sConfirm (%sy%s/%sN%s) >> %s' % (
                                fg(colors.main), fg(colors.second),
                                fg(colors.main), fg(colors.second),
                                fg(colors.main), fg(colors.second) ))

                            if post_confirm == "y" or post_confirm == "Y":
                                requests.post('https://dangeru.us/reply', data = {'board': boardname, 'parent': threadno, 'content': post_content})
                                print('> Reply posted')

                        except KeyboardInterrupt:
                            pass

                    elif th_userin == 'back' or th_userin == 'up':
                        break

                    elif th_userin == 'clear' or th_userin == 'cls':
                        system(clear_prompt)

                    elif th_userin == 'exit' or th_userin == 'quit':
                        sys.exit()

                    else:
                        print('aw/u/:', th_userin +": unrecognized command")
            
            else:
                print("Example usage: thread list")
                print("               thread 61204")


        elif userin == "clear" or userin == "cls":
            system(clear_prompt)

        elif userin == "back" or userin == "up":
            break

        elif userin == "exit" or userin == "quit":
            sys.exit()

        else:
            print('aw/u/:', userin + ': unrecognized command')

print('\naw/u/ v' + version)
print('Type `%shelp%s` or `%scommands%s` for a list of available commands.' % ( 
    fg(colors.second), attr('reset'),
    fg(colors.second), attr('reset') ))

while True:
    userin = input('\n%saw%s/%su%s/%s >> %s' % ( 
        fg(colors.main), fg(colors.second),
        fg(colors.main), fg(colors.second),
        fg(colors.main), attr('reset') )).lower()

    if "board" in userin:
        if " list" in userin: 
            # Fetch boards from the API
            boards = json.loads( requests.get("https://dangeru.us/api/v2/boards").text )

            # Array board counter
            bc = 0

            while True:
                try:
                    # Get the details of the current board in the counter
                    detail = json.loads( requests.get("https://dangeru.us/api/v2/board/" + boards[bc] + "/detail").text )

                    # Board in the counter and its description
                    print(  "%s/%s" % ( fg(colors.second), fg(colors.main) ) + 
                            boards[bc] + 
                            "%s/%s" % ( fg(colors.second), attr('reset') ) + 
                            "\t\t" + detail['desc'] )
                    bc += 1

                except IndexError:
                    break
            
        elif any( name in userin for name in boards ):
            try:
                board(str( userin.split(' ')[1:][0] ))
            
            except IndexError:
                print('Example usage: board list')
                print('               board cyb')
            
            except requests.exceptions.ConnectionError:
                print('%sConnection error:%s Check your internet connection and try again.' % (
                        fg('red'), attr('reset') ))

    elif userin == "commands" or userin == "help":
        print('board <option>       Enter a board')
        print('  list                 List available boards')
        print('  (name)               Enter the selected board')
        print('thread <option>      Enter or start a thread    (only works if you are on a board)')
        print('  start                Start a thread           (content must be one line)')
        print('  list                 List active threads')
        print('  (id)                 Enter the thread with the selected ID')
        print('show                 Show a thread\'s replies    (only works if you are in a therad)')
        print('post                 Reply to a thread          (only works if you are in a thread)')
        print('back|up              Move up one level          (thread > board > aw/u/)')
        print('exit|quit            Terminate aw/u/')

    elif userin == "clear" or userin == "cls":
        system(clear_prompt)

    elif userin == "exit" or userin == "quit":
        sys.exit()

    else:
        print('aw/u/:', userin + ': unrecognized command')
