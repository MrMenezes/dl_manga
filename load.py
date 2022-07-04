import sys

def print_progress(i):
    loading = "Loading: [----------]"
    sys.stdout.write("\r"+loading+" %d%%" % i)
    if i == 10 or i == 20 or i == 30 or i == 40 or i == 50 or i == 60 or i == 70 or i == 80 or i == 90 or i == 100:
        loading = loading.replace("-","=",1)
    sys.stdout.flush()