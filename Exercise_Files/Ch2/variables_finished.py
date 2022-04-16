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




if __name__ == '__main__':
    args = parser()
    args.prs = ",".join(list(set(re.findall(r'\d+',args.prs))))


    for pr in args.prs.split(","):

        print("\n\n\nStart  . . ." + pr)
        result = run_system_cmd("/volume/buildtools/bin/query-pr  -H gnats -P 1529 -e'Planned-Release == \"{1}\" & State != \"closed\" & Scope-Product-Group == \"{2}\"' -f'\"%s,%s,%s,%s\"Scope:identifier Originator Created Target' {0}".format(pr, args.branch, args.product) )
        print(result['ret_str'])
        scope = originator = created = target = ""

        resolution = "not-fixed"
        resolution_reason = "Issue not applicable"

        if not result['ret_val'] == 0:
          print("Scope Not found")
          continue
        else:
          scope, originator, created, target = result['ret_str'].split(",")


        if ( ( "Oct 29" in created  or "Oct 30" in created ) and "2021" in created and  originator == args.id):
            print( pr + " : This was created last week . . .")
            # Close it 
  

        else:
            print("This was not created last week . . .")
            print("check if the scope was created previously by the developers and we opened it again")
            audit = run_system_cmd("/volume/buildtools/bin/query-pr  -H gnats -P 1529 -f'\"%s\"Audit-Trail' {0} | grep 'State{{{1}}}-Changed-From-To: closed->' | grep '{2}' ".format(pr, scope, args.id) )


            
            print(audit['ret_str'])
            if ( "2021-10-29" in audit['ret_str']  or "2021-10-30" in audit['ret_str'] ):
                print(" This was updated and re-opened recently")    

                pr_text = """From: {2}@juniper.net
  Reply-To:

  >Number: {1}
  >State{{{0}}}: assigned
  >Responsible-Changed-Why{{{0}}}: [comp-ci] Opened by mistake during FreeBSD pointer update.
  >Responsible{{{0}}}: rbu-builder
  >State-Changed-Why{{{0}}}: [comp-ci] Changed by mistake during FreeBSD pointer update\n""".format(scope, pr, args.id)
                f = open("pr_text_main.txt", "w")
                f.write(pr_text)
                f.close()
                if not args.debug: 
                    run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -n _devpublish {0}".format(pr, args.id))
                    time.sleep(4)
                    run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -f pr_text_main.txt {0}".format(pr, args.id))
                    time.sleep(4)
                    run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -u  {0}".format(pr, args.id))
                 
            else:
                  print("It was not created or re-opened recently, skipping . . . ") 
                  continue
            
        target = target.replace("20211026.151229__ci_fbsd_builder_stable_11.0.f6087d9", "")          
        print(target)

        pr_text = """From: {2}@juniper.net
Reply-To:

>Number: {1}
>State{{{0}}}: closed
>Resolution{{{0}}}: not-fixed
>Resolution-Reason{{{0}}}: Issue not applicable
>Responsible-Changed-Why{{{0}}}: [comp-ci] Opened by mistake during FreeBSD pointer update.
>Responsible{{{0}}}: rbu-builder
>State-Changed-Why{{{0}}}: [comp-ci] Changed by mistake during FreeBSD pointer update
>Target{{{0}}}: {3}
>Target-Changed-Why{{{0}}}: [comp-ci] Updated by mistake during FreeBSD pointer update\n""".format(scope, pr, args.id, target)

        f = open("pr_text.txt", "w")
        f.write(pr_text)
        f.close()

        print(pr_text)

        if not args.debug: 
           run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -n _devpublish {0}".format(pr, args.id))
           time.sleep(4)
           run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -f pr_text.txt {0}".format(pr, args.id))
           time.sleep(4)
           run_system_cmd("/volume/buildtools/bin/pr-edit  -H gnats -P 1529 -d scm -v builder -w jnpr -e {1} -u  {0}".format(pr, args.id))

sys.exit(0)