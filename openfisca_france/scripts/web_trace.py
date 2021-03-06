#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Send scenario to tracer."""


import datetime
import io
import json
import logging
import os
import urllib
import webbrowser


from openfisca_core import periods

app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def trace(scenario, variables, period = None, browser_name = 'chromium',
          api_url = u"http://api.openfisca.fr", json_dumped_file = None):

    scenario_json = scenario.to_json()
    simulation_json = {
        "scenarios": [scenario_json],
        "variables": variables,
        }
    trace_base_url = u"http://www.openfisca.fr/outils/trace"
    url = trace_base_url + "?" + urllib.urlencode({
        "simulation": json.dumps(simulation_json),
        "api_url": api_url,
        })
    browser = webbrowser.get(browser_name)
    browser.open_new_tab(url)
    if json_dumped_file:
        with io.open(json_dumped_file, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(scenario_json, ensure_ascii=False, encoding='utf-8', indent = 2)))


if __name__ == '__main__':
    from openfisca_france.tests.base import tax_benefit_system
    period = "2014-12"
    parent1 = dict(
        birth = datetime.date(periods.period(period).start.year - 40, 1, 1),
        salbrut = {"2014-12": 1445.38},
        )

    scenario = tax_benefit_system.new_scenario().init_single_entity(
        period = period,
        parent1 = parent1,
        )
    variables = ["salsuperbrut"]
    trace(
        scenario,
        variables,
        api_url = u"http://127.0.0.1:2000",
        json_dumped_file = "test_smicard.json",
        )
