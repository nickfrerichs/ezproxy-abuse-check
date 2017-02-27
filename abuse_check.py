import subprocess
import operator
import sys
from datetime import datetime
import time

# Our Log format
# 0.0.0.0 - XXXXXXX@XXX.XXX [13/Sep/2016:14:11:27 -0600] "GET https://blahblah:443/favicon.ico HTTP/1.1" 404 260


def main():
     # This command grabs the most recent log file
     cmd = "ls -latr /usr/local/ezproxy/*.log* | awk '/./{line=$0} END{print line}' | awk '{print $9}'"
     
     filename = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].strip()
     
     users = dict()
     ips = dict()
     user_ips = dict()

     with open(filename) as f:
          for line in f:
               row = line.split(" ")

               # This "row" in your log file has the IP address
               ip = row[0]

               # This "row" in your log file has the username
               username = row[2].lower()

               # This "row" in your log file has the date
               timestamp = datetime.strptime(row[3].replace("[",""),'%d/%b/%Y:%H:%M:%S')

               if int(time.time()) - (604800) > int(time.mktime(timestamp.timetuple())):
                    continue
               if username == "-": continue
               if users.get(username) is None:
                    users[username] = 0
               users[username] += 1

               if user_ips.get(username) is None:
                    user_ips[username] = set()
               user_ips[username].add(ip)

               if ips.get(ip) is None:
                    ips[ip] = 0
               ips[ip]+=1



     user_ip_counts = dict()
     for one in user_ips:
          if user_ip_counts.get(one) is None:
               user_ip_counts[one] = len(user_ips[one])

     users = sorted(users.items(), key=operator.itemgetter(1))
     users.reverse()

     user_ip_counts = sorted(user_ip_counts.items(), key=operator.itemgetter(1))
     user_ip_counts.reverse()

     ips = sorted(ips.items(), key=operator.itemgetter(1))
     ips.reverse()


     print "Top unique IPs per User"
     print "-----------------------------"
     print_list(user_ip_counts)
     print

     print "Users above 10 unique IPs"
     print "-----------------------------"
     for one in user_ips:
          if len(user_ips[one]) >= 10:
               print one
               for ip in user_ips[one]:
                    print ip
               print

     print "Hits per IP"
     print "-----------------------------"
     print_list(ips)
     print


     print "Hits per User"
     print "-----------------------------"
     print_list(users)
     print





def print_list(list):
     for i in range(0,20):
          print str(list[i][0]).ljust(20)+str(list[i][1]).ljust(20)
          
main()
