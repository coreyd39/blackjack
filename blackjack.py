'''
DESCRIPTION:

This program allows the user to play Blackjack in the display window. The user is able to play a variety
of different preset gamemodes or implement unique rules to their game. There is also an option to minimize text/print
responses if desired with the (eventual) ability run simulations without input from the user.

See README.md on GitHub for a full description of the features of the program. 

LAST UPDATED: 11/20/23

TO DO LIST:
- The ability to split a pair of numbers
    - Allowing a single player to play multiple hands (having multiple hands connected to a single bankroll)
- Greater variety of preset gametypes
- Make card counting toggleable 
- Inputtable deck penetration value (to determine when shuffles happen)

CURRENT BUGS:
- If a player surrenders and the dealer busts, the player wins 50% of their bet instead of losing all of it
- Taking insurance when dealer has blackjack displays as a loss
- Running/True count account for the 2nd, face down dealer card

'''

import random

def shuffle(shoe):
    # Shuffles the shoe
    shoe=random.shuffle(shoe);
    return shoe

def generate_shoe(deck_num):
    # Generates cards within the shoe
    cards=[2,3,4,5,6,7,8,9,10,'J','Q','K','A'];
    deck=4*cards;
    shoe=deck_num*deck;
    return shoe

def deal(shoe,og_shoe,players,discarded):
    # Deals cards to each player and dealer
    # Generates list of lists where each individual list represents a person's hand (dealer is final list)
    # Returns updated shoe
    
    # Checks to see if there are enough cards to deal,
    # If not, shuffles then deals
    if len(shoe)<2*(players+1):
        # MUST RESEARCH BJ SHUFFLING
        print('The shoe was shuffled')
        shoe=shuffle(og_shoe);
        
    # Generates starting hands
    hands=[];
    for x in range(0,2):
        
        cards=[];
        for person in range(0,players+1):
            card=shoe[0];
            discarded=discarded+[card];
            shoe.remove(shoe[0]);
            cards=cards+[card];
            
        hands=hands+[cards];
    
    # Reformats starting hands
    starting=[];
    for y in range(0,players+1):
        dealt=[hands[0][y],hands[1][y]];
        starting=starting+[dealt];
    
    return [starting,shoe,discarded]

def sum_hand(hand):
    total=0;
    aces=0;
    for x in range(0,len(hand)):
        if hand[x]== 'J' or hand[x] == 'Q' or hand[x] == 'K':
            val=10;
        elif hand[x]=='A':
            val=11;
            aces=aces+1;
        else:
            val=int(hand[x]);
            
        total=total+val;
        
    while total>21 and aces>0:
        total=total-10;
        aces=aces-1;
        
    return total

def hit(hand,shoe,discard):
    # Check before running that the shoe is not empty
    
    hand=hand+[shoe[0]];
    discard=discard+[shoe[0]];
    shoe.remove(shoe[0]);
    
    return [hand,discard]

def print_hands(hands,players,dealer_status):
    
    # Prints hands
    if dealer_status == 0:
        print('Dealer shows ' +str(hands[players][0]))
        
    else:
        t='Dealer: '
        for j in range(0,len(hands[players])):
            t=t+str(hands[players][j]);
            if j != (len(hands[players])-1):
                t=t+','
            
        print(t)
    for n in range(0,players):
        text=('Player ' + str(n+1)+': ')
        
        for x in range(0,len(hands[n])):
            text=text+str(hands[n][x]);
            
            if x != (len(hands[n])-1):
                text=text+','
            
        print(text)
            
    print('')
    
    return

def shoe_remaining(discarded, decks, n):
    # Determines and returns the amount of decks left to be dealt,
    # n variable is an integer refering to the closest (nearest) deck size the total is estimated/rounded to
    # (i.e. n=1 is nearest full deck, n=2 is nearest half deck, so on)
    # nearest must be an integer satisfying 1 <= n <= 52 where n = 52 is 100% accurate
    # prints the amount of decks that have been dealt
    
    cards_to_be_dealt=52*decks-len(discarded);
    decks_to_be_dealt=cards_to_be_dealt/52;
    approximate=round(decks_to_be_dealt*n)/n;
    
    return approximate

def current_count(discarded,running_count=0,previous_read=0):
    # Evaluates cards currently in the discard pile (including those in play)
    # and reads their value, updating a running card count
    
    # Only counts newly added cards to the discard pile
    for x in range(previous_read,len(discarded)):
        val=sum_hand([discarded[x]]);
        if val == 10:
            running_count=running_count-1;
            
        elif val <= 6:
            running_count=running_count+1;
    
    total_read=len(discarded);
    
    return [running_count,total_read]

def calc_true(running_count,decks_to_be_dealt):
    # Calculates true card count
    true_count=running_count/decks_to_be_dealt;
    
    return true_count

def count_cards(discarded, decks, n, running_count, previous_read):
    # Runs all card counting related functions
    
    decks_remaining=shoe_remaining(discarded,decks,n);
    [running_count,previous_read]=current_count(discarded,running_count,previous_read)
    true_count=calc_true(running_count,decks_remaining)
    
    return [decks_remaining, running_count, true_count, previous_read]
    

def blackjack(gamemode='test',printed='t',players=1,count='true'):
    # Initializes important global sets/values
    action_list=['hit','h','stand','stay','s', 'split','sp','surrender','sur','double down','double','d']
    
    # Initializes game, allows for preset gamemodes or customizable games
    if 'standard' in gamemode:
        # Plays a standard 8 deck shoe game
        deck_num=8;
        payroll_number=players;
        determined='true';
        bankroll_list=[];

    elif 'test' in gamemode:
        # Plays a standard 8 deck shoe game
        # Assumes ideal game conditions and set bankroll 
        deck_num=8;
        determined='true';
        bankroll_list=players*[1000];
        payroll_number=players;
        blackjack_payout=1.5;

    else:
        deck_num=int(input('Indicate number of decks in the shoe: '));
        players=int(input('Indicate number of players/hands being played: '));
        determined='false';
        bankroll_list=[];
    
    # Initializes card counting functionalities (if desired)
    if 'true' in count:
        running_count=0;
        accuracy=1;
        previous_read=0;
    
    # BEGINS GAME
    # Determines number of bankrolls to consider
    while determined=='false':
        payroll_number=int(input('Number of bankrolls to account for: '))
        if payroll_number> players:
            print('There are more payrolls than there are players, please select a new number')
        else:
            determined='true';
            
    # Determines bankroll sizes if necessary
    if len(bankroll_list)==0:
        for p in range(0,payroll_number):
            bankroll=int(input('Player ' + str(p+1) + '\'s bankroll: '))
            bankroll_list=bankroll_list+[bankroll];            
            
    # Generates Shoe
    shoe=generate_shoe(deck_num);
    shuffle(shoe)
    
    # Saves original deck for eventual reshuffle
    og_shoe=shoe;
    
    # Initializes discard pile for eventual reshuffle AND possible card counting
    discard=[];
    
    status='bet';
    while status!='n':
        
        # Determines bet sizes (if applicable) when necessary
        if status=='bet':
            bet_list=[];
            for b in range(0,len(bankroll_list)):
                bet=[int(input('Player ' + str(b+1) + '\'s bet: '))]
                bet_list=bet_list+bet;                
    
        
        # Deals hands
        [hands,shoe,discard]=deal(shoe,og_shoe,players,discard);
        print_hands(hands,players,0)
        
        # Updates bets
        winnings=bet_list+[];
        
        # Checks if insurance is necessary then checks for blackjack
        # Initializes insurance check
        dealer_bj='';
        insurance_list=[];
        dealer_up_card=sum_hand([hands[players][0]]);
        if dealer_up_card == 10 or dealer_up_card == 11:
            
            # Provides card count (if necessary)
            if 'true' in count:
                [decks_remaining, running_count, true_count, previous_read]=count_cards(discard, deck_num, accuracy, running_count, previous_read);
                print('Decks Remaining: '+ str(decks_remaining) + ', Running Count: ' + str(running_count) +', True Count: ' + str(true_count)+'\n')
            
            # make for-loop to ask each player whose bankroll matters
            for i in range(0,len(bankroll_list)):
                ins=' ';
                while ins!='y' and ins!='n':
                    ins=input('Insurance for player ' + str(i+1)+' (type y/n): ');
                    if ins!='y' and ins!='n':
                        print('That input is not supported at this time')
                        
                insurance_list=insurance_list+[ins];            
            
            # if dealer has blackjack, immediately calculate and end the hand
            if sum_hand(hands[players])==21:
                dealer_bj='true';
                print('The Dealer has blackjack')
                print('')
                
            else:
                print('The Dealer does not have blackjack')
                print('')
              
        # Goes through each player hand to determine action
        # until player stands or busts
        for x in range(0,players):
            
            # Automatically ends round if the dealer has blackjack
            if dealer_bj=='true':
                break
            
            action='';
            while action != 's':
                
                ''' Bug exists here '''
                # PROVIDE CARD COUNT HERE (if desired)
                if 'true' in count:
                    [decks_remaining, running_count, true_count, previous_read]=count_cards(discard, deck_num, accuracy, running_count, previous_read);
                    print('Decks Remaining: '+ str(decks_remaining) + ', Running Count: ' + str(running_count) +', True Count: ' + str(true_count)+'\n')
                
                # Determines player action
                action=input('Player ' +str(x+1)+ '\'s action: ');
                action=action.lower();
                
                while action not in action_list:
                    print(action_list)
                    print('That action is not supported at this time, please try again')
                    action=input('Player ' +str(x+1)+ '\'s action:')
                    action=action.lower();
                    
                    # FIX THIS (MUST FIGURE OUT WTF TO DO WITH SPLIT)
                if action == 'hit' or action == 'h':
                    # Check before running that the shoe is not empty
    
                    hands[x]=hands[x]+[shoe[0]];
                    discard=discard+[shoe[0]];
                    shoe.remove(shoe[0]);
                    if sum_hand(hands[x])>21:
                        action='s';
                    
                elif action == 'double down' or action == 'double' or action == 'd':
                    # Hits hand, ends the action
                    # Only able to on first turn of hand
                    
                    hands[x]=hands[x]+[shoe[0]];
                    discard=discard+[shoe[0]];
                    shoe.remove(shoe[0]);
                    winnings[x]=2*winnings[x];
                    action='s';

                elif action == 'split' or action == 'sp':
                    # Must code
                    action='s';
                
                elif action == 'surrender' or action == 'sur':
                    # Forfeits hand, loses half of bet
                    # Turns hand total to 0
                    
                    hands[x]=[0];
                    if x < len(bet_list):
                        winnings[x]=winnings[x]/2;
                        
                    action='s';
                
                print('')
                print_hands(hands,players,0)
                
                if action == 'stand' or action == 'stay':
                    action='s';
    
        # Reveals second dealer card, then hits until 17 (does not hit on soft 17)
        print_hands(hands,players,1)
        while sum_hand(hands[players]) < 17:           
            hands[players]=hands[players]+[shoe[0]];
            discard=discard+[shoe[0]];
            shoe.remove(shoe[x]);
            print_hands(hands,players,1)
        
        # Determines winners and losers, accounting for blackjack
        dealer_total=sum_hand(hands[players]);
        
        for y in range(0, len(bet_list)):
            player_total=sum_hand(hands[y]);
            
            if player_total == 21 and len(hands[y]) == 2 and dealer_bj != 'true':
                bankroll_list[y]=bankroll_list[y]+blackjack_payout*winnings[y];
                print('Player ' + str(y+1) +' wins $'+ str(blackjack_payout*winnings[y]))

            elif (player_total < 22 and dealer_total > 21) or (player_total < 22 and player_total > dealer_total):
                # Return to this when bankroll feature is added to account for winnings/losses
                bankroll_list[y]=bankroll_list[y]+winnings[y];
                print('Player ' + str(y+1) +' wins $'+ str(winnings[y]))

                
            elif player_total < 22 and player_total == dealer_total:
                print('Player ' + str(y+1) +' pushes')
                
            else:
                bankroll_list[y]=bankroll_list[y]-winnings[y];
                print('Player ' + str(y+1) +' loses $'+ str(winnings[y])+' (unlucky)')
        
        print('')
       
        status=input('Continue playing (y/n): ')
    return bankroll_list

bankrolls=blackjack()
