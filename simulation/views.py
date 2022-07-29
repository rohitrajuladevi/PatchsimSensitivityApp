from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import patchsim as sim
import os
import pandas as pd
import numpy as np
import plotly.express as px

def entropy(values):
    values=values[values > 0 ]
    values= values[~np.isnan(values)]
    values = values/np.sum(values)
    ent = np.sum([-v*np.log(v) for v in values])
    return(ent)

def index(request):
    listofcon = ['CZE',
    'VUT',
    'CPV',
    'LBY',
    'SLV',
    'MLI',
    'XNC',
    'CAN',
    'BDI',
    'NPL',
    'SEN',
    'PER',
    'DEU',
    'KOR',
    'WSM',
    'CHL',
    'HRV',
    'MLT',
    'GUM',
    'BRA',
    'AGO',
    'POL',
    'HUN',
    'MSR',
    'YEM',
    'MRT',
    'GRC',
    'CUB',
    'NRU',
    'BEL',
    'PYF',
    'THA',
    'GBR',
    'MKD',
    'VNM',
    'BTN',
    'ZAF',
    'ARE',
    'AZE',
    'URY',
    'COG',
    'BRB',
    'WLF',
    'PAK',
    'TKL',
    'JEY',
    'IDN',
    'SWE',
    'TON',
    'GAB',
    'HTI',
    'PRI',
    'HKG',
    'GNB',
    'TWN',
    'GRD',
    'NER',
    'GUY',
    'MYS',
    'SYC',
    'ISL',
    'BMU',
    'PSE',
    'CMR',
    'GNQ',
    'MNE',
    'GEO',
    'CHN',
    'SDN',
    'AND',
    'UGA',
    'KWT',
    'LTU',
    'CYP',
    'MDA',
    'SYR',
    'VGB',
    'COL',
    'LAO',
    'NZL',
    'TLS',
    'MOZ',
    'GTM',
    'CAF',
    'TGO',
    'BLZ',
    'TTO',
    'DOM',
    'TKM',
    'DJI',
    'DNK',
    'TJK',
    'MMR',
    'UKR',
    'EST',
    'ESP',
    'MYT',
    'GHA',
    'BWA',
    'BHR',
    'FRO',
    'LIE',
    'PRY',
    'LVA',
    'ASM',
    'ETH',
    'GIN',
    'BOL',
    'ARG',
    'PLW',
    'LBR',
    'ITA',
    'NIC',
    'COM',
    'TUV',
    'TZA',
    'TUR',
    'FJI',
    'ALA',
    'KHM',
    'ECU',
    'OMN',
    'CRI',
    'UZB',
    'XKO',
    'KAZ',
    'CHE',
    'VCT',
    'ROU',
    'MUS',
    'GMB',
    'SLE',
    'BES',
    'KNA',
    'ISR',
    'REU',
    'GGY',
    'GUF',
    'MTQ',
    'BHS',
    'TCD',
    'SWZ',
    'KGZ',
    'NCL',
    'IRL',
    'CIV',
    'FIN',
    'VEN',
    'PNG',
    'MWI',
    'MAC',
    'NOR',
    'MNG',
    'SMR',
    'SHN',
    'MDG',
    'SUR',
    'KEN',
    'SGP',
    'ERI',
    'STP',
    'USA',
    'ALB',
    'IND',
    'NLD',
    'PAN',
    'MAR',
    'MEX',
    'PRT',
    'SVN',
    'ZWE',
    'PHL',
    'BFA',
    'SLB',
    'LSO',
    'AUS',
    'COD',
    'RWA',
    'IRQ',
    'JOR',
    'SAU',
    'TCA',
    'SSD',
    'BLR',
    'MNP',
    'BGR',
    'AFG',
    'SRB',
    'ARM',
    'NAM',
    'LCA',
    'ESH',
    'DMA',
    'LKA',
    'HND',
    'BEN',
    'GLP',
    'DZA',
    'BRN',
    'JPN',
    'FSM',
    'BIH',
    'SOM',
    'ATG',
    'EGY',
    'LUX',
    'NGA',
    'BGD',
    'QAT',
    'SVK',
    'GRL',
    'CYM',
    'LBN',
    'ZMB',
    'AUT',
    'TUN',
    'IRN',
    'IMN',
    'FRA',
    'VIR',
    'JAM',
    'RUS',
    'PRK']
    listofcon.sort()
    context = {"countries": listofcon}
    return render(request, 'simulation/index.html', context)

def graph(request):
    if request.method == 'POST':

        scale = 0.0001

        exposure = request.POST["Exposure"]
        admin = request.POST["Admin"]
        radiation = request.POST["Radiation"]
        country = request.POST["Country"]
        n = request.POST["Skew"]
        n = int(n)
        cd = os.getcwd()
        
        # openfile = cd + '\\simulation\\tests\\IND_admin1_radiation_constant_0.05_normalized.patchsim'
        # popfile = cd + '\\simulation\\tests\\IND_admin1_population.patchsim'
        popfile = "https://raw.githubusercontent.com/NSSAC/patchflow-data/main/data/v1.0/"+country+"/"+country+"_admin"+admin+"_population.patchsim"
        openfile = "https://raw.githubusercontent.com/NSSAC/patchflow-data/main/data/v1.0/"+country+"/"+country+"_admin"+admin+"_radiation_constant_"+radiation+"_normalized.patchsim"
        cfgfile = cd + '\\simulation\\tests\\sample.cfg'
        seedfile = cd + '\\simulation\\tests\\seed.txt'
        
        dfcleanpop = pd.read_csv(popfile, sep=' ', header = None)
        total_pop = dfcleanpop[1].sum()
        scaled_pop = int(total_pop*scale)
        seed_names=np.asarray(dfcleanpop[0])
        populations=np.asarray(dfcleanpop[1])
        populations = np.nan_to_num(populations)

        prob = (populations**n)/(populations**n).sum()


        seedfl = open(seedfile,"w")

        for i in range(len(seed_names)):
            seedfl.write('0'+" "+seed_names[i]+" "+str(int(prob[i]*scaled_pop))+'\n')
        seedfl.close()
    
        
        

        cfg = sim.read_config(cfgfile)


        cfg['PatchFile'] = popfile
        cfg['NetworkFile'] = openfile
        cfg['SeedFile'] = seedfile
        cfg['ExposureRate'] = exposure




        dfh = sim.run_disease_simulation(cfg, return_epi=True,write_epi=True)
        ent = entropy(dfh.sum())

        fig =px.line(dfh.sum(), title = 'Total Number of Cases Per Day for '+country+', Epidemic Entropy: '+str(round(ent, 3))).update_layout(
        xaxis_title="Number of Days", yaxis_title="New Cases")

        fig.write_html(cd + "\\simulation\\templates\\simulation\\file.html")
        return render(request, 'simulation/file.html')
