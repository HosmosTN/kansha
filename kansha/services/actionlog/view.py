# -*- coding:utf-8 -*-
# --
# Copyright (c) 2012-2014 Net-ng.
# All rights reserved.
#
# This software is licensed under the BSD License, as described in
# the file LICENSE.txt, which you should have received as part of
# this distribution.
# --

from nagare import presentation, ajax
from nagare.i18n import format_datetime, _

from .comp import ActionLog


@presentation.render_for(ActionLog)
def render_ActionLog(self, h, comp, *args):
    return comp.render(h.AsyncRenderer(), 'history')


@presentation.render_for(ActionLog, 'history')
def render_ActionLog_history(self, h, *_args):
    h << h.h2(_('Action log'))
    board = self.board#.data
    with h.div(id='action-log'):
        with h.form:
            with h.select(onchange=ajax.Update(action=self.user_id)):
                h << h.option(_('all users'), value='')
                for member in board.all_members:
                    h << h.option(member().fullname, value=member().username).selected(
                        self.user_id())
            with h.select(onchange=ajax.Update(action=lambda x: self.card_id(x))):
                h << h.option(_('all cards'), value=0)
                for col in board.columns:
                    for card in col().cards:
                        h << h.option(card().get_title(), value=card().id).selected(
                            self.card_id())
        with h.div(class_='history'):
            with h.table(class_='table table-striped table-hover'):
                with h.body:
                    for event in self.get_history():
                        with h.tr:
                            h << h.th(format_datetime(event.when, 'short'))
                            h << h.td(event.to_string())
    return h.root
