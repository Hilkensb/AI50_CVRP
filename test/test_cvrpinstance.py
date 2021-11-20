#!/usr/bin/env python3
# Standard Library
import unittest
import json

# Modules
from problem.cvrp.instance import Cvrp


class WidgetTestCase(unittest.TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.cvrp_instance: Cvrp = Cvrp(
            file_path="http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances/P/P-n16-k8.vrp",
            file_type="web"
        )

    def test_numberCustomer(self):
        """
        """

        self.assertEqual(
            self.cvrp_instance.nb_customer, 15,
            'Incorrect number of customers.'
        )

    def test_depotCoordinates(self):
        """
        """

        self.assertEqual(
             self.cvrp_instance.depot.getCoordinates(), (30, 40),
            'Incorrect position of the depot.'
        )
        
    def test_vehicleCapacity(self):
        """
        """

        self.assertEqual(
             self.cvrp_instance.vehicule_capacity, 35,
            'Incorrect vehicle capacity.'
        )
        
    def test_numberOfVehicle(self):
        """
        """

        self.assertEqual(
             self.cvrp_instance.minVehiculeNumber(), 8,
            'Incorrect minimum number of vehciles.'
        )

    def test_JSON(self):
        """
        """

        # Get the json
        cvrp_json: str = self.cvrp_instance.toJSON()
        # Copy from the conversion
        json_copy_instance: Cvrp = Cvrp()
        # Parse the JSON
        json_copy_instance.fromJSON(json=eval(cvrp_json))
        
        self.assertEqual(
             str(self.cvrp_instance), str(json_copy_instance),
            'Incorrect encoding and/or decoding JSON.'
        )

