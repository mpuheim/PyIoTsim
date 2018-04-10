import os, shutil, time

results_directory="results"

for folder in os.listdir(results_directory):
    path = os.path.join(results_directory,folder)
    print("Removing folder '"+path+"'... ",end="")
    time.sleep(0.1)
    shutil.rmtree(path)
    print("Done.")