import reader
import writer
import algorithm




def main():
    filenames = ('../dataset/a_example.in', '../dataset/b_should_be_easy.in',
                 '../dataset/c_no_hurry.in', '../dataset/d_metropolis.in', '../dataset/e_high_bonus.in')
    filename = filenames[4]
    out_filename = '../output/oute.out'
    r = reader.Reader(filename)

    a = algorithm.GreedyAlgorithm(r.get_rides(), r.get_meta_info())
    a = algorithm.RideAssigner(r.get_rides(), r.get_meta_info())
    a.assign_rides()

    w = writer.Writer(a.assigned_rides, out_filename)


if __name__ == '__main__':
    main()