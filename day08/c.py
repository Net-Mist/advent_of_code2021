len_5 = []
len_6 = []
question_1_counter = 0
with open("input.txt") as f:
    s = 0
    for line in f.readlines():
        figure_to_signal = {}
        signal_to_figure = {}
        part_1 = line.split("|")[0].split()
        for signal in part_1:
            if len(signal) == 2:
                figure_to_signal[1] = signal
            if len(signal) == 4:
                figure_to_signal[4] = signal
            if len(signal) == 3:
                figure_to_signal[7] = signal
            if len(signal) == 7:
                figure_to_signal[8] = signal
            if len(signal) == 5:
                len_5.append(signal)
            if len(signal) == 6:
                len_6.append(signal)
        # we know 1 4 7 8
        # 4 - 1 gives segment present in 6 or 9 but not 0
        four_minus_one = [c for c in figure_to_signal[4] if c not in figure_to_signal[1]]

        # len 6 : 0, 6, 9
        for signal in len_6:
            if not (four_minus_one[0] in signal and four_minus_one[1] in signal):
                figure_to_signal[0] = signal
            elif figure_to_signal[1][0] in signal and figure_to_signal[1][1] in signal:
                figure_to_signal[9] = signal
            else:
                figure_to_signal[6] = signal

        # len 5 : 2 3 5
        for signal in len_5:
            # if 1 in the signal : 3
            if figure_to_signal[1][0] in signal and figure_to_signal[1][1] in signal:
                figure_to_signal[3] = signal
            # if signal in 6 :5
            elif all(c in figure_to_signal[6] for c in signal):
                figure_to_signal[5] = signal
            else:
                figure_to_signal[2] = signal

        # compute signal_to_figure:
        signal_to_figure = {}
        for i in range(0, 10):
            signal_to_figure["".join(sorted(figure_to_signal[i]))] = i

        part_2 = line.split("|")[1].split()
        n = 0
        for signal in part_2:
            s2 = "".join(sorted(signal))
            n = n * 10 + signal_to_figure[s2]
            if signal_to_figure[s2] in [1, 4, 7, 8]:
                question_1_counter += 1
        s += n

print("part1:", question_1_counter)
print("part2:", s)
