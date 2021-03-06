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

import appier
import appier_extras

class BudyBase(appier_extras.admin.Base):

    tokens = appier.field(
        index = True,
        safe = True
    )

    @classmethod
    def token_names(cls):
        return []

    @classmethod
    def find_s(cls, *args, **kwargs):
        find_s = kwargs.get("find_s", None)
        if find_s: kwargs["find_s"] = cls._simplify(find_s)
        return cls.find(*args, **kwargs)

    @classmethod
    def _simplify(cls, value):
        value = value.lower()
        value = value.replace(appier.legacy.u("á"), "a")
        value = value.replace(appier.legacy.u("é"), "e")
        value = value.replace(appier.legacy.u("í"), "i")
        value = value.replace(appier.legacy.u("ó"), "o")
        value = value.replace(appier.legacy.u("ú"), "u")
        value = value.replace(appier.legacy.u("ã"), "a")
        value = value.replace(appier.legacy.u("õ"), "o")
        value = value.replace(appier.legacy.u("â"), "a")
        value = value.replace(appier.legacy.u("ô"), "o")
        value = value.replace(appier.legacy.u("ç"), "c")
        return value

    @classmethod
    def _pluralize(cls, value):
        return value + "s"

    @appier.operation(name = "Update Tokens")
    def update_search_description_s(self):
        self._update_tokens()
        self.save()

    def pre_save(self):
        appier_extras.admin.Base.pre_save(self)
        self._update_tokens()

    def _update_tokens(self):
        cls = self.__class__
        tokens = []
        for name, pluralize in cls.token_names():
            field_tokens = self._get_tokens(name, pluralize = pluralize)
            tokens.extend(field_tokens)
        tokens = list(set(tokens))
        tokens.sort()
        self.tokens = "|".join(tokens)

    def _get_tokens(self, name, pluralize = False):
        cls = self.__class__

        tokens = []

        names = name.split(".")
        name = names[0]
        names = names[1:] if len(names) > 1 else []
        if not hasattr(self, name): return []

        value = getattr(self, name)
        if not value: return []

        is_iterable = hasattr(value, "__iter__")
        is_iterable = is_iterable and not appier.legacy.is_string(value, all = True)
        values = value if is_iterable else [value]

        for value in values:
            for _name in names:
                if not value: break
                value = getattr(value, _name)
            if not value: continue
            token = value
            token = cls._simplify(token)
            token_p = cls._pluralize(token)
            tokens.append(token)
            if pluralize: tokens.append(token_p)

        return tokens
