# shortcuts - https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf

# C:\Miniconda3\python.exe - select enviroment 

# settings 

# Preferences: Open Settings (JSON) 
# Python: Select Interpreter 
# Prerferences: Open Workspace Settings
# Python: Run File in Termnal 
# Jupyter: Create Interactive Window 


# create new section in file 
#%% 

#install package 
 C:/Users/joshu/AppData/Local/Programs/Python/Python311/python.exe -m pip install -U numpy

#venv 
conda config --append channels conda-forge
conda create --name pycaret python=3.9
conda activate pycaret
conda install -c conda-forge <package>
!pip install -r requirments.txt

conda install --name pycaret flake8 -y
