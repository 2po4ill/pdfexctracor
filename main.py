from PyPDF2 import PdfReader, PdfWriter
import os

path = open('PATH.txt', 'r')
pdfs = path.readline()[:-1]
archive = path.readline()[:-1]
examples = path.readline()[:-1]


def numbers(number):
    new = ''
    for m in number:
        if m in '.0123456789':
            new += m
    return new


def verify(file):
    for pdf in os.listdir(examples)[::-1]:
        if pdf[:-4] in file and pdf != '':
            return False
    return True


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
    def __init__(self, lowidle, highidle, ratedhp, torquepeak, lowidle2):
        self.lowidle = lowidle
        self.highidle = highidle
        self.ratedhp = ratedhp
        self.torquepeak = torquepeak
        self.lowidle2 = lowidle2

    def __str__(self):
        strtext = 'LOW_IDLE \n' + \
                  'SPEED: ' + '\n' + str(self.lowidle[0]) + '\n' + \
                  'P_OIL: ' + '\n' + str(self.lowidle[1]) + '\n' + \
                  'OPA_ANGL: ' + '\n' + str(self.lowidle[2]) + '\n \n' + \
                  'HIGH_IDLE \n' + \
                  'SPEED: ' + '\n' + str(self.highidle[0]) + '\n' + \
                  'P_OIL: ' + '\n' + str(self.highidle[1]) + '\n \n' + \
                  'RATED_HP \n' + \
                  'SPEED: ' + '\n' + str(self.ratedhp[0]) + '\n' + \
                  'P: ' + '\n' + str(self.ratedhp[1]) + '\n' + \
                  'FB_RATE: ' + '\n' + str(self.ratedhp[2]) + '\n' + \
                  'P_INTAKE: ' + '\n' + str(self.ratedhp[3]) + '\n' + \
                  'P_OIL: ' + '\n' + str(self.ratedhp[4]) + '\n' + \
                  'BLOW_VAL: ' + '\n' + str(self.ratedhp[5]) + '\n' + \
                  'OPA_ANGL: ' + '\n' + str(self.ratedhp[6]) + '\n' + \
                  'T_FUEL: ' + '\n' + str(self.ratedhp[7]) + '\n' + \
                  'P_FUEL: ' + '\n' + str(self.ratedhp[8]) + '\n' + \
                  'T_TUR_IN: ' + '\n' + str(self.ratedhp[9]) + '\n \n' + \
                  'TORQUE_PEAK \n' + \
                  'SPEED: ' + '\n' + str(self.torquepeak[0]) + '\n' + \
                  'TORQUE: ' + '\n' + str(self.torquepeak[1]) + '\n' + \
                  'FB_RATE: ' + '\n' + str(self.torquepeak[2]) + '\n' + \
                  'BLOW_VAL: ' + '\n' + str(self.torquepeak[3]) + '\n' + \
                  'OPA_ANGL: ' + '\n' + str(self.torquepeak[4]) + '\n' + \
                  'T_FUEL: ' + '\n' + str(self.torquepeak[5]) + '\n' + \
                  'P_FUEL: ' + '\n' + str(self.torquepeak[6]) + '\n' + \
                  'T_TUR_IN: ' + '\n' + str(self.torquepeak[7]) + '\n \n' + \
                  'LOW_IDLE_2 \n' + \
                  'SPEED: ' + '\n' + str(self.lowidle2[0]) + '\n' + \
                  'P_OIL: ' + '\n' + str(self.lowidle2[1]) + '\n' + \
                  'OPA_ANGL: ' + '\n' + str(self.lowidle2[2]) + '\n'
        return strtext


class ValueNode:
    def __init__(self, unit, lowerlimit, value, upperlimit, status):
        self.unit = unit
        self.lowerlimit = lowerlimit
        self.value = value
        self.upperlimit = upperlimit
        self.status = status

    def __str__(self):
        text = 'unit: ' + self.unit + '\n' + \
               'lowerlimit: ' + self.lowerlimit + '\n' + \
               'value: ' + self.value + '\n' + \
               'upperlimit: ' + self.upperlimit + '\n' + \
               'status: ' + self.status + '\n'
        return text

    def extention(self):
        text = self.unit + ';' + self.lowerlimit + \
               ';' + self.value + ';' + self.upperlimit + \
               ';' + self.status
        return text


def tablerules(line):
    if len(line) == 6:
        incurrent = ValueNode(line[1], line[2], line[3], line[4], line[5])
    elif len(line) == 5:
        try:
            if float(line[2]) > float(line[3]):
                incurrent = ValueNode(line[1], '', line[3], line[2], line[4])
            else:
                incurrent = ValueNode(line[1], line[2], line[3], '', line[4])
        except ValueError:
            incurrent = ValueNode(line[1], line[2], line[3], '', line[4])
    elif len(line) == 4:
        incurrent = ValueNode(line[1], '', line[2], '', line[3])
    else:
        incurrent = ValueNode(line[1], '', numbers(line[2]), '', '')
    return incurrent


for i in os.listdir(pdfs):
    if '.pdf' in i:
        reader = PdfReader(pdfs + '\\' + i)
        writer = PdfWriter()
        flag = verify(i)
        if flag:
            if len(reader.pages) < 9:
                document = reader.pages[0].extract_text()
                listing = document.split('\n')
                serialnumber, testdate, teststart, teststatus, testpal, testbed = '', '', '', '', '', ''
                clearance = [ValueNode('', '', '', '', '') for o in range(11)]
                speed, p, torque, fbrate, pintake, poil, blowval, opanlg, tfuel, pfuel, tturin = clearance
                testlowidle = (speed, poil, opanlg)
                testhighidle = (speed, poil)
                testratedhp = (speed, p, fbrate, pintake, poil, blowval, opanlg, tfuel, pfuel, tturin)
                testtorquepeak = (speed, torque, fbrate, blowval, opanlg, tfuel, pfuel, tturin)
                testlowidle2 = (speed, poil, opanlg)
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
                        teststatus = j.split()[n + 1]

                values = reader.pages[-1].extract_text()
                listing = values.split('\n')
                for j in listing:
                    match j:
                        case 'LOW_IDLE':
                            if j != 'LOW_IDLE_2':
                                index = listing.index(j) + 1
                                head = listing[index]
                                while head != 'HIGH_IDLE':
                                    if 'SPEED' in head:
                                        speed = tablerules(head.split())
                                    elif 'P_OIL' in head:
                                        poil = tablerules(head.split())
                                    elif 'OPA_ANLG' in head:
                                        opanlg = tablerules(head.split())
                                    index += 1
                                    if index != len(listing):
                                        head = listing[index]
                                    else:
                                        break
                                testlowidle = (speed, poil, opanlg)
                                speed, p, torque, fbrate, pintake, poil, blowval, opanlg, tfuel, pfuel, tturin = clearance
                        case 'HIGH_IDLE':
                            index = listing.index(j) + 1
                            head = listing[index]
                            while head != 'RATED_HP':
                                if 'SPEED' in head:
                                    speed = tablerules(head.split())
                                elif 'P_OIL' in head:
                                    poil = tablerules(head.split())
                                index += 1
                                if index != len(listing):
                                    head = listing[index]
                                else:
                                    break
                            testhighidle = (speed, poil)
                            speed, p, torque, fbrate, pintake, poil, blowval, opanlg, tfuel, pfuel, tturin = clearance
                        case 'RATED_HP':
                            index = listing.index(j) + 1
                            head = listing[index]
                            while head != 'TORQUE_PEAK':
                                if 'SPEED' in head:
                                    speed = tablerules(head.split())
                                elif 'P ' in head:
                                    p = tablerules(head.split())
                                elif 'FB_RATE' in head:
                                    fbrate = tablerules(head.split())
                                elif 'P_INTAKE' in head:
                                    pintake = tablerules(head.split())
                                elif 'P_OIL' in head:
                                    poil = tablerules(head.split())
                                elif 'BLOW_VAL' in head:
                                    blowval = tablerules(head.split())
                                elif 'OPA_ANLG' in head:
                                    opanlg = tablerules(head.split())
                                elif 'T_FUEL' in head:
                                    tfuel = tablerules(head.split())
                                elif 'P_FUEL' in head:
                                    pfuel = tablerules(head.split())
                                elif 'T_TUR_IN' in head:
                                    tturin = tablerules(head.split())
                                index += 1
                                if index != len(listing):
                                    head = listing[index]
                                else:
                                    break
                            testratedhp = (speed, p, fbrate, pintake, poil, blowval, opanlg, tfuel, pfuel, tturin)
                            speed, p, torque, fbrate, pintake, poil, blowval, opanlg, tfuel, pfuel, tturin = clearance
                        case 'TORQUE_PEAK':
                            index = listing.index(j) + 1
                            head = listing[index]
                            while head != 'LOW_IDLE_2' or 'TORQUE_PEAK' in head:
                                if 'SPEED' in head:
                                    speed = tablerules(head.split())
                                elif 'TORQUE' in head and 'PEAK' not in head:
                                    torque = tablerules(head.split())
                                elif 'FB_RATE' in head:
                                    fbrate = tablerules(head.split())
                                elif 'BLOW_VAL' in head:
                                    blowval = tablerules(head.split())
                                elif 'OPA_ANLG' in head:
                                    opanlg = tablerules(head.split())
                                elif 'T_FUEL' in head:
                                    tfuel = tablerules(head.split())
                                elif 'P_FUEL' in head:
                                    pfuel = tablerules(head.split())
                                elif 'T_TUR_IN' in head:
                                    tturin = tablerules(head.split())
                                index += 1
                                if index != len(listing):
                                    head = listing[index]
                                else:
                                    break
                            testtorquepeak = (speed, torque, fbrate, blowval, opanlg, tfuel, pfuel, tturin)
                            speed, p, torque, fbrate, pintake, poil, blowval, opanlg, tfuel, pfuel, tturin = clearance
                        case 'LOW_IDLE_2':
                            index = listing.index(j) + 1
                            head = listing[index]
                            while head != 'Test Report':
                                if 'SPEED' in head:
                                    speed = tablerules(head.split())
                                elif 'P_OIL' in head:
                                    poil = tablerules(head.split())
                                elif 'OPA_ANLG' in head:
                                    opanlg = tablerules(head.split())
                                index += 1
                                head = listing[index]
                            testlowidle2 = (speed, poil, opanlg)
                            speed, p, torque, fbrate, pintake, poil, blowval, opanlg, tfuel, pfuel, tturin = clearance
                testdata = Document(serialnumber, testdate, teststart, teststatus, testpal, testbed)
                testvalues = Values(testlowidle, testhighidle, testratedhp, testtorquepeak, testlowidle2)
                extention = testdata.serialnumber + ';' + testdata.bed + \
                            ';' + testdata.pal + ';' + testdata.date + \
                            ';' + testdata.start + ';' + testdata.status + \
                            ';' + testvalues.lowidle[0].extention() + ';' + testvalues.lowidle[1].extention() + \
                            ';' + testvalues.lowidle[2].extention() + ';' + testvalues.highidle[0].extention() + \
                            ';' + testvalues.highidle[1].extention() + \
                            ';' + testvalues.ratedhp[0].extention() + ';' + testvalues.ratedhp[1].extention() + \
                            ';' + testvalues.ratedhp[2].extention() + ';' + testvalues.ratedhp[3].extention() + \
                            ';' + testvalues.ratedhp[4].extention() + ';' + testvalues.ratedhp[5].extention() + \
                            ';' + testvalues.ratedhp[6].extention() + ';' + testvalues.ratedhp[7].extention() + \
                            ';' + testvalues.ratedhp[8].extention() + ';' + testvalues.ratedhp[9].extention() + \
                            ';' + testvalues.torquepeak[0].extention() + ';' + testvalues.torquepeak[1].extention() + \
                            ';' + testvalues.torquepeak[2].extention() + ';' + testvalues.torquepeak[3].extention() + \
                            ';' + testvalues.torquepeak[4].extention() + ';' + testvalues.torquepeak[5].extention() + \
                            ';' + testvalues.torquepeak[6].extention() + ';' + testvalues.torquepeak[7].extention() + \
                            ';' + testvalues.lowidle2[0].extention() + testvalues.lowidle2[1].extention() + \
                            ';' + testvalues.lowidle2[2].extention() + ';'
                name = numbers(testdata.date) + '_' + numbers(testdata.start) + '_' + \
                       testdata.serialnumber + '_' + testdata.status
                write = open(examples + '\\' + name + '.txt', 'w')
                write.write(extention + '\n \n' + str(testdata) + '\n \n' + str(testvalues))
        if len(reader.pages) < 8:
            for x in reader.pages:
                writer.add_page(x)
            writer.write(archive + '\\' + i)
            if os.path.exists(archive + '\\' + i) and os.stat(archive + '\\' + i).st_size > 1000:
                os.remove(pdfs + '\\' + i)
