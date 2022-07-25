from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import patchsim as sim
import os
import plotly.express as px


def index(request):
    
    return render(request, 'simulation/index.html')

def graph(request):
    if request.method == 'POST':
        exposure = request.POST["Exposure"]
        cd = os.getcwd()
        openfile = cd + '\\simulation\\tests\\IND_admin1_radiation_constant_0.05_normalized.patchsim'
        popfile = cd + '\\simulation\\tests\\IND_admin1_population.patchsim'
        cfgfile = cd + '\\simulation\\tests\\sample.cfg'
        seedfile = cd + '\\simulation\\tests\\seed.txt'

        cfg = sim.read_config(cfgfile)

        cfg['PatchFile'] = popfile
        cfg['NetworkFile'] = openfile
        cfg['SeedFile'] = seedfile
        cfg['ExposureRate'] = exposure
        dfh = sim.run_disease_simulation(cfg, return_epi=True,write_epi=True)
        fig =px.line(dfh.sum())
        fig.write_html(cd + "\\simulation\\templates\\simulation\\file.html")
        return render(request, 'simulation/file.html')
