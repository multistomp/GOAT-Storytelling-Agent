"""Unifies all plot forms such as by-chapter and by-scene outlines in a single dict."""
import re
import json


"""
FUNCTION MAP

normalize_text_plan
    |--->parse_text_plan
         |---> split_by_act
         |---> parse_act
    |--->plan_2_str

act_2_str

save_plan

"""


class Plan:
    
    """
    action: split up the plan into acts
    input: original_plan
    calls:
    returns: "acts" as LIST
    """
    @staticmethod
    def split_by_act(original_plan):
        # removes only Act texts with newline prepended soemwhere near
        acts = re.split('\n.{0,5}?Act ', original_plan)
        # remove random short garbage from re split
        acts = [text.strip() for text in acts[:]
                if (text and (len(text.split()) > 3))]
        if len(acts) == 4:
            acts = acts[1:]
        elif len(acts) != 3:
            print('Fail: split_by_act, attempt 1', original_plan)
            acts = original_plan.split('Act ')
            if len(acts) == 4:
                acts = acts[-3:]
            elif len(acts) != 3:
                print('Fail: split_by_act, attempt 2', original_plan)
                return []

        # [act1, act2, act3], [Act + act1, act2, act3]
        if acts[0].startswith('Act '):
            acts = [acts[0]] + ['Act ' + act for act in acts[1:]]
        else:
            acts = ['Act ' + act for act in acts[:]]
        return acts


    """
    action: split up an act tino chapters
    input: act
    calls:
    returns: acts and chapters as DICTIONARY
    """
    @staticmethod
    def parse_act(act):
        act = re.split(r'\n.{0,20}?Chapter .+:', act.strip())
        chapters = [text.strip() for text in act[1:]
                    if (text and (len(text.split()) > 3))]
        return {'act_descr': act[0].strip(), 'chapters': chapters}

    
    """
    action: split up the plan into acts
    input: text plan
    calls: split_by_act() and parse_act()
    returns: plan as LIST
    """
    @staticmethod
    def parse_text_plan(text_plan):
        acts = Plan.split_by_act(text_plan)
        if not acts:
            return []
        plan = [Plan.parse_act(act) for act in acts if act]
        plan = [act for act in plan if act['chapters']]
        return plan

    """
    action: takes a text plan, splits into acts, then turns it into a string
    input: text_plan
    calls: parse_text_plan() and plan_2_str()
    returns: text_plan as STRING
    """
    @staticmethod
    def normalize_text_plan(text_plan):
        plan = Plan.parse_text_plan(text_plan)
        text_plan = Plan.plan_2_str(plan)
        return text_plan
        
    """
    action: turns an act into a string
    input: plan and act_num
    calls: 
    returns: text_plan as STRING
    """
    @staticmethod
    def act_2_str(plan, act_num):
        text_plan = ''
        chs = []
        ch_num = 1
        for i, act in enumerate(plan):
            act_descr = act['act_descr'] + '\n'
            if not re.search(r'Act \d', act_descr[0:50]):
                act_descr = f'Act {i+1}:\n' + act_descr
            for chapter in act['chapters']:
                if (i + 1) == act_num:
                    act_descr += f'- Chapter {ch_num}: {chapter}\n'
                    chs.append(ch_num)
                elif (i + 1) > act_num:
                    return text_plan.strip(), chs
                ch_num += 1
            text_plan += act_descr + '\n'
        return text_plan.strip(), chs

    """
    action: turns a plan into a string
    input: plan
    calls: 
    returns: text_plan as STRING
    """
    @staticmethod
    def plan_2_str(plan):
        text_plan = ''
        ch_num = 1
        for i, act in enumerate(plan):
            act_descr = act['act_descr'] + '\n'
            if not re.search(r'Act \d', act_descr[0:50]):
                act_descr = f'Act {i+1}:\n' + act_descr
            for chapter in act['chapters']:
                act_descr += f'- Chapter {ch_num}: {chapter}\n'
                ch_num += 1
            text_plan += act_descr + '\n'
        return text_plan.strip()

    """
    action: saves a plan as a JSON file
    input: plan, fpath
    calls: 
    returns: 
    """
    @staticmethod
    def save_plan(plan, fpath):
        with open(fpath, 'w') as fp:
            json.dump(plan, fp, indent=4)
