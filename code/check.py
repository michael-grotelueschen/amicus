


if __name__ == "__main__":
    ok_cases = []
    with open('ok_cases') as f:
        for line in f:
            case = line.split('.')[0]
            ok_cases.append(case)

    final_term_cases = []
    with open('2014_term_cases') as f:
        for line in f:
            case = line.replace('\n', '')
            final_term_cases.append(case)

    ok_cases_train_set = []
    ok_cases_test_set = []
    for case in ok_cases:
        if case in final_term_cases:
            ok_cases_test_set.append(case)
        else:
            ok_cases_train_set.append(case)

    with open('ok_cases_train_set', 'w') as f:
        f.write('\n'.join(ok_cases_train_set))

    with open('ok_cases_test_set', 'w') as f:
        f.write('\n'.join(ok_cases_test_set))