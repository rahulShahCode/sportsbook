class Event:
    def __init__(self, id, name):
            self.id = id 
            self.markets = [] 
            self.name = name 


class Market: 
    def __init__(self, id, runners, marketName): 
        self.id =id 
        self.runners = runners  
        self.name = marketName

class Runner: 
    def __init__(self, runner): 
        self.id = runner['selectionId']
        self.name = runner['runnerName']
        self.handicap = runner['handicap']
        self.odds = runner['winRunnerOdds']['americanDisplayOdds']['americanOdds']
    def update(self, cmpr): 
        # if self.id == cmpr['selectionId']:
            # When handicap is 0, moneyline bet, check odds for changes
            # if self.handicap == 0:
            #     if self.odds != cmpr['winRunnerOdds']['americanDisplayOdds']['americanOdds']: 
            #         old_odds = self.odds 
            #         self.odds = cmpr['winRunnerOdds']['americanDisplayOdds']['americanOdds']
            #         return old_odds 
            # else: 
                # When handicap is used (spread / total points)
        if self.handicap != cmpr['handicap']: 
            old_handicap = self.handicap 
            self.handicap = cmpr['handicap']
            self.odds = cmpr['winRunnerOdds']['americanDisplayOdds']['americanOdds']
            return old_handicap 
        return None  