###### LYSO813 ######  non irr

# ------ ANGLE 52 --------  
#---- config 23.00 :     LYSO 813 HPK non irr C25          T2
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 0.8         -r 5473   -e angle52
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 1.5         -r 5474   -e angle52
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 3.5         -r 5475   -e angle52
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 0.5         -r 5476   -e angle52 

#--- angle scan
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 3.5         -r 5477  -e angle52
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 3.5         -r 5478  -e angle40
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 3.5         -r 5479  -e angle30
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 3.5         -r 5480  -e angle20
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 3.5         -r 5481  -e angle10
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 3.5         -r 5482  -e angle0
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_23.00     -ov 3.5         -r 5483  -e angle350





###### LYSO815 ######    HPK 25 um irr 2E14

# ------ ANGLE 52 --------
#----- config 24.00:     LYSO 815 HPK 2E14  25um       T2      T-40
python create_config.py     -t -40     -ml HPK_2E14_LYSO815    -c config_24.00    -ov 1.0       -r 5487        -e angle52         
python create_config.py     -t -40     -ml HPK_2E14_LYSO815    -c config_24.00    -ov 2.0       -r 5488        -e angle52   
python create_config.py     -t -40     -ml HPK_2E14_LYSO815    -c config_24.00    -ov 1.5       -r 5489,5490   -e angle52   
python create_config.py     -t -40     -ml HPK_2E14_LYSO815    -c config_24.00    -ov 1.25      -r 5491        -e angle52
python create_config.py     -t -40     -ml HPK_2E14_LYSO815    -c config_24.00    -ov 0.6       -r 5492        -e angle52
python create_config.py     -t -40     -ml HPK_2E14_LYSO815    -c config_24.00    -ov 0.8       -r 5493        -e angle52


#----- config 24.03:     LYSO 815 HPK 2E14         T2      T-35
python create_config.py     -t -35     -ml HPK_2E14_LYSO815    -c config_24.03    -ov 1.5       -r 5501     -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO815    -c config_24.03    -ov 1.25      -r 5502     -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO815    -c config_24.03    -ov 1.0       -r 5503     -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO815    -c config_24.03    -ov 0.8       -r 5504     -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO815    -c config_24.03    -ov 0.6       -r 5505     -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO815    -c config_24.03    -ov 2.0       -r 5506     -e angle52


#----- config 24.04:     LYSO 815 HPK 2E14         T2      T-30
python create_config.py     -t -30      -ml HPK_2E14_LYSO815    -c config_24.04    -ov 0.6      -r 5507   -e angle52
python create_config.py     -t -30      -ml HPK_2E14_LYSO815    -c config_24.04    -ov 0.8      -r 5508   -e angle52
python create_config.py     -t -30      -ml HPK_2E14_LYSO815    -c config_24.04    -ov 1.0      -r 5509   -e angle52
python create_config.py     -t -30      -ml HPK_2E14_LYSO815    -c config_24.04    -ov 1.25     -r 5510   -e angle52
python create_config.py     -t -30      -ml HPK_2E14_LYSO815    -c config_24.04    -ov 1.5      -r 5511   -e angle52
python create_config.py     -t -30      -ml HPK_2E14_LYSO815    -c config_24.04    -ov 2.0      -r 5512   -e angle52



# ------ ANGLE 64 --------
#----- config 24.10:     LYSO 815 HPK 2E14         T2      T-35  
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.10    -ov 2.0      -r 5513     -e angle64
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.10    -ov 1.5      -r 5514     -e angle64
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.10    -ov 1.25     -r 5515     -e angle64
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.10    -ov 1.0      -r 5516     -e angle64
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.10    -ov 0.8      -r 5517     -e angle64
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.10    -ov 0.6      -r 5518     -e angle64
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.10    -ov 1.5      -r 5519     -e angle64_long



# ------ ANGLE 32 --------
#----- config 24.11:     LYSO 815 HPK 2E14         T2      T-35  
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.11    -ov 0.6      -r 5520     -e angle32
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.11    -ov 0.8      -r 5521     -e angle32
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.11    -ov 1.0      -r 5522     -e angle32
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.11    -ov 1.25     -r 5523     -e angle32
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.11    -ov 1.5      -r 5524     -e angle32
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.11    -ov 2.0      -r 5525     -e angle32
python create_config.py     -t -35      -ml HPK_2E14_LYSO815    -c config_24.11    -ov 1.5      -r 5526     -e angle32_long





#### LYSO825 #####    HPK 20 um  irr 2E14
# ------ ANGLE 52 --------
#----- config 25.00:     LYSO 825 HPK 2E14  20um       T2      T-40
python create_config.py     -t -40     -ml HPK_2E14_LYSO825    -c config_25.00    -ov 0.6        -r 5528        -e angle52
python create_config.py     -t -40     -ml HPK_2E14_LYSO825    -c config_25.00    -ov 0.8        -r 5529        -e angle52
python create_config.py     -t -40     -ml HPK_2E14_LYSO825    -c config_25.00    -ov 1.0        -r 5530        -e angle52
python create_config.py     -t -40     -ml HPK_2E14_LYSO825    -c config_25.00    -ov 1.25       -r 5531,5532   -e angle52
python create_config.py     -t -40     -ml HPK_2E14_LYSO825    -c config_25.00    -ov 1.5        -r 5533,5535   -e angle52
python create_config.py     -t -40     -ml HPK_2E14_LYSO825    -c config_25.00    -ov 2.0        -r 5534        -e angle52
python create_config.py     -t -40     -ml HPK_2E14_LYSO825    -c config_25.00    -ov 2.5        -r 5536,5537   -e angle52

#----- config 25.01:     LYSO 825 HPK 2E14  20um       T2      T-35
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.01    -ov 0.6        -r 5538       -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.01    -ov 0.8        -r 5539       -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.01    -ov 1.0        -r 5540       -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.01    -ov 1.25       -r 5541       -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.01    -ov 1.5        -r 5542       -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.01    -ov 2.0        -r 5543       -e angle52
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.01    -ov 2.5        -r 5544,5545  -e angle52


#----- config 25.02:     LYSO 825 HPK 2E14  20um       T2      T-30
python create_config.py     -t -30     -ml HPK_2E14_LYSO825    -c config_25.02    -ov 0.6        -r 5546        -e angle52
python create_config.py     -t -30     -ml HPK_2E14_LYSO825    -c config_25.02    -ov 0.8        -r 5547,5548   -e angle52
python create_config.py     -t -30     -ml HPK_2E14_LYSO825    -c config_25.02    -ov 1.0        -r 5549        -e angle52
python create_config.py     -t -30     -ml HPK_2E14_LYSO825    -c config_25.02    -ov 1.25       -r 5550        -e angle52
python create_config.py     -t -30     -ml HPK_2E14_LYSO825    -c config_25.02    -ov 1.5        -r 5551,5552   -e angle52
python create_config.py     -t -30     -ml HPK_2E14_LYSO825    -c config_25.02    -ov 2.0        -r 5553        -e angle52
python create_config.py     -t -30     -ml HPK_2E14_LYSO825    -c config_25.02    -ov 2.5        -r 5554        -e angle52

# ------ ANGLE 64 --------  
#----- config 25.03:     LYSO 825 HPK 2E14  20um       T2      T-35  
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.03    -ov 0.6        -r 5555       -e angle64
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.03    -ov 0.8        -r 5556       -e angle64
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.03    -ov 1.0        -r 5557       -e angle64
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.03    -ov 1.25       -r 5558       -e angle64
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.03    -ov 1.5        -r 5559       -e angle64
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.03    -ov 2.0        -r 5560       -e angle64
python create_config.py     -t -35     -ml HPK_2E14_LYSO825    -c config_25.03    -ov 2.5        -r 5561       -e angle64




##-----LYSO819 #####    HPK 25 um  irr 1E14 T1
#------ ANGLE 52 --------

#----- config 27.00:     LYSO 819 HPK 1E14  25um       T1      T-32
# -- delayT scan
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.25        -r 5565         -e delayT0b01111111
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.25        -r 5566         -e delayT0b00111111
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.25        -r 5567         -e delayT0b00011111
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.25        -r 5568         -e delayT0b00001111
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.25        -r 5569         -e delayT0b00000111
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.25        -r 5570         -e delayT0b00000011
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.25        -r 5571         -e delayT0b00000001


# -- ov scan
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 2.5            -r 5572       -e self-heating
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 0.6            -r 5573       -e angle52
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 0.8            -r 5574,5575  -e angle52
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.0            -r 5576,5577  -e angle52
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.25           -r 5578       -e angle52
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 1.5            -r 5579,5580  -e angle52
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 2.0            -r 5581       -e angle52
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.00    -ov 2.5            -r 5582       -e angle52



#----- config 27.01:     LYSO 819 HPK 1E14  25um       T1      T-37
# -- delayT scan 

python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.25        -r 5583         -e delayT0b01111111
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.25        -r 5584         -e delayT0b00111111
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.25        -r 5586,5587,5588         -e delayT0b00011111
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.25        -r 5589         -e delayT0b00001111
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.25        -r 5590         -e delayT0b00000111
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.25        -r 5591         -e delayT0b00000011
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.25        -r 5592         -e delayT0b00000001


# -- ov scan
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 0.6            -r 5593        -e angle52
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 0.8            -r 5594,5595   -e angle52
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.0            -r 5596        -e angle52
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.25           -r 5597        -e angle52
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 1.5            -r 5598        -e angle52
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 2.0            -r 5599        -e angle52
python create_config.py     -t -37     -ml HPK_1E14_LYSO819    -c config_27.01    -ov 2.5            -r 5600,5601   -e angle52


#----- config 27.02:     LYSO 819 HPK 1E14  25um       T1      T-27 
# -- delayT scan  
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.25        -r 5602         -e delayT0b01111111
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.25        -r 5603         -e delayT0b00111111
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.25        -r 5604         -e delayT0b00011111
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.25        -r 5605         -e delayT0b00001111
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.25        -r 5606         -e delayT0b00000111
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.25        -r 5607         -e delayT0b00000011
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.25        -r 5608         -e delayT0b00000001


# -- ov scan 
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 0.6            -r 5609        -e angle52
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 0.8            -r 5610        -e angle52
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.0            -r 5611,5612   -e angle52
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.25           -r 5613        -e angle52
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 1.5            -r 5614        -e angle52
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 2.0            -r 5616,5617   -e angle52
python create_config.py     -t -27     -ml HPK_1E14_LYSO819    -c config_27.02    -ov 2.5            -r 5618        -e angle52


#----- config 27.03:     LYSO 819 HPK 1E14  25um       T1      T-22
# -- ov scan  
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.03    -ov 0.6            -r 5619        -e angle52
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.03    -ov 0.8            -r 5620        -e angle52
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.03    -ov 1.0            -r 5621        -e angle52
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.03    -ov 1.25           -r 5622,5623   -e angle52
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.03    -ov 1.5            -r 5624        -e angle52
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.03    -ov 2.0            -r 5625,5626   -e angle52
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.03    -ov 2.5            -r 5627        -e angle52





# ------ ANGLE 64 -------- 
#----- config 27.04:     LYSO 819 HPK 1E14  25um       T1      T-32
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.04     -ov 0.6            -r 5628        -e angle64
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.04     -ov 0.8            -r 5629        -e angle64
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.04     -ov 1.0            -r 5630        -e angle64
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.04     -ov 1.25           -r 5631        -e angle64
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.04     -ov 1.5            -r 5632        -e angle64
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.04     -ov 2.0            -r 5633        -e angle64
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.04     -ov 2.5            -r 5634,5635   -e angle64





#----- config 27.06:     LYSO 819 HPK 1E14  25um       T1      T-22 
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.06     -ov 0.6            -r 5636       -e angle64
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.06     -ov 0.8            -r 5637       -e angle64
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.06     -ov 1.0            -r 5638,5639  -e angle64
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.06     -ov 1.25           -r 5640       -e angle64
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.06     -ov 1.5            -r 5641,5642  -e angle64
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.06     -ov 2.0            -r 5643       -e angle64
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.06     -ov 2.5            -r 5644,5645  -e angle64




# ------ ANGLE 32 --------   
#----- config 27.08:     LYSO 819 HPK 1E14  25um       T1      T-22      
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.08     -ov 0.6            -r 5646,5647  -e angle32
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.08     -ov 0.8            -r 5648       -e angle32
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.08     -ov 1.0            -r 5649,5650  -e angle32
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.08     -ov 1.25           -r 5651       -e angle32
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.08     -ov 1.5            -r 5652       -e angle32
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.08     -ov 2.0            -r 5653       -e angle32
python create_config.py     -t -22     -ml HPK_1E14_LYSO819    -c config_27.08     -ov 2.5            -r 5654       -e angle32



#----- config 27.09:     LYSO 819 HPK 1E14  25um       T1      T-32 
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.09     -ov 0.6            -r 5655       -e angle32
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.09     -ov 0.8            -r 5656,5658  -e angle32
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.09     -ov 1.0            -r 5659       -e angle32
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.09     -ov 1.25           -r 5660       -e angle32
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.09     -ov 1.5            -r 5661,5662  -e angle32
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.09     -ov 2.0            -r 5663       -e angle32
python create_config.py     -t -32     -ml HPK_1E14_LYSO819    -c config_27.09     -ov 2.5            -r 5664       -e angle32







#### LYSO829 #####    HPK 25 um  irr 1E13 T1
# ------ ANGLE 52 --------

# #----- config 28.00:     LYSO 829 HPK 1E13  25um       T1      T-19
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.00      -ov 3.0           -r 5665            -e angle52
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.00      -ov 0.8           -r 5666            -e angle52
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.00      -ov 1.5           -r 5667,5668       -e angle52
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.00      -ov 2.0           -r 5669,5670,5671  -e angle52


#----- config 28.01:     LYSO 829 HPK 1E13  25um       T1      T-32
python create_config.py     -t -32     -ml HPK_1E13_LYSO829    -c config_28.01      -ov 0.8           -r 5673            -e angle52
python create_config.py     -t -32     -ml HPK_1E13_LYSO829    -c config_28.01      -ov 1.5           -r 5675            -e angle52
python create_config.py     -t -32     -ml HPK_1E13_LYSO829    -c config_28.01      -ov 2.0           -r 5676            -e angle52
python create_config.py     -t -32     -ml HPK_1E13_LYSO829    -c config_28.01      -ov 3.0           -r 5677            -e angle52


#----- config 28.02:     LYSO 829 HPK 1E13  25um       T1      T 0 
python create_config.py     -t 0       -ml HPK_1E13_LYSO829    -c config_28.02      -ov 0.6           -r 5680            -e angle52
python create_config.py     -t 0       -ml HPK_1E13_LYSO829    -c config_28.02      -ov 0.8           -r 5681,5682       -e angle52
python create_config.py     -t 0       -ml HPK_1E13_LYSO829    -c config_28.02      -ov 1.25          -r 5683            -e angle52
python create_config.py     -t 0       -ml HPK_1E13_LYSO829    -c config_28.02      -ov 1.5           -r 5684            -e angle52
python create_config.py     -t 0       -ml HPK_1E13_LYSO829    -c config_28.02      -ov 2.0           -r 5685            -e angle52
python create_config.py     -t 0       -ml HPK_1E13_LYSO829    -c config_28.02      -ov 2.5           -r 5686            -e angle52


#----- config 28.03:     LYSO 829 HPK 1E13  25um       T1      T 12  
python create_config.py     -t 12      -ml HPK_1E13_LYSO829    -c config_28.03      -ov 0.6           -r 5687,5689       -e angle52
python create_config.py     -t 12      -ml HPK_1E13_LYSO829    -c config_28.03      -ov 0.8           -r 5690,5691       -e angle52
python create_config.py     -t 12      -ml HPK_1E13_LYSO829    -c config_28.03      -ov 1.0           -r 5692            -e angle52
python create_config.py     -t 12      -ml HPK_1E13_LYSO829    -c config_28.03      -ov 1.25          -r 5693            -e angle52


# ------ ANGLE 64 --------   
#----- config 28.04:     LYSO 829 HPK 1E13  25um       T1      T -19
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.04      -e angle64      -ov 0.6           -r 5696
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.04      -e angle64      -ov 0.8           -r 5697
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.04      -e angle64      -ov 1.0           -r 5698,5699
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.04      -e angle64      -ov 1.25          -r 5700
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.04      -e angle64      -ov 1.5           -r 5704,5706
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.04      -e angle64      -ov 2.0           -r 5707,5708
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.04      -e angle64      -ov 2.5           -r 5709,5710

# ------ ANGLE 32 --------   
#----- config 28.06:     LYSO 829 HPK 1E13  25um       T1      T -19
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.06      -e angle32      -ov 0.6           -r 5711,5713
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.06      -e angle32      -ov 0.8           -r 5714
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.06      -e angle32      -ov 1.0           -r 5715
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.06      -e angle32      -ov 1.25          -r 5716
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.06      -e angle32      -ov 1.5           -r 5717,5718
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.06      -e angle32      -ov 2.0           -r 5720,5721
python create_config.py     -t -19     -ml HPK_1E13_LYSO829    -c config_28.06      -e angle32      -ov 2.5           -r 5722







#### LYSO817 #####    HPK 25 um  irr 1E14 T3
# ------ ANGLE 64 --------

# #----- config 29.00:     LYSO 817 HPK 1E14  25um       T3      T-32
python create_config.py     -t -32     -ml HPK_1E14_LYSO817    -c config_29.00     -e angle64       -ov 0.6           -r 5723
python create_config.py     -t -32     -ml HPK_1E14_LYSO817    -c config_29.00     -e angle64       -ov 0.6           -r 5724
python create_config.py     -t -32     -ml HPK_1E14_LYSO817    -c config_29.00     -e angle64       -ov 0.6           -r 5725
python create_config.py     -t -32     -ml HPK_1E14_LYSO817    -c config_29.00     -e angle64       -ov 0.6           -r 5726
python create_config.py     -t -32     -ml HPK_1E14_LYSO817    -c config_29.00     -e angle64       -ov 0.6           -r 5727
python create_config.py     -t -32     -ml HPK_1E14_LYSO817    -c config_29.00     -e angle64       -ov 0.6           -r 5728
python create_config.py     -t -32     -ml HPK_1E14_LYSO817    -c config_29.00     -e angle64       -ov 0.6           -r 5729,5730




#----- config 29.01:     LYSO 817 HPK 1E14  25um       T3      T-22
