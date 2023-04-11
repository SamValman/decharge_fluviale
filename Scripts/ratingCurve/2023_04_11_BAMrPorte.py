# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 09:48:05 2023

@author: lgxsv2
"""


import pandas as pd
import numpy as np 

#%% Data management

fn = r"E:\Mitacs\decharge_fluviale\Scripts\ratingCurve\demoData\rating_curve_HQ.csv"

# this has depth, Q but not width
# Manually add width
# width was added with noise but to correlate very strongly with depth.
wd = pd.read_csv(fn)
wd = wd[wd['Gauge']=='Colpach']
wd = wd.loc[:,['Date', 'Level', 'Q_m3s']]
width = wd.Level*100 + np.random.normal(size=wd.Level.size)
wd['Width']=width

'''
This is normally sorted into a class of BAM_data 
in this case we wont use object orientated programming for now 

It is still lacking the predicted discharge but we can work with this current one for now 
'''




#%% Bam Estimate 
def bam_estimate(data, variant='manning', bampriors=xx):
    
    # variant previously chosen from list based on closest match:
        # options = ("manning", "amhg", "manning_amhg")
        
    # need to work out Bam priors - the function is on anoter sheet.
        # here the function uses Null and then carries out the Bam priors function for that 
        # bampriors <- bam_priors(bamdata, variant = variant)
    bampriors = bam_priors(data, variant=variant)
    print('shh')

#%% The R code
'''
Comment out the code below as it is included into the bam estimate
'''


# bam_estimate <- function(bamdata, 
                         # variant = c("manning", "amhg", "manning_amhg"), 
                         bampriors = NULL, 
                         meas_error = TRUE,
                         reparam = TRUE,
                         cores = getOption("mc.cores", default = parallel::detectCores()),
                         chains = 3L,
                         iter = 1000L,
                         stanmodel = NULL,
                         pars = NULL, 
                         include = FALSE,
                         ...) {
  # variant <- match.arg(variant)
  stopifnot(is(bamdata, "bamdata"))
  if (is.null(bampriors))
    bampriors <- bam_priors(bamdata, variant = variant)
  stopifnot(is(bampriors, "bampriors"))
  
  baminputs <- compose_bam_inputs(bamdata, bampriors)
  
  if (!is.null(stanmodel)) {
    stopifnot(inherits(stanmodel, "stanmodel"))
    stanfit <- stanmodel
  } else {
    stanfit <- stanmodels[["master"]]
  }
  baminputs$meas_err <- ifelse(meas_error && !reparam, 1, 0)
  baminputs$inc_m <- ifelse(variant %in% c("manning", "manning_amhg"), 1, 0)
  baminputs$inc_a <- ifelse(variant %in% c("amhg", "manning_amhg"), 1, 0)
  
  if (is.null(pars)) {
    pars <- c("man_rhs", "amhg_rhs", "logWSpart", 
              "logQtn", "logQnbar",
              "Sact", "Wact", "dAact")
  }
  
  if (reparam && meas_error) {
    logS_sigsq_obs <- ln_sigsq(obs = baminputs$Sobs, err_sigma = baminputs$Serr_sd)
    logW_sigsq_obs <- ln_sigsq(obs = baminputs$Wobs, err_sigma = baminputs$Werr_sd)
    baminputs$sigma_man <- sqrt(baminputs$sigma_man^2 + 
                                  logS_sigsq_obs * (3 / 6)^2 +
                                  logW_sigsq_obs * (4 / 6)^2)
    baminputs$sigma_amhg <- sqrt(baminputs$sigma_amhg^2 +
                                   logW_sigsq_obs)
  }
  
  out <- sampling(stanfit, data = baminputs, 
                  cores = cores, chains = chains, iter = iter,  
                  pars = pars, include = include,
                  ...)
  
  out
}






