# ������������� Piet
������ 0.1.0

�����: �������� ����� (pavelcherentsov23@gmail.com)

����� ���������: ������ ������ ���������


## ��������
������������� �������������� ����� ���������������� Piet. �� ���� ��������� 
��������� �� ����� Piet, �� ����� ��������� ��������� ���������� ���������.
������������: http://www.dangermouse.net/esoteric/piet.html

## ����������
* Python ������ �� ���� 3.6
* Pillow ������ 1.1.7


## ������
* ���������� ������: `piet_interp.py`
* ������: `modules/`
* ������� ���������: `programs/`
* �����: `tests/` 


## ����������� ������
������� �� �������: `py piet_interp.py --help`

������ �������: `py piet_interp.py HelloWorld.png`
������ ������� c ������� ���������� ����������: `py piet_interp.py HelloWorld.png --trace`


## ����������� ����������
������, ���������� �� ������ ��������������, ����������� � ������ modules.
�� ������ ������ (`modules`) �������� �����, �� ����� ����� � `tests/`.
�������� �� ������� ���������� ����� 92%:

    Name                          Stmts   Miss  Cover
    -------------------------------------------------
    modules\CodelChooser.py           9      0   100%
    modules\ColorTable.py            21      0   100%
    modules\Direction.py              1      0   100%
    modules\DirectionPointer.py       8      0   100%
    modules\Function.py              59      2    97%
    modules\Interpreter.py          189     25    87%
    modules\Point.py                 10      1    90%
    modules\Stack.py                 13      5    62%
    piet_interp.py                   18     11    39%
    tests\test_all.py               226      1    99%
    -------------------------------------------------
    TOTAL                           554     45    92%

    
    
    
    
