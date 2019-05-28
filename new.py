#
# diseaseSim.py - simulates the spread of disease through a population
#
# Student Name   : RAJ SURESH PATEL
# Student Number : 19701855
#
# Version history: 20.0
#
# 27/5/19 - LATEST VERSION UPDATED

#1] ADDED OPTION FOR MOORE AND VON NEUMANN
#2] ADDED ADDITIONAL BEHAVIOR FOR DEATH(BLACK SPOTS), IMMUNITY(DARKGREEN SPOT) AND RECOVERY(AQUA SPOTS)
#3] ADDED STATISTICS FOR BOT INFECTED VS UNINFECTED AND FOR REST OF THE ADDITIONAL BEHAVIOUR.
#4] ADDED AIRPORT FOR PEOPLE FOR FLYING TO OTHER GRID OR BLOCK.
#5] ADDED COMMAND LINE ARGUEMENT(CAN BE GIVEN AS INIT_POP, INIT_INFECTED, INIT_ROWS, INIT_COLS, INIT_STEPS, _MOVEMENT OPTION FOR MOORE AS 2 AND VONNEUAMNN AS 1, [DEFAULT IS MOORE WHICH IS 2])
#6] ADDED BASH SCRIPT WHICH CAN BE RUN USING SH SIMULATION_SWEEP.SH BY GIVING COMMAND LINE ARGUEMENT FOR LOWEST NUMBER OF POPULATION, HIGHEST NUMBER OF POPULATION, NUMBER OF STEPS, LOWEST NUMBER OF INFECTION, HIGHEST NUMBER OF INFECTION, NUMBER OF STEPS.


import numpy as np
import matplotlib.pyplot as plt
import random
import array
import sys

#COMMAND LINE ARGUEMENT:

if(len(sys.argv) < 7):
    print('argv is too short, usage:python3 < Population> < infected>')
    Ipopulation = 900
    Iinfected = 150
    Irows = 30
    Icols = 30
    Isteps = 10
    #DEFAULT WILL BE MOORE AS MOVEMENT OPTION AS 2, IF YOU TO APPLY VON NEUMANN USER MUST DO IT FROM COMMAND LINE ARGUEMENT.
    Ia=2
else:
    Ipopulation = int(sys.argv[1])    #TOTAL POPULATIONS
    Iinfected = int(sys.argv[2])      #INFECTED PEOPLES
    Irows = int(sys.argv[3])          #TOTAL NUMBER OF ROWS
    Icols = int(sys.argv[4])          #TOTAL NUMBER OF COLS
    Isteps = int(sys.argv[5])          #NUMBER OF STEPS
    Ia = int(sys.argv[6])          #MOVEMENT OPTION

def distribute(grid, r, c, numpeep):
    #DISTRIBUTING PEOPLE WITH 50 -50 % PROBABILITY OF APPEARING IN ALL 4 GRIF OR BLOCK .
    for i in range(numpeep):
        A = random.randint(0,1)
        if A == 0:
            rpos = random.randint(1, (r/2)-1)
        if A == 1:
            rpos = random.randint(((r/2)+1), r-2)
        B = random.randint(0,1)
        if B == 0:
            cpos = random.randint(1,(c/2)-1)
        if B == 1:
            cpos = random.randint(((c/2)+1),c-2)
        grid[rpos, cpos] += 1
#        print("Adding 1 to (", xpos, ",", ypos,")")

def makeScatter(grid, num_r, num_c):
    r_values = []
    c_values = []
    count_values = []
    for row in range(num_r):
        for col in range(num_c):
            if grid[row,col] > 0:
                r_values.append(row)
                c_values.append(col)
                count_values.append(grid[row,col]*100)
#                print("Value at (", row, ",", col, ") is ", grid[row, col])
    return(r_values, c_values, count_values)



def displayGrid(grid, num_r, num_c):
    for row in range(num_r-1, -1, -1):
        for col in range(num_c):
            print(grid[row,col], end=" ")
        print()

def plotGrids():
    plt.figure(figsize=(20,20))
    Irows, Icols,Icount = makeScatter(infected, NUM_ROWS, NUM_COLS)
    plt.scatter(Irows, Icols, s=200, c="r", linewidth = 1,alpha=0.4)
    Urows, Ucols, Ucount = makeScatter(uninfected, NUM_ROWS, NUM_COLS)
    plt.scatter(Urows, Ucols, s=200, c="b",linewidth = 1,alpha=0.4)
    Drows, Dcols, Dcount = makeScatter(deaths, NUM_ROWS, NUM_COLS)
    plt.scatter(Dcols, Drows, s=200, c='black',linewidth = 1, alpha=0.4)
    Rrows, Rcols, Rcount = makeScatter(recovers, NUM_ROWS, NUM_COLS)
    plt.scatter(Rcols, Rrows, s=200, c='aqua',linewidth = 1, alpha=0.4)
    IMrows, IMcols, IMcount = makeScatter(immunes, NUM_ROWS, NUM_COLS)
    plt.scatter(IMcols, IMrows, s=IMcount, c='darkgreen', linewidth = 1,alpha=0.4)
    Brows, Bcols, Bcount = makeScatter(barr, NUM_ROWS, NUM_COLS)
    plt.scatter(Brows, Bcols, s=Bcount, c='black', marker='H', linewidth = 4, alpha=1)
    Wrows, Wcols, Wcount = makeScatter(wall, NUM_ROWS, NUM_COLS)
    plt.scatter(Wrows, Wcols, s=Wcount, c='black', marker='H', linewidth = 5, alpha=1)
    plot2(Airports,4,'lime',"Airport")
 



def movePeeps(cur, next, r, c):
    if A ==1:        #VON NEUMANN
        for peep in range(cur[r,c]):
            rMove = random.randint(-1,1)
            cMove = random.randint(-1,1)

            if (r + rMove +cMove) > (NUM_ROWS-2) or (r + rMove +cMove) < 1:
                rMove = 0
            if (c + cMove + rMove) > (NUM_COLS-2) or (c + cMove + rMove) < 1:
                cMove = 0
            if barr[r+rMove, c+cMove] == 1:
                rMove = 0
                cMove = 0
            #FURTHER TWO IF STATEMENT WILL PREVENT PEOPLE IN VON NEUMANN ENVIRONMENT TO MOVE DIAGONALLY THROUGH THE BARRIERS (BOTH INNER AND OUTER).
            if(c + rMove) >= (NUM_ROWS-2) or (c + rMove) <= 1:
                cMove = 0
                rMove = 0
            if(r +cMove) >= (NUM_COLS-2) or (r + cMove) <= 1:
                rMove = 0
                cMove = 0
            #FURTHER TWO STEPS WILL LET PEOPLE MOVE DIAGONALLY AS WELL.
            if(c + rMove) < (NUM_ROWS-2) or (c + rMove) > 1:
                cMove = cMove
                rMove = rMove
            if(r +cMove) < (NUM_COLS-2) or (r + cMove) > 1:
                rMove = rMove
                cMove = cMove
            #FURTHER FOUR IF  STATEMENT WILL TRANSPORT PEOPLE OR PEOPLE CAN FLY FROM ONE AIRPORT TO ANOTHER AS PER INDICATED IN IF STATEMENT.
            if(r + rMove) == (NUM_COLS/4,2) or (r + rMove) == (2, 3*NUM_ROWS/4) or (r +rMove) == (NUM_COLS-2,3*NUM_ROWS/4):
                rMove = (NUM_COLS-2, NUM_ROWS/4)
            
            if(c + cMove) == (NUM_COLS-2,NUM_ROWS/4) or (c + cMove) == (NUM_COLS-2, 3*NUM_ROWS/4) or (c + cMove) == (NUM_COLS/4,2):
                cMove = (2, 3*NUM_ROWS/4)
            if(c + rMove) == (NUM_COLS/4,2) or (c + rMove) == (2, 3*NUM_ROWS/4):
                cMove = (NUM_COLS-2,NUM_ROWS/4)
            if(c + rMove) == (NUM_COLS/4,2) or (c + rMove) == (2, 3*NUM_ROWS/4):
                cMove = (NUM_COLS-2,NUM_ROWS/4)
                rMove = (NUM_COLS-2, 3*NUM_ROWS/4)
            if(r +cMove) == (NUM_COLS-2,NUM_ROWS/4) or (r + cMove) == (NUM_COLS-2, 3*NUM_ROWS/4):
                rMove = (2, 3*NUM_ROWS/4)
                cMove = (NUM_COLS-2, NUM_ROWS/4)

            next[r + rMove, c + cMove] +=1

    elif A == 2:             #MOORE
        for peep in range(cur[r, c]):
            rMove = random.randint(-1, 1)
            cMove = random.randint(-1, 1)
            #         print("Move from ", ( r, c), "to", ( r+rMove, c+cMove ))
            if (r + rMove) > (NUM_ROWS - 2) or (r + rMove) < 1:
                rMove = 0
            if (c + cMove) > (NUM_COLS - 2) or (c + cMove) < 1:
                cMove = 0
            if barr[r+rMove, c+cMove] == 1:
                rMove = 0
                cMove = 0
            #FURTHER TWO IF  STATEMENT WILL TRANSPORT PEOPLE OR PEOPLE CAN FLY FROM ONE AIRPORT TO ANOTHER AS PER INDICATED IN IF STATEMENT.
            if(r + rMove) == (NUM_COLS/4,2) or (r + rMove) == (2, 3*NUM_ROWS/4) or (r +rMove) == (NUM_COLS-2,3*NUM_ROWS/4):
                rMove = (NUM_COLS-2, NUM_ROWS/4)
            if(c + cMove) == (NUM_COLS-2,NUM_ROWS/4) or (c + cMove) == (NUM_COLS-2, 3*NUM_ROWS/4) or (c + cMove) == (NUM_COLS/4,2):
                cMove = (2, 3*NUM_ROWS/4)
            
            next[r + rMove,c + cMove] +=1

#CODE FOR MAKING AIRPORT CAN BE SEEN AS LIME COLOR SQAURE BOXES IN EACH BARRIER BOXES.
NUM_COLS = 30
NUM_ROWS = 30
Airports = [(NUM_COLS/4,2),(NUM_COLS-2,NUM_ROWS/4),(2,3*(NUM_ROWS/4)),(NUM_COLS-2,3*NUM_ROWS/4)]
def plot2(Cells,size,color='',label="default"):
        q= []
        w=[]
        for x,y in Cells:
                q.append(x)
                w.append(y)
        plt.scatter(q,w,s=size*25,marker='s',linewidth = 10,c=color,alpha=1.0)
#tried flying people from airport with random logic but failed, sorry. did manually by hardcoding the airport location and shiftings.
#def fly(cur, next, r, c):
 #   cur_port = np.array([r,c])
  # for cur in range(cur[r-2,c-2]):
   #     new = cur_port
     #   while (new == cur_port).all():
      #      new = random.choice(Airports)
       #     
        #    next[cur, new] += 1
         #   print("TRANSFERRING PEOPLE FROM",cur,"TO", new )
        #return fly

def infect(inf, notinf, r, c, prob):
#    print("Pos (", r, ",", c, ") has ", inf[r,c], " inf people and ", notinf[r,c], " well people")
    prob = prob * inf[r, c]
    if prob:
        for peep in range(notinf[r,c]):
            if random.random() < prob:
                inf[r, c] +=1
                notinf[r, c] -=1
#                print("***** NEW_INFECTION_WAS_FOUND_AT:-(", r, ",", c, ")")
                print("TOTAL_NUMBER_OF_INFECTED_PEOPLE:-",sum(sum(inf)))

def death(deat, inf, r, c, prob):
    prob = prob * inf[r,c]   
    if prob:
        for peep in range(inf[r,c]):
            if random.random() < prob:
                inf[r, c] -= 1
                deat[r,c] +=1
                print("TOTAL_DEATH:-", sum(sum(deat)))
def recovery(reco, inf, r, c, prob):
    prob = prob * inf[r,c]
    if prob:
        for peeps in range(inf[r,c]):
            if random.random() < prob:
                inf[r,c] -=1
                reco[r,c] +=1
                print("TOTAL_NUMBER_OF_RECOVERY",sum(sum(reco)))
def immunity(immu, notinf, r, c, prob):
    prob= prob * notinf[r,c]
    if prob:
        for peeps in range(notinf[r,c]):
            if random.random() < prob:
                notinf[r,c] -=1
                immu[r,c] +=1
                print("TOTAL_NUMBER_OF_IMMUNE_PEOPLE:-",sum(sum(immu)))
def stat(s_inf, s_uninf,s_deat, s_immu, s_reco):
    total_infected = np.sum(s_inf)
    total_uninfected = np.sum(s_uninf)
    stat_infected.append(total_infected)
    stat_uninfected.append(total_uninfected)
    total_deaths = np.sum(s_deat)
    total_immunes = np.sum(s_immu)
    total_recovers = np.sum(s_reco)
    stat2_deaths.append(total_deaths)
    stat2_immunes.append(total_immunes)
    stat2_recovers.append(total_recovers)

#DEFINING BARRIER TO PREVENT PEOPLE FROM MOVING THROUGH THE GIVEN BARRIER.
def bars(bar, c, r):
    #FOR VERTICAL BARRIER AND HORIZONTAL BARRIER.
    for i in range(0,c):
        bar[int(r/2), i] = 1
    for i in range(0,r):
        bar[i, int(c/2)] = 1
    #FOR PROVIND A GAP IN A RANDOM MANNER WHICH APPEARS RANDOMLY WITH EVERY TIME EXECUTION OF CODE.
    one  = random.randint(0,c-1)
    two = random.randint(0,c-1)

    for i in range(0,c):
        bar[int(r/2), one] = 0
        bar[int(r/2), two] = 0

    three = random.randint(0,r-1)
    four = random.randint(0,r-1)

    for i in range(0,r):
       bar[three, int(c/2)] = 0
       bar[four, int(c/2)] = 0

#DEFINING BARRIER OR WORLD TO PREVENT POPULATION FROM MOVING OUT OF THE WORLD.
def wall_world(wor, c, r):
    for i in range(0,c):
        wor[r-1, i] = 1
        wor[0, i] = 1
    for i in range(0,r):
        wor[i, c-1] = 1
        wor[i,0] = 1



INIT_POP=Ipopulation
INIT_INFECTED = Iinfected
NUM_COLS = Irows
NUM_ROWS = Icols
NUM_STEPS = Isteps
INIT_DEATHS = 0
INIT_RECOVERS = 0
INIT_IMMUNES = 0
stat_infected = [INIT_INFECTED]
stat_uninfected = [INIT_POP]
stat2_deaths = [INIT_DEATHS]
stat2_immunes = [INIT_IMMUNES]
stat2_recovers = [INIT_RECOVERS]


#OPTION FOR MOORE AND VON NEUMANN WHICH IS THEN AUTOMATED TO PERFORM ONLY MOORE IF USER WANT TO VON NEUMANN HAS TO DO BY USING COMMAND LINE ARGUEMENT.
#A = int(input("GIVE INPUT AS:-\n\n\n [1]VON NEUMANN \n\n\n [2]MOORE\n\n\n"))
A = Ia



infected = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
uninfected = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
distribute(infected, NUM_ROWS, NUM_COLS, INIT_INFECTED)
distribute(uninfected, NUM_ROWS, NUM_COLS, INIT_POP)
wall = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
barr = np.zeros((NUM_ROWS, NUM_COLS), dtype = np.int)
#print(infected)
#print(uninfected)

deaths = np.zeros((NUM_ROWS, NUM_COLS),  dtype=np.int)
recovers = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
immunes = np.zeros((NUM_ROWS, NUM_COLS), dtype= np.int)
#f1 = np.ones((NUM_ROWS, NUM_COLS), dtype= np.int)
#f2 = np.ones((NUM_ROWS, NUM_COLS), dtype= np.int)

#fly(f1,f2, NUM_ROWS, NUM_COLS)
bars(barr, NUM_COLS, NUM_ROWS)
wall_world(wall, NUM_COLS, NUM_ROWS)
#fly(f1, f2 NUM_ROWS, NUM_COLS)
#print(deaths)
#print(recovers)
#print(immunes)
#print(world)
#print()
displayGrid(infected, NUM_ROWS, NUM_COLS)

#print()
displayGrid(uninfected, NUM_ROWS, NUM_COLS)
displayGrid(deaths, NUM_ROWS, NUM_COLS)
displayGrid(recovers, NUM_ROWS, NUM_COLS)
#print()
displayGrid(immunes, NUM_ROWS, NUM_COLS)
#print()
plotGrids()

for timestep in range(NUM_STEPS):
    print("\n###################### TIMESTEP", timestep, "#####################\n")
    infected2 = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
    uninfected2 = np.zeros((NUM_ROWS, NUM_COLS), dtype=np.int)
    death2 = np.zeros((NUM_ROWS, NUM_COLS), dtype = np.int)
    recovers2 = np.zeros((NUM_ROWS, NUM_COLS), dtype = np.int)
    immunes2 = np.zeros((NUM_ROWS, NUM_COLS), dtype = np.int)
    #f2 = np.zeros((NUM_ROWS, NUM_COLS), dtype = np.int)
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            infect(infected, uninfected, row, col, 0.7)
            death(deaths, infected, row, col, 0.02)
            recovery(recovers, infected, row, col, 0.01)
            immunity(immunes, uninfected, row, col, 0.02)
            movePeeps(infected, infected2, row, col)
            movePeeps(uninfected, uninfected2, row, col)
            movePeeps(recovers, recovers2, row, col)
            movePeeps(immunes, immunes2, row, col)
            #fly(f1, f2, row, col)
    infected = infected2
    uninfected = uninfected2
    recovers = recovers2
    immunes = immunes2
    #f1 = f2
    stat(infected, uninfected, deaths,immunes,recovers)
    fig1 =plt.gcf() 
    fig1.savefig("OUTPUT_IMAGE"+str(timestep)+".png")
    print("\n\nIGURE SAVED IN FOLDER\n\n")
    plt.show()
    plt.close()
    plotGrids()
    #THIS TO TAKE OUT DEAD PEOPLE FROM THE WORLD.
    deaths = death2
print("Done")

# FOR STATISTICS.
print("\n\n\n INFECTION,POPULATION, DEATHS, IMMUNITY, RECOVERY BEHAVIOURS AS A LINE GRAPH\n\n\n")
xlabel =[i for i in range(len(stat_infected))]
print(xlabel)
print(stat_infected)
print(stat_uninfected)
print(stat2_deaths)
print(stat2_immunes)
print(stat2_recovers)

plt.figure(figsize=(20,2))
plt.title("INFECTION,POPULATION BEHAVIOUR. INFECTECTION = RED COLOR ,POPULATION = BLUE COLOR" )
plt.plot(xlabel, stat_infected, 'r',linewidth = 3,label="INFECTED/INFECTION")
plt.plot(xlabel, stat_uninfected, 'b', linewidth =3,label="UNINFECTED/UNINFECTION")
plt.plot(xlabel, stat2_deaths, 'black',linestyle='-',linewidth=2,label="DEATH-BLACK LINE")
plt.plot(xlabel, stat2_immunes, 'darkgreen',linestyle='--', linewidth= 2,label="IMMUNITY- DARKGREEN COLOR LINE")
plt.plot(xlabel, stat2_recovers, 'aqua',linestyle =':',linewidth=2, label="RECOVERY- AQUA COLOR LINE")
plt.legend()
A = 'STATISTICS OUTPUT_IMAGE'                                                                                                                     
plt.savefig(A)
print("FIGURE FOR STATISTICS IS SAVE AS:-", A)
#plt.close()
plt.show()

