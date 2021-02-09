#ProgrammingLab Exam
#1st Appello - 09/02/2021

# Author : Vittorio Amoruso
# MAT : SM3201172

#Declaring custom Exception class
class ExamException(Exception):
    pass

#Declaring main Exam class
class CSVTimeSeriesFile:

    #Magic method as class constructor 
    #Class instances initialized on file name
    def __init__(self, name):
        self.name = name

    #Method to check and extract data from a file
    def get_data(self):

        #Checking whether file name is readable
        x = isinstance(self.name, str)
        if(x is False):
            raise ExamException('File name should be str type \n')

        #Checking whether file exists and could be opened
        try:
            afile = open(self.name, 'r')
        except:
            raise ExamException('Error opening File with {} name \n'.format(self.name))

        #Final list to return after having computed data
        list_to_return = [ ]

        #Checking whether file length is an invalid value
        file_length = 0

        for line in afile:
            
            file_length += 1

        if(file_length == 0):
            raise ExamException('Value list empty \n')
        
        #Resetting file "index" to the first line
        afile.seek(0, 0)

        #Starting computation of file data
        #For each line of the file only those who meet
        #the specifications will be considered
        for line in afile:

            try:
                elements = line.split(',')

                elements[0] = elements[0].strip()
                elements[1] = elements[1].strip()

                if(len(elements) != 2):
                    #print('Invalid amount of elements on line {}'.format(line))
                    continue

                if(elements[0] == 'epoch' or elements[0] == 'temperature'):
                    #print('Skipping Header line {}'.format(line))
                    continue

                if(elements[1] == 'epoch' or elements[1] == 'temperature'):
                    #print('Skipping Header line {}'.format(line))
                    continue

                timestamp_int_converted = int( float(elements[0]) )
                temperature_float_converted = float(elements[1])

                eventual_errors = ['', ' ', 'None', None]

                if(timestamp_int_converted in eventual_errors):
                    #print('Invalid input line : {}'.format(line))
                    continue

                if(timestamp_int_converted < 0):
                    #print('Invalid input line : {}'.format(line))
                    continue

                if(temperature_float_converted in eventual_errors):
                    #print('Invalid input line : {}'.format(line))
                    continue

                wrapper = [ timestamp_int_converted, temperature_float_converted ]
                list_to_return.append(wrapper)

            except:
                #print('Invalid input line : {}'.format(line))
                continue

        #Don't forget to close the file previously opened
        afile.close()

        #Checking whether extracted data allows
        #Unsorted or Duplicated elements
        epoch_values = [ ]

        for item in list_to_return:
            temp_cell = item[0]
            epoch_values.append(temp_cell)

        control_list = sorted(epoch_values)
        
        for item in range(0, len(epoch_values), 1):
            if(epoch_values[item] != control_list[item]):
                raise ExamException('Encountered Unsorted Timestamps \n')

        for index in range(0, len(epoch_values)-1, 1):
            for sndindex in range(index + 1, len(epoch_values), 1):
                if(epoch_values[index] == epoch_values[sndindex]):
                    raise ExamException('Encountered Duplicated Timestamps \n')

        return list_to_return 
        

#Declaring Function to calculate requested days statistics
def daily_stats(time_series):

    list_to_return = [ ]

    epoch_to_days_list = [ ]
    days_index = 0

    #For each day in the argument list
    #will create a sub-list (working_list) containing only values 
    #that belongs to that specific day
    #Min, max and average temperature will be computed from
    #each and every working_list then appended on to the
    #Final list that has to be returned
    for item in time_series:
        day_start_epoch = item[0] - (item[0] % 86400)

        if(day_start_epoch in epoch_to_days_list):
            continue
        else:
            epoch_to_days_list.append(day_start_epoch)

    for item in epoch_to_days_list:
        working_list = [ ]

        for snditem in time_series:
            day_start_epoch = snditem[0] - (snditem[0] % 86400)

            if(item == day_start_epoch):
                working_list.append(snditem[1])

        max_number = max(working_list)
        min_number = min(working_list)
        sum_value = sum(working_list)
        working_list_length = len(working_list)

        wrapper = [ min_number, max_number, sum_value/working_list_length ]
        list_to_return.append(wrapper)

    return list_to_return


#Declaring and initializing a CSVTimeSeriesFile instance
time_series_file = CSVTimeSeriesFile(name='data.csv')

#Dumping Data from the selected file
time_series = time_series_file.get_data()

#Declaring and initializing results variable
#N.b results elements will contain final days statistics
results = daily_stats(time_series)

#Printing each element of results list variable
print(results)