import sys


class ProgressBar:
    def __init__(self, total, status=''):
        self.current_count = 0
        self.total_count = total
        self.status = status

    def update_current_count(self, count):
        self.current_count = self.current_count + count

    def print(self):
        bar_len = 60
        filled_len = int(round(bar_len * self.current_count / float(self.total_count)))
        percents = 100.0 * self.current_count / float(self.total_count)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('[{0}] {1:.2f}% ...{2}\r'.format(bar, percents, self.status))
        sys.stdout.flush()
