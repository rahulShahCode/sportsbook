import requests 
from classes import * 
from twitter import * 
import time 

valid_market_names = ("Spread Betting", "Total Points", "Moneyline")
url_market_prices = "https://smp.nj.sportsbook.fanduel.com/api/sports/fixedodds/readonly/v1/getMarketPrices?priceHistory=1"
url_nba = "https://sbapi.nj.sportsbook.fanduel.com/api/content-managed-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&includeRaceCards=false&includeSeo=true&language=en&regionCode=NAMERICA&timezone=America%2FNew_York&includeMarketBlurbs=true&_ak=FhMFpcPWXMeyZxOx&page=CUSTOM&customPageId=nba"



def init(): 
    resp = requests.get(url_nba) 
    data = resp.json()['attachments']
    events = load_events(data['events'])

    for key,value in data['markets'].items(): 
        if value['marketName'] in valid_market_names: 
            runners = [Runner(value['runners'][0]), Runner(value['runners'][1])]
            market = Market(value["marketId"], runners, value["marketName"])
            found = find_event(events,value["eventId"])
            if found is not None: 
                found.markets.append(market)
    return events 

def find_market(marketId, event=None): 
    if event: 
        for m in event.markets: 
            if m.id == marketId: 
                return m  
    else: 
        for e in events: 
            for m in e.markets: 
                if m.id == marketId:
                    return m 
    return None 
def find_event(events, eventId=None, marketId=None): 
    for e in events: 
        if marketId and find_market(marketId, e):
            return e 
        elif e.id == eventId:
            return e 
    return None 


def load_events(e): 
    competitionId = 10547864
    lst = [] 
    for x,y in e.items(): 
        if y['competitionId'] == competitionId:
            lst.append(Event(y['eventId'], y['name']))
    return lst 


def fetch_live(e):
    url = "https://smp.nj.sportsbook.fanduel.com/api/sports/fixedodds/readonly/v1/getMarketPrices?priceHistory=1"
    for e in events: 
        ids = [m.id for m in e.markets]
        payload = {"marketIds" : ids}
        response = requests.post(url,json=payload).json()
        update_lines(response)

def update_lines(response): 
    for r in response: 
        if not r['inplay']:
            market = find_market(r['marketId'])
            event = find_event(events, marketId=r['marketId'])
            for i in range(0,1):
                old_line = market.runners[i].update(r['runnerDetails'][i])
                new_handicap = market.runners[i].handicap
                if old_line is not None: 
                    print("Tweet Posted!")
                    post_tweet(client, f"{event.name}: {market.name} for {market.runners[i].name} from {old_line} to {new_handicap}")
                    time.sleep(10)


debugFlag = True 
events = init()  
events = events[1:]
print("Successfully Loaded Events")
while(True):
    print("Fetching...")
    fetch_live(events)
    time.sleep(300)
