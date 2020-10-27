import pandas as pd
import matplotlib.pyplot as plt

# pyqt fix
import sys
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
sys.excepthook = my_exception_hook


def linebar(x, y1, y2, x_label, y1_label="Yield", y2_label="Count", ax1=None):
    if not ax1:
        fig, ax1 = plt.subplots()

    bar_width = 0.5 / len(x)

    # Plot line and bar on same x-axis
    ax2 = ax1.twinx()
    ax1.plot(x, y1, 'ko-')
    ax2.bar(x, y2, width=bar_width)

    # Axis labels
    ax1.set_title(y1_label)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label)
    ax2.set_ylabel(y2_label)

    # PLOT FORMATTING
    # Grid lines
    ax1.grid(linestyle=':')
    # Set axis number format
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.1%}'.format(y)))
    # Set axis angle
    ax1.xaxis.set_tick_params(rotation=0)
    # Set yield axis range
    new_bottom = ax1.get_ylim()[0] - (ax1.get_ylim()[1] - ax1.get_ylim()[0]) * 0.5

    print(ax1.get_ylim()[1] - ax1.get_ylim()[0])
    if (ax1.get_ylim()[1] - ax1.get_ylim()[0]) < 0.03:
        new_bottom = ax1.get_ylim()[1] - 0.03
        print(new_bottom)

    print(ax1.get_ylim()[0], ax1.get_ylim()[1])

    ax1.set_ylim(bottom=new_bottom)
    # Reduce bar height
    ax2.set_ylim(top=ax2.get_ylim()[1] * 5)

    ax1.xaxis.set_tick_params(labelbottom=True)

    # Reference lines
    TGT = 4.15
    LSL = 3.37
    USL = 5.22

    ax1.vlines(TGT, 0, 1, colors='g')
    ax1.vlines([LSL, USL], 0, 1, colors='r')

def function_pack(df):
    colnames = df.columns

    if 'Lot5' in colnames:
        pass
    elif 'Data Lot' in colnames:
        df['Lot5'] = df['Data Lot'].str[:5]
    elif 'UNIT_SERIAL_NUMBER' in colnames:
        df['Lot5'] = df.UNIT_SERIAL_NUMBER.str[:5]

    return df

def percentage_of_group(df, variable, groups):
    '''
    Proportion of each variable value within each possible combo of groups values
    '''
    if type(groups)!=type([]):
        groups = [groups]


    # Calculate the count of each variable value within each group value combo. The unstack.stack is to get rows with
    # count 0 for group value combos that don't actually appear in the data.
    group_counts = df.groupby([*groups, variable]).size().unstack(fill_value=0).stack()
    group_ratios = group_counts.groupby(groups).apply(
        lambda x: x / x.sum()).rename(variable + " %").reset_index()

    return group_ratios

def load(path):
    # Read dataframe from CSV and attempt to parse every column as a date
    size = len(pd.read_csv(path, nrows=0).columns)
    df = pd.read_csv(path, parse_dates=list(range(0,size)))

path = r'C:\_MyFiles\Projects\VG10 K1 K2 FT Rolloff\VG10_K1_K2_FWET_2017_18.csv'
df = pd.read_csv(path, parse_dates=[1,2,3,4,5])
print(percentage_of_group(df, 'Data Lot','Week'))


import mytimer
import time
T = mytimer.MyTimer()
T.tick()

df = pd.read_csv(path)

T.tick()

size = len(pd.read_csv(path, nrows=0).columns)
df = pd.read_csv(path, parse_dates=list(range(0,size)))

T.tick()

size = len(pd.read_csv(path, nrows=0).columns)
df = pd.read_csv(path, parse_dates=list(range(0,size)), infer_datetime_format=True)

T.tick()

time.sleep(1)

T.tick()

time.sleep(1)

T.tock()
