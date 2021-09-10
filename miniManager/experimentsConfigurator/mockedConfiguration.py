from .entities import *
import xmlschema

class MockedConfiguration():
    def getConfiguration(self):

        measure2 = Measure()
        measure2.id = 2
        measure2.name = 'rssi'
        measure2.unit = ''
        measurement2 = Measurement()
        measurement2.period = 1
        measurement2.measure = measure2

        measure3 = Measure()
        measure3.id = 3
        measure3.name = 'channel'
        measure3.unit = ''
        measurement3 = Measurement()
        measurement3.period = 1
        measurement3.measure = measure3

        measure4 = Measure()
        measure4.id = 4
        measure4.name = 'channel'
        measure4.unit = ''
        measurement4 = Measurement()
        measurement4.period = 1
        measurement4.measure = measure4

        measure5 = Measure()
        measure5.id = 5 
        measure5.name = 'band'
        measure5.unit = ''
        measurement5 = Measurement()
        measurement5.period = 1
        measurement5.measure = measure5

        measure6 = Measure()
        measure6.id = 6
        measure6.name = 'ssid'
        measure6.unit = ''
        measurement6 = Measurement()
        measurement6.period = 1
        measurement6.measure = measure6

        measure7 = Measure()
        measure7.id = 7
        measure7.name = 'txpower'
        measure7.unit = ''
        measurement7 = Measurement()
        measurement7.period = 1
        measurement7.measure = measure7

        measure8 = Measure()
        measure8.id = 8
        measure8.name = 'ip'
        measure8.unit = ''
        measurement8 = Measurement()
        measurement8.period = 1
        measurement8.measure = measure8

        measure10 = Measure()
        measure10.id = 10
        measure10.name = 'position'
        measure10.unit = ''
        measurement10 = Measurement()
        measurement10.period = 1
        measurement10.measure = measure10

        measure11 = Measure()
        measure11.id = 11
        measure11.name = 'associatedto'
        measure11.unit = ''
        measurement11 = Measurement()
        measurement11.period = 1
        measurement11.measure = measure11


        configuration = Configuration()
        configuration.id = 1
        #configuration.medicao_schema = xmlschema.XMLSchema('experimentsConfigurator/mockedXMLSchema.xsd')
        configuration.measurements = [measurement2, measurement3, measurement4, measurement5, measurement6, measurement7, measurement8, measurement10, measurement11]

        return configuration