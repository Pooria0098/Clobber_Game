# Clobber_Game
Final AI Project
<br/><hr/>
![](Capture.PNG)
<br/><hr/>
Instaltion:<br/>
1) add dependency: pip install pygame==2.0.1<br/>
2) run python with below descriptions<br/>
python clobber.py dim1 dim2 opt<br/>
dim1 = num of rows between [1 to 25]<br/>
dim2 = num of cols between[2 to 25]<br/>
opt = 1: comp will choose to clobber a stone from the largest connected component of white stones<br/>
opt = 2: comp will choose to clobber a stone from the smallest connected component of white stones<br/>
opt = 3: comp will randomly choose a white stone to clobber<br/>
default: 6x5 board, opt = 1
