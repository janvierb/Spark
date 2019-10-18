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


class VisitTemp(models.Model):
    _name = 'sparkit.visit.temp'

    implementation_partner = fields.Selection([('burera', 'Burera'),
                                               ('rulindo', 'Rulindo'),
                                               ('musanze', 'Musanze')])
    facilitator_id = fields.Many2one('res.users')
    co_facilitator_id = fields.Many2one('res.users')
    session_id = fields.Char()
    current_level = fields.Integer()
    community_id = fields.Many2one('sparkit.community')
    visit_date = fields.Date()
    next_visit_date = fields.Date()
    state = fields.Selection([
        ('visited', 'Visited'),
        ('cancelled', 'Cancelled')])
    visit_type = fields.Selection([
        ('community_meeting', 'Meeting - Community Meeting'),
        ('committee_meeting', 'Meeting - Committee Meeting'),
        ('meeting_other', 'Meeting - Other')])
    attendance_females = fields.Integer()
    attendance_males = fields.Integer()
    speakers_female = fields.Integer()
    speakers_male = fields.Integer()
    attendance_female_leaders = fields.Integer()
    attendance_male_leaders = fields.Integer()
    conflicts_in_meeting = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    conflicts_in_meeting_resolved = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    activity1_id = fields.Many2one('sparkit.fcapactivity')
    activity1_accomplished = fields.Boolean()
    activity2_id = fields.Many2one('sparkit.fcapactivity')
    activity2_accomplished = fields.Boolean()
    activity3_id = fields.Many2one('sparkit.fcapactivity')
    activity3_accomplished = fields.Boolean()
    leadership_reported_finances = fields.Selection([('1', 'Yes'), ('0', 'No')])
    leadership_presented_updated_cashbook = fields.Selection([('1', 'Yes'), ('0', 'No')])
    leadership_presented_accurate_cashbook = fields.Selection([('1', 'Yes'), ('0', 'No')])
    updated_accurate_receipts = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    phase = fields.Selection([
        ('community_identification', 'Community Identification'),
        ('planning', 'Planning'),
        ('implementation', 'Implementation'),
        ('post_implementation', 'Post Implementation'),
        ('graduated', 'Graduated')])
    step_id = fields.Many2one('sparkit.fcapstep', string="Step")
    phase_id = fields.Many2one('sparkit.fcapmap', string="Phase")
    phase_name = fields.Char()
    no_step = fields.Boolean(default=False)
    lang = fields.Selection([('en_US', 'English'),
                             ('RW', 'Kinyarwanda'),
                             ('Bl', 'Kirundi')])
    attendance_government_officials = fields.Integer()