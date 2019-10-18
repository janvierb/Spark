# -*- coding: utf-8 -*-
######################################################################################################
#
# Copyright (C) B.H.C. sprl - All Rights Reserved, http://www.bhc.be
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied,
# including but not limited to the implied warranties
# of merchantability and/or fitness for a particular purpose
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
######################################################################################################

import logging
from odoo import models, fields, api ,_

_logger = logging.getLogger(__name__)


class Community(models.Model):
    _inherit = 'sparkit.community'

    # Bukhonzo

    @api.multi
    def debugging_workflow(self):
        _logger.info('Debugging...')
        if self.state == 'post_implementation1':
            try:
                self.write({
                    'phase': 'implementation',
                    'state': 'imp_transition_strategy'
                })
                _logger.info('Debugging done !')
            except Exception as e:
                _logger.error(str(e))
        if self.state == 'post_implementation2':
            try:
                self.write({
                    'phase': 'post_implementation',
                    'state': 'post_implementation1'
                })
                _logger.info('Debugging done !')
            except Exception as e:
                _logger.error(str(e))
        if self.state == 'post_implementation3':
            try:
                self.write({
                    'phase': 'post_implementation',
                    'state': 'post_implementation2'
                })
                _logger.info('Debugging done !')
            except Exception as e:
                _logger.error(str(e))

