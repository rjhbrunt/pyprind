# Sebastian Raschka 2014
#
# Progress Percentage class to instantiate a percentage indicator object
# that is printed to the standard output screen to visualize the
# progress in a iterative Python procedure

from pyprind.prog_class import Prog


class ProgPercent(Prog):
    """
    Initializes a percentage indicator object that allows visuzalization
    of an iterational computation in the standard output screen. 

    Keyword Arguments:
        iterations (int): number of iterations of the computation
        track_time (bool): default True. Prints elapsed time when loop has finished
        stream (int): default 2. Takes 1 for stdout, 2 for stderr, or given stream object
        title (str): default ''. A title for the progress bar
        monitor (bool): default False. Monitors CPU and memory usage if True 
            (requires 'psutil' package).

    """
    def __init__(self, iterations, track_time=True, stream=2, title='', monitor=False):
        Prog.__init__(self, iterations, track_time, stream, title, monitor)
        self.perc = 0
        self._print_update()
        if monitor:
            self.process.cpu_percent()
            self.process.memory_percent()

    def _print_update(self):
        """Prints formatted integer percentage and tracked time to the screen."""
        self._stream_out('\r[%3d %%]' % (self.perc))
        if self.track:
            self._stream_out(' elapsed[sec]: {:.3f}'.format(self._elapsed()))
            if self._calc_eta():
                self._stream_out(' | ETA[sec]: {:.3f} '.format(self._calc_eta()))  
            self._stream_flush()

    def update(self, iterations=1):
        """
        Updates the progress bar in every iteration of the task.

        Keyword arguments:
            iterations (int): default argument can be changed to integer values
                >=1 in order to update the progress indicators more than once 
                per iteration.

        """
        self.cnt += iterations
        next_perc = self._calc_percent()
        if next_perc > self.perc:
            self.perc = next_perc
            self._print_update()
            self._stream_flush()
        self._finish()
