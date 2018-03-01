import reader
import writer
import algorithm




def main():
<<<<<<< HEAD
    filenames = ('a_example.in', 'b_should_be_easy.in',
                 'c_no_hurry.in', 'd_metropolis.in', 'e_high_bonus.in')
    filename = filenames[4]
    out_filename = '../output/{}.out'.format(filename[:filename.index('.')])
    r = reader.Reader('../dataset/' + filename)
=======
    filenames = ('../dataset/a_example.in', '../dataset/b_should_be_easy.in',
                 '../dataset/c_no_hurry.in', '../dataset/d_metropolis.in', '../dataset/e_high_bonus.in')
    filename = filenames[4]
    out_filename = '../output/oute.out'
    r = reader.Reader(filename)
>>>>>>> 07b3f6c9f3b6983d8aac2a0e034d73a7ba6c97bd

    a = algorithm.GreedyAlgorithm(r.get_rides(), r.get_meta_info())
    a = algorithm.RideAssigner(r.get_rides(), r.get_meta_info())
    a.assign_rides()

    w = writer.Writer(a.assigned_rides, out_filename)


if __name__ == '__main__':
    main()