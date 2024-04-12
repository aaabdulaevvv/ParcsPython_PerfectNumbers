from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        n = self.read_input()

        # map
        mapped = []
        #r = (n+3) / len(self.workers)
        for i in range(0, len(self.workers)):
            print("map %d" % i)
            mapped.append(self.workers[i].mymap(2+i, len(self.workers), n+1))
            #mapped.append(self.workers[i].mymap(2 + i*r, 1, 2+(i+1)*r))

        # reduce
        reduced = self.myreduce(mapped)

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(l, step, r):
        print(l, step)
        perfect = []

        for i in range(l,r,step):
            sum = 1
            for j in range(2, i/2+1):
                if (i % j == 0):
                    sum += j
            if (sum == i):
                perfect.append(str(i))

        return perfect

    @staticmethod
    @expose
    def myreduce(mapped):
        print("reduce")
        output = []

        for perfect in mapped:
            print("reduce loop")
            output = output + perfect.value
        print("reduce done")
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        n = int(f.readline())
        f.close()
        return n

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(', '.join(output))
        f.write('\n')
        f.close()
        print("output done")