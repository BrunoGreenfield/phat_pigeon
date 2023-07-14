leaderboardtxt = open("leaderboard.txt", "r+")
leaderboardtxtsp = leaderboardtxt.read().splitlines()
new = leaderboardtxtsp[0::2]

topscore = [i for i in leaderboardtxtsp]

print(leaderboardtxt)
print(topscore)
print(new)