#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Standard library
import sys
import os
import random
import subprocess
import argparse
import pwd
import time
import re

# Either the Branch Name or Planned Release will be required for the PR Updates.
def parser():
    desc= "This is a new Component CI PR Workflow Update Script. "
    arg_parser = argparse.ArgumentParser(description=desc)
    arg_parser.add_argument('-prs', '--prs',
                            type=str,
                            help='Provide the list of PRs comma seperated. ')
    arg_parser.add_argument('-id', '--id',
                            type=str,
                            help='ID ')
    arg_parser.add_argument('-branch', '--branch',
                            type=str,
                            help='branch ')
    arg_parser.add_argument('-product', '--product',
                            type=str,
                            help='product ')        
    arg_parser.add_argument('-d', '--debug',
                                help="Print lots of debugging statements", action='store_true')
                                                                           
    return arg_parser.parse_args()

def run_system_cmd(cmd):
    ## Subroutine to run UNIX system Comamnd
    print(cmd)
    ret_doc = {}
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell="true")
    ret_doc['ret_str'] = p.communicate()[0].decode('utf-8').rstrip()
    ret_doc['ret_val'] = p.returncode
    return ret_doc

def pr_update(pr_text, pr):
    file_name = str(time.time()) + "pr_text.txt"
    f = open(file_name , "w")
    f.write(pr_text)
    f.close()
    print(pr_text)
    if not args.debug: 
        run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -n _devpublish {0}".format(pr, args.id))
        time.sleep(4)
        run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -f {2} {0}".format(pr, args.id, file_name))
        time.sleep(4)
        run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -u  {0}".format(pr, args.id))



if __name__ == '__main__':
    args = parser()
    args.prs = ",".join(list(set(re.findall(r'\d+',args.prs))))


    for pr in args.prs.split(","):

        print("\n\n\nStart  . . ." + pr)
        result = run_system_cmd("/volume/buildtools/bin/query-pr  -H gnats -P 1529 -e'Planned-Release == \"{1}\" & State != \"closed\" & Scope-Product-Group == \"{2}\"' -f'\"%s,%s,%s,%s,%s\"Scope:identifier Originator Created Target State' {0}".format(pr, args.branch, args.product) )
        print(result['ret_str'])
        scope = originator = created = target = state = ""


        resolution = "not-fixed"
        resolution_reason = "Issue not applicable"

        if not result['ret_val'] == 0:
          print("Scope Not found")
          continue
        else:
          scope, originator, created, target, state = result['ret_str'].split(",")
          target = target.replace("20211026.151229__ci_fbsd_builder_stable_11.0.f6087d9", "")          
          print(target)


        if ( ( "Oct 29" in created  or "Oct 30" in created ) and "2021" in created and  originator == args.id):
            print( pr + " : This was created last week . . .")
            # Close it 

            if "verify-resolution" in state:

               pr_text = """From: {2}@juniper.net
Reply-To:

>Number: {1}
>State{{{0}}}: assigned
>Resolution{{{0}}}: {4}
>Resolution-Reason{{{0}}}: {5}
>Responsible-Changed-Why{{{0}}}: .
>Responsible{{{0}}}: rbu-builder
>State-Changed-Why{{{0}}}: .
>Target{{{0}}}: {3}
>Target-Changed-Why{{{0}}}: [comp-ci] Updated by mistake during FreeBSD pointer update\n""".format(scope, pr, args.id, target, resolution, resolution_reason)
               pr_update(pr_text, pr)


            pr_text = """From: {2}@juniper.net
Reply-To:

>Number: {1}
>State{{{0}}}: closed
>Resolution{{{0}}}: {4}
>Resolution-Reason{{{0}}}: {5}
>Responsible-Changed-Why{{{0}}}: [comp-ci] Opened by mistake during FreeBSD pointer update.
>Responsible{{{0}}}: rbu-builder
>State-Changed-Why{{{0}}}: [comp-ci] Changed by mistake during FreeBSD pointer update
>Target{{{0}}}: {3}
>Target-Changed-Why{{{0}}}: [comp-ci] Updated by mistake during FreeBSD pointer update\n""".format(scope, pr, args.id, target, resolution, resolution_reason)

            pr_update(pr_text, pr)





        else:
            resolution = "fixed"
            resolution_reason = "Fix Submitted"

            print("\n\n\nThis was not created last week, But looks it was updated/re-opened last week . . .") 
            last_update_state = run_system_cmd("/volume/buildtools/bin/query-pr  -H gnats -P 1529 -f'\"%s\"Audit-Trail' {0}  | grep 'State{{{1}}}-Changed-From-To: '  | grep rbu-builder | egrep '2021-10-29|2021-10-30' | head -n 1 ".format(pr, scope) + " | awk -F':' '{print $NF}' | awk -F'->' '{print $1}' " )
            if "closed" in last_update_state['ret_str']:
               print("Looks like the scope was in closed state") 
               last_update_res = run_system_cmd("/volume/buildtools/bin/query-pr  -H gnats -P 1529 -f'\"%s\"Audit-Trail' {0}  | grep 'Resolution-Reason{{{1}}}-Changed-From-To: '  | grep rbu-builder | egrep '2021-10-29|2021-10-30' | head -n 1 ".format(pr, scope) + " | awk -F':' '{print $NF}' | awk -F'->' '{print $1}' " ) 
               resolution_reason = last_update_res['ret_str']
               if ( "Fix" not in resolution_reason ):
                  print("Not in Fixed") 
                  pr_text = """From: {2}@juniper.net

Reply-To:

>Number: {1}
>State{{{0}}}: closed
>Resolution{{{0}}}: fixed
>Resolution-Reason{{{0}}}: Fix Submitted
>Verification-Status{{{0}}}: resolution-accepted
>Verification-Status-Changed-Why{{{0}}}: [comp-ci] Changed the scope by mistake during FreeBSD pointer update
>State-Changed-Why{{{0}}}: [comp-ci] Changed the state by mistake during FreeBSD pointer update
>Target{{{0}}}: {3}
>Target-Changed-Why{{{0}}}: [comp-ci] Updated the target by mistake during FreeBSD pointer update\n""".format(scope, pr, args.id, target, resolution, resolution_reason)
                  pr_update(pr_text, pr)
                  sys.exit(0)


               pr_text = """From: {2}@juniper.net
Reply-To:

>Number: {1}
>State{{{0}}}: closed
>Resolution{{{0}}}: {4}
>Resolution-Reason{{{0}}}: {5}
>Verification-Status{{{0}}}: resolution-accepted
>Verification-Status-Changed-Why{{{0}}}: [comp-ci] Changed the scope by mistake during FreeBSD pointer update
>State-Changed-Why{{{0}}}: [comp-ci] Changed the state by mistake during FreeBSD pointer update
>Target{{{0}}}: {3}
>Target-Changed-Why{{{0}}}: [comp-ci] Updated the target by mistake during FreeBSD pointer update\n""".format(scope, pr, args.id, target, resolution, resolution_reason)
               pr_update(pr_text, pr)
            else:
               print("It was not created or re-opened recently, skipping . . . ") 
               sys.exit(0) 
            



sys.exit(0)