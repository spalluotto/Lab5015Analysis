#---- config 3.00 :     LYSO 528 HPK non irr           T2
python create_config.py -r 66353-66395,66418-66447              -t 12   -ov 3.5     -ml HPK_nonIrr_C15_LYSO528
python create_config.py -r 66396-66413,66414-66417,66448-66461  -t 12   -ov 1.5     -ml HPK_nonIrr_C15_LYSO528
python create_config.py -r 66462-66479,66482-66515              -t 12   -ov 1.0     -ml HPK_nonIrr_C15_LYSO528
python create_config.py -r 66516-66539                          -t 12   -ov 2.0     -ml HPK_nonIrr_C15_LYSO528


#----- config 4.00 :    LYSO 813 HPK non irr 25 um     T2
python create_config.py -r 66542-66597,66882-66888              -t 12   -ov 3.5     -ml HPK_nonIrr_C25_LYSO813
python create_config.py -r 66598-66653,66889-66895              -t 12   -ov 1.5     -ml HPK_nonIrr_C25_LYSO813
python create_config.py -r 66654-66709,66878-66881,66896-66902  -t 12   -ov 1.0     -ml HPK_nonIrr_C25_LYSO813
python create_config.py -r 66710-66765,66903-66909              -t 12   -ov 2.0     -ml HPK_nonIrr_C25_LYSO813
python create_config.py -r 67124-67163                          -t 12   -ov 0.8     -ml HPK_nonIrr_C25_LYSO813
python create_config.py -r 67092-67123                          -t 12   -ov 0.5     -ml HPK_nonIrr_C25_LYSO813


# - angle 64
python create_config.py -r 66918-66977                          -t 12   -ov 3.5     -ml HPK_nonIrr_C25_LYSO813 -e angle64
python create_config.py -r 66978-67018                          -t 12   -ov 1.5     -ml HPK_nonIrr_C25_LYSO813 -e angle64
python create_config.py -r 67019-67050                          -t 12   -ov 0.5     -ml HPK_nonIrr_C25_LYSO813 -e angle64
python create_config.py -r 67051-67090                          -t 12   -ov 0.8     -ml HPK_nonIrr_C25_LYSO813 -e angle64



#----- config 5.00 :    LYSO 818 HPK non irr 25 um     T1
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 3.5        -r 67164-67203
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 1.5        -r 67204-67243
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 0.5        -r 67244-67279
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 0.8        -r 67280-67319

# - angle 64
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 3.5        -r 67330-67369 -e angle64
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 1.5        -r 67370-67412 -e angle64 
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 0.5        -r 67413-67445 -e angle64
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 0.8        -r 67460-67505 -e angle64 # run presi la mattina dopo

# - angle 32
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 3.5        -r 67506-67544 -e angle32
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 3.5        -r 67545-67547 -e angle32_check

python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 1.5        -r 67548-67587 -e angle32

python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 0.5        -r 67588-67592,67593-67512 -e angle32
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO818    -ov 0.8        -r 67613-67636 -e angle32



#----- config 6.00 :    LYSO 816 HPK non irr 25 um     T3

python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO816    -ov 3.5        -r 67641-67660
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO816    -ov 1.5        -r 67661-67680
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO816    -ov 0.5        -r 67681-67696
python create_config.py  -t 12      -ml HPK_nonIrr_C25_LYSO816    -ov 0.8        -r 67697-67716


