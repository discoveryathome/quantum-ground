from fractions import Fraction
from pathlib import Path
import itertools
import numpy as np
import pytest
from qground.evaluator import (contraction, verify, decimal_interval, dense_state,
                               hamiltonian_id, load_witness)
from qground.exactdiag import matrix, reference
from qground.optimize import model, run, save


def case(L=6, j2='0.5', delta='1'):
    return dict(id='test', L=L, J1='1', J2=j2, delta=delta,
                boundary='open', basis='down,up', chi_max=8)


def test_singlet_exact_and_interval():
    a = np.zeros((1,2,2)); a[0,0,0]=1; a[0,1,1]=1
    b = np.zeros((2,2,1)); b[0,1,0]=1; b[1,0,0]=-1
    e,n = contraction([a,b],case(2))
    assert e == Fraction(-3,4) and n == 2
    for q in [e,Fraction(-1,3),Fraction(1,3),Fraction(0)]:
        lo,hi=map(Fraction,decimal_interval(q))
        assert lo <= q <= hi and hi-lo <= Fraction(1,10**14)


def test_exact_transfer_matches_independent_full_fraction():
    rng=np.random.default_rng(193)
    c=case(4,'0.375','1.25')
    shapes=[(1,2,2),(2,2,3),(3,2,2),(2,2,1)]
    tensors=[rng.integers(-3,4,size=s).astype(float)/8 for s in shapes]
    amplitudes=[]
    for bits in itertools.product(range(2),repeat=4):
        v=[Fraction(1)]
        for a,s in zip(tensors,bits):
            v=[sum(v[i]*Fraction(float(a[i,s,j])) for i in range(len(v)))
               for j in range(a.shape[2])]
        amplitudes.append(v[0])
    h=matrix(c).toarray()
    n=sum(v*v for v in amplitudes)
    e=sum(amplitudes[i]*Fraction(float(h[i,j]))*amplitudes[j]
          for i in range(16) for j in range(16))/n
    assert contraction(tensors,c) == (e,n)


@pytest.mark.parametrize('j2,delta',[('0','1'),('0.25','1'),('0.625','1.25')])
def test_tenpy_mpo_matches_bit_hamiltonian(j2,delta):
    from tenpy.algorithms.exact_diag import ExactDiag
    c=case(6,j2,delta)
    ed=ExactDiag(model(c)); ed.build_full_H_from_mpo()
    assert np.max(abs(ed.full_H.to_ndarray()-matrix(c).toarray())) < 1e-14


def test_dmrg_small_system_matches_ed(tmp_path):
    c=case()
    r=run(c,'baseline',1729,tmp_path,6)
    v=verify(tmp_path/'sweep-6.npz',c,r['history'][-1]['optimizer_energy'])
    ed=reference(c)
    assert abs(v['energy']-ed['energy']) < 1e-10
    assert ed['residual_norm'] < 1e-11
    tensors=load_witness(tmp_path/'sweep-6.npz',c)
    state=dense_state(tensors)
    assert abs(state@matrix(c)@state/(state@state)-v['energy'])<1e-12


@pytest.mark.parametrize('problem',['nan','zero','norm','bond','hash','complex','claim','extra','object'])
def test_reject_invalid(tmp_path,problem):
    c=case(2)
    tensors=[np.array([1.,0.]).reshape(1,2,1) for _ in range(2)]
    if problem=='nan': tensors[0][0,0,0]=np.nan
    if problem=='zero': tensors[0]*=0
    if problem=='norm': tensors[0]*=0.5
    if problem=='bond': tensors[0]=np.ones((1,2,9))
    if problem=='complex': tensors[0]=tensors[0].astype(complex)
    if problem=='object': tensors[0]=tensors[0].astype(object)
    path=tmp_path/'bad.npz'
    save(path,tensors,c)
    if problem=='hash': c={**c,'J2':'0.75'}
    if problem=='extra': np.savez(path,A0=tensors[0],A1=tensors[1],hamiltonian_id=hamiltonian_id(c),extra=1)
    with pytest.raises((ValueError,TypeError)):
        verify(path,c,claim=-100 if problem=='claim' else None)
