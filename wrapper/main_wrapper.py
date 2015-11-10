__author__ = 'juan'

from tweepy import *
import tweepy
import random
import time
from datetime import date

IDs = ['376226019','581872947','1949495336','44101578','1179241530','23761908','24052903','226164824','14824411','404877094','339205288','36392123','22628924','25310399','17289752','39490506','17233550','47350606','26750370','252962982','23423414','74480484','1652028870','1026012882','18318781','251034857','19900973','26458162','10701602','160449058','21854181','6751502','13294452','194619416','138343953','29418160','7343682','66324459','70349639','470030489','21845251','398672330','50982086','3801501','14291684','19287037','819698388','21994861','102018086','122392201','14997025','14462419','200772249','68644850','21289183','190362598','18387196','190365803','2212224854','28356775','19594736','14078646','150196030','78546768','40254263','821247049','7599192','28076891','102333395','25277786','429355291','73633446','18687011','3796501','5680622','42378378','316488595','14514457','24688336','28079017','22007737','14553288','27052329','32454634','17408229','187864310','84053338','15280016','185675039','155544328','18124359','18448607','15529670','77821953','14411725','29958529','11043512','15753618','236561299','22144552','209652779','19093128','46538880','7089792','26265110','22360764','65134133','95455794','819772525','20429858','21107582','22822040','94963212','36626717','147543162','2183999026','492336552','1024976264','172727702','2200330036','268292782','36347825','23770198','53003895','133043282','20560841','19334929','293572225','45425854','217757724','21878991','138355318','20509689','436799542','19226961','19014898','53347647','365980939','56410958','1364120132','596468348','278641905','17883318','15877628','2231621580','14281853','21090736','81838067','1227448789','910439228','28342191','13514762','169387991','142575646','410065049','358204197','150557711','22473403','78085410','164664039','97878686','196980761','169426475','17675072','856010760','2292454922','23339387','16600393']
credentials = json.load(open('credentials.json', 'r'))
CONSUMER_KEY = credentials['consumer_key']
CONSUMER_SECRET = credentials['consumer_secret']
ACCESS_KEY = credentials['oauth_token']
ACCESS_SECRET = credentials['oauth_secret']
FILE_NUM = 0
starting_point = time.time()


class StdOutListener(StreamListener):
    def on_data(self, data):
        global starting_point, FILE_NUM
        elapsed_time = time.time () - starting_point
        if elapsed_time > (30*60):
            starting_point = time.time()
            FILE_NUM += 1
        d = date.today()
        file = "eu-elections-"+str(d.day)+"-"+str(FILE_NUM)+".txt"
        text_file = open(file, "a")
        text_file.write(str(data))

    def on_error(self, status):
        print "ERROR : " , status

    def on_limit(self, track):
        print "ON_LIMIT : " , track

if __name__ == '__main__':
    starting_point = time.time()
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    stream = Stream(auth, l, timeout=60.0)
    while True:
        # Call tweepy's userstream method with async=False to preventhtop
        # creation of another thread.
        try:
            stream.filter(follow=IDs)
            break
        except Exception, e:
             nsecs = random.randint(30, 33)
             print e, "Relanzando Wrapper en ",nsecs," segundos."
             time.sleep(nsecs)

