# -*- coding: utf-8 -*-

from openerp.tools.translate import _
from openerp import models, fields, api
from openerp.addons.base.ir.ir_actions import VIEW_TYPES

from lxml import etree
from logging import getLogger


_logger = getLogger(__name__)
VIEW_TYPE = ('todo', _('Todo Demo'))
VIEW_TYPES.append(VIEW_TYPE)


def valid_node_group(node):
    res = True
    if not valid_type_todo(node):
        res = False
    return res


def valid_type_todo(arch, fromgroup=True):
    return True


class IrUiView(models.Model):

    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[VIEW_TYPE])

    @api.multi
    def _check_xml_todo(self):
        domain = [
            ('id', 'in', self.ids), ('type', '=', VIEW_TYPE[0]),
        ]
        for view in self.search(domain):

            fvg = self.env[view.model].fields_view_get(
                view_id=view.id, view_type=view.type
            )
            view_arch_utf8 = fvg['arch']
            view_docs = [etree.fromstring(view_arch_utf8)]

            if view_docs[0].tag == 'data':
                view_docs = view_docs[0]
            for view_arch in view_docs:
                if not valid_type_todo(view_arch, fromgroup=False):
                    return False
        return True

    _constraints = [
        (
            _check_xml_todo,
            'Invalid XML for todo view architecture',
            ['arch'],
        ),
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: