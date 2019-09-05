# Copyright 2019 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Tests for labmaze.RandomMaze."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy

from absl.testing import absltest
import labmaze
import numpy as np
from six.moves import range


class RandomMazeTest(absltest.TestCase):
  """Tests for labmaze.RandomMaze.

  Tests whose name contain the word 'golden' are brittle since the output
  depends on the specific implementation of various random algorithms in the C++
  standard library. Each test case contains two sets of golden output data,
  generated by libstdc++ and libc++.
  """

  def testGolden7x9Maze(self):
    maze = labmaze.RandomMaze(height=7, width=9, random_seed=12345)

    expected_mazes = {('*********\n'
                       '*********\n'
                       '*********\n'
                       '***   ***\n'
                       '***   ***\n'
                       '***   ***\n'
                       '*********\n'),  # libstdc++
                      ('*********\n'
                       '*********\n'
                       '*********\n'
                       '*     ***\n'
                       '*     ***\n'
                       '*     ***\n'
                       '*********\n'),  # libc++
                     }
    actual_maze = str(maze.entity_layer)
    self.assertIn(actual_maze, expected_mazes)
    np.testing.assert_array_equal(maze.entity_layer,
                                  labmaze.TextGrid(actual_maze))

    expected_variations = actual_maze.replace('*', '.').replace(' ', 'A')
    self.assertEqual(str(maze.variations_layer), expected_variations)
    np.testing.assert_array_equal(maze.variations_layer,
                                  labmaze.TextGrid(expected_variations))

  def testGoldenTwoRoom9x11Maze(self):
    maze = labmaze.RandomMaze(height=9, width=11,
                              max_rooms=2, room_min_size=4, room_max_size=6,
                              random_seed=12345)

    expected_mazes = {('***********\n'
                       '***     ***\n'
                       '*** *   ***\n'
                       '*** *     *\n'
                       '*** * *** *\n'
                       '*** *   * *\n'
                       '*** *   * *\n'
                       '***       *\n'
                       '***********\n'),  # libc++
                      ('***********\n'
                       '*     *****\n'
                       '*   * *****\n'
                       '*         *\n'
                       '*   *     *\n'
                       '*   *     *\n'
                       '* *** *****\n'
                       '*     *****\n'
                       '***********\n'),  # libstdc++
                      ('***********\n'
                       '*       ***\n'
                       '*     * ***\n'
                       '*     * ***\n'
                       '*** * * ***\n'
                       '***       *\n'
                       '*****     *\n'
                       '*****     *\n'
                       '***********\n'),  # MSVC14
                     }
    self.assertIn(str(maze.entity_layer), expected_mazes)

    expected_variations = {('...........\n'
                            '.....AAA...\n'
                            '.....AAA...\n'
                            '.....AAA...\n'
                            '...........\n'
                            '.....BBB...\n'
                            '.....BBB...\n'
                            '.....BBB...\n'
                            '...........\n'),  # libstdc++
                           ('...........\n'
                            '.AAA.......\n'
                            '.AAA.......\n'
                            '.AAA.BBBBB.\n'
                            '.AAA.BBBBB.\n'
                            '.AAA.BBBBB.\n'
                            '...........\n'
                            '...........\n'
                            '...........\n'),  # libc++
                           ('...........\n'
                            '.AAAAA.....\n'
                            '.AAAAA.....\n'
                            '.AAAAA.....\n'
                            '...........\n'
                            '.....BBBBB.\n'
                            '.....BBBBB.\n'
                            '.....BBBBB.\n'
                            '...........\n'),  # MSVC14
                          }

    self.assertIn(str(maze.variations_layer), expected_variations)

  def testRegenerate(self):
    maze = labmaze.RandomMaze(height=51, width=31,
                              max_rooms=5, room_min_size=10, room_max_size=20,
                              random_seed=12345)
    old_maze, old_variations = None, None
    for _ in range(5):
      maze.regenerate()
      if old_maze is not None:
        self.assertNotEqual(str(maze.entity_layer), str(old_maze))
        self.assertTrue(np.any(maze.entity_layer != old_maze))
        self.assertNotEqual(str(maze.variations_layer), str(old_variations))
        self.assertTrue(np.any(maze.variations_layer != old_variations))
      old_maze = copy.deepcopy(maze.entity_layer)
      old_variations = copy.deepcopy(maze.variations_layer)

  def testGoldenMazeRegeneration(self):
    # This test makes sure that regeneration logic is not operating on an
    # old, dirty maze object.
    maze = labmaze.RandomMaze(height=17, width=17,
                              max_rooms=9, room_min_size=3, room_max_size=3,
                              random_seed=12345)
    expected_mazes = {('*****************\n'
                       '*   *****     ***\n'
                       '*   ***** *** ***\n'
                       '*         ***   *\n'
                       '*** *** *****   *\n'
                       '*     * *       *\n'
                       '*   * * *   *** *\n'
                       '*   *           *\n'
                       '* * * * * * * ***\n'
                       '*         *     *\n'
                       '* *   *   * *   *\n'
                       '* *   *     *   *\n'
                       '* ***** *** * * *\n'
                       '*     *       * *\n'
                       '***** *   *   * *\n'
                       '*****     *     *\n'
                       '*****************\n'),  #  libstdc++
                      ('*****************\n'
                       '***             *\n'
                       '*** *********** *\n'
                       '***     *     * *\n'
                       '*** *   * *   * *\n'
                       '*       * *   * *\n'
                       '*   ***** ***** *\n'
                       '*   ***         *\n'
                       '*** *** * ***** *\n'
                       '*   *   * *   * *\n'
                       '*   *   * *   * *\n'
                       '*       * *     *\n'
                       '*** *** * * * * *\n'
                       '*   ***     *   *\n'
                       '*   *** *   *   *\n'
                       '*       *       *\n'
                       '*****************\n'),  #  libc++
                      ('*****************\n'
                       '*********       *\n'
                       '********* ***** *\n'
                       '*   *****     * *\n'
                       '*   ***** *   * *\n'
                       '*         *   * *\n'
                       '* ************* *\n'
                       '*   *           *\n'
                       '*   *   *** * ***\n'
                       '*           *   *\n'
                       '* ***** *   *** *\n'
                       '*           *** *\n'
                       '*   * ***** *** *\n'
                       '*           *   *\n'
                       '* ***   *   *   *\n'
                       '*       *       *\n'
                       '*****************\n'),  #  MSVC14
                     }
    self.assertIn(str(maze.entity_layer), expected_mazes)
    maze.regenerate()
    expected_mazes_2 = {('*****************\n'
                         '***       *     *\n'
                         '***   *   *   * *\n'
                         '*     *       * *\n'
                         '* * *** ******* *\n'
                         '* *   *     *** *\n'
                         '* *   * *** *** *\n'
                         '*     *   *   * *\n'
                         '* * * * * *   * *\n'
                         '*       * *   * *\n'
                         '*   * *** ***** *\n'
                         '*       *       *\n'
                         '*** *   * ***** *\n'
                         '*       * *     *\n'
                         '*   ***** *   ***\n'
                         '*         *   ***\n'
                         '*****************\n'),  # libstdc++
                        ('*****************\n'
                         '*********   *****\n'
                         '*********   *****\n'
                         '*     *         *\n'
                         '* *   * *** *** *\n'
                         '* *   *     *   *\n'
                         '* ***** *   *   *\n'
                         '*       *       *\n'
                         '* *** ***** *** *\n'
                         '*       *       *\n'
                         '*   *   *   *   *\n'
                         '*   *       *   *\n'
                         '* * * * * *** ***\n'
                         '*             ***\n'
                         '***   ***********\n'
                         '***   ***********\n'
                         '*****************\n'),  # libc++
                        ('*****************\n'
                         '*           *****\n'
                         '*   * ***   *****\n'
                         '*               *\n'
                         '*** *   * ***** *\n'
                         '*       *   *   *\n'
                         '* ***** *** *   *\n'
                         '*               *\n'
                         '*   * * *** * * *\n'
                         '*   * *   *     *\n'
                         '* * * *   *   * *\n'
                         '* *           * *\n'
                         '* *   * * * *** *\n'
                         '* *   *         *\n'
                         '* * *** *   *****\n'
                         '*       *   *****\n'
                         '*****************\n'),  # MSVC14
                       }
    self.assertIn(str(maze.entity_layer), expected_mazes_2)

  def testInvalidArguments(self):
    with self.assertRaisesRegexp(ValueError, 'height.*integer'):
      labmaze.RandomMaze(height=2.5)
    with self.assertRaisesRegexp(ValueError, 'height.*positive'):
      labmaze.RandomMaze(height=-3)
    with self.assertRaisesRegexp(ValueError, 'height.*odd'):
      labmaze.RandomMaze(height=4)
    with self.assertRaisesRegexp(ValueError, 'width.*integer'):
      labmaze.RandomMaze(width=1.25)
    with self.assertRaisesRegexp(ValueError, 'width.*positive'):
      labmaze.RandomMaze(width=-5)
    with self.assertRaisesRegexp(ValueError, 'width.*odd'):
      labmaze.RandomMaze(width=2)
    with self.assertRaisesRegexp(ValueError, 'room_min_size.*integer'):
      labmaze.RandomMaze(room_min_size=3.3)
    with self.assertRaisesRegexp(ValueError, 'room_min_size.*positive'):
      labmaze.RandomMaze(room_min_size=-1)
    with self.assertRaisesRegexp(ValueError, 'room_max_size.*integer'):
      labmaze.RandomMaze(room_max_size=4.4)
    with self.assertRaisesRegexp(ValueError, 'room_max_size.*positive'):
      labmaze.RandomMaze(room_max_size=-2)
    with self.assertRaisesRegexp(
        ValueError, 'room_min_size.*less than or equal to.*room_max_size'):
      labmaze.RandomMaze(room_min_size=4, room_max_size=3)
    with self.assertRaisesRegexp(ValueError, 'retry_count.*integer'):
      labmaze.RandomMaze(retry_count=5.4)
    with self.assertRaisesRegexp(ValueError, 'retry_count.*positive'):
      labmaze.RandomMaze(retry_count=-7)
    with self.assertRaisesRegexp(
        ValueError, 'extra_connection_probability.*between 0.0 and 1.0'):
      labmaze.RandomMaze(extra_connection_probability=1.1)
    with self.assertRaisesRegexp(ValueError, 'max_variations.*integer'):
      labmaze.RandomMaze(max_variations=6.7)
    with self.assertRaisesRegexp(
        ValueError, 'max_variations.*between 0 and 26'):
      labmaze.RandomMaze(max_variations=27)
    with self.assertRaisesRegexp(ValueError, 'spawn_token.*single character'):
      labmaze.RandomMaze(spawn_token='foo')
    with self.assertRaisesRegexp(ValueError, 'object_token.*single character'):
      labmaze.RandomMaze(object_token='bar')

if __name__ == '__main__':
  absltest.main()
