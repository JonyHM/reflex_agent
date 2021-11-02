class Apriori:

    def __init__(self, itemSet, transactions):
        self.itemSet = itemSet
        self.transactions = transactions

    #Support calculation
    def support(self, Ix, Iy, bd):
        sup = 0
        for transaction in bd:
            if (Ix.union(Iy)).issubset(transaction):
                sup+=1
        sup = sup/len(bd)
        return sup

    # Confidence calculation
    def confidence(self, Ix, Iy, bd):
        Ix_count = 0
        Ixy_count = 0
        for transaction in bd:
            if Ix.issubset(transaction):
                Ix_count+=1
                if (Ix.union(Iy)).issubset(transaction):
                    Ixy_count += 1
        conf = Ixy_count / Ix_count
        return conf              

    # This function eliminates all the items in 
    # ass_rules which have sup < min_sup and
    # conf < min_conf. It returns a "pruned" list
    def prune(self, ass_rules, min_sup, min_conf):
        pruned_ass_rules = []
        for ar in ass_rules:
            if ar['support'] >= min_sup and ar['confidence'] >= min_conf:
                pruned_ass_rules.append(ar)
        return pruned_ass_rules
        

    # Apriori for association between 2 items
    def apriori_2(self, itemset, bd, min_sup, min_conf):
        ass_rules = []
        ass_rules.append([]) #level 1 (large itemsets)
        for item in itemset:
            sup = self.support({item},{item},bd) # Pq envia o mesmo item duas vezes?
            ass_rules[0].append({'rule': str(item), \
                                'support':sup, \
                                'confidence': 1})        
        ass_rules[0] = self.prune(ass_rules[0],min_sup, min_conf)
        ass_rules.append([]) #level 2 (2 items association)
        for item_1 in ass_rules[0]:
            for item_2 in ass_rules[0]:
                if item_1['rule'] != item_2['rule']:
                    rule = item_1['rule']+'_'+item_2['rule']
                    Ix = {item_1['rule']}
                    Iy = {item_2['rule']}
                    sup = self.support(Ix,Iy, bd)
                    conf = self.confidence(Ix, Iy, bd)
                    ass_rules[1].append({'rule':rule, \
                                        'support': sup, \
                                        'confidence': conf})
        ass_rules[1] = self.prune(ass_rules[1],min_sup, min_conf)
        return ass_rules

    def start(self):
        print(self.apriori_2(self.itemSet, self.transactions, 0.07, 0.07))
        cont = input('Press enter to continue...')
