#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Budy
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Budy.
#
# Hive Budy is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Budy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Budy. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import logging
import unittest

import appier

import budy

class ProductTest(unittest.TestCase):

    def setUp(self):
        self.app = budy.BudyApp(level = logging.ERROR)

    def tearDown(self):
        self.app.unload()
        adapter = appier.get_adapter()
        adapter.drop_db()

    def test_add_remove_images(self):
        file = appier.typesf.ImageFile(
            dict(
                name = "name",
                data = "data",
                mime = "mime"
            )
        )

        media_1 = budy.Media(
            description = "description",
            label = "label",
            order = 1,
            file = file
        )
        media_1.save()

        media_2 = budy.Media(
            description = "description",
            label = "label",
            order = 1,
            file = file
        )
        media_2.save()

        product = budy.Product(
            short_description = "product",
            gender = "Male",
            price = 10.0
        )
        product.save()

        self.assertEqual(len(product.images), 0)

        product.add_image_s(media_1)

        self.assertEqual(len(product.images), 1)
        self.assertEqual(product.images[0].id, media_1.id)

        product.add_image_s(media_1)

        self.assertEqual(len(product.images), 1)
        self.assertEqual(product.images[0].id, media_1.id)

        product.add_image_s(media_2)

        self.assertEqual(len(product.images), 2)
        self.assertEqual(product.images[0].id, media_1.id)
        self.assertEqual(product.images[1].id, media_2.id)

        product = product.reload()

        self.assertEqual(len(product.images), 2)
        self.assertEqual(product.images[0].id, media_1.id)
        self.assertEqual(product.images[1].id, media_2.id)

        product.remove_image_s(media_1)

        self.assertEqual(len(product.images), 1)
        self.assertEqual(product.images[0].id, media_2.id)

        product.remove_image_s(media_1)

        self.assertEqual(len(product.images), 1)
        self.assertEqual(product.images[0].id, media_2.id)

        product.remove_image_s(media_2)

        self.assertEqual(len(product.images), 0)

        product = product.reload()

        self.assertEqual(len(product.images), 0)

    def test_measurements(self):
        product = budy.Product(
            short_description = "product",
            gender = "Male",
            price = 10.0,
            quantity_hand = None
        )
        product.save()

        measurement = budy.Measurement(
            name = "size",
            value = 12,
            price = None,
            quantity_hand = 2.0,
            product = product
        )
        measurement.save()

        self.assertEqual(product.quantity_hand, None)

        product.measurements.append(measurement)
        product.save()

        self.assertEqual(product.quantity_hand, 2.0)

        result = product.get_measurement(12, name = "size")

        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "size")
        self.assertEqual(result.value, 12)
        self.assertEqual(result.price, None)
        self.assertEqual(result.quantity_hand, 2.0)
        self.assertEqual(result.product.id, 1)
        self.assertEqual(result.product.short_description, "product")
        self.assertEqual(result.product.quantity_hand, 2.0)
