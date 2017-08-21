# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Alex Turbov <i.zaufi@gmail.com>
#
# Trivial YAML Config is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Trivial YAML Config is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

''' Unit tests for collections module '''

# Project specific imports
from context import make_data_filename
from ycfg.collections import folded_keys_dict, ordered_dict_node_factory, value_dict_pair, dict_and_value_node_factory

# Standard imports
import collections
import pytest


_TEST_DICT = {
    'lang.english': {
        'counting.one': 1
      , 'counting.two': 2
      }
  , 'lang.bahasa': {
        'counting.satu': 1
      , 'counting.dua': 2
      }
  }


class folded_keys_dict_tester:
    '''
        TODO Tests for invalid keys?
             (Line w/ leading/trailing dots)
    '''

    def ctor_test_1(self):
        d = folded_keys_dict({
            'one': 1
          , 'two': 2
          })
        assert len(d) == 2
        assert 'one' in d
        assert 'two' in d


    def ctor_test_2(self):
        d = folded_keys_dict({
            'english.one': 1
          , 'english.two': 2
          , 'bahasa.satu': 1
          , 'bahasa.dua': 2
          })
        assert len(d) == 2
        assert 'english' in d
        assert 'bahasa' in d

        assert len(d['english']) == 2
        assert 'one' in d['english']
        assert 'two' in d['english']

        assert len(d['bahasa']) == 2
        assert 'satu' in d['bahasa']
        assert 'dua' in d['bahasa']


    def ctor_test_3(self):
        d = folded_keys_dict({
            'english': {
                'one': 1
              , 'two': 2
              }
          , 'bahasa': {
                'satu': 1
              , 'dua': 2
              }
          })

        assert len(d) == 2
        assert 'english' in d
        assert 'bahasa' in d

        assert len(d['english']) == 2
        assert 'one' in d['english']
        assert 'two' in d['english']

        assert len(d['bahasa']) == 2
        assert 'satu' in d['bahasa']
        assert 'dua' in d['bahasa']


    def ctor_test_4(self):
        d = folded_keys_dict({
            'lang.english': {
                'one': 1
              , 'two': 2
              }
          , 'lang.bahasa': {
                'satu': 1
              , 'dua': 2
              }
          })

        assert len(d) == 1
        assert 'lang' in d

        assert len(d['lang']) == 2
        assert 'english' in d['lang']
        assert 'bahasa' in d['lang']

        assert len(d['lang']['english']) == 2
        assert 'one' in d['lang']['english']
        assert 'two' in d['lang']['english']

        assert len(d['lang']['bahasa']) == 2
        assert 'satu' in d['lang']['bahasa']
        assert 'dua' in d['lang']['bahasa']


    def ctor_test_5(self):
        d = folded_keys_dict(_TEST_DICT)

        assert len(d) == 1
        assert 'lang' in d

        assert len(d['lang']) == 2
        assert 'english' in d['lang']
        assert 'bahasa' in d['lang']

        assert len(d['lang']['english']) == 1
        assert 'counting' in d['lang']['english']

        assert len(d['lang']['bahasa']) == 1
        assert 'counting' in d['lang']['bahasa']

        assert len(d['lang']['english']['counting']) == 2
        assert 'one' in d['lang']['english']['counting']
        assert 'two' in d['lang']['english']['counting']

        assert len(d['lang']['bahasa']['counting']) == 2
        assert 'satu' in d['lang']['bahasa']['counting']
        assert 'dua' in d['lang']['bahasa']['counting']


    def access_test_1(self):
        d = folded_keys_dict(_TEST_DICT)

        l = d['lang']
        assert isinstance(l, folded_keys_dict)
        assert len(l) == 2

        l = d['lang.bahasa']
        assert isinstance(l, folded_keys_dict)
        assert len(l) == 1
        assert 'counting' in l

        l = d['lang.bahasa.counting']
        assert isinstance(l, folded_keys_dict)
        assert len(l) == 2
        assert 'satu' in l
        assert 'dua' in l

        assert d['lang.english.counting.one'] == 1


    @pytest.mark.parametrize(
        'key'
      , ['root-not-exist', 'lang.not-exist', 'lang.english.counting.leaf-not-exist']
      )
    def access_test_2(self, key):
        d = folded_keys_dict(_TEST_DICT)

        with pytest.raises(KeyError):
            try_value = d[key]


    def access_test_3(self):
        d = folded_keys_dict(_TEST_DICT)

        with pytest.raises(TypeError):
            try_value = d['lang.english.counting.one.not-existed']


    def assign_test_1(self):
        d = folded_keys_dict({})

        d['lang.english.one'] = 1

        assert len(d['lang']) == 1
        assert len(d['lang']['english']) == 1
        assert len(d['lang.english']) == 1

        assert d['lang']['english']['one'] == 1
        assert d['lang.english']['one'] == 1
        assert d['lang']['english.one'] == 1
        assert d['lang.english.one'] == 1

        d['lang.english.two'] = 2

        assert len(d['lang']) == 1
        assert len(d['lang']['english']) == 2
        assert len(d['lang.english']) == 2

        assert d['lang']['english']['two'] == 2
        assert d['lang.english']['two'] == 2
        assert d['lang']['english.two'] == 2
        assert d['lang.english.two'] == 2


    def contains_test_1(self):
        d = folded_keys_dict(_TEST_DICT)

        assert 'lang' in d

        assert 'lang.english' in d
        assert 'lang.bahasa' in d
        assert 'lang.russian' not in d

        assert 'lang.english.counting' in d

        assert 'lang.english.counting.one' in d
        assert 'lang.english.counting.two' in d
        assert 'lang.english.counting.tree' not in d

        l = d['lang.bahasa']

        assert 'counting' in l
        assert 'founding' not in l

        l = d['lang.bahasa.counting']

        assert 'satu' in l
        assert 'dua' in l
        assert 'tiga' not in l


    @pytest.mark.parametrize(
        'key'
      , ['root-not-exist', 'lang.not-exist', 'lang.english.counting.leaf-not-exist']
      )
    def delete_test_1(self, key):
        d = folded_keys_dict(_TEST_DICT)

        with pytest.raises(KeyError):
            del d[key]


    def delete_test_2(self):
        d = folded_keys_dict(_TEST_DICT)

        del d['lang.english.counting.one']
        assert len(d['lang.english.counting']) == 1
        assert 'lang.english.counting.one' not in d
        assert 'lang.english.counting.two' in d

        del d['lang.english.counting']
        assert 'lang.english.counting' not in d

        del d['lang.bahasa']
        assert len(d['lang']) == 1
        assert 'lang.bahasa' not in d
        assert 'lang.bahasa.counting' not in d
        assert 'lang.english' in d


    def iterate_test_1(self):
        d = folded_keys_dict(_TEST_DICT)

        # No exceptions/errors expected
        for k, v in d.items():
            print('{}={}'.format(k, v))


    def attribute_test_1(self):
        d = folded_keys_dict(_TEST_DICT)

        # Access dict items as attributes
        assert d.lang.english.counting.one == 1
        assert d.lang.bahasa.counting.dua == 2

        assert len(d.lang) == 2

        #d.lang.russian.counting.raz = 1

    def equal_test_1(self):
        d = folded_keys_dict(_TEST_DICT)
        e = folded_keys_dict(_TEST_DICT)

        assert id(d) != id(e)
        assert d == e

        assert d.lang.english.counting == e.lang.english.counting
        assert d.lang.english.counting == {'one': 1, 'two': 2}

        assert d.lang.english.counting.one == e.lang.english.counting.one
        assert d.lang.english.counting.one == 1


class folded_keys_ordered_dict_tester:

    def assign_test_1(self, capfd, expected_out):
        d = folded_keys_dict(collections.OrderedDict(), node_factory=ordered_dict_node_factory())
        d['lang.english.counting.one'] = 1
        d['lang.english.counting.two'] = 2
        d['lang.bahasa.counting.satu'] = 1
        d['lang.bahasa.counting.dua'] = 2

        # No exceptions/errors expected
        import pprint
        pprint.pprint(d)

        stdout, stderr = capfd.readouterr()
        assert expected_out == stdout


class value_dict_pair_tester:

    def assign_value_test(self):
        p = value_dict_pair()
        assert p.value is None
        assert not p.data

        p['lang'] = value_dict_pair()

        assert p.value is None
        assert 'lang' in p.data
        assert 'lang' in p

        assert p['lang'].value is None
        assert not p['lang'].data


class folded_keys_value_dict_pair_tester:

    def assign_test_1(self, capfd, expected_out):
        p = value_dict_pair(data=collections.OrderedDict())
        d = folded_keys_dict(p, node_factory=dict_and_value_node_factory(node_prototype=p))

        d['lang.english.counting.one'] = 1
        assert d.lang.english.counting.one.value == 1

        d['lang.english.counting.one.text'] = 'one'
        assert d.lang.english.counting.one.text == 'one'

        d['lang.english.counting.two.text'] = 'two'
        d['lang.english.counting.two'] = 2

        import pprint
        pprint.pprint(d)

        stdout, stderr = capfd.readouterr()
        assert expected_out == stdout
