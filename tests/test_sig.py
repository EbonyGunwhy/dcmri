import numpy as np
import dcmri as dc


def test_signal_dsc():
    S0 = 1
    TE = 0
    TR = 0
    R2 = 1
    R1 = 1
    S = dc.signal_dsc(R1, R2, S0, TR, TE)
    assert S==0


def test_signal_t2w():
    S0 = 1
    TE = 0
    R2 = 1
    S = dc.signal_t2w(R2, S0, TE)
    assert S==1


def test_signal_ss():
    R1 = 1
    S0 = 1
    TR = 1
    FA = 0
    S = dc.signal_ss(S0, R1, TR, FA)
    assert S==0
    v = [0.5, 0.5]
    try:
        S = dc.signal_ss(S0, R1, TR, FA, v=v)
    except:
        assert True
    else:
        assert False
    R1 = [1,1]
    S = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=np.inf)
    assert S==0
    S = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=0)
    assert S==0
    Fw = [[0,1],[1,0]]
    S = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=Fw)
    assert S==0
    R1 = np.ones((2,10))
    S = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=np.inf)
    assert 0==np.linalg.norm(S)
    S = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=0)
    assert 0==np.linalg.norm(S)

    # Calibrate on other R10 reference
    R1 = 1
    S0 = 5
    TR = 1
    FA = 45
    S = dc.signal_ss(S0, R1, TR, FA, R10=R1)
    assert np.round(S)==5
    R1 = [1,1]
    v = [0.5, 0.5]
    S = dc.signal_ss(S0, R1, TR, FA, v=v, R10=R1, Fw=np.inf)
    assert np.round(S)==5

    # Check exceptions
    try:
        S = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=[1,1])
    except:
        assert True
    else:
        assert False

    try:
        S = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=np.ones((3,3)))
    except:
        assert True
    else:
        assert False

    v = [0.1, 0.4, 0.5]
    try:
        S = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=0)
    except:
        assert True
    else:
        assert False

    R1 = [1,1]
    try:
        S = dc.signal_ss(S0, R1, TR, FA, v=v)
    except:
        assert True
    else:
        assert False

    # Check boundary regimes with flow
    n = 100
    R1 = np.ones((2,n))
    j = np.ones((2,n))
    v = [0.5, 0.5]
    S0 = 1
    TR = 1
    FA = 10

    # No water exchange
    zero = 1e-6
    Fw = [[0.1,zero],[zero,1]]
    S1 = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=Fw, j=j)
    Fw = [[0.1,0],[0,1]]
    S2 = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=Fw, j=j)
    assert np.linalg.norm(S1-S2) < 1e-6*np.linalg.norm(S2)

    # Fast water exchange
    inf = 1e+6
    Fw = np.array([[0.1,inf],[inf,1]])
    S1 = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=Fw, j=j)
    Fw = np.array([[0.1,np.inf],[np.inf,1]])
    S2 = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=Fw, j=j)
    assert np.linalg.norm(S1-S2) < 1e-6*np.linalg.norm(S2)
    Fw = [[0.1,inf],[np.inf,1]]
    try:
        S2 = dc.signal_ss(S0, R1, TR, FA, v=v, Fw=Fw, j=j)
    except:
        assert True
    else:
        assert False
    # assert np.linalg.norm(S1-S2) < 1e-6*np.linalg.norm(S2)


def test_signal_spgr():
    R1 = 1
    S0 = 1
    TR = 1
    FA = 0
    TC = 1
    n = TC/TR
    S = dc.signal_spgr(S0, R1, TC, TR, FA, n0=0)
    assert S==0
   
    v = [0.5, 0.5]
    try:
        S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, n0=0)
    except:
        assert True
    else:
        assert False
    R1 = [1,1]
    S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, n0=0)
    assert S==0
    S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, Fw=0, n0=0)
    assert S==0
    Fw = [[0,1],[1,0]]
    S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, Fw=Fw, n0=0)
    assert S==0
    R1 = np.ones((2,10))
    S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, n0=0)
    assert 0==np.linalg.norm(S)
    S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, Fw=0, n0=0)
    assert 0==np.linalg.norm(S)

    # Check exceptions
    try:
        S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, Fw=[1,1], n0=0)
    except:
        assert True
    else:
        assert False

    v = [0.1, 0.4, 0.5]
    try:
        S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, Fw=0, n0=0)
    except:
        assert True
    else:
        assert False

    R1 = [1,1]
    try:
        S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, n0=0)
    except:
        assert True
    else:
        assert False

    # Calibrate on other R10 reference
    R1 = 1
    S0 = 5
    TR = 1
    FA = 45
    S = dc.signal_spgr(S0, R1, TC, TR, FA, R10=R1, n0=0)
    assert np.round(S)==5
    R1 = [1,1]
    v = [0.5, 0.5]
    S = dc.signal_spgr(S0, R1, TC, TR, FA, v=v, R10=R1, n0=0)
    assert np.round(S)==5

    # With preparation
    R1 = 1
    S0 = 1
    TR = 1
    FA = 0
    TC = 1
    TP = 0
    S = dc.signal_spgr(S0, R1, TC, TR, FA, TP)
    assert S==0
    v = [0.5, 0.5]
    try:
        S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v)
    except:
        assert True
    else:
        assert False
    R1 = [1,1]
    S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v)
    assert S==0
    S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v, Fw=0)
    assert S==0
    Fw = [[0,1],[1,0]]
    S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v, Fw=Fw)
    assert S==0
    R1 = np.ones((2,10))
    S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v)
    assert 0==np.linalg.norm(S)
    S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v, Fw=0)
    assert 0==np.linalg.norm(S)

    # Check exceptions
    try:
        S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v, Fw=[1,1])
    except:
        assert True
    else:
        assert False

    try:
        S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v, Fw=np.ones((3,3)))
    except:
        assert True
    else:
        assert False

    v = [0.1, 0.4, 0.5]
    try:
        S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v, Fw=0)
    except:
        assert True
    else:
        assert False

    R1 = [1,1]
    try:
        S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v)
    except:
        assert True
    else:
        assert False

    # Calibrate on other R10 reference
    R1 = 1
    S0 = 5
    TR = 1
    FA = 45
    S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, R10=R1)
    assert np.round(S)==5
    R1 = [1,1]
    v = [0.5, 0.5]
    S = dc.signal_spgr(S0, R1, TC, TR, FA, TP, v=v, R10=R1)
    assert np.round(S)==5

    # Check convergence to fast exchange


def test_signal_free():
    TC = 0
    R1 = 1
    S0 = 1 
    FA = 45
    S = dc.signal_free(S0, R1, TC, FA, R10=None)
    assert S==0
    TC = 1
    S0 = 0
    S = dc.signal_free(S0, R1, TC, FA, R10=1)
    assert S==0


def test_signal_lin():
    R1 = 2
    S0 = 3
    assert 6 == dc.signal_lin(R1, S0)


def test_conc_t2w():
    S = np.ones(10)
    TE = np.inf
    C = dc.conc_t2w(S, TE, r2=1, n0=1)
    assert 0 == np.linalg.norm(C)
    
def test_conc_ss():
    S = np.ones(10)
    TR = 1
    FA = 45
    T10 = np.inf
    C = dc.conc_ss(S, TR, FA, T10, r1=1, n0=1)
    assert 0 == np.linalg.norm(C)

    # Data without solution
    S = [1,2,0]
    T10 = 1
    C = dc.conc_ss(S, TR, FA, T10, r1=1, n0=1)
    assert C[-1] == -1

def test_conc_src():
    S = np.ones(10)
    TC = 1
    T10 = np.inf
    C = dc.conc_src(S, TC, T10, r1=1, n0=1)
    assert 0 == np.linalg.norm(C)

def test_conc_lin():
    S = np.ones(10)
    T10 = 1
    C = dc.conc_lin(S, T10, r1=1, n0=1)
    assert np.linalg.norm(C)==0


if __name__ == "__main__":

    test_signal_dsc()
    test_signal_t2w()
    test_signal_ss()
    test_signal_spgr()
    test_signal_free()
    test_signal_lin()

    test_conc_t2w()
    test_conc_ss()
    test_conc_src()
    test_conc_lin()

    print('All sig tests passing!')