from PyPDF2 import PdfReader
import os


def numbers(number):
    new = ''
    for i in number:
        if i in '.0123456789':
            new += i
    return new


class Document:
    def __init__(self, number, date, start, status, pal, bed):
        self.serialnumber = number
        self.date = date
        self.start = start
        self.status = status
        self.pal = pal
        self.bed = bed

    def __str__(self):
        strtext = 'Engine Serial Number: ' + self.serialnumber + '\n' + \
                  'Testbed: ' + self.bed + '\n' + \
                  'TST_PAL: ' + self.pal + '\n' + \
                  'Test Date: ' + self.date + '\n' + \
                  'Test Start: ' + self.start + '\n' + \
                  'Test Status: ' + self.status
        return strtext


class Values:
    def __init__(self, ratedhp, torquepeak, lowidle2):
        self.ratedhp = ratedhp
        self.torquepeak = torquepeak
        self.lowidle2 = lowidle2

    def __str__(self):
        strtext = 'RATED_HP \n' + \
                  'P: ' + self.ratedhp[0] + '\n' + \
                  'FB_RATE: ' + self.ratedhp[1] + '\n' + \
                  'P_OIL: ' + self.ratedhp[2] + '\n' + \
                  'OPA_ANGL: ' + self.ratedhp[3] + '\n \n' + \
                  'TORQUE_PEAK \n' + \
                  'TORQUE: ' + self.torquepeak[0] + '\n' + \
                  'FB_RATE: ' + self.torquepeak[1] + '\n' + \
                  'OPA_ANGL: ' + self.torquepeak[2] + '\n \n' + \
                  'LOW_IDLE_2 \n' + \
                  'P_OIL: ' + self.lowidle2[0] + '\n' + \
                  'OPA_ANGL: ' + self.lowidle2[1] + '\n'
        return strtext


previous = ''
for i in os.listdir(r'primer otchetov'):
    if '.pdf' in i and (previous[:-4] not in i or previous == '') and i[:-4] + '.txt' not in os.listdir('examples'):
        reader = PdfReader('primer otchetov\\' + i)
        if len(reader.pages) == 4:
            document = reader.pages[0].extract_text()
            listing = document.split('\n')
            for j in listing:
                if 'Engine Serial Number' in j and 'Page' not in j:
                    serialnumber = j.split()[3]
                elif 'Testbed' in j:
                    testbed = j.split()[3]
                elif 'Test Date' in j:
                    testdate = j.split()[3]
                elif 'Test Start' in j:
                    teststart = j.split()[2]
                elif 'TST_PAL' in j:
                    testpal = j.split()[1]
                elif 'Status:' in j:
                    n = j.split().index('Status:')
                    teststatus = j.split()[n+1]

            values = reader.pages[3].extract_text()
            listing = values.split('\n')
            for j in listing:
                match j:
                    case 'RATED_HP':
                        index = listing.index(j) + 1
                        head = listing[index]
                        while head != 'TORQUE_PEAK':
                            if 'P ' in head:
                                p = head.split()[3]
                            elif 'FB_RATE' in head:
                                fbrate = head.split()[3]
                            elif 'P_OIL' in head:
                                poil = head.split()[3]
                            elif 'OPA_ANLG' in head:
                                opanlg = head.split()[3]
                            index += 1
                            head = listing[index]
                        testratedhp = (p, fbrate, poil, opanlg)
                    case 'TORQUE_PEAK':
                        index = listing.index(j) + 1
                        head = listing[index]
                        while head != 'LOW_IDLE_2':
                            if 'TORQUE' in head:
                                torque = head.split()[3]
                            elif 'FB_RATE' in head:
                                fbrate = head.split()[3]
                            elif 'OPA_ANLG' in head:
                                opanlg = head.split()[3]
                            index += 1
                            head = listing[index]
                        testtorquepeak = (torque, fbrate, opanlg)
                    case 'LOW_IDLE_2':
                        index = listing.index(j) + 1
                        head = listing[index]
                        while head != 'Test Report':
                            if 'P_OIL' in head:
                                poil = head.split()[3]
                            elif 'OPA_ANLG' in head:
                                opanlg = head.split()[2]
                            index += 1
                            head = listing[index]
                        testlowidle2 = (poil, numbers(opanlg))
            testdata = Document(serialnumber, testdate, teststart, teststatus, testpal, testbed)
            testvalues = Values(testratedhp, testtorquepeak, testlowidle2)
            extention = testdata.serialnumber + ';' + testdata.bed + \
                        ';' + testdata.pal + ';' + testdata.date + \
                        ';' + testdata.start + ';' + testdata.status + \
                        ';' + testvalues.ratedhp[0] + ';' + testvalues.ratedhp[1] + \
                        ';' + testvalues.ratedhp[2] + ';' + testvalues.ratedhp[3] + \
                        ';' + testvalues.torquepeak[0] + ';' + testvalues.torquepeak[1] + \
                        ';' + testvalues.torquepeak[2] + ';' + testvalues.lowidle2[0] + \
                        ';' + testvalues.lowidle2[1]+';'
            name = numbers(testdata.date) + '_' + numbers(testdata.start) + '_' + \
                   testdata.serialnumber + '_' + testdata.status + '.txt'
            write = open('examples\\' + name, 'w')
            write.write(extention + '\n \n' + str(testdata) + '\n \n' + str(testvalues))
    previous = i




