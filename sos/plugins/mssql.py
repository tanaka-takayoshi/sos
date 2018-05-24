# Copyright (C) 2018 Red Hat, K.K., Takayoshi Tanaka <tatanaka@redhat.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from sos.plugins import Plugin, RedHatPlugin

class MsSQL(Plugin, RedHatPlugin):
    """Microsoft SQL Server on Linux
    """

    plugin_name = "mssql"
    profiles = ('services',)
    packages = ('mssql-server',)

    option_list = [
        ('mssql_conf', 'SQL Server configuration file.', '', 
                        '/var/opt/mssql/mssql.conf')
    ]

    def setup(self):
        mssql_conf = self.get_option('mssql_conf')

        # https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-configure-mssql-conf?view=sql-server-linux-2017#mssqlconf-format
        section = ''
        errorlogfile = '/var/opt/mssql/log'
        sqlagent_errorlogfile = '/var/opt/mssql/log/sqlagentlog.log'
        for line in open(mssql_conf).read().splitlines():
            if line.startswith('['):
                section = line
                continue
            words = line.split('=')
            if words[0].strip() == 'errorlogfile':
                if section == '[filelocation]':
                    errorlogfile = words[1].strip()
                elif section == '[sqlagent]':
                    sqlagent_errorlogfile = words[1].strip()

        self.add_copy_spec([
            errorlogfile + '/*',
            sqlagent_errorlogfile
        ])

        self.add_journal(units=["mssql-server"])

# vim: set et ts=4 sw=4 :
