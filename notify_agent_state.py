# -*- coding: utf-8 -*-
import time
import sys
from script_call_function_cloud import call_function_cloud
import json
from collections import defaultdict
#import numpy
#import tensorflow as tf

def run_parse_agents(name):
    result=json.loads(call_function_cloud("notifyAgentState",{"name":name}))["result"]
    print result

if __name__=='__main__':
    if len(sys.argv)>1:
        run_parse_agents(sys.argv[1])
    else:
        print "missing agent name"
