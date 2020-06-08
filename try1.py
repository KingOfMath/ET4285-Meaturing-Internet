import sys, getopt
import numpy as np


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
        f = fairness_Jain_Index(SR_1, SR_2)
        file.write(str(f) + "\n")
    file.close()

    RTT_1 = extractRTT(data_1, length_1)
    RTT_2 = extractRTT(data_2, length_2)

    Loss_1 = average(extractLoss(data_1, length_1))
    Loss_2 = average(extractLoss(data_2, length_2))

    ACK_1 = average(extractACK(data_1, length_1))
    ACK_2 = average(extractACK(data_2, length_2))

    if 1:
        SendRateFairness = fairness_Jain_Index(average(SendRate_1), average(SendRate_2))
        print(SendRateFairness)


def fairness_Jain_Index(x1, x2):
    return pow(x1 + x2, 2) / (2 * (pow(x1, 2) + pow(x2, 2)))


def fairness_Jain_Index_User(x1, x2):
    return x1 / pow(x1 + x2, 2) / (x1 + x2), x2 / pow(x1 + x2, 2) / (x1 + x2)


def fairness_entropy(x1, x2):
    p1 = x1 / (x1 + x2)
    p2 = x2 / (x1 + x2)
    return - p1 * np.log2(p1) - p2 * np.log2(p2)


def fairness_utility(x1, x2):
    # Yousefi’zadeh, H., Jafarkhani, H., & Habibi, A. (2005).
    # Layered media multicast control (LMMC): rate allocation and partitioning.
    # IEEE/ACM Transactions on Networking, 13(3), 540–553. doi:10.1109/tnet.2005.850227
    if x1 > x2:
        return x2 / x1
    else:
        return x1 / x2


# def fairness_unfairness(x1, x2):
#     # Ma, C. Y. T., Yau, D. K. Y., Jren-chit Chin, Rao, N. S. V., & Shankar, M. (2009).
#     # Matching and Fairness in Threat-Based Mobile Sensor Coverage.
#     # IEEE Transactions on Mobile Computing, 8(12), 1649–1662. doi:10.1109/tmc.2009.83
#     p1 = x1 / (x1 + x2)
#     p2 = x2 / (x1 + x2)

def fairness_QoE(x1, x2, H=2, L=0):
    return 1 - 2 * (np.std(x1, x2)) / (H - L)


def average(data):
    return sum(data) / len(data)


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
