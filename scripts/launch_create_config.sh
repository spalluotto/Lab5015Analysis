# --- CONFIG number is not used at the end because at FNAL data taken all with same disc_calibration.tsv

#---- config 3.00 :     LYSO 528 HPK non irr           T2
python create_config.py -r 66353-66395,66418-66447              -t 12   -ov 3.5     -ml HPK_nonIrr_LYSO528     -c config_3.00   -e angle52 
python create_config.py -r 66396-66413,66414-66417,66448-66461  -t 12   -ov 1.5     -ml HPK_nonIrr_LYSO528     -c config_3.00   -e angle52
python create_config.py -r 66462-66479,66482-66515              -t 12   -ov 1.0     -ml HPK_nonIrr_LYSO528     -c config_3.00   -e angle52
python create_config.py -r 66516-66539                          -t 12   -ov 2.0     -ml HPK_nonIrr_LYSO528     -c config_3.00   -e angle52


#----- config 4.00 :    LYSO 813 HPK non irr 25 um     T2
python create_config.py -r 66542-66597,66882-66888              -t 12   -ov 3.5     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle52
python create_config.py -r 66598-66653,66889-66895              -t 12   -ov 1.5     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle52
python create_config.py -r 66654-66709,66878-66881,66896-66902  -t 12   -ov 1.0     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle52
python create_config.py -r 66710-66765,66903-66909              -t 12   -ov 2.0     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle52
python create_config.py -r 67124-67163                          -t 12   -ov 0.8     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle52
python create_config.py -r 67092-67123                          -t 12   -ov 0.5     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle52


# - angle 64
python create_config.py -r 66918-66977                          -t 12   -ov 3.5     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle64
python create_config.py -r 66978-67018                          -t 12   -ov 1.5     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle64
python create_config.py -r 67019-67050                          -t 12   -ov 0.5     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle64
python create_config.py -r 67051-67090                          -t 12   -ov 0.8     -ml HPK_nonIrr_LYSO813     -c config_4.00   -e angle64



#----- config 5.00 :    LYSO 818 HPK non irr 25 um     T1
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 3.5        -r 67164-67203                    -c config_5.00   -e angle52
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 1.5        -r 67204-67243                    -c config_5.00   -e angle52
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 0.5        -r 67244-67279                    -c config_5.00   -e angle52
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 0.8        -r 67280-67319                    -c config_5.00   -e angle52

# - angle 64
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 3.5        -r 67330-67369                    -c config_5.00    -e angle64
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 1.5        -r 67370-67412                    -c config_5.00    -e angle64 
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 0.5        -r 67413-67445                    -c config_5.00    -e angle64
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 0.8        -r 67460-67505                    -c config_5.00    -e angle64 # run presi la mattina dopo

# - angle 32
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 3.5        -r 67506-67544                    -c config_5.00     -e angle32
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 3.5        -r 67545-67547                    -c config_5.00     -e angle32_check

python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 1.5        -r 67548-67587                    -c config_5.00     -e angle32

python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 0.5        -r 67588-67592,67593-67612        -c config_5.00     -e angle32
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO818    -ov 0.8        -r 67613-67636                    -c config_5.00    -e angle32



#----- config 6.00 :    LYSO 816 HPK non irr 25 um     T3
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO816    -ov 3.5        -r 67641-67660                    -c config_6.00   -e angle52
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO816    -ov 1.5        -r 67661-67680                    -c config_6.00   -e angle52
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO816    -ov 0.5        -r 67681-67696                    -c config_6.00   -e angle52
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO816    -ov 0.8        -r 67697-67716                    -c config_6.00   -e angle52



#----- config 7.00 :    LYSO 814 HPK non irr 20 um     T2 
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO814    -ov 3.5        -c config_7.00   -e angle52             -r 67722-67741
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO814    -ov 1.5        -c config_7.00   -e angle52             -r 67742-67761,67818-67827
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO814    -ov 1.0        -c config_7.00   -e angle52             -r 67762-67781
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO814    -ov 0.5        -c config_7.00   -e angle52             -r 67782-67804
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO814    -ov 0.8        -c config_7.00   -e angle52             -r 67805-67817




#----- config 8.00 :    LYSO 824 HPK non irr 25 um low Cgrid     T2 
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO824 -ov 3.5       -c config_8.00    -e angle52             -r 67842-67861
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO824 -ov 1.5       -c config_8.00    -e angle52             -r 67862-67881
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO824 -ov 0.5       -c config_8.00    -e angle52             -r 67882-67897
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO824 -ov 0.8       -c config_8.00    -e angle52             -r 67898-67917




#----- config 9.00 :    LYSO 828 HPK non irr 25 um     T1 vendor 5
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO828    -ov 3.5        -c config_9.00   -e angle52             -r 67922-67941
python create_config.py  -t 12      -ml HPK_nonIrr_LYSO828    -ov 1.5        -c config_9.00   -e angle52             -r 67942-67959




# -- CHARGE SHARING test

#----- config 10.00 :   LYSO 813 HPK non irr 25 um
