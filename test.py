from mpipe import OrderedWorker, Stage, Pipeline, UnorderedStage, UnorderedWorker
import time
import torch

def load_model(model_path, device_id):
    device = torch.device("cuda:{}".format(device_id))
    model =torch.jit.load(model_path)
    model.eval().to(device)
    time.sleep(10)
    return model

# class DecoderStage(object):
#     """The Stage is an assembly of workers of identical functionality."""

#     def __init__(
#         self,
#         worker_class,
#         size=1,
#         device_ids=[0],
#         disable_result=False,
#         do_stop_task=False,
#         input_tube=None,
#         **worker_args
#         ):
#         """Create a stage of workers of given *worker_class* implementation,
#         with *size* indicating the number of workers within the stage.
#         *disable_result* overrides any result defined in worker implementation,
#         and does not propagate it downstream (equivalent to the worker
#         producing ``None`` result).

#         *do_stop_task* indicates whether the incoming "stop" signal (``None`` value)
#         will actually be passed to the worker as a task. When using this option,
#         implement your worker so that, in addition to regular incoming tasks,
#         it handles the ``None`` value as well. This will be
#         the worker's final task before the process exits.

#         Any worker initialization arguments are given in *worker_args*."""
#         self._worker_class = worker_class
#         self._worker_args = worker_args
#         self._size = size
#         self._disable_result = disable_result
#         self._do_stop_task = do_stop_task
#         self._input_tube = self._worker_class.getTubeClass()() \
#                            if not input_tube else input_tube
#         self._output_tubes = list()
#         self._next_stages = list()
#         self._device_ids = device_ids

#     def put(self, task):
#         """Put *task* on the stage's input tube."""
#         self._input_tube.put((task,0))

#     def get(self, timeout=None):
#         """Retrieve results from all the output tubes."""
#         valid = False
#         result = None
#         for tube in self._output_tubes:
#             if timeout:
#                 valid, result = tube.get(timeout)
#                 if valid:
#                     result = result[0]
#             else:
#                 result = tube.get()[0]
#         if timeout:
#             return valid, result
#         return result

#     def results(self):
#         """Return a generator to iterate over results from the stage."""
#         while True:
#             result = self.get()
#             if result is None: break
#             yield result

#     def link(self, next_stage):
#         """Link to the given downstream stage *next_stage*
#         by adding its input tube to the list of this stage's output tubes.
#         Return this stage."""
#         if next_stage is self: raise ValueError('cannot link stage to itself')
#         self._output_tubes.append(next_stage._input_tube)
#         self._next_stages.append(next_stage)
#         return self

#     def getLeaves(self):
#         """Return the downstream leaf stages of this stage."""
#         result = list()
#         if not self._next_stages:
#             result.append(self)
#         else:
#             for stage in self._next_stages:
#                 leaves = stage.getLeaves()
#                 result += leaves
#         return result

#     def build(self):
#         """Create and start up the internal workers."""

#         # If there's no output tube, it means that this stage
#         # is at the end of a fork (hasn't been linked to any stage downstream).
#         # Therefore, create one output tube.
#         if not self._output_tubes:
#             self._output_tubes.append(self._worker_class.getTubeClass()())

#         self._worker_class.assemble(
#             self._worker_args,
#             self._input_tube,
#             self._output_tubes,
#             self._size,
#             self._disable_result,
#             self._do_stop_task,
#             self._device_ids,
#             )

#         # Build all downstream stages.
#         for stage in self._next_stages:
#             stage.build()



#     def process(self, item):
#         return self.model(item)

# class PriorStage(Stage):
#     def __init__(self, model):
#         super().__init__(self)
#         self.model = model

#     def process(self, item):
#         return self.model(item)


class PriorWorker(OrderedWorker):
    # def doInit(self):
    #     """Implement this method in the subclass in case there's need
    #     for additional initialization after process startup.
    #     Since this class inherits from :class:`multiprocessing.Process`,
    #     its constructor executes in the spawning process.
    #     This method allows additional code to be run in the forked process,
    #     before the worker begins processing input tasks.
    #     """
    #     device = torch.device("cuda:{}".format(id))
    #     self.model = load_model()

    #     return None

    def doTask(self, value):
        time.sleep(2)
        return value

class DecoderWorker(OrderedWorker):
    # def doInit(self):
    #     """Implement this method in the subclass in case there's need
    #     for additional initialization after process startup.
    #     Since this class inherits from :class:`multiprocessing.Process`,
    #     its constructor executes in the spawning process.
    #     This method allows additional code to be run in the forked process,
    #     before the worker begins processing input tasks.
    #     """
    #     return None

    def doTask(self, value):
        time.sleep(3)
        return value

stage1 = Stage(PriorWorker)
stage2 = Stage(DecoderWorker)

stage1.link(stage2)

pipe = Pipeline(stage1)

start = time.time()
for number in range(5):
    pipe.put(number)

pipe.put(None)

for result in pipe.results():
    # print(result)
    pass
print("Time taken", time.time() - start)
