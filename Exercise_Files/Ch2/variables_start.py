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
import time

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
    return arg_parser.parse_args()

def run_system_cmd(cmd):
    ## Subroutine to run UNIX system Comamnd
    print(cmd)
    ret_doc = {}
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell="true")
    ret_doc['ret_str'] = p.communicate()[0].decode('utf-8').rstrip()
    ret_doc['ret_val'] = p.returncode
    return ret_doc

def pr_update(pr_text, pr, id, debug):
    file_name = time.time() + "pr_text.txt"
    f = open(file_name , "w")
    f.write(pr_text)
    f.close()
    print(pr_text)
    run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -n _devpublish {0}".format(pr, args.id))
    time.sleep(4)
    run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -f pr_text.txt {0}".format(pr, args.id))
    time.sleep(4)
    run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -u  {0}".format(pr, args.id))



if __name__ == '__main__':
    args = parser()
    args.prs = ",".join(list(set(re.findall(r'\d+',args.prs))))


    for pr in args.prs.split(","):

        print("\n\n\nStart  . . ." + pr)
        result = run_system_cmd("/volume/buildtools/bin/query-pr  -H gnats -P 1529 -e'Planned-Release == \"stable_11\" & State != \"closed\" & Scope-Product-Group == \"freebsd\"' -f'\"%s,%s,%s,%s\"Scope:identifier Originator Created Target' {0}".format(pr) )
        print(result['ret_str'])
        scope = originator = created = target = resolution = resolution_reason = ""

        if not result['ret_val'] == 0:
          print("Scope Not found")
        else:
          scope, originator, created, target = result['ret_str'].split(",")


        if ( ( "Fri Oct 29" in created  or "Fri Oct 30" in created ) and "2021" in created and  originator == args.id):
            print( pr + " : This was created last week . . .")
            # Just Close them
            resolution_reason = "Issue not applicable"
            resolution = "not-fixed"

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

            f = open("pr_text.txt", "w")
            f.write(pr_text)
            f.close()

            print(pr_text)

            run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -n _devpublish {0}".format(pr, args.id))
            time.sleep(4)
            run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -f pr_text.txt {0}".format(pr, args.id))
            time.sleep(4)
            run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -u  {0}".format(pr, args.id))

        else:

            last_update_state = run_system_cmd("/volume/buildtools/bin/query-pr  -H gnats -P 1529 -f'\"%s\"Audit-Trail' {0}  | grep 'State{{{1}}}-Changed-From-To: '  | grep rbu-builder | egrep '2021-10-29|2021-10-30' | head -n 1 | awk -F\":\" '\{print $NF\}' | | awk -F\"->\" '\{print $NF\} ".format(pr, scope) )
            if last_update_state['ret_str'] == "closed":
               last_update_res = run_system_cmd("/volume/buildtools/bin/query-pr  -H gnats -P 1529 -f'\"%s\"Audit-Trail' {0}  | grep 'Resolution-Reason{{{1}}}-Changed-From-To: '  | grep rbu-builder | egrep '2021-10-29|2021-10-30' | head -n 1 | awk -F\":\" '\{print $NF\}' | | awk -F\"->\" '\{print $NF\} ".format(pr, scope) ) 
               resolution_reason = last_update_res['ret_str']


            print("This was not created last week . . .")
            print("check if the scope was created previously by the developers and we opened it again")
            audit = run_system_cmd("/volume/buildtools/bin/query-pr  -H gnats -P 1529 -f'\"%s\"Audit-Trail' {0} | grep 'State{{{1}}}-Changed-From-To: closed->' | grep '{2}' ".format(pr, scope, args.id) )
            print(audit['ret_str'])
            if ( "2021-10-29" in audit['ret_str']  or "2021-10-30" in audit['ret_str'] ):
               print(" This was updated and re-opened recently")    
            else:
               print("It was not created or re-opened recently, skipping . . . ") 
               continue
            
        target = target.replace("20211026.151229__ci_fbsd_builder_stable_11.0.f6087d9", "")          

        print(target)
        pr_text = """From: {2}@juniper.net
Reply-To:

>Number: {1}
>State{{{0}}}: closed
>Resolution-Reason{{{0}}}: {5}
>State-Changed-Why{{{0}}}: [comp-ci] Changed by mistake during FreeBSD pointer update
>Target{{{0}}}: {3}
>Target-Changed-Why{{{0}}}: [comp-ci] Updated by mistake during FreeBSD pointer update\n""".format(scope, pr, args.id, target, resolution, resolution_reason)

        f = open("pr_text.txt", "w")
        f.write(pr_text)
        f.close()

        print(pr_text)

        run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -n _devpublish {0}".format(pr, args.id))
        time.sleep(4)
        run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -f pr_text.txt {0}".format(pr, args.id))
        time.sleep(4)
        run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -u  {0}".format(pr, args.id))

sys.exit(0)