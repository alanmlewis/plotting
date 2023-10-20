# These libraries contain useful tools we will use to load, processes and plot data
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from os.path import splitext
from inspect import getfullargspec
from glob import glob


# This allows us to pass arguments to our program
from sys import argv

# ----------------------------- FITTING OPTIONS --------------------------------------------

# Set fit to True to calculate a fit to the (possibly manipulated) data
fit = False

# Define the form of the function to be fit to the data (default: linear a*x+b)
def func(x,m,c):
    return m*x+c
    
# For a simple exponential fit (delete before giving to students?)
#def func(x,a,b):
#    return b*np.exp(-a*x)
    

# ----------------------------- OUTPUT OPTIONS --------------------------------------------
# Add a unique suffix to the name of each output file
suffix = '_output'


# Set output to True to write the parameters of the line of best fit
# of every processed data file to a single external file.
output = False


# If we are not performing a fit, there will be nothing to output!
if fit == False: output = False

# Set the name of this external file
output_fname = 'fit_data'

# -------------------------------READ IN DATA---------------------------------------------------

# The first argument is always the name of the program; we will remove it
# If the filename is not a csv file, it will be skipped
args = [f for l in argv[1:] for f in glob(l) if f[-4:] == '.csv']
nfiles=len(args)
print('A total of '+str(nfiles)+' csv files will be processed. Any other files will be ignored.')

# We need to collect the fit data for each file we process
if output:
    fit_data = []
    data_fnames = []

i=0
# We will create a plot from every csv file passed to the program
for fname in args:
    i=i+1
    print('Processing file '+str(i)+' of '+str(nfiles))
    # Load the x and y data from the csv file. Note that the column indexes start from 0, not 1.
    try:
        data = np.loadtxt(fname,delimiter=",",skiprows=1)
    except:
        print("Could not process file",fname,". This is probably because it contains text outside of the header line. It has been skipped.")
        continue
    x = data[:,0]
    y = data[:,1]
    
    # Add the name of each file we will process to a list
    if output: data_fnames.append(fname)

    # ----- DATA MANIPULATION --------------------------------------------------------------
    # Uncomment the relevent line from this section or add your own code

    # Convert time from minutes to seconds
    # x = x*60

    # Convert y to ln(y)
    # y = np.log(y) 

    # --------------------------------------------------------------------------------------

    # Calculate a line of best fit, if fit is true. The best fit parameters are stored in variable p.
    if fit:
        fit_params,pcov = curve_fit(func,x,y)
        if output: fit_data.append(fit_params)
    
    # Create the figure
    fig = plt.figure()
    # Create the "Axes", which contains information for the graph
    ax = plt.axes()

    # This creates a line graph, adding a straight line between each point
    # in the input data file
    ax.plot(x,y,label='Data')

    # Add a line of best fit to the plot, if fit is true
    if fit: ax.plot(x,func(x,*fit_params),label='Line of best fit')

    # --------------- PLOTTING DETAILS -----------------------------------------------------
    # Modify the following lines to be appropriate for the graph you are currently plotting

    # Axes labels and units for the x and y axes
    ax.set_xlabel("X axis / units")
    ax.set_ylabel("Y axis / units")
    
    # Set the maximum values of the x and y axes
    # ax.set_xlim([0,200])
    # ax.set_ylim([0.0,1.0])

    # Show a legend
    #ax.legend()

    # Add a title to the graph; by default this is the
    # name of the input data file
    ax.set_title(fname)

    # -------------------------------CREATE OUTPUT FILES-------------------------------------------------------

    fig.savefig(splitext(fname)[0]+suffix+".png")

# Output the parameters of the line of best fit for every file processed if output enabled
params = getfullargspec(func)[0][1:]
if output and len(data_fnames)>0: np.savetxt(output_fname+suffix+'.csv',np.vstack((data_fnames,np.array(fit_data).T)).T,delimiter=',',header='File Name,'+','.join(params),comments='',fmt="%s")
if nfiles > 0: print('All files processed')
