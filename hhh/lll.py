import sys
import re
# from node import Node, Composition
import re

class Composition:
    def __init__(self, comp):
        self.comp=comp
    
    def value(self):
        return self.comp
    
    def __add__(self, b):
        for el in b.comp:
            self.comp[el]=self.comp.get(el,0)+b.comp[el]
        return self
        
    def __mul__(self, m):
        for el in self.comp:
            self.comp[el]*=m
        return self
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)
    
    def cleanup(self):
        el='H'
        if self.comp[el] ==0:
            del self.comp[el]
        return self
        
class Node:
    def __init__(self, type='', value='', mult='', parent=None):
        # print(tag_name)
        self.type = type
        self.value = value
        self.mult = mult
        self.children = []
        self.parent = parent
        if parent:
            self.parent.children.append(self)

    def __str__(self):
        if self.value:
            value=self.type + ": " + ((self.mult + ' ') if self.mult else '') + self.value
        else:
            value=''

        # if self.parent:
        #     value+=' has parent'
        
        children_str='\n'.join(re.sub('^', lambda m: ' '+m.group(0), str(c) , flags=re.M) for c in self.children)            
        if children_str:
            return value+'\n'+children_str
        else:
            return value

    def composition(self, p):
        # comp=p.get_comp(self.type, self.value)
        # for c in self.children:
        #     comp+=c.composition(p)
        # comp*=p.get_multvalue(self.mult)
        # return comp
        return (p.get_comp(self.type, self.value)+sum((c.composition(p) for c in self.children), start=Composition({})))*p.get_multvalue(self.mult)
    
        
        
    def update(self, tag_name, value, mult=None, parent=None):
        self.type = tag_name
        self.value=value

        if not self.parent:
            self.parent = parent
        if mult:
            self.mult=mult
        return self
    
    def update_mult(self, mult):
        self.mult=mult
    
    def create_child(self, tag_name, value, mult=''):
        child = Node(tag_name, value, mult, self)
        # print(child)
        return child

# octane = Node('radical', val='oct')
# octane.add_child('suffix', 'ene', 'di')
# octane.add_child('suffix', 'ane')
# octane.add_child('suffix', 'oate', 'di').add_child('radical', 'meth').add_child('suffix', 'yl')

# print(octane)

class ParseHer(object):

    RADICALS    = ["meth", "eth", "prop", "but",   "pent",  "hex",  "hept",  "oct",  "non",  "dec",  "undec",  "dodec",  "tridec",  "tetradec",  "pentadec",  "hexadec",  "heptadec",  "octadec",  "nonadec"]
    MULTIPLIERS = [        "di",  "tri",  "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"]
    
    SUFFIXES    = [         "ol",      "al", "one", "oic acid", "carboxylic acid",                "oate",             "ether", "amide", "amine", "imine", "benzene", "thiol",    "phosphine", "arsine"]
    PREFIXES    = ["cyclo", "hydroxy",       "oxo",             "carboxy",         "oxycarbonyl", "oyloxy", "formyl", "oxy",   "amido", "amino", "imino", "phenyl",  "mercapto", "phosphino", "arsino", "fluoro", "chloro", "bromo", "iodo"]

    SUFFIXES_c = {"ol": [('O', 1)],
                  "al": [('O', 1), ('H', -2)],
                  "one": [('O', 1), ('H', -2)],
                  "oic acid": [('O', 2), ('H', -2)],
                  "carboxylic acid": [('O', 2), ('C', 1), ('H', 0)],
                  "oate": [('O', 2), ('H', -2)],
                  "ether": [('O', 1), ('H', 2)],
                  "amide": [('O', 1), ('N', 1), ('H', -1)],
                  "imine": [('N', 1), ('H', -1)],
                  "benzene": [('H', -6)],
                  "thiol": [('S', 1)],
                  "amine": [('N', 1), ('H', 1)],
                  "phosphine":  [('P', 1), ('H', 1)],
                  "arsine":  [('As', 1), ('H', 1)],
                  "ene": [('H', -2 )],
                  "en": [('H', -2 )],
                  "yne": [('H', -4 )],
                  "yn": [('H', -4 )],
                  "yl": [('H', -2)],
                  "an": [],
                  "ane": []}
    PREFIXES_c = {"cyclo": [('H', -2)],
                  "hydroxy": [('O', 1)],
                  "oxo": [('O', 1), ('H', -2)],
                  "carboxy": [('C', 1), ('O', 2), ('H', 0)],
                  "oxycarbonyl": [('C', 1), ('O', 2), ('H', -2)],
                  "oyloxy": [('O', 2), ('H', -4)],
                  "formyl": [('C', 1), ('O', 1), ('H', 0)],
                  "oxy": [('O', 1), ('H', -2)],
                  "amido": [('O', 1), ('N', 1), ('H', -1)],
                  "imino": [('N', 1), ('H', -1)],
                  "phenyl": [('C', 6), ('H', 4)],
                  "mercapto": [('S', 1)],
                  "amino": [('N', 1), ('H', 1)],
                  "phosphino": [('P', 1), ('H', 1)],
                  "arsino":  [('As', 1), ('H', 1)],
                  "fluoro": [('F', 1), ('H', -1)],
                  "chloro": [('Cl', 1), ('H', -1)],
                  "bromo": [('Br', 1), ('H', -1)],
                  "iodo": [('I', 1), ('H', -1)]}
    
    def add_token(self, type, val):
        if type != 'position':
            self.tokens.append((type,val))
        # print(type, val)

    def raise_error(self):
        print('error: no match at', self.name[:self.current+1],'<=', self.name[self.current+1:])
        self.error=True

    def __init__(self, name, debug=False):
        self.name=name
        self.tokens=[]
        self.re_radical='amine|arsine|phosphine|ether|benzene|'+"|".join(sorted(self.RADICALS, key=lambda x: -len(x)))
        self.re_suffix='|'.join(sorted(self.SUFFIXES, key=lambda x: -len(x)))+'|yl|ane?|ene?|yne?'
        self.re_prefix='|'.join(sorted(self.PREFIXES, key=lambda x: -len(x)))
        self.re_position=r'-?\d+(,\d+)*-'
        self.re_precisepositioner='|'.join(r'(?:\d+(?:,\d+){'+str(n+1)+'}-)'+v for n,v in enumerate(self.MULTIPLIERS))
        self.re_multiplier='|'.join(sorted(self.MULTIPLIERS, key=lambda x: -len(x)))
        self.re_leftbracket=r'\['
        self.re_rightbracket=r']'
        self.debug=debug
        
    def peek_positioner(self, pos):
        m=re.search('(({})?({}))$'.format(self.re_position, self.re_multiplier), self.name[:pos+1])
        return True if m else False
 
    def peek_rightbracket(self, pos):
        m=re.search('('+self.re_rightbracket+')$', self.name[:pos+1])
        return True if m else False
    
    def peek_precisepositioner(self, pos):
        # print('pos', self.name[:pos+1])
        m=re.search('('+self.re_precisepositioner+')$', self.name[:pos+1])
        return True if m else False
    
    def peek_prefix_in_yl(self, pos):
        m=re.search('(oxycarbonyl|phenyl|formyl)$', self.name[:pos+3])
        return True if m else False
    
    def peek_iodo_amido(self, pos):
        m=re.search('((io|ami)do)$', self.name[:pos+3])
        return True if m else False
        
    def generic_matching(self, regex, type):
        m=re.search('('+regex + ')$', self.name[:self.current+1])
        if m:
            self.add_token(type, self.name[m.start():self.current+1])
            self.current=m.start()-1
            return True
        else:
            return False
        
    def is_radical(self):
        m=re.search('('+self.re_radical+')$', self.name[:self.current+1])
        if m:
            # arsine and like with a preceeding multiplier, position or rightbracket are considered suffix
            # if m.group() in [ 'arsine', 'amine', 'phosphine'] and (self.peek_positioner(m.start()-1) or self.peek_rightbracket(m.start()-1)):
            if m.group() in [ 'arsine', 'amine', 'phosphine'] and self.peek_positioner(m.start()-1):
                return False
            elif m.group() == 'dodec' and self.peek_iodo_amido(m.start()-1):
                self.add_token('radical', 'dec')
                self.current=m.start()+1
            elif m.group()[-3:] == 'dec' and self.peek_precisepositioner(m.end()-4):
                self.add_token('radical', 'dec')
                self.current=m.end()-4
            else:
                self.add_token('radical', self.name[m.start():self.current+1])
                self.current=m.start()-1
                return True
        else:
            return False
    
    def is_suffix(self):
        m=re.search('('+self.re_suffix+')$', self.name[:self.current+1])
        if m:
            # arsine and like with a preceeding multiplier or position are considered suffix
            if m.group() in [ 'yl' ] and self.peek_prefix_in_yl(m.start()-1):
                return False
            else:
                self.add_token('suffix', self.name[m.start():self.current+1])
                self.current=m.start()-1
                return True
        else:
            return False
        
    def is_prefix(self): return self.generic_matching(self.re_prefix, 'prefix')
    def is_multiplier(self): return self.generic_matching(self.re_multiplier, 'multiplier')
    def is_position(self): return self.generic_matching(self.re_position, 'position')
    def is_leftbracket(self): return self.generic_matching(self.re_leftbracket, 'leftbracket')
    def is_rightbracket(self): return self.generic_matching(self.re_rightbracket, 'rightbracket')
            
    def lexer(self):
        self.error = False
        self.current = len(self.name)-1
        while self.current >=0 and not self.error:
            char=self.name[self.current]
            if char == ' ':
                self.current -= 1
                continue
            if char.isalpha():
                if self.is_radical(): continue
                if self.is_suffix(): continue        
                if self.is_multiplier(): continue
                if self.is_prefix(): continue
                else:
                    self.raise_error()
            elif char in '[' and self.is_leftbracket(): continue
            elif char in ']' and self.is_rightbracket(): continue
            elif char in '-' and self.is_position(): continue
            else:
                self.raise_error()
        return not self.error

    def add_radical(self, comp, radical, mult=1):
        if radical == 'benzene':
            comp['C']=comp.get('C',0) + mult * 6
            comp['H']=comp.get('H',0) + mult * 6
        elif radical == 'ether':
            comp['O']=comp.get('O',0) + mult * 1
            comp['H']=comp.get('H',0) + mult * 2
        elif radical == 'arsine':
            comp['As']=comp.get('As',0) + 1 # *mult
            comp['H']=comp.get('H',0) + 3 # *mult
            self.main_radical_NPAs=True
        elif radical == 'amine':
            comp['N']=comp.get('N',0) + 1 # *mult
            comp['H']=comp.get('H',0) + 3 # *mult
            self.main_radical_NPAs=True
        elif radical == 'phosphine':
            comp['P']=comp.get('P',0) + 1 # *mult
            comp['H']=comp.get('H',0) + 3 # *mult
            self.main_radical_NPAs=True
        else: # alkane
            carbon=self.RADICALS.index(radical)+1
            hydrogen=2*carbon+2
            # print("C {} H {} * {}".format(carbon, hydrogen, mult), end='')
            comp['C']=comp.get('C',0) + mult * carbon
            comp['H']=comp.get('H',0) + mult * hydrogen
        return comp
    
    def get_token(self):
        if len(self.tokens)>0:
            if self.debug:
                print('tok:',self.tokens[0])
            return self.tokens.pop(0)
        else:
            return None
        
    def peek_type(self, type):
        # if len(self.tokens)>0:
        #     print('peek for',type, ':', self.tokens[0][0])
        if len(self.tokens)>0 and self.tokens[0][0] == type:
            return True
        else:
            return False

    def peek_cyclo(self):
        # if len(self.tokens)>0:
        #     print('peek for',type, ':', self.tokens[0][0])
        if len(self.tokens)>0 and self.tokens[0][1] == 'cyclo':
            return True
        else:
            return False

    def get_mult_str(self):
        if self.peek_type('multiplier'):
            return self.get_token()[1]
        else:
            return ''
# ---
    def list_to_dict(self,l):
        return {a:b for a,b in l}
            
    def get_comp(self, type, value):
        if type=='radical':
            return Composition(self.add_radical({},value))
        elif type == 'suffix':
            return Composition(self.list_to_dict(self.SUFFIXES_c[value]))
        elif type == 'prefix':
            return Composition(self.list_to_dict(self.PREFIXES_c[value]))
        else:
            return Composition({})
    
    def special_case(self, comp):
        if self.main_radical_NPAs and self.found_alkan:
            comp+=Composition({'H': -2})
            pass
        return comp
        
    def get_multvalue(self, m):
        if m in self.MULTIPLIERS:
                return 2 + ( self.MULTIPLIERS.index(m))
        else:
            return 1 
    
# --- full parser ----
    
    def get_suffixes(self, node):
        if self.peek_type('suffix'):
            node=Node(parent=node)
        while self.peek_type('suffix'):
            token=self.get_token()
            mult=self.get_mult_str()
            if token[1] in ['en', 'yn']:  # in amide like subchain alkene and alkyne are likle yl
                self.found_alkan= True
            
            if token[1]=='an': # in amide like subchain alkane are likle yl
                self.found_alkan= True
            elif token[1]=='oate':
                self.ester=node.create_child('suffix', token[1], mult=mult)
            else:
                node.create_child('suffix', token[1], mult=mult)
        return node # an empty radical node to which suffix nodes are attached
    
    def get_subpart(self, node):
        self.get_token() # rightbracket
        # print(']')
        nodes=[]
        while not self.peek_type('leftbracket'):
            if self.peek_type('suffix'):
                suffix_node=self.get_suffixes(node)
                if self.peek_type('radical'):
                    nodes.append(self.get_radical(suffix_node, include_prefix=False))
            if self.peek_type('prefix'):
                nodes.append(self.get_prefix(node))
                
        self.get_token() # leftbracket
        # print('[')
        # raise NameError('expected leftbracket not found:', self.tokens)
        if self.peek_type('multiplier'):
            if len(nodes)>1:
                #: 3,4,7,7-tetra[9-chloro-2,3,4,5-tetrapenten-3-ynyl]tridec-6,12-diynylcyclooctane -> tetra is for tridec
                nodes[0].parent.update_mult(self.get_token()[1])
                # print("Error: multiplier before multiple subparts")
                return node
            else:
                subpart_node=nodes[0]
                subpart_node.parent.update_mult(self.get_token()[1])
                # if subpart_node.mult != '':
                #     # 2,4-di[1-hydroxy]prop-2-enylpentandioic acid
                #     # 2,5-di[dimethyl]ethylhexan-1,6-diol -> di applies to ethyl
                #     subpart_node.parent.update_mult(self.get_token()[1])
                # else:
                #     # 2,4-di[1-hydroxyprop-2-enyl]pentandioic acid -> di applies to the subpart                    
                #     # ethyl 2,5,7-tridodecyl-5,7-di[4-phenyl]decoxyoctan-1,8-dioate -> di applies to phenyl
                #     subpart_node.update_mult(self.get_token()[1])
                return node
                
        # subpart_nodes=self.get_subpart(prefix_node)
        # if self.peek_type('multiplier'):
        #     if len(subpart_nodes)>1:
        #         # raise NameError('multiplier before multiple subparts')
        #         # print("Error: multiplier before multiple subparts")
        #         subpart_nodes[0].parent.update_mult(self.get_token()[1])
        #         return subpart_nodes[0].parent
        #     else:
        #         subpart_node=subpart_nodes[0]
        #         if subpart_node.mult != '':
        #         # -3,5-di[dinonadecyl]phosphino
        #             subpart_node.parent.update_mult(self.get_token()[1])
        #         else:
        #             subpart_node.update_mult(self.get_token()[1])

    def get_radical(self, node, include_prefix=True):
        if self.peek_type('radical'):
            if node==None: # create a node if not existing
                node=Node()
            elif node.type!='': # create a child node if the existing node is not a node of blank type created by a suffix
                node=Node(parent=node)
            token=self.get_token() # xxx add the assignment immediatly
            node.update('radical', token[1])
            if self.peek_cyclo():
                token=self.get_token()
                # print('for', token[1])
                prefix_node=node.create_child('prefix', token[1])
            if self.peek_type('multiplier'): # a radical with a preceeding multiplier is final
                mult=self.get_token()[1]
                node.update_mult(mult )
                return node
    
        if self.peek_type('multiplier'):
            node.update_mult(self.get_token()[1])
            return node

        if self.peek_type('rightbracket'):
            self.get_subpart(node)
            
        elif include_prefix:
            self.get_prefix(node)

        return node
        
    def get_prefix(self, node):
        if self.peek_type('prefix'):
            while self.peek_type('prefix'):
                token=self.get_token()
                # print('for', token[1])
                prefix_node=node.create_child('prefix', token[1])
                if token[1] in ['oxycarbonyl', 'oyloxy', 'oxy']:
                    subchain_node=self.get_chain(prefix_node)
                    if subchain_node.mult != '':
                        # [2,9,14-trihexyl-14-nonyl-7,8,9,16-tetraoctadecoxy]heptadecyl hept-6-enoate - tetra applies to oxy
                        prefix_node.update_mult(subchain_node.mult)
                        subchain_node.update_mult('')
 
                elif self.peek_type('rightbracket'):
                    self.get_subpart(prefix_node)
 
                elif self.peek_type('multiplier'):
                    if token[1] != 'cyclo':
                        # 1,2-diamino...
                        prefix_node.update_mult(self.get_token()[1])
                    else:
                        prefix_node.parent.update_mult(self.get_token()[1])
                    # 3,3,6,12-tetracyclooctadecen-3,14-diynylcyclotridec-7,9-diyne
                    
            return prefix_node
        return node
                
    def get_chain(self, parent=None):
        node=self.get_suffixes(parent)
        new_node=self.get_radical(node)
        return new_node

    def parse(self):
        self.ester=False
        self.main_radical_NPAs=False
        self.found_alkan=False

        self.lexer()
        # print('lexer done')
        tree=self.get_chain()
        while len(self.tokens) > 0:
            if self.peek_type('suffix'):
                suffix_node=self.get_suffixes(tree)
                if self.peek_type('radical'):
                    self.get_radical(suffix_node, include_prefix=False)
            if self.peek_type('prefix'):
                self.get_prefix(tree)
            # self.get_chain(tree)
        if self.ester:
            self.ester.children.append(tree.children.pop())
            
        # print('---')
                
        if self.debug:
            print(tree)
        return self.special_case(tree.composition(self)).cleanup().value()
