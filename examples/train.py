import sys
from time import sleep

from absl import app, flags
from ml_collections.config_dict import ConfigDict

sys.path.append('../..')
from src.malet.experiment import Experiment

def train(config: ConfigDict, experiment: Experiment):
    
    data = [*range(100)]
    fA = lambda x: 1
    fB = lambda x: x+1
    fC = lambda x: 2*x
    
    metric_dict = {
        'A': [],
        'B': [],
        'C': [],
    }
    if config in experiment.log:
        metric_dict = experiment.get_log_checkpoint(config, metric_dict)
        print('hihihi', len(metric_dict['A']))
    
    for d in data:
        # sleep(1)
        
        metric_dict['A'].append(fA(d))
        metric_dict['B'].append(fB(d))
        metric_dict['C'].append(fC(d))
        
        if not (d+1)%5:
            print(len(metric_dict['A']))
            experiment.update_log(metric_dict, config=config)
    
    return metric_dict



FLAGS = flags.FLAGS
def main(argv):
    metric_fields =  ['A', 'B', 'C']
    experiment = Experiment('../../src/tests/test_exp', train, metric_fields,
                            total_splits=FLAGS.total_splits,
                            curr_split=FLAGS.curr_splits,
                            auto_update_tsv=FLAGS.auto_update_tsv,
                            configs_save=FLAGS.configs_save,
                            checkpoint=FLAGS.checkpoint)
    experiment.run()


if __name__=='__main__':
  flags.DEFINE_string('total_splits', '1', '')
  flags.DEFINE_string('curr_splits', '0', '')
  flags.DEFINE_bool('auto_update_tsv', True, '')
  flags.DEFINE_bool('configs_save', True, '')
  flags.DEFINE_bool('checkpoint', True, '')
  app.run(main)