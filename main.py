import os
import sys
import argparse
import platform
#import csv
import gc
from watchwords import Watchwords

os_details = {}

#HACK: The method for setting the slash off of the environment doesnt always work. so this is a workaround 
def execution_slash(pth : str):
    if '/' in pth:
        os_details['env_slash'] = '/'
    else:
        os_details['env_slash'] = '\\'

def get_os_details():
    try:
        os_details['os'] = platform.system()
        if platform.system() == 'Linux':
            os_details['slash'] = '//'
        else:
            os_details['slash'] = '\\'
    except Exception as e:
        print(f'Exception thrown in get_os_details: {e}')

def check_path_details(d, s, f):
    print(f'********************************************************************************\nCURRENT DIR: {d}\nSUB-DIRS: {s}\n FILES: {f}\n******************************************************\n ')


def get_args() -> tuple:
    parser = argparse.ArgumentParser(
        description='search through files in a directory and those in their subdirectories for hashes of keywords. Place you list of keywords in the folder NYPKeywordList.'
    )

    parser.add_argument(
        '-d', '--sourcedirectory', help='specify path to directory of files you wish examined'
    )
    parser.add_argument(
        '--csv', help='path to write .csbv file to'
    )
    args = parser.parse_args()
    #print(args.sourcedirectory)
    sourcepath = args.sourcedirectory
    writepath = args.csv
    print(f'Directory path: {sourcepath}')
    print(f'write path: {writepath}')
    return (sourcepath, writepath)


def get_keywords(target_dir):
    watchwords_list = []
    try:
        print(f'Target Dir: {target_dir}')
        for currentDir, subs, files in os.walk(target_dir):
            for f in files:
                f_name, f_extension = os.path.splitext(f)
                kwrds = Watchwords(f_name, [], [])
                thefile = target_dir+os_details.get('env_slash')+f
                
                with open(thefile, 'r') as keyword_list:
                    for line in keyword_list:
                        kwrds.words.append(line.rstrip())
                watchwords_list.append(kwrds)
    except Exception as e:
        print(f'ERROR: Unbound exception in get_keywords(). Message: {e}')
    finally:
        return watchwords_list         


def check_for_keywords(kwrds, target_dir):
    counter = 1
    unsearched = 0
    files_extensions_searched = []
    files_extensions_not_searched = []
    print(f'begining check_for_keywords')
    try:
        for currentDir, subs, files in os.walk(target_dir):
            print(f'CURRNET DIR: {currentDir}')
            if files:
                try:
                    for f in files:
                        f_name, f_extension = os.path.splitext(f)                        
                        thefile = currentDir+os_details.get('env_slash')+f
                        report = []
                        with open(thefile, 'r') as f_line:
                            #TODO: Swap arround the line and kwrds readign order. Do this so that you can log files you can read through excpeiton handling
                            for line in f_line:
                                try:
                                    for word_list in kwrds:
                                        for word in word_list.words:
                                            if word in line:
                                                #NOTE: The name of the list of words, the word found. the File it was found in, The line in the file it was found
                                                report.append((word_list.name, word, thefile, line))
                                                #print(f'{word_list.name}, {word}, {thefile}, {line}')
                                        word_list.report.extend(report)
                                except Exception as e:
                                    word_list.log.append(F'UNABLE TO READ FILE: {f} REASON: {type(e)}')
                except UnicodeDecodeError:
                    unsearched += 1
                    files_extensions_not_searched.append(f_extension)
                   # print(f'UnicodeDecodeError: could not the file {f} ')
                
                except Exception as e:
                    unsearched +=1
                    print('--------------------------------------------------------------------------------------------------------------------------------')
                    print(f'Unhandled exception in check_for_keywords:\n')
                    print(type(e))
                    print(e.args)
                    print(e)
                    check_path_details(currentDir, subs, files)
                    print('--------------------------------------------------------------------------------------------------------------------------------\n')
                else:
                    files_extensions_searched.append(f_extension)
                    counter +=1
                
    except Exception as e:
        print('------------------------------------------------------------------------------------------------------------------------------')
        print(f'Error in check_for_keywords:\n')
        print(type(e))
        print(e.args)
        print(e)
        check_path_details(currentDir, subs, files)
        print('--------------------------------------------------------------------------------------------------------------------------------\n')
    finally:
        print(f'returning keywords...')
        return kwrds


def get_application_path():
    # determine if application is a script file or frozen 
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)
    return application_path



if __name__ == '__main__':
    args = get_args()
    sourcepath = args[0]
    writepath = args[1]
    get_os_details() #get the operating system so you can use the correct slahsed for file paths
    keyword_path = get_application_path() #get the path to the dir the applicaiotn is running in
    print(f'APPLICATION PATH: {keyword_path}')
    execution_slash(keyword_path)
    watch_words = get_keywords(keyword_path+os_details.get('env_slash')+'keywords'+os_details.get('env_slash')) #append the path to the folder where keywords are kept to the give keyword_path
    updated_reports = check_for_keywords(watch_words,sourcepath)
    
    for repo in updated_reports:
        print(len(updated_reports))
        repo.write_report(writepath+os_details.get('env_slash')+repo.name+'-keyword-check-report.csv')
    print(f'Process complete')
