import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import os, shutil, glob
 
 
def raw_to_csv(filname):
    base = os.path.splitext(filname)[0]
    newFilename = base + '.csv'
    shutil.copy(filname, newFilename)
 
    with open(newFilename, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(newFilename, 'w') as fout:
        replace = [x.replace("\t", ";") for x in data[5:]]
        fout.writelines(replace)
    return newFilename
 
    for file in glob.glob("*.raw"):
        raw_to_csv(file)
 
 
def load_data(filename):
    print("---------NeW------")
    print(filename)
    data = pd.read_csv(raw_to_csv(filename), delimiter=";")
 
    for column in data:
        data[column] = data[column].astype(str).apply(lambda x: x.replace(",", ".")).astype(float)
 
    data = data.drop(columns=[' Index', '        Seed'])
    print(data.head())
    return data
 
 
def find_limits(data, spacing=0.1):
    min_ = min(data[0])
    max_ = max(data[0])
    for d in data:
        if min(d) < min_:
            min_ = min(d)
        if max(d) > max_:
            max_ = max(d)
    diff = abs(max_ - min_)
    return min_ - diff * spacing, max_ + diff * spacing
 
 
def Plot(plots, labels, colors, desc, name):
    index = 0
    times = 10
 
    plt.figure(figsize=(10, 8), dpi=80)
 
    for plot in plots:
        try:
            gkde = stats.gaussian_kde(dataset=plot)
 
            plt.plot(x, gkde.evaluate(x)*times, color=colors[index])
            index += 1
        except Exception:
            pass
 
    plt.hist(plots, bins=bins, color=colors, label=labels)
 
    xmin, xmax = find_limits(plots, 0.1)
 
    # print (name + " : " + str(xmin) + ", " + str(xmax))
 
    plt.xlim(xmin, xmax)
    plt.legend()
    # plt.title(desc + "_" + i, )
    plt.xlabel(name, fontsize=12)
 
    plt.savefig("pictures\\" + desc + "_" + name + ".png")
    plt.clf()
    plt.close("all")
 
 
def save_statistics(data: pd.DataFrame):
 
    f = open("result.csv", "w+")
 
    for i in range(0, len(data[0].columns)):
        for compare_data in data[1:]:
            if data[0].columns[i] != compare_data.columns[i]:
                raise Exception("Headers do not match")
 
    str_temp = "Name;"
 
    for _ in range(len(data)):
        str_temp += "Mean;Std;Mean-5Std;Mean+5Std;"
 
    str_temp += "\n"
 
    for column in data[0].columns:
        str_temp += column + ";"
        for files in data:
            mean = np.mean(files[column])
            std = np.std(files[column])
            str_temp += str(round(mean, 3)) + ";" + str(round(std, 3)) + ";" + str(round(mean-std * 5, 2)) + ";" + str(round(mean + std * 5, 2)) + ";"
        str_temp += "\n"
 
    f.write(str_temp.replace(".", ","))
 
    f.close()
 
 
# -------start---------
# INPUT!!!
files = {
    "Normal": "E8126460_CM_Normal.raw",
    "Uniform": "E8126460_CM_Uniform.raw"
    }
 
# Main
 
data = [load_data("data\\" + i) for i in files.values()]
 
save_statistics(data)
 
x = np.linspace(start=stats.norm.ppf(0.01), stop=stats.norm.ppf(0.99), num=250)
 
bins = 40
 
for i in data[0].columns:
    Plot([data[0][i], data[1][i]], [i for i in files], ['blue', 'red'], "Compare", i)
 
print("DONE")