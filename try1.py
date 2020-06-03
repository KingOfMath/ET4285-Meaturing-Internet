import sys, getopt


def run(argv):
    _, args = getopt.getopt(argv, "null")
    file = open('data/fairness.txt', 'w')

    data_1 = loadData(args[0])
    length_1 = len(data_1)

    data_2 = loadData(args[1])
    length_2 = len(data_2)

    SendRate_1 = extractSendRate(data_1, length_1)
    SendRate_2 = extractSendRate(data_2, length_2)
    for i in range(int(length_1 / 4)):
        SR_1 = SendRate_1[i]
        SR_2 = SendRate_2[i]
        f = fairness(SR_1, SR_2)
        file.write(str(f) + "\n")
    file.close()

    RTT_1 = extractRTT(data_1, length_1)
    RTT_2 = extractRTT(data_2, length_2)
    print(RTT_1)
    print(RTT_2)

    Loss_1 = average(extractLoss(data_1, length_1))
    Loss_2 = average(extractLoss(data_2, length_2))

    ACK_1 = average(extractACK(data_1, length_1))
    ACK_2 = average(extractACK(data_2, length_2))

    if 1:
        SendRateFairness = fairness(average(SendRate_1), average(SendRate_2))
        print(SendRateFairness)


    if 0:
        print(Loss_1)
        print(Loss_2)
        LossFairness = fairness(Loss_1, Loss_2)
        print(LossFairness)

    if 0:
        print(ACK_1)
        print(ACK_2)
        ACKFairness = fairness(ACK_1, ACK_2)
        print(ACKFairness)


def average(data):
    return sum(data) / len(data)


def fairness(x1, x2):
    return pow(x1 + x2, 2) / (2 * (pow(x1, 2) + pow(x2, 2)))


def extractSendRate(data, length):
    SendRate = []
    i = 0
    for i in range(0, length - 1):
        if (i + 1) % 4 == 1:
            SendRate.append(float(data[i]))
    return SendRate


def extractRTT(data, length):
    RTT = []
    for i in range(0, length - 1):
        if (i + 1) % 4 == 2:
            RTT.append(float(data[i]))
    return RTT


def extractLoss(data, length):
    Loss = []
    for i in range(0, length - 1):
        if (i + 1) % 4 == 3:
            Loss.append(float(data[i]))
    return Loss


def extractACK(data, length):
    ACK = []
    for i in range(0, length - 1):
        if (i + 1) % 4 == 0:
            ACK.append(float(data[i]))
    return ACK


def loadData(filename):
    with open(filename) as proto1:
        temp = proto1.read().splitlines()
        return temp


if __name__ == '__main__':
    run(sys.argv[1:])
