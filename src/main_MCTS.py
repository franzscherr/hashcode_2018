import reader
import writer
import algorithm


def main():
    filenames = ('a_example.in', 'b_should_be_easy.in',
                 'c_no_hurry.in', 'd_metropolis.in', 'e_high_bonus.in')
    filename = filenames[1]
    out_filename = '../output/{}_MCTS.out'.format(filename[:filename.index('.')])
    r = reader.Reader('../dataset/' + filename)

    a = algorithm.MCTSAlgorithm(r.get_rides(), r.get_meta_info())
    a.assign_rides()

    w = writer.Writer(a.assigned_rides, out_filename)


if __name__ == '__main__':
    main()