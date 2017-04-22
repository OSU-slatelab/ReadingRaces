class CommandLineUI(object):
    def display(self, n_best, creative_mispellings):
        labels = range(1, len(n_best) + 1)

        print('LABEL\tPRONUNCIATION\t\tSOUNDS-LIKE SPELLING')
        for line in zip(labels, n_best, creative_mispellings):
            print(str(line[0]) + '\t' + str(line[1]) + '\t' + line[2])

    def prompt_choice(self, n_best, creative_mispellings):
        self.display(n_best, creative_mispellings)
        prompt_string = ' '.join(("Please choose a pronunciation number to hear pronounced,",
            "between 1 and", str(len(n_best)), "or enter 's' to enter your own sounds-like pronunciation: "))
        valid_choices = range(1, len(n_best) + 1)
        choice = raw_input(prompt_string).lower().strip()

        while (choice != 's') and (int(choice) not in valid_choices):
            print('Invalid choice: ' + str(choice) + '\nValid choices are: ' + str(valid_choices))
            choice = raw_input(prompt_string).lower().strip()

        if choice == 's':
            return choice
        return n_best[int(choice)-1]

    def get_sounds_like(self, word):
        sounds_like = raw_input('Enter the sounds-like spelling: ').upper().strip()
        return sounds_like

    def get_user_acceptance(self):
        res = ''
        while res not in ['y','n']:
            res = raw_input('Is this the correct pronunciation? (y/n): ').lower().strip()

        return res == 'y'

    def prompt_audio(self):
        return raw_input('If you would like to provide a pre-recorded .wav file, enter the path.'
                + ' If you would like to record the word now, enter \'r\': ')

    def show_new(self, word):
        print('Out-of-vocabulary word found:\t' + word)

