from stanza.server import CoreNLPClient
from schemata.parse.util import DependencyParserWrapper

def get_heads(dicts):
    # takes a list of dictionaries with heads and descendants and creates one dictionary with
    # heads and descendants
    ls = sorted([(item['dependent'], item['governor']) for item in dicts])
    ls = [x[1] for x in ls]
    return ls

class StanfordParser(DependencyParserWrapper):
    def __init__(self):
        super().__init__()
        self.client = CoreNLPClient()

    def __call__(self, sent):
        return self.get_spans(sent)    

    def get_spans(self, sent):
        ann = self.client.annotate(sent, annotators='parse', output_format='json')
        dependencies_list = ann['sentences'][0]['basicDependencies']
        heads = get_heads(dependencies_list)
        tree = DependencyParserWrapper.head_to_tree(heads)
        non_singletons = DependencyParserWrapper.compute_spans(tree)
        singletons = [(n, n + 1) for n in range(len(dependencies_list))]
        return set(non_singletons) | set(singletons)
