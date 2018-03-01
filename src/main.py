import reader
import writer
import algorithm


def main():
    filename = '../dataset/a_example.in'
    out_filename = '../output/out.out'
    r = reader.Reader(filename)

    a = algorithm.GreedyAlgorithm(r.get_rides(), r.get_meta_info())
    a.assign_rides()

    w = writer.Writer(a.assigned_rides, out_filename)


if __name__ == '__main__':
    main()