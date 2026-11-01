"""Reconcile own accepted calls against public logs; never infer a changed menu."""
import re
from gpt_native_replay import R

def align(rows,logs):
    # With batched calls a preceding observation cannot identify the next menu.
    # Use the actual accepted public log sequence, never a guessed stale menu.
    actions=[]
    for log in logs:
        text=log['message']
        match=re.search(r'^Chose #(\d+): ([^\n]+)',text,re.M)
        if not match:continue
        quarter=log['entry_type']=='fixed_event' and any(a in text for a in (*R.ENERGY_FX,*R.MAIN_FX))
        if log['entry_type']!='action' and not quarter:continue
        month=re.match(r'Month (\d+) \|',text);assert month
        actions.append((int(month[1]),int(match[1]),match[2],quarter))
    # Initial onboarding document is logged without a "Chose" line and precedes
    # the month-3 replay anchor. Do not shift the accepted action alignment.
    assert rows[0]['phase']=='document' and rows[0]['before']['month']==1
    rows=rows[1:]
    assert len(actions)==len(rows), (len(actions),len(rows))
    repaired=[];mismatches=0
    for row,(month,choice,action,quarter) in zip(rows,actions):
        assert choice==row['choice']
        if quarter:
            assert action in R.ENERGY_FX or action in R.MAIN_FX
            phase='energy' if action in R.ENERGY_FX else 'main_action'
            mismatches+=row['phase']!=phase or row.get('quarter_action')!=action
            repaired.append({'before':{'month':month},'phase':phase,'quarter_action':action})
        else:
            assert row['before']['month']==month and row['phase'] in ('event','document') and not row['stale_menu']
            repaired.append(row)
    return repaired,{'public_log_action_pairings':len(actions),'stale_menu_quarter_attributions_repaired':mismatches}
