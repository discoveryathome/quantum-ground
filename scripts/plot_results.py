"""Export a static, data-backed public-demo figure. No synthetic improvements."""
import json
from pathlib import Path
import os
os.environ['MPLCONFIGDIR']=str(Path('.tmp/matplotlib').resolve())
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main(supplement=False):
    dev=json.loads(Path('results/pilot/dev.json').read_text())
    trial=json.loads(Path('research/contributor-001/summary.json').read_text())
    added=json.loads(Path('research/contributor-001/dev.json').read_text())
    if supplement: trial=json.loads(Path('research/contributor-001/supplement/summary.json').read_text())
    selected=trial['selected']
    rows=[r for r in dev+added if r['instance']=='dev24' and r['seed']==1729]
    floor=min(r['energy'] for r in rows)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,axes=plt.subplots(1,2,figsize=(13,5.6),gridspec_kw={'width_ratios':[1,1.1]})
    colors={'baseline':'#68798d','dimer':'#248c8b','nnn_dimers':'#9b5eae','continuation':'#d17a26','ramp':'#2a76b4','random':'#c05072','single_site':'#849b36','hybrid_polish':'#592b8a'}
    methods=list(dict.fromkeys(['baseline',selected,trial['pairs'][0]['strong_control_method'],'dimer','nnn_dimers','continuation']))
    for m in methods:
        r=next((r for r in rows if r['method']==m),None)
        if not r:continue
        y=[h['energy']-floor for h in r['history']]
        axes[0].plot(range(1,7),y,'o-',lw=2,label=m.replace('_',' '),color=colors[m],ms=4)
    axes[0].set_yscale('symlog',linthresh=1e-8)
    axes[0].set_xlabel('Completed sweeps (same bond cap: 8)')
    axes[0].set_ylabel('Energy above best saved candidate, J1')
    axes[0].set_title('Development: changing the optimization strategy',loc='left',fontweight='bold')
    axes[0].legend(fontsize=9,frameon=False)
    axes[0].grid(axis='y',alpha=.15)
    pairs=trial['pairs'];x=np.arange(len(pairs));width=.26
    vals=[(p['equal_sweeps']['gain'] if p['equal_sweeps']['outcome']!='tie' else 0)/p['case']['L']*1e6 for p in pairs]
    vals2=[(p['matched_cpu'].get('gain',float('nan')) if p['matched_cpu']['outcome']!='tie' else 0)/p['case']['L']*1e6 for p in pairs]
    vals3=[(p['versus_initial_winner_equal_sweeps']['gain'] if p['versus_initial_winner_equal_sweeps']['outcome']!='tie' else 0)/p['case']['L']*1e6 for p in pairs]
    axes[1].bar(x-width,vals,width,label='vs standard DMRG: 6 sweeps',color='#248c8b')
    axes[1].bar(x,vals2,width,label='vs standard: common CPU cap',color='#2a76b4')
    axes[1].bar(x+width,vals3,width,label='vs earlier development winner',color='#d17a26')
    axes[1].axhline(0,color='#374151',lw=.8)
    axes[1].set_xticks(x,[f"{p['case']['L']} spins\nJ2={p['case']['J2']}" for p in pairs])
    axes[1].set_ylabel('Energy reduction per spin (millionths of J1)')
    axes[1].set_title('Post-hoc coverage supplement' if supplement else 'Primary fresh tests: known dimer line',loc='left',fontweight='bold')
    axes[1].legend(fontsize=8,frameon=False)
    axes[1].grid(axis='y',alpha=.15)
    fig.suptitle('A quantum magnet is a checkable optimization puzzle',x=.04,ha='left',fontsize=18,fontweight='bold')
    fig.text(.04,.01,'Every score is checked by exact integer arithmetic. Lower energy is a better variational upper bound, not a ground-state proof.\nPositive bars mean improvement; negative bars mean regression. Differences <=1e-10 J1 are shown as zero. Timings reflect a busy shared machine.',fontsize=9,color='#4b5563')
    fig.tight_layout(rect=[.02,.09,.99,.92])
    base='docs/contributor-supplement' if supplement else 'docs/contributor-demo'
    fig.savefig(base+'.png',dpi=160)
    fig.savefig(base+'.svg')
    print('Wrote '+base+' from recorded data')
    plt.close(fig)

if __name__=='__main__':
    main()
    if Path('research/contributor-001/supplement/summary.json').exists():main(True)
