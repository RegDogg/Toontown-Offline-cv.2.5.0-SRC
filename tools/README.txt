Steps to Dump TTOffGame.pyd Source Code

1. Install Immunity Debugger (https://www.immunityinc.com/products/debugger/index.html)
2. Copy (dump_files.py) to your Immunity Debugger program folder
3. Run Immunity Debugger AS ADMINISTRATOR (Or it won't save the dumped files)
4. Open (ppython.exe) from Panda3D-1.8.1 in Immunity Debugger so its automatically attached to the game
5. Import GameStart.pyc
6. Run the Program if it is stopped automatically in Immunity Debugger
7. Click the 3rd box in the tab below the "View" Button
8. Scroll down to find (dump_files.py)
9 Double Click it and click Ok when it shows "PyCommand Extra Arguments"
10. Goto your Immunity Debugger root folder, and voila! The Files have been Dumped from TTOffGame.pyd
