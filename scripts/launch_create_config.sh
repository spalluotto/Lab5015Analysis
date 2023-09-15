###### LYSO813 ######  non irr

# ------ ANGLE 52 --------  
#---- config 50.00 :     LYSO 813 HPK non irr C25          T2

python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_50.00     -e angle52      -ov 3.5   -r 6001
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_50.00     -e angle52      -ov 0.6   -r 6004
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_50.00     -e angle52      -ov 0.8   -r 6005
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_50.00     -e angle52      -ov 1.0   -r 6006
python create_config.py     -t 5     -ml HPK_nonIrr_LYSO813    -c config_50.00     -e angle52      -ov 1.5   -r 6007



###### LYSO 100 056 ###### HPK 25 um irr 2E14    ES2

# ------ ANGLE 52 --------   
#----- config 51.00:     LYSO 100 056 HPK 2E14 25 um     T1     T-40

# -- delayT scan
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -ov 1.25      -e angle52_delayT0b00000111   -r 6008
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -ov 1.25      -e angle52_delayT0b00011111   -r 6010
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -ov 1.25      -e angle52_delayT0b01111111   -r 6011
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -ov 1.25      -e angle52_delayT0b10000001   -r 6012
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -ov 1.25      -e angle52_delayT0b10000111   -r 6013
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -ov 1.25      -e angle52_delayT0b10011111   -r 6014
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -ov 1.25      -e angle52_delayT0b11111111   -r 6015
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -ov 1.25      -e angle52_delayT0b00000111   -r 6016


# -- ov scan
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -e angle52    -ov 0.6         -r 6019
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -e angle52    -ov 0.8         -r 6020
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -e angle52    -ov 1.0         -r 6021
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -e angle52    -ov 1.25        -r 6022
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -e angle52    -ov 1.5         -r 6023
python create_config.py     -t -40     -ml HPK_2E14_LYSO100056    -c config_51.00    -e angle52    -ov 2.0         -r 6024


