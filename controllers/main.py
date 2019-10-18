# -*- coding: utf-8 -*-
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

import logging
import sys
from odoo import http, _
from odoo.http import request
from datetime import datetime
_logger = logging.getLogger(__name__)

#import importlib
#from importlib import reload
#reload(sys)
#sys.setdefaultencoding('utf8')


class Dashboard(http.Controller):

    @http.route('/web/ussd/callback', type="http", auth='public', csrf=False)
    def ussd_callback(self, text, sessionId, phoneNumber, serviceCode="", networkCode=None):

        users = request.env['res.users'].sudo().search([('id', '!=', 1)], order='id asc')
        users_tab = []
        for i in users:
            users_tab.append(i.id)

        visit_community_temp = request.env['sparkit.visit.temp']
        visit_community = request.env['sparkit.vrf']
        visit_ids = request.env['sparkit.visit.temp'].sudo().search([])
        current_level = 0

        text_array = text.split("*")
        user_response = text_array[len(text_array) - 1]

        _logger.info(user_response)
        _logger.info(networkCode)

        if current_level == 0:
            if user_response == '':
                partner = request.env['res.partner'].sudo().search(['|', ('phone', '=', phoneNumber), ('mobile', '=', phoneNumber)])
                if partner.user_ids:
                    ctx = request.env.context.copy()
                    ctx.update({
                        'lang': partner.lang,
                    })
                    request.env.context = ctx
                    visit_community_temp.sudo().create({
                        'session_id': sessionId,
                        'current_level': 1,
                        'lang': partner.lang
                    })
                    menu = (_("CON Implementation Partner :\n"))
                    menu += (_("1. Burera \n"))
                    menu += (_("2. Rulindo \n"))
                    menu += (_("3. Musanze \n"))
                    return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                else:
                    menu = (_("END Your phone number is not registered in our Odoo system. Transaction cancelled.\n"))
                    return request.render('sparkit_bhc.ussd_template', {'menu': menu})

        for temp in visit_ids:
            if temp.session_id == sessionId:
                ctx = request.env.context.copy()
                ctx.update({
                    'lang': temp.lang,
                })
                request.env.context = ctx
                if temp.current_level == 1:
                    facilitator_list = []
                    if int(user_response) == 1:
                        temp.sudo().write({
                            'implementation_partner': 'burera',
                            'current_level': 2
                        })
                        menu = (_("CON Partner Facilitator Name :\n"))
                        community = request.env['sparkit.community'].sudo().search([('district', '=', 'Burera'), ('phase', '!=', 'graduated')])
                        for i in community:
                            facilitator_list.append(i.facilitator_id.id)
                            facilitator_list.append(i.co_facilitator_id.id)
                        list_distinct = list(set(facilitator_list))
                        list_distinct.sort()
                        for j in list_distinct:
                            if j:
                                user = request.env['res.users'].sudo().search([('id', '=', j)])
                                if user:
                                    menu += ('%s : %s \n' % (user.id, user.name))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        temp.sudo().write({
                            'implementation_partner': 'rulindo',
                            'current_level': 2
                        })
                        menu = (_("CON Partner Facilitator Name :\n"))
                        community = request.env['sparkit.community'].sudo().search([('district', '=', 'Rulindo'), ('phase', '!=', 'graduated')])
                        for i in community:
                            facilitator_list.append(i.facilitator_id.id)
                            facilitator_list.append(i.co_facilitator_id.id)
                        list_distinct = list(set(facilitator_list))
                        list_distinct.sort()
                        for j in list_distinct:
                            if j:
                                user = request.env['res.users'].sudo().search([('id', '=', j)])
                                if user:
                                    menu += ('%s : %s \n' % (user.id, user.name))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 3:
                        temp.sudo().write({
                            'implementation_partner': 'musanze',
                            'current_level': 2
                        })
                        menu = (_("CON Partner Facilitator Name :\n"))
                        community = request.env['sparkit.community'].sudo().search([('district', '=', 'Musanze'), ('phase', '!=', 'graduated')])
                        for i in community:
                            facilitator_list.append(i.facilitator_id.id)
                            facilitator_list.append(i.co_facilitator_id.id)
                        list_distinct = list(set(facilitator_list))
                        list_distinct.sort()
                        for j in list_distinct:
                            if j:
                                user = request.env['res.users'].sudo().search([('id', '=', j)])
                                if user:
                                    menu += ('%s : %s \n' % (user.id, user.name))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                # Communauté dont la phase est différente de graduated
                if temp.current_level == 2:
                    facilitator_list = []
                    if temp.implementation_partner == 'burera':
                        community = request.env['sparkit.community'].sudo().search([('district', '=', 'Burera'), ('phase', '!=', 'graduated')])
                        for i in community:
                            facilitator_list.append(i.facilitator_id.id)
                            facilitator_list.append(i.co_facilitator_id.id)
                        list_distinct = list(set(facilitator_list))
                        list_distinct.sort()
                    if temp.implementation_partner == 'rulindo':
                        community = request.env['sparkit.community'].sudo().search([('district', '=', 'Rulindo')])
                        for i in community:
                            facilitator_list.append(i.facilitator_id.id)
                            facilitator_list.append(i.co_facilitator_id.id)
                        list_distinct = list(set(facilitator_list))
                        list_distinct.sort()
                    if temp.implementation_partner == 'musanze':
                        community = request.env['sparkit.community'].sudo().search([('district', '=', 'Musanze')])
                        for i in community:
                            facilitator_list.append(i.facilitator_id.id)
                            facilitator_list.append(i.co_facilitator_id.id)
                        list_distinct = list(set(facilitator_list))
                        list_distinct.sort()
                    if int(user_response) in list_distinct:
                        user = request.env['res.users'].sudo().search([('id', '=', int(user_response))])
                        temp.sudo().write({
                            'facilitator_id': user.id,
                            'co_facilitator_id': user.id,
                            'current_level': 3
                        })
                        if temp.implementation_partner == 'burera':
                            community2 = request.env['sparkit.community'].sudo().search([('district', '=', 'Burera')])
                            community_filtred = community2.sudo().search(
                                ['|', ('facilitator_id', '=', int(user_response)),
                                 ('co_facilitator_id', '=', int(user_response)), ('phase', '!=', 'graduated')])
                            menu = (_("CON Community:\n"))
                            for j in community_filtred:
                                menu += ('%s : %s \n' % (j.id, j.name))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        if temp.implementation_partner == 'rulindo':
                            community2 = request.env['sparkit.community'].sudo().search([('district', '=', 'Rulindo')])
                            community_filtred = community2.sudo().search(
                                ['|', ('facilitator_id', '=', int(user_response)),
                                 ('co_facilitator_id', '=', int(user_response)), ('phase', '!=', 'graduated')])
                            menu = (_("CON Community:\n"))
                            for j in community_filtred:
                                menu += ('%s : %s \n' % (j.id, j.name))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        if temp.implementation_partner == 'musanze':
                            community2 = request.env['sparkit.community'].sudo().search([('district', '=', 'Musanze')])
                            community_filtred = community2.sudo().search(
                                ['|', ('facilitator_id', '=', int(user_response)),
                                 ('co_facilitator_id', '=', int(user_response)), ('phase', '!=', 'graduated')])
                            menu = (_("CON Community:\n"))
                            for j in community_filtred:
                                menu += ('%s : %s \n' % (j.id, j.name))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 3:
                    if int(user_response):
                        community = request.env['sparkit.community'].sudo().search([('id', '=', int(user_response))])
                        phase = request.env['sparkit.fcapmap'].sudo().search([('phase', '=', community.phase)])
                        temp.sudo().write({
                            'current_level': 4,
                            'community_id': community.id,
                            'phase_id': phase.id,
                            'phase': community.phase
                        })
                        menu = (_("CON Date of the Meeting (MM/DD/YYYY):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 4:
                    if user_response:
                        try:
                            date = datetime.strptime(user_response, '%m/%d/%Y')
                            visit_date = date.strftime('%m/%d/%Y')
                            year = date.strftime('%Y')
                            if year >= '2019':
                                temp.sudo().write({
                                    'visit_date': visit_date,
                                    'current_level': 5
                                })
                                menu = (_("CON Date of next Meeting (MM/DD/YYYY):\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                            else:
                                menu = (_("CON Wrong date format, use 'MM/DD/YYYY':\n"))
                                menu += (_("Date of Meeting :\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        except:
                            menu = (_("CON Wrong date format, use 'MM/DD/YYYY':\n"))
                            menu += (_("Date of Meeting :\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 5:
                    if user_response:
                        try:
                            date = datetime.strptime(user_response, '%m/%d/%Y')
                            next_visit_date = date.strftime('%m/%d/%Y')
                            year = date.strftime('%Y')
                            if year >= '2019':
                                temp.sudo().write({
                                    'next_visit_date': next_visit_date,
                                    'current_level': 6
                                })
                                menu = (_("CON State:\n"))
                                menu += (_("1. Visited\n"))
                                menu += (_("2. Cancelled\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                            else:
                                menu = (_("CON Wrong date format, use 'MM/DD/YYYY':\n"))
                                menu += (_("Date of next Meeting :\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        except:
                            menu = (_("CON Wrong date format, use 'MM/DD/YYYY':\n"))
                            menu += (_("Date of next Meeting :\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 6:
                    if int(user_response) == 1:
                        steps = request.env['sparkit.fcapstep'].sudo().search([('phase_id', '=', temp.phase_id.id)])
                        if not steps:
                            temp.sudo().write({
                                'state': 'visited',
                                'no_step': True,
                                'current_level': 8
                            })
                            menu = (_("CON Meeting type:\n"))
                            menu += (_("1. Meeting - Community\n"))
                            menu += (_("2. Meeting - Committee\n"))
                            menu += (_("3. Meeting - Other\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        if steps:
                            temp.sudo().write({
                                'state': 'visited',
                                'current_level': 7
                            })
                            menu = (_("CON Step:\n"))
                            for i in steps:
                                menu += ('%s : %s \n' % (i.id, i.name))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        temp.sudo().write({
                            'current_level': 99
                        })

                if temp.current_level == 7:
                    steps = request.env['sparkit.fcapstep'].sudo().search([('phase_id', '=', temp.phase_id.id)])
                    steps_tab = []
                    for i in steps:
                        steps_tab.append(i.id)
                    if int(user_response) in steps_tab:
                        steps = request.env['sparkit.fcapstep'].sudo().search(
                            [('id', '=', int(user_response))])
                        temp.sudo().write({
                            'step_id': steps.id,
                            'current_level': 8
                        })
                        menu = (_("CON Meeting type:\n"))
                        menu += (_("1. Meeting - Community\n"))
                        menu += (_("2. Meeting - Committee\n"))
                        menu += (_("3. Meeting - Other\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 8:
                    if int(user_response) == 1:
                        temp.sudo().write({
                            'visit_type': 'community_meeting',
                            'current_level': 9
                        })
                        menu = (_("CON Female Attendance (type in number):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        temp.sudo().write({
                            'visit_type': 'committee_meeting',
                            'current_level': 9
                        })
                        menu = (_("CON Female Attendance (type in number):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 3:
                        temp.sudo().write({
                            'visit_type': 'meeting_other',
                            'current_level': 9
                        })
                        menu = (_("CON Female Attendance (type in number):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 9:
                    if int(user_response) >= 0:
                        temp.sudo().write({
                            'attendance_females': int(user_response),
                            'current_level': 10
                        })
                        menu = (_("CON Male Attendance (type in number):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 10:
                    if int(user_response) >= 0:
                        temp.sudo().write({
                            'attendance_males': int(user_response),
                            'current_level': 11
                        })
                        menu = (_("CON Female Speakers (type in number):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 11:
                    if int(user_response) >= 0:
                        temp.sudo().write({
                            'speakers_female': int(user_response),
                            'current_level': 12
                        })
                        menu = (_("CON Male Speakers (type in number):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 12:
                    if int(user_response) >= 0:
                        temp.sudo().write({
                            'speakers_male': int(user_response),
                            'current_level': 13
                        })
                        menu = (_("CON Female leaders in Attendance (type in number):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 13:
                    if int(user_response) >= 0:
                        temp.sudo().write({
                            'attendance_female_leaders': int(user_response),
                            'current_level': 14
                        })
                        menu = (_("CON Male leaders in Attendance (type in number):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 14:
                    if int(user_response) >= 0:
                        temp.sudo().write({
                            'attendance_male_leaders': int(user_response),
                            'current_level': 15
                        })
                        menu = (_("CON Government Officials in Attendance (type in number):\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 15:
                    if int(user_response) >= 0:
                        temp.sudo().write({
                            'attendance_government_officials': int(user_response),
                            'current_level': 16
                        })
                        menu = (_("CON Were there any conflicts in the meeting ?\n"))
                        menu += (_("1. Yes\n"))
                        menu += (_("2. No\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 16:
                    if int(user_response) == 1:
                        temp.sudo().write({
                            'conflicts_in_meeting': 'yes',
                            'current_level': 17
                        })
                        menu = (_("CON Were they resolved ?\n"))
                        menu += (_("1. Yes\n"))
                        menu += (_("2. No\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        if not temp.no_step:
                            temp.sudo().write({
                                'conflicts_in_meeting': 'no',
                                'current_level': 18
                            })
                            menu = (_("CON Activity 1 :\n"))
                            menu += (_('0 : No activity\n'))
                            activities = request.env['sparkit.fcapactivity'].sudo().search(
                                [('step_id', '=', temp.step_id.id)])
                            for i in activities:
                                menu += ('%s : %s \n' % (i.id, i.name))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        if temp.no_step:
                            temp.sudo().write({
                                'conflicts_in_meeting': 'no',
                                'current_level': 24
                            })
                            menu = (_("CON Did the community leaders provide an update on fiances during the meeting?\n"))
                            menu += (_("1. Yes\n"))
                            menu += (_("2. No\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 17:
                    if int(user_response) == 1:
                        if not temp.no_step:
                            temp.sudo().write({
                                'conflicts_in_meeting_resolved': 'yes',
                                'current_level': 18
                            })
                            menu = (_("CON Activity 1 :\n"))
                            menu += (_('0 : No activity\n'))
                            activities = request.env['sparkit.fcapactivity'].sudo().search(
                                [('step_id', '=', temp.step_id.id)])
                            for i in activities:
                                menu += ('%s : %s \n' % (i.id, i.name))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        if temp.no_step:
                            temp.sudo().write({
                                'conflicts_in_meeting_resolved': 'yes',
                                'current_level': 24
                            })
                            menu = (_("CON Did the community leaders provide an update on fiances during the meeting?\n"))
                            menu += (_("1. Yes\n"))
                            menu += (_("2. No\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        if not temp.no_step:
                            temp.sudo().write({
                                'conflicts_in_meeting_resolved': 'no',
                                'current_level': 18
                            })
                            menu = (_("CON Activity 1 :\n"))
                            menu += (_('0 : No activity\n'))
                            activities = request.env['sparkit.fcapactivity'].sudo().search(
                                [('step_id', '=', temp.step_id.id)])
                            for i in activities:
                                menu += ('%s : %s \n' % (i.id, i.name))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        if temp.no_step:
                            temp.sudo().write({
                                'conflicts_in_meeting_resolved': 'no',
                                'current_level': 24
                            })
                            menu = (_("CON Did the community leaders provide an update on fiances during the meeting?\n"))
                            menu += (_("1. Yes\n"))
                            menu += (_("2. No\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 18:
                    activities = request.env['sparkit.fcapactivity'].sudo().search(
                        [('step_id', '=', temp.step_id.id)])
                    activities_tab = []
                    for i in activities:
                        activities_tab.append(i.id)
                    if int(user_response) in activities_tab or int(user_response) == 0:
                        if int(user_response) == 0:
                            if temp.phase != 'planning':
                                temp.sudo().write({
                                    'current_level': 24
                                })
                                menu = (_("CON Did the community leaders provide an update on fiances during the meeting?\n"))
                                menu += (_("1. Yes\n"))
                                menu += (_("2. No\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                            else:
                                visit_community.sudo().create({
                                    'facilitator_id': temp.facilitator_id.id or False,
                                    'co_facilitator_id': temp.co_facilitator_id.id or False,
                                    'community_id': temp.community_id.id or False,
                                    'visit_date': temp.visit_date or False,
                                    'next_visit_date': temp.next_visit_date or False,
                                    'state': temp.state or False,
                                    'visit_type': temp.visit_type or False,
                                    'attendance_females': temp.attendance_females or False,
                                    'attendance_males': temp.attendance_males or False,
                                    'speakers_female': temp.speakers_female or False,
                                    'speakers_male': temp.speakers_male or False,
                                    'attendance_female_leaders': temp.attendance_female_leaders or False,
                                    'attendance_male_leaders': temp.attendance_male_leaders or False,
                                    'attendance_government_officials': temp.attendance_government_officials or False,
                                    'conflicts_in_meeting': temp.conflicts_in_meeting or False,
                                    'conflicts_in_meeting_resolved': temp.conflicts_in_meeting_resolved or False,
                                    'activity1_id': temp.activity1_id.id or False,
                                    'activity1_accomplished': temp.activity1_accomplished or False,
                                    'activity2_id': temp.activity2_id.id or False,
                                    'activity2_accomplished': temp.activity2_accomplished or False,
                                    'activity3_id': temp.activity3_id.id or False,
                                    'activity3_accomplished': temp.activity3_accomplished or False,
                                    'phase_id': temp.phase_id or False,
                                    'phase': temp.phase or False,
                                    'phase_name': temp.phase_id.name or False,
                                    'step_id': temp.step_id.id or False,
                                    'created_on_ussd': True,
                                })
                                temp.sudo().unlink()
                                menu = (_("END Visit saved, thank you !\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        else:
                            activities = request.env['sparkit.fcapactivity'].sudo().search([('id', '=', int(user_response))])
                            temp.sudo().write({
                                'activity1_id': activities.id,
                                'current_level': 19
                            })
                            menu = (_("CON Activity 1 accomplished ?\n"))
                            menu += (_("1. Yes\n"))
                            menu += (_("2. No\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 19:
                    if int(user_response) == 1:
                        temp.sudo().write({
                            'activity1_accomplished': True,
                            'current_level': 20
                        })
                        menu = (_("CON Activity 2 :\n"))
                        menu += (_("0 : No activity\n"))
                        activities = request.env['sparkit.fcapactivity'].sudo().search(
                            [('step_id', '=', temp.step_id.id)])
                        for i in activities:
                            menu += ('%s : %s \n' % (i.id, i.name))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        temp.sudo().write({
                            'activity1_accomplished': False,
                            'current_level': 20
                        })
                        menu = (_("CON Activity 2 :\n"))
                        menu += (_("0 : No activity\n"))
                        activities = request.env['sparkit.fcapactivity'].sudo().search(
                            [('step_id', '=', temp.step_id.id)])
                        for i in activities:
                            menu += ('%s : %s \n' % (i.id, i.name))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 20:
                    activities = request.env['sparkit.fcapactivity'].sudo().search(
                        [('step_id', '=', temp.step_id.id)])
                    activities_tab = []
                    for i in activities:
                        activities_tab.append(i.id)
                    if int(user_response) in activities_tab or int(user_response) == 0:
                        if int(user_response) == 0:
                            if temp.phase != 'planning':
                                temp.sudo().write({
                                    'current_level': 24
                                })
                                menu = (_("CON Did the community leaders provide an update on fiances during the meeting?\n"))
                                menu += (_("1. Yes\n"))
                                menu += (_("2. No\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                            else:
                                visit_community.sudo().create({
                                    'facilitator_id': temp.facilitator_id.id or False,
                                    'co_facilitator_id': temp.co_facilitator_id.id or False,
                                    'community_id': temp.community_id.id or False,
                                    'visit_date': temp.visit_date or False,
                                    'next_visit_date': temp.next_visit_date or False,
                                    'state': temp.state or False,
                                    'visit_type': temp.visit_type or False,
                                    'attendance_females': temp.attendance_females or False,
                                    'attendance_males': temp.attendance_males or False,
                                    'speakers_female': temp.speakers_female or False,
                                    'speakers_male': temp.speakers_male or False,
                                    'attendance_female_leaders': temp.attendance_female_leaders or False,
                                    'attendance_male_leaders': temp.attendance_male_leaders or False,
                                    'attendance_government_officials': temp.attendance_government_officials or False,
                                    'conflicts_in_meeting': temp.conflicts_in_meeting or False,
                                    'conflicts_in_meeting_resolved': temp.conflicts_in_meeting_resolved or False,
                                    'activity1_id': temp.activity1_id.id or False,
                                    'activity1_accomplished': temp.activity1_accomplished or False,
                                    'activity2_id': temp.activity2_id.id or False,
                                    'activity2_accomplished': temp.activity2_accomplished or False,
                                    'activity3_id': temp.activity3_id.id or False,
                                    'activity3_accomplished': temp.activity3_accomplished or False,
                                    'phase_id': temp.phase_id or False,
                                    'phase': temp.phase or False,
                                    'phase_name': temp.phase_id.name or False,
                                    'step_id': temp.step_id.id or False,
                                    'created_on_ussd': True,
                                })
                                temp.sudo().unlink()
                                menu = (_("END Visit saved, thank you !\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        else:
                            activities = request.env['sparkit.fcapactivity'].sudo().search([('id', '=', int(user_response))])
                            temp.sudo().write({
                                'activity2_id': activities.id,
                                'current_level': 21
                            })
                            menu = (_("CON Activity 2 accomplished ?\n"))
                            menu += (_("1. Yes\n"))
                            menu += (_("2. No\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 21:
                    if int(user_response) == 1:
                        temp.sudo().write({
                            'activity2_accomplished': True,
                            'current_level': 22
                        })
                        menu = (_("CON Activity 3 :\n"))
                        menu += (_("0 : No activity\n"))
                        activities = request.env['sparkit.fcapactivity'].sudo().search(
                            [('step_id', '=', temp.step_id.id)])
                        for i in activities:
                            menu += ('%s : %s \n' % (i.id, i.name))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        temp.sudo().write({
                            'activity2_accomplished': False,
                            'current_level': 22
                        })
                        menu = (_("CON Activity 3:\n"))
                        menu += (_("0 : No activity\n"))
                        activities = request.env['sparkit.fcapactivity'].sudo().search(
                            [('step_id', '=', temp.step_id.id)])
                        for i in activities:
                            menu += ('%s : %s \n' % (i.id, i.name))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 22:
                    activities = request.env['sparkit.fcapactivity'].sudo().search(
                        [('step_id', '=', temp.step_id.id)])
                    activities_tab = []
                    for i in activities:
                        activities_tab.append(i.id)
                    if int(user_response) in activities_tab or int(user_response) == 0:
                        if int(user_response) == 0:
                            if temp.phase != 'planning':
                                temp.sudo().write({
                                    'current_level': 24
                                })
                                menu = (_("CON Did the community leaders provide an update on fiances during the meeting?\n"))
                                menu += (_("1. Yes\n"))
                                menu += (_("2. No\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                            else:
                                visit_community.sudo().create({
                                    'facilitator_id': temp.facilitator_id.id or False,
                                    'co_facilitator_id': temp.co_facilitator_id.id or False,
                                    'community_id': temp.community_id.id or False,
                                    'visit_date': temp.visit_date or False,
                                    'next_visit_date': temp.next_visit_date or False,
                                    'state': temp.state or False,
                                    'visit_type': temp.visit_type or False,
                                    'attendance_females': temp.attendance_females or False,
                                    'attendance_males': temp.attendance_males or False,
                                    'speakers_female': temp.speakers_female or False,
                                    'speakers_male': temp.speakers_male or False,
                                    'attendance_female_leaders': temp.attendance_female_leaders or False,
                                    'attendance_male_leaders': temp.attendance_male_leaders or False,
                                    'attendance_government_officials': temp.attendance_government_officials or False,
                                    'conflicts_in_meeting': temp.conflicts_in_meeting or False,
                                    'conflicts_in_meeting_resolved': temp.conflicts_in_meeting_resolved or False,
                                    'activity1_id': temp.activity1_id.id or False,
                                    'activity1_accomplished': temp.activity1_accomplished or False,
                                    'activity2_id': temp.activity2_id.id or False,
                                    'activity2_accomplished': temp.activity2_accomplished or False,
                                    'activity3_id': temp.activity3_id.id or False,
                                    'activity3_accomplished': temp.activity3_accomplished or False,
                                    'phase_id': temp.phase_id or False,
                                    'phase': temp.phase or False,
                                    'phase_name': temp.phase_id.name or False,
                                    'step_id': temp.step_id.id or False,
                                    'created_on_ussd': True,
                                })
                                temp.sudo().unlink()
                                menu = (_("END Visit saved, thank you !\n"))
                                return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        else:
                            activities = request.env['sparkit.fcapactivity'].sudo().search(
                                [('id', '=', int(user_response))])
                            temp.sudo().write({
                                'activity3_id': activities.id,
                                'current_level': 23
                            })
                            menu = (_("CON Activity 3 accomplished ?\n"))
                            menu += (_("1. Yes\n"))
                            menu += (_("2. No\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 23:
                    if temp.phase != 'planning':
                        if int(user_response) == 1:
                            temp.sudo().write({
                                'activity3_accomplished': True,
                                'current_level': 24
                            })
                            menu = (_("CON Did the community leaders provide an update on fiances during the meeting?\n"))
                            menu += (_("1. Yes\n"))
                            menu += (_("2. No\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                        if int(user_response) == 2:
                            temp.sudo().write({
                                'activity3_accomplished': False,
                                'current_level': 24
                            })
                            menu = (_("CON Did the community leaders provide an update on fiances during the meeting?\n"))
                            menu += (_("1. Yes\n"))
                            menu += (_("2. No\n"))
                            return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    else:
                        visit_community.sudo().create({
                            'facilitator_id': temp.facilitator_id.id or False,
                            'co_facilitator_id': temp.co_facilitator_id.id or False,
                            'community_id': temp.community_id.id or False,
                            'visit_date': temp.visit_date or False,
                            'next_visit_date': temp.next_visit_date or False,
                            'state': temp.state or False,
                            'visit_type': temp.visit_type or False,
                            'attendance_females': temp.attendance_females or False,
                            'attendance_males': temp.attendance_males or False,
                            'speakers_female': temp.speakers_female or False,
                            'speakers_male': temp.speakers_male or False,
                            'attendance_female_leaders': temp.attendance_female_leaders or False,
                            'attendance_male_leaders': temp.attendance_male_leaders or False,
                            'attendance_government_officials': temp.attendance_government_officials or False,
                            'conflicts_in_meeting': temp.conflicts_in_meeting or False,
                            'conflicts_in_meeting_resolved': temp.conflicts_in_meeting_resolved or False,
                            'activity1_id': temp.activity1_id.id or False,
                            'activity1_accomplished': temp.activity1_accomplished or False,
                            'activity2_id': temp.activity2_id.id or False,
                            'activity2_accomplished': temp.activity2_accomplished or False,
                            'activity3_id': temp.activity3_id.id or False,
                            'activity3_accomplished': temp.activity3_accomplished or False,
                            'phase_id': temp.phase_id or False,
                            'phase': temp.phase or False,
                            'phase_name': temp.phase_id.name or False,
                            'step_id': temp.step_id.id or False,
                            'created_on_ussd': True,
                        })
                        temp.sudo().unlink()
                        menu = (_("END Visit saved, thank you !\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 24:
                    if int(user_response) == 1:
                        temp.sudo().write({
                            'leadership_reported_finances': '1',
                            'current_level': 25
                        })
                        menu = (_("CON Did the community leaders present an updated (current) cash book?\n"))
                        menu += (_("1. Yes\n"))
                        menu += (_("2. No\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        temp.sudo().write({
                            'leadership_reported_finances': '0',
                            'current_level': 25
                        })
                        menu = (_("CON Did the community leaders present an updated (current) cash book?\n"))
                        menu += (_("1. Yes\n"))
                        menu += (_("2. No\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 25:
                    if int(user_response) == 1:
                        temp.sudo().write({
                            'leadership_presented_updated_cashbook': '1',
                            'current_level': 26
                        })
                        menu = (_("CON Did the community leaders present an accurate cash book?\n"))
                        menu += (_("1. Yes\n"))
                        menu += (_("2. No\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        temp.sudo().write({
                            'leadership_presented_updated_cashbook': '0',
                            'current_level': 26
                        })
                        menu = (_("CON Did the community leaders present an accurate cash book?\n"))
                        menu += (_("1. Yes\n"))
                        menu += (_("2. No\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 26:
                    if int(user_response) == 1:
                        temp.sudo().write({
                            'leadership_presented_accurate_cashbook': '1',
                            'current_level': 27
                        })
                        menu = (_("CON Does the community have accurate, complete and high quality receipts per the disbursement schedule?\n"))
                        menu += (_("1. Yes\n"))
                        menu += (_("2. No\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        temp.sudo().write({
                            'leadership_presented_accurate_cashbook': '0',
                            'current_level': 27
                        })
                        menu = (_("CON Does the community have accurate, complete and high quality receipts per the disbursement schedule?\n"))
                        menu += (_("1. Yes\n"))
                        menu += (_("2. No\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

                if temp.current_level == 27:
                    if int(user_response) == 1:
                        temp.sudo().write({
                            'updated_accurate_receipts': 'yes',
                            'current_level': 28
                        })
                        visit_community.sudo().create({
                            'facilitator_id': temp.facilitator_id.id or False,
                            'co_facilitator_id': temp.co_facilitator_id.id or False,
                            'community_id': temp.community_id.id or False,
                            'visit_date': temp.visit_date or False,
                            'next_visit_date': temp.next_visit_date or False,
                            'state': temp.state or False,
                            'visit_type': temp.visit_type or False,
                            'attendance_females': temp.attendance_females or False,
                            'attendance_males': temp.attendance_males or False,
                            'speakers_female': temp.speakers_female or False,
                            'speakers_male': temp.speakers_male or False,
                            'attendance_female_leaders': temp.attendance_female_leaders or False,
                            'attendance_male_leaders': temp.attendance_male_leaders or False,
                            'attendance_government_officials': temp.attendance_government_officials or False,
                            'conflicts_in_meeting': temp.conflicts_in_meeting or False,
                            'conflicts_in_meeting_resolved': temp.conflicts_in_meeting_resolved or False,
                            'activity1_id': temp.activity1_id.id or False,
                            'activity1_accomplished': temp.activity1_accomplished or False,
                            'activity2_id': temp.activity2_id.id or False,
                            'activity2_accomplished': temp.activity2_accomplished or False,
                            'activity3_id': temp.activity3_id.id or False,
                            'activity3_accomplished': temp.activity3_accomplished or False,
                            'leadership_reported_finances': temp.leadership_reported_finances or False,
                            'leadership_presented_updated_cashbook': temp.leadership_presented_updated_cashbook or False,
                            'leadership_presented_accurate_cashbook': temp.leadership_presented_accurate_cashbook or False,
                            'updated_accurate_receipts': temp.updated_accurate_receipts or False,
                            'phase_id': temp.phase_id or False,
                            'phase': temp.phase or False,
                            'phase_name': temp.phase_id.name or False,
                            'step_id': temp.step_id.id or False,
                            'created_on_ussd': True,
                        })
                        temp.sudo().unlink()
                        menu = (_("END Visit saved, thank you !\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})
                    if int(user_response) == 2:
                        temp.sudo().write({
                            'updated_accurate_receipts': 'no',
                            'current_level': 28
                        })
                        visit_community.sudo().create({
                            'facilitator_id': temp.facilitator_id.id or False,
                            'co_facilitator_id': temp.co_facilitator_id.id or False,
                            'community_id': temp.community_id.id or False,
                            'visit_date': temp.visit_date or False,
                            'next_visit_date': temp.next_visit_date or False,
                            'state': temp.state or False,
                            'visit_type': temp.visit_type or False,
                            'attendance_females': temp.attendance_females or False,
                            'attendance_males': temp.attendance_males or False,
                            'speakers_female': temp.speakers_female or False,
                            'speakers_male': temp.speakers_male or False,
                            'attendance_female_leaders': temp.attendance_female_leaders or False,
                            'attendance_male_leaders': temp.attendance_male_leaders or False,
                            'attendance_government_officials': temp.attendance_government_officials or False,
                            'conflicts_in_meeting': temp.conflicts_in_meeting or False,
                            'conflicts_in_meeting_resolved': temp.conflicts_in_meeting_resolved or False,
                            'activity1_id': temp.activity1_id.id or False,
                            'activity1_accomplished': temp.activity1_accomplished or False,
                            'activity2_id': temp.activity2_id.id or False,
                            'activity2_accomplished': temp.activity2_accomplished or False,
                            'activity3_id': temp.activity3_id.id or False,
                            'activity3_accomplished': temp.activity3_accomplished or False,
                            'leadership_reported_finances': temp.leadership_reported_finances or False,
                            'leadership_presented_updated_cashbook': temp.leadership_presented_updated_cashbook or False,
                            'leadership_presented_accurate_cashbook': temp.leadership_presented_accurate_cashbook or False,
                            'updated_accurate_receipts': temp.updated_accurate_receipts or False,
                            'phase': temp.phase or False,
                            'phase_id': temp.phase_id or False,
                            'phase_name': temp.phase_id.name or False,
                            'step_id': temp.step_id.id or False,
                            'created_on_ussd': True,
                        })
                        temp.sudo().unlink()
                        menu = (_("END Visit saved, thank you !\n"))
                        return request.render('sparkit_bhc.ussd_template', {'menu': menu})

            if temp.current_level == 99:
                temp.sudo().unlink()
                menu = (_("END Visit cancelled!\n"))
                return request.render('sparkit_bhc.ussd_template', {'menu': menu})









