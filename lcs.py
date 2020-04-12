from collections import deque
import copy

class LCS:
    def __init__(self, left, right):
        cells = [[None for _ in range(len(right) + 1)] for i in range(len(left) + 1)]
        cells[0][0] = (None, 0)
        for i in range(1, len(left) + 1):
            cells[i][0] = ((i - 1, 0), 0)
        for j in range(1, len(right) + 1):
            cells[0][j] = ((0, j - 1), 0)

        for i in range(1, len(left) + 1):
            for j in range(1, len(right) + 1):
                lel, rel = left[i - 1], right[j - 1]
                candidate = max(((i - 1, j), cells[i - 1][j][1]), ((i, j - 1), cells[i][j - 1][1]), key = lambda t: t[1])
                if lel != rel:
                    cells[i][j] = candidate
                    continue
                common = ((i - 1, j - 1), cells[i - 1][j - 1][1] + 1)
                cells[i][j] = max(common, candidate, key = lambda t: t[1])
        self.size = cells[len(left)][len(right)][1]
        trace = []
        start = (len(left), len(right))
        while start != (0, 0):
            step = cells[start[0]][start[1]][0]
            if start[0] == step[0]:
                trace.append((None, start[1] - 1))
            elif start[1] == step[1]:
                trace.append((start[0] - 1, None))
            else:
                trace.append((start[0] - 1, start[1] - 1))
            start = step
        self.trace = trace

    def diff(self):
        trace = copy.deepcopy(self.trace)
        diffs = []
        cur_diff = ((0, 0), (0, 0))
        lidx = 0
        ridx = 0
        while len(trace) > 0:
            lr = trace.pop()
            if lr[0] is None:
                cur_diff = ((cur_diff[0][0] + 1, cur_diff[0][1]), cur_diff[1])
                ridx += 1
            elif lr[1] is None:
                cur_diff = (cur_diff[0], (cur_diff[1][0] + 1, cur_diff[1][1]))
                lidx += 1
            else:
                if cur_diff[0][0] > 0 or cur_diff[1][0] > 0:
                    diffs.append(cur_diff)
                ridx += 1
                lidx += 1
                cur_diff = ((0, lidx), (0, ridx))

        if cur_diff[0][0] > 0 or cur_diff[1][0] > 0:
            diffs.append(cur_diff)
        
        return diffs
            
        

