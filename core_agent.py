#import psycopg2
import sys
import threading
import Queue
import datetime
import time
import traceback
import httplib2 
import urllib 
from notify_agent_state import run_parse_agents
#from firebase import firebase

class ConeptumNotifier:
    #fb = firebase.FirebaseApplication('https://irviasyncro.firebaseio.com', None)  

    def coneptum_notify(self,agent,var,value):
        try:
            run_parse_agents(agent)
        except:
            print "error reporting state"

    def notify_freq(self,a,freq):
        data = {'freq_seconds':freq,'name':a,'status':'OK'}
        #self.fb.patch('/agents/%s' %(a),data)

class ConeptumAgent(threading.Thread):
    agent_name='unknown'
    
    def __init__(self, bucket, pause_time):
        threading.Thread.__init__(self)
        self.bucket = bucket
        self.notifier=ConeptumNotifier()
        self.notifier.notify_freq(self.agent_name,pause_time)

    def run(self):
        try:
            self.runSafe()
        except:
            self.bucket.put(traceback.format_exc())
    def coneptum_notify(self,var,value):
        self.notifier.coneptum_notify(self.agent_name,var,value)

    def runSafe(self):
        pass

INFINITE=10000000000

def seconds(d):
    return d.seconds + d.days*86400

class AgentRunner:
    #agent_type = ONCE|INFINITE
    def __init__(self,agent_class,agent_type='INFINITE',max_duration=INFINITE,pause_time=0,monitor_freq=0.1):
        self.bucket = Queue.Queue()
        self.agent_type=agent_type
        self.max_duration=max_duration
        self.pause_time=pause_time
        self.monitor_freq=monitor_freq

        i=0
        while self.agent_type=='INFINITE' or i==0:
            start_time=now_time=datetime.datetime.now()
            self.agent=agent_class(self.bucket,pause_time)
            self.agent.start()
            error=False
            while seconds(now_time-start_time)<self.max_duration:
                error= error or self.check_exceptions()
                self.agent.join(self.monitor_freq)
                now_time=datetime.datetime.now()
                if self.agent.isAlive():
                    continue
                else:
                    break
            if self.agent.isAlive():
                self.agent._Thread__delete()
                self.agent.coneptum_notify('timeout',str(seconds(now_time-start_time)))
                error=True
            error=error or self.check_exceptions()
            if not error:
                print str(now_time-start_time)
                self.agent.coneptum_notify('duration',str(seconds(now_time-start_time)))
            i+=1
            if self.agent_type=='INFINITE':
                print "pause %s seconds"%(self.pause_time,)
                time.sleep(self.pause_time)
            
            
    def check_exceptions(self):
        exceptions=False
        try:
            exc = self.bucket.get(block=False)
        except Queue.Empty:
            pass
        else:
            exceptions=True
            self.agent.coneptum_notify('exception',exc)
        return exceptions
if __name__=='__main__':
    AgentRunner(ConeptumAgent,'INFINITE',INFINITE,pause_time=1,monitor_freq=0.1)
