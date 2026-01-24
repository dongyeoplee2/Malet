
import os
import shutil
import time
import traceback
import uuid
import warnings
from _thread import start_new_thread
from ast import literal_eval
from contextlib import ContextDecorator
from ctypes import c_long, py_object, pythonapi
from multiprocessing import TimeoutError as MpTimeoutError
from queue import Empty as Queue_Empty
from queue import Queue
from typing import Optional, Sequence

from absl import logging
from rich.table import Table

warnings.simplefilter(action='ignore')

def create_dir(dir, overwrite=False):
  """Creates a directory at the specified path. If the directory already exists, 
  it can optionally overwrite its contents.

  Args:
    dir (str): The path of the directory to create.
    overwrite (bool, optional): If True and the directory exists, 
      all its contents will be removed. Defaults to False.
  """
  if os.path.exists(dir):
    if overwrite:
      for f in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, f)):
          shutil.rmtree(os.path.join(dir, f))
        else:
          os.remove(os.path.join(dir, f))
  else:
    os.makedirs(dir)

def to_eng_str(num, long_than=4, precision=3):
  """Convert a number to engineering notation with a specified precision.

  Args:
    num (float): The number to convert.
    long_than (int, optional): The minimum length of the number string. 
      Defaults to 4.
    precision (int, optional): The number of decimal places to include. 
      Defaults to 3.

  Returns:
    str: The number in engineering notation.
  """
  if not isinstance(num, (int, float)):
    return str(num)
    
  if 10**-long_than < abs(num) < 10**long_than:
    num = str(num)
    if len(num) > long_than:
      return num[:long_than]
    return num

  return f'{num:.{precision}e}'


def df2richtable(
  df,
  title=None,
  max_row_len=None,
  highlight_columns: Optional[list]=None,
  max_col_width=None,
  col_center=None,
  max_seq_value_len=None,
  list_centers: Optional[dict]=None,
  highlight_list_centers=False,
  alternating_row_colors=False,
  use_eng_str=False,
):
  def _trnc(l_len, width=None, center=0):
    if not width or l_len <= width:
      return (0, l_len), (False, False), 0
    mid = width // 2
    raw_lr = (center - mid, center + mid + 1)
    trunc_lr = (raw_lr[0] > 0, raw_lr[1] < l_len)
    shift = 0
    if not trunc_lr[0]:
      shift = -raw_lr[0]
    elif not trunc_lr[1]:
      shift = l_len - raw_lr[1]
    final_lr = (i + shift for i in raw_lr)
    center_idx = mid - shift
    return final_lr, trunc_lr, center_idx
  
  def add_trnc_ind(l, trc, s='...', sft=0):
    if trc[0]:
      l = l[:sft] + [s] + l[sft:]
    if trc[1]:
      l = l + [s]
    return l 
  
  idx_len = len(df.index.names)
  col_center = df.columns.get_loc(col_center or df.columns[0])
  col_lr, is_trnc_col_lr, _ = _trnc(len(df.columns), max_col_width, col_center)
  df = df[df.columns[slice(*col_lr)]]
  
  df = df.reset_index()
  df_len = len(df)
  
  if max_row_len:
    df_tail = len(df), *df.tail(1).iloc[0].values
    df = df.head(max_row_len)
  
  list_centers = list_centers or {}
  centers = [None] + [list_centers.get(n, None) for n in df.columns]
  centers = add_trnc_ind(centers, is_trnc_col_lr, s=None, sft=idx_len+1)
    
  highlight_columns = highlight_columns or []
  h_col = [None] + [n in highlight_columns for n in df.columns]
  h_col = add_trnc_ind(h_col, is_trnc_col_lr, s=None, sft=idx_len+1)
    
  table = Table(title=title)
  table.add_column('id')
  for f in add_trnc_ind(list(df), is_trnc_col_lr, sft=idx_len):
    table.add_column(f)
  
  ilen = len(df.index.names) + is_trnc_col_lr[0]
  def _process_entry(v, col_i):
    clr = lambda s: f'[on red]{s}[/on red]' if h_col[col_i] else str(s)
    if (
      not max_seq_value_len or
      not isinstance(v, Sequence) or
      len(v) <= max_seq_value_len
    ):
      if use_eng_str and isinstance(v, (int, float)):
        v = to_eng_str(v, precision=0)
      return clr(v)
    
    par = '[]' if isinstance(v, list) else '()'
    is_tuple = isinstance(v, tuple)
    v = list(v)
    
    l2s = lambda l: par[0] + ', '.join(map(str, l)) + par[1]
    
    # if v is seq
    c = centers[col_i] or 0
    ml = max_seq_value_len
    
    lr, is_trnc_lr, c_i = _trnc(len(v), ml, c)
    slc_l = v[slice(*lr)]
    slc_l = add_trnc_ind(slc_l, is_trnc_lr, s='...', sft=0)
    
    if use_eng_str:
      slc_l = [to_eng_str(n, precision=0) for n in slc_l]
    if highlight_list_centers:
      
      slc_l[c_i+idx_len] = clr(slc_l[c_i+idx_len])
      return l2s(slc_l)
    else:
      return clr(l2s(tuple(slc_l) if is_tuple else slc_l))
    
  prev_row = None
  for i, row in enumerate(df.itertuples(name=None)):
    print_row = [*row]
    if prev_row:
      print_row = ['' if p==r else r for p, r in zip(prev_row, print_row)]
    print_row = add_trnc_ind(print_row, is_trnc_col_lr, sft=idx_len+1)
    
    table.add_row(
      *[_process_entry(v, j) for j, v in enumerate(print_row)],
      style="on bright_black" if (alternating_row_colors and i%2) else ""
    )
    prev_row = row
    
  
  if max_row_len and max_row_len<df_len:
    table.add_row('', *(['']*len(df.columns)))
    table.add_row('...', *(['...']*len(df.columns)))
    table.add_row('', *(['']*len(df.columns)))
    print(df_tail[0])
    df_tail = add_trnc_ind(df_tail, is_trnc_col_lr, sft=idx_len+1)
    table.add_row(*[_process_entry(v, j) for j, v in enumerate(df_tail)])
    
  return table


def list2tuple(l):
  if isinstance(l, list):
    return tuple(map(list2tuple, l))
  if isinstance(l, dict):
    return {k: list2tuple(v) for k, v in l.items()}
  return l
    

def str2value(value_str):
    """Casts string back to standard python types"""
    if not isinstance(value_str, str): return value_str
    value_str = value_str.replace('inf', '2e+308')\
                         .replace('nan', 'None')
    try:
      return literal_eval(value_str)
    except:
      return value_str


def append_metrics(metric_log=None, **new_metrics):
    '''Add new metrics to metric_log'''
    if metric_log==None:
        metric_log = {}
    for k, v in new_metrics.items():
        assert type(v) in {int, float, bool, str}
        metric_log[k] = metric_log.get(k, [])
        metric_log[k].append(v)
    return metric_log


class QueuedFileLock(ContextDecorator):
  __delim = '\n'
  
  def __init__(self, lock_file: str, timeout: float = 10):
    self.lock_file = lock_file
    self.timeout = timeout
    self.id = uuid.uuid4().int
    
    self.acquire_count = 0
    
    if not os.path.exists(lock_file):
      with open(lock_file, 'w') as f:
        f.write('')
      
    self.__read_queue()
    
  def __read_queue(self):
    success=False
    for i in range(10):
      try:
        with open(self.lock_file, 'r') as f:
          s = f.read()
          parseint = lambda x: int(x.strip('\x00'))
          self.queue = [*map(parseint, filter(bool, s.split(self.__delim)))]
          success = True
        break
      except:
        logging.info(f'Failed to read queue from {self.lock_file} (Attempt: {i+1}/10). Retrying after 0.1s.')
        time.sleep(0.1)
        continue
    if not success:
      raise Exception(f'Failed to read queue from {self.lock_file}.')
      
  def __write_queue(self):
    with open(self.lock_file, 'w') as f:
      s = self.__delim.join(map(str, self.queue))
      f.write(s)
    
  def __append_write(self):
    with open(self.lock_file, 'a') as f:
      f.write(f'{self.__delim}{self.id}')
    self.__read_queue()
    
  @property
  def is_locked(self):
    self.__read_queue()
    return not self.queue or self.queue[0] != self.id
  
  def acquire(
    self, 
    timeout: Optional[float]=None, 
    poll_interval: float = 0.05
  ):
    self.acquire_count += 1
    
    if timeout is None:
      timeout = self.timeout
      
    self.__read_queue()
    if self.id not in self.queue:
      self.__append_write()
    
    logging.debug(f'Attempting to acquire filelock {self.id} on {self.lock_file}.')
    start_t = time.time()
    while self.is_locked:
      logging.debug(f'Failed to acquire filelock {self.id} on {self.lock_file}. Waiting for {poll_interval} seconds.')
      time.sleep(poll_interval)
      
      if time.time() - start_t > timeout:
        raise TimeoutError(f'Timeout while acquiring filelock {self.id} on {self.lock_file}.')
    
    logging.debug(f'Filelock {self.id} acquired on {self.lock_file}.')
      
  def release(self, force=False):
    if self.acquire_count == 0: return
    
    if self.acquire_count >= 1:
      self.acquire_count -= 1
    
    if self.acquire_count == 0 or force:
      self.acquire_count = 0
      self.__read_queue()
      self.queue.remove(self.id)
      self.__write_queue()
      
      logging.debug(f'Released filelock {self.id} on {self.lock_file}.')
  
  def __enter__(self):
    self.acquire()
    return self
    
  def __exit__(self, *args):
    self.release()
    
  def __del__(self):
    self.release(force=True)



class FuncTimeoutError(Exception):
    pass

def async_raise(tid, exctype=Exception):
    """
    Raise an Exception in the Thread with id `tid`. Perform cleanup if
    needed.
    Based on Killable Threads By Tomer Filiba
    from http://tomerfiliba.com/recipes/Thread2/
    license: public domain.
    """
    assert isinstance(tid, int), 'Invalid  thread id: must an integer'

    tid = c_long(tid)
    exception = py_object(exctype)
    res = pythonapi.PyThreadState_SetAsyncExc(tid, exception)
    if res == 0:
        raise ValueError('Invalid thread id.')
    elif res != 1:
        # if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError('PyThreadState_SetAsyncExc failed.')


def settimeout_func(func, timeout=3*24*60*60):
    if timeout is None: return func
    
    def timeoutfunc(*args, **kwargs):
      """
      Threads-based interruptible runner, but is not reliable and works
      only if everything is pickable.
      """
      # We run `func` in a thread and block on a queue until timeout
      q = Queue()

      def runner():
          try:
              _res = func(*(args or ()), **(kwargs or {}))
              q.put((None, _res))
          except FuncTimeoutError:
              # rasied by async_rasie to kill the orphan threads
              pass
          except Exception as ex:
              q.put((ex, None))

      tid = start_new_thread(runner, ())

      try:
          err, res = q.get(timeout=timeout)
          if err:
              raise err
          return res
      except (Queue_Empty, MpTimeoutError):
          raise FuncTimeoutError(
                  "{0} timeout (taking more than {1} sec)".format(func.__name__, timeout)
              )
      finally:
          try:
              async_raise(tid, FuncTimeoutError)
          except (SystemExit, ValueError):
              pass
    
    return timeoutfunc
  
def path_common_decomposition(paths):
  if len(paths) == 0: return '', []
  elif len(paths) == 1: return paths[0], []
  
  paths = [p.split('/') for p in paths]
  
  # Find common prefix
  common = []
  for _ in range(min(map(len, paths))):
    if len(set(p[0] for p in paths)) != 1: break
    common.append(paths[0][0])
    paths = [p[1:] for p in paths]
  non_common = [os.path.join(*p) for p in paths]
  return common, non_common

def get_wandb_sweep_exp_dir(base_dir, entity, project, sweep_id):
  return os.path.join(base_dir, project, sweep_id)